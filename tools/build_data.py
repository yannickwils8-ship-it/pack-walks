#!/usr/bin/env python3
"""Builds the walk data that Pack Walks loads instead of asking public map servers each time.

Reads a Belgium OpenStreetMap extract and writes small map squares ("tiles"):
  <out>/paths/<x>_<y>.json  walkable ways, for building trail loops
  <out>/meta/<x>_<y>.json   knooppunten, network links, marked routes, dog places, parkings,
                            villages, and green or built-up areas
plus <out>/anb.json (Natuur en Bos nature areas and dog zones), <out>/walkgrid.json (walking
quality per ~1 km square, see walk_grid.py) and <out>/index.json.

Coordinates are integers of 1e-5 degree (about 1 m), each line stored as differences from the
previous point to keep files small.

Usage: python build_data.py belgium-latest.osm.pbf _site/data
"""
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict

import osmium

TLAT, TLON = 0.1, 0.15   # tile size in degrees, about 11 x 10.5 km in Belgium
Q = 100000

# Walkable way types. New types are added at the end so older pages keep reading the numbers right.
WALK = ['path', 'footway', 'track', 'bridleway', 'steps', 'cycleway', 'pedestrian',
        'living_street', 'service', 'unclassified', 'residential',
        'tertiary', 'secondary', 'primary', 'trunk']
CLS = {h: i for i, h in enumerate(WALK)}
SERVICE_EXCLUDED = {'parking_aisle', 'driveway', 'drive-through', 'emergency_access'}
FOOT_OK = {'yes', 'designated', 'permissive'}
PAVED = {'paved', 'asphalt', 'concrete', 'paving_stones', 'sett', 'cobblestone', 'metal', 'wood',
         'chipseal', 'bricks'}
UNPAVED = {'unpaved', 'compacted', 'fine_gravel', 'gravel', 'pebblestone', 'dirt', 'earth', 'ground',
           'grass', 'mud', 'sand', 'woodchips', 'rock', 'forest_floor'}
SIDEWALK_YES = {'both', 'left', 'right', 'yes', 'separate'}
HARD_SAC = {'demanding_mountain_hiking', 'alpine_hiking', 'demanding_alpine_hiking', 'difficult_alpine_hiking'}
# Flags stored per way (one number, add them up)
F_PAVED, F_UNPAVED, F_SIDEWALK, F_DIFFICULT, F_LEASHED = 1, 2, 4, 8, 16
GREEN = [('landuse', 'forest', 'f'), ('natural', 'wood', 'f'),
         ('landuse', 'meadow', 'g'), ('landuse', 'grass', 'g'), ('landuse', 'farmland', 'g'),
         ('landuse', 'orchard', 'g'), ('landuse', 'recreation_ground', 'g'),
         ('natural', 'heath', 'g'), ('natural', 'grassland', 'g'), ('natural', 'scrub', 'g'),
         ('leisure', 'park', 'g'), ('leisure', 'nature_reserve', 'g')]
URBAN = {'residential', 'commercial', 'retail', 'industrial'}
WALK_ROUTES = {'hiking', 'foot', 'walking'}
NO_ACCESS = {'private', 'no'}


def tile(lat, lon):
    return f'{math.floor(lon / TLON)}_{math.floor(lat / TLAT)}'


def tiles_bbox(min_lat, min_lon, max_lat, max_lon):
    return {f'{x}_{y}'
            for x in range(math.floor(min_lon / TLON), math.floor(max_lon / TLON) + 1)
            for y in range(math.floor(min_lat / TLAT), math.floor(max_lat / TLAT) + 1)}


def tiles_of(coords):
    return {tile(la, lo) for la, lo in coords}


def q(v):
    return int(round(v * Q))


def enc(coords):
    out, pla, plo = [], 0, 0
    for la, lo in coords:
        a, b = q(la), q(lo)
        out += [a - pla, b - plo]
        pla, plo = a, b
    return out


def walk_class(t):
    """The walking type of a way, or None when it isn't walkable (or not for us)."""
    hw = t.get('highway')
    if not hw or t.get('area') == 'yes':
        return None
    if hw.endswith('_link'):
        hw = hw[:-5]   # a slip road counts as the road it belongs to
    if hw == 'road':
        hw = 'unclassified'
    if hw not in CLS:
        return None
    foot = t.get('foot')
    if foot in NO_ACCESS:
        return None
    if t.get('access') in NO_ACCESS and foot not in FOOT_OK:
        return None
    if hw == 'service' and t.get('service') in SERVICE_EXCLUDED:
        return None   # car park aisles, private drives
    if hw == 'trunk' and foot not in FOOT_OK:
        return None
    return hw


def way_flags(t, hw):
    f = 0
    s, tt = t.get('surface'), t.get('tracktype')
    if s in PAVED or (hw == 'track' and tt == 'grade1'):
        f |= F_PAVED
    elif s in UNPAVED or (hw == 'track' and tt in ('grade2', 'grade3', 'grade4', 'grade5')):
        f |= F_UNPAVED
    if any(t.get(k) in SIDEWALK_YES for k in ('sidewalk', 'sidewalk:both', 'sidewalk:left', 'sidewalk:right')):
        f |= F_SIDEWALK
    if t.get('sac_scale') in HARD_SAC:
        f |= F_DIFFICULT
    if t.get('dog') == 'leashed':
        f |= F_LEASHED
    return f


def densify(coords, step_km):
    """Points along a line at most step_km apart."""
    out = [coords[0]]
    for a, b in zip(coords, coords[1:]):
        n = max(1, math.ceil(length_km([a, b]) / step_km))
        out += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(1, n + 1)]
    return out


def thin(ring, step_km):
    """Keeps points at least step_km apart, to keep big outlines small."""
    out = [ring[0]]
    for p in ring[1:]:
        if length_km([out[-1], p]) >= step_km:
            out.append(p)
    if out[-1] != ring[-1]:
        out.append(ring[-1])
    return out


def length_km(coords):
    total = 0.0
    for (a1, o1), (a2, o2) in zip(coords, coords[1:]):
        dy = (a2 - a1) * 111.32
        dx = (o2 - o1) * 111.32 * math.cos(math.radians((a1 + a2) / 2))
        total += math.hypot(dx, dy)
    return total


class RelationPass(osmium.SimpleHandler):
    """First pass: which ways belong to knooppunten links and to marked walking routes."""

    def __init__(self):
        super().__init__()
        self.segs, self.routes, self.need = {}, {}, set()

    def relation(self, r):
        t = r.tags
        if t.get('route') not in WALK_ROUTES:
            return
        ways = [m.ref for m in r.members if m.type == 'w']
        if not ways:
            return
        if t.get('network:type') == 'node_network':
            self.segs[r.id] = ways
        elif t.get('network') not in ('iwn', 'nwn'):   # long-distance routes never make a short loop
            self.routes[r.id] = (t.get('name') or t.get('ref') or 'Marked walking route', ways)
        else:
            return
        self.need.update(ways)


class MainPass(osmium.SimpleHandler):
    def __init__(self, need):
        super().__init__()
        self.need = need
        self.geo = {}
        self.paths = defaultdict(list)
        self.meta = defaultdict(lambda: defaultdict(list))

    def add(self, kind, la, lo, item):
        self.meta[tile(la, lo)][kind].append(item)

    def add_water(self, coords):
        """Water for the dogs: points every 25 m along streams, rivers and shores, grouped per tile."""
        by_tile = defaultdict(list)
        for p in densify(coords, 0.025):
            by_tile[tile(*p)].append(p)
        for tl, pts in by_tile.items():
            self.meta[tl]['wt'].append(enc(pts))

    def node(self, n):
        t = n.tags
        if len(t) == 0:
            return
        la, lo = n.location.lat, n.location.lon
        if 'rwn_ref' in t:
            self.add('k', la, lo, [t['rwn_ref'], q(la), q(lo)])
        if t.get('place') in ('village', 'town', 'city', 'hamlet'):
            self.add('pl', la, lo, [q(la), q(lo), t['place'][0]])   # c, t, v or h
        if t.get('amenity') == 'drinking_water' or (t.get('man_made') == 'water_tap' and t.get('drinking_water') == 'yes'):
            self.add('wa', la, lo, [q(la), q(lo)])
        if t.get('amenity') == 'toilets' and t.get('access') not in ('private', 'no', 'customers'):
            self.add('wc', la, lo, [q(la), q(lo)])
        if t.get('amenity') == 'parking' and t.get('access') not in ('private', 'no', 'customers'):
            self.add('pk', la, lo, [q(la), q(lo)])
        if t.get('leisure') == 'dog_park':
            self.add('off', la, lo, {'n': t.get('name', ''), 'p': [q(la), q(lo)]})

    def way(self, w):
        try:
            coords = [(nd.lat, nd.lon) for nd in w.nodes]
        except osmium.InvalidLocationError:
            return
        if len(coords) < 2:
            return
        if w.id in self.need:
            self.geo[w.id] = coords
        t = w.tags
        hw = walk_class(t)
        if hw:
            if t.get('dog') == 'no':
                line = enc(coords)
                for tl in tiles_of(coords):
                    self.meta[tl]['banl'].append(line)
            else:
                item = [CLS[hw], way_flags(t, hw)] + enc(coords)
                for tl in tiles_of(coords):
                    self.paths[tl].append(item)
        if t.get('waterway') in ('stream', 'river'):
            self.add_water(coords)
        for kind, ok in (('pk', t.get('amenity') == 'parking'), ('wc', t.get('amenity') == 'toilets')):
            if ok and t.get('access') not in ('private', 'no', 'customers'):
                la = sum(c[0] for c in coords) / len(coords)
                lo = sum(c[1] for c in coords) / len(coords)
                self.add(kind, la, lo, [q(la), q(lo)])

    def area(self, a):
        t = a.tags
        kind = next((c for k, v, c in GREEN if t.get(k) == v), None)
        if not kind and t.get('landuse') in URBAN:
            kind = 'u'
        dog = t.get('dog')
        dogk = ('off' if t.get('leisure') == 'dog_park' or dog == 'unleashed'
                else 'lead' if dog == 'leashed' else 'ban' if dog == 'no' else None)
        # In nature reserves dogs stay on a lead unless the reserve says otherwise
        if not dogk and t.get('leisure') == 'nature_reserve' and dog not in ('yes', 'unleashed'):
            dogk = 'lead'
        water = t.get('natural') == 'water'
        if not kind and not dogk and not water:
            return
        try:
            rings = [[(n.lat, n.lon) for n in outer] for outer in a.outer_rings()]
        except osmium.InvalidLocationError:
            return
        if water:
            for r in rings:
                self.add_water(r)
            if not kind and not dogk:
                return
        pts = [p for r in rings for p in r]
        if not pts:
            return
        lats, lons = [p[0] for p in pts], [p[1] for p in pts]
        box = (min(lats), min(lons), max(lats), max(lons))
        cover = tiles_bbox(*box)
        if kind:
            item = [kind] + [q(v) for v in box]
            for tl in cover:
                self.meta[tl]['gr'].append(item)
        if dogk:
            item = {'n': t.get('name', ''), 'r': [enc(thin(r, 0.03)) for r in rings]}
            for tl in cover:
                self.meta[tl][dogk].append(item)


def fetch_json(url, params):
    full = url + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(full, headers={'User-Agent': 'PackWalks data build (github.com/yannickwils8-ship-it/pack-walks)'})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def natuur_en_bos():
    """Official Natuur en Bos nature areas (names and outlines) and dog off-leash zones."""
    base = 'https://gis-extern.natuurenbos.be/arcgis/rest/services/Belevingssite'
    z = fetch_json(f'{base}/Belevingssite/MapServer/37/query',
                   {'where': '1=1', 'outFields': 'Naam,Parent', 'outSR': 4326, 'f': 'json'})
    zones = [[f['attributes'].get('Naam') or 'Hondenzone', f['attributes'].get('Parent') or '',
              round(f['geometry']['y'], 5), round(f['geometry']['x'], 5)]
             for f in z.get('features', []) if f.get('geometry')]
    a = fetch_json(f'{base}/Belevingssite_detail/MapServer/18/query',
                   {'where': '1=1', 'outFields': 'Naam', 'outSR': 4326, 'returnGeometry': 'true',
                    'maxAllowableOffset': 0.0004, 'geometryPrecision': 5, 'f': 'json'})
    by_name = {}
    for f in a.get('features', []):
        name = (f['attributes'].get('Naam') or '').strip()
        rings = (f.get('geometry') or {}).get('rings') or []
        if not name or not rings:
            continue
        by_name.setdefault(name, []).extend([[[p[1], p[0]] for p in r] for r in rings])
    areas = []
    for name, rings in sorted(by_name.items()):
        pts = [p for r in rings for p in r]
        lats, lons = [p[0] for p in pts], [p[1] for p in pts]
        # Centre: the outline point nearest the middle of the area, so it is always inside it
        mla, mlo = sum(lats) / len(lats), sum(lons) / len(lons)
        c = min(pts, key=lambda p: (p[0] - mla) ** 2 + ((p[1] - mlo) * 0.64) ** 2)
        areas.append({'n': name, 'c': [round(c[0], 5), round(c[1], 5)],
                      'b': [min(lats), min(lons), max(lats), max(lons)], 'r': rings})
    return {'zones': zones, 'areas': areas}


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))


def main():
    pbf, out = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else 'data')
    t0 = time.time()

    rel = RelationPass()
    rel.apply_file(pbf)
    print(f'relations: {len(rel.segs)} knooppunten links, {len(rel.routes)} marked routes ({time.time() - t0:.0f}s)', flush=True)

    m = MainPass(rel.need)
    m.apply_file(pbf, locations=True, idx='flex_mem')
    print(f'main pass done ({time.time() - t0:.0f}s)', flush=True)

    for rid, ways in rel.segs.items():
        geoms = [m.geo[w] for w in ways if w in m.geo]
        if not geoms:
            continue
        item = [rid, [enc(g) for g in geoms]]
        for tl in set().union(*(tiles_of(g) for g in geoms)):
            m.meta[tl]['s'].append(item)
    kept = 0
    for rid, (name, ways) in rel.routes.items():
        geoms = [m.geo[w] for w in ways if w in m.geo]
        if not geoms or sum(length_km(g) for g in geoms) > 40:
            continue
        kept += 1
        item = [rid, name, [enc(g) for g in geoms]]
        for tl in set().union(*(tiles_of(g) for g in geoms)):
            m.meta[tl]['r'].append(item)
    print(f'marked routes kept: {kept}', flush=True)

    for key, ways in m.paths.items():
        write(f'{out}/paths/{key}.json', {'w': ways})
    for key, kinds in m.meta.items():
        write(f'{out}/meta/{key}.json', kinds)

    try:
        anb = natuur_en_bos()
        print(f"Natuur en Bos: {len(anb['areas'])} areas, {len(anb['zones'])} dog zones", flush=True)
    except Exception as e:   # the walk data is still useful without it
        print(f'Natuur en Bos data unavailable: {e}', flush=True)
        anb = {'zones': [], 'areas': []}
    write(f'{out}/anb.json', anb)

    write(f'{out}/index.json', {
        'built': time.strftime('%Y-%m-%d', time.gmtime()),
        'v': 2,   # paths: [type, flags, shape...]; flags 1 paved, 2 unpaved, 4 sidewalk, 8 difficult, 16 lead
        'tile': [TLAT, TLON], 'q': Q, 'walk': WALK,
        'paths': sorted(m.paths), 'meta': sorted(m.meta),
    })
    print(f'wrote {len(m.paths)} path tiles and {len(m.meta)} meta tiles in {time.time() - t0:.0f}s', flush=True)

    # The walking-quality grid for fair start places (the rest of the data is useful without it)
    try:
        import walk_grid
        print(f'walk grid: {walk_grid.build(out)} squares ({time.time() - t0:.0f}s)', flush=True)
    except Exception as e:
        print(f'walk grid failed: {e}', flush=True)


if __name__ == '__main__':
    main()
