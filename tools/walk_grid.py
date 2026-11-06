#!/usr/bin/env python3
"""Walking-quality grid for choosing fair start places.

Reads the tiles that build_data.py wrote and sums, per square of about 1.1 x 1.05 km:
metres of path, of small street and of road, metres unpaved, water points for the dogs,
knooppunten, and one public parking (the one nearest the middle of the square).

Writes <out>/walkgrid.json:
  {"g": [0.01, 0.015], "c": [[i, j, path, street, road, unpaved, water, knoop, plat, plon], ...]}
with i = floor(lat / 0.01), j = floor(lon / 0.015), lengths in units of 10 m, and the parking as
integers of 1e-5 degree (0, 0 when the square has none).

The app reads it to rank start places quickly without loading the paths of half of Belgium.

Usage: python walk_grid.py _site/data
"""
import json
import math
import os
import sys
from collections import defaultdict

GLAT, GLON = 0.01, 0.015
PATH = {'path', 'footway', 'track', 'bridleway', 'steps'}
ROAD = {'tertiary', 'secondary', 'primary', 'trunk'}
SOFT = {'path', 'track', 'bridleway'}   # unpaved unless tagged otherwise


def seg_m(a, b):
    """Metres between two points (lat, lon), flat-earth approximation (fine for short pieces)."""
    dy = (b[0] - a[0]) * 111320
    dx = (b[1] - a[1]) * 111320 * math.cos(math.radians((a[0] + b[0]) / 2))
    return math.hypot(dx, dy)


def decode(flat, start, q):
    out, la, lo = [], 0, 0
    for i in range(start, len(flat) - 1, 2):
        la += flat[i]
        lo += flat[i + 1]
        out.append((la / q, lo / q))
    return out


def build(out):
    with open(f'{out}/index.json', encoding='utf-8') as f:
        ix = json.load(f)
    tlat, tlon = ix['tile']
    q, walk, first = ix['q'], ix['walk'], 2 if ix.get('v', 1) >= 2 else 1
    cells = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0, 0, None])

    def cell(la, lo):
        return math.floor(la / GLAT), math.floor(lo / GLON)

    for key in ix['paths']:
        x, y = map(int, key.split('_'))
        with open(f'{out}/paths/{key}.json', encoding='utf-8') as f:
            ways = json.load(f)['w']
        for w in ways:
            hw = walk[w[0]]
            flags = w[1] if first == 2 else 0
            kind = 0 if hw in PATH else 2 if hw in ROAD else 1
            unpaved = bool(flags & 2) or (hw in SOFT and not flags & 1)
            pts = decode(w, first, q)
            for a, b in zip(pts, pts[1:]):
                mla, mlo = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                # A way is stored in every tile it touches: count each piece in one tile only
                if math.floor(mlo / tlon) != x or math.floor(mla / tlat) != y:
                    continue
                m = seg_m(a, b)
                c = cells[cell(mla, mlo)]
                c[kind] += m
                if unpaved:
                    c[3] += m

    for key in ix['meta']:
        with open(f'{out}/meta/{key}.json', encoding='utf-8') as f:
            meta = json.load(f)
        for flat in meta.get('wt', []):
            for la, lo in decode(flat, 0, q):
                cells[cell(la, lo)][4] += 1
        for it in meta.get('k', []):
            cells[cell(it[1] / q, it[2] / q)][5] += 1
        for it in meta.get('pk', []):
            la, lo = it[0] / q, it[1] / q
            i, j = cell(la, lo)
            if (i, j) not in cells:
                continue   # a parking with no walkable way around it
            c = cells[(i, j)]
            mid = ((i + 0.5) * GLAT, (j + 0.5) * GLON)
            d = (la - mid[0]) ** 2 + ((lo - mid[1]) * 0.64) ** 2
            if c[6] is None or d < c[6][0]:
                c[6] = (d, it[0], it[1])

    rows = []
    for (i, j), c in sorted(cells.items()):
        p = c[6]
        rows.append([i, j, round(c[0] / 10), round(c[1] / 10), round(c[2] / 10), round(c[3] / 10),
                     min(c[4], 999), c[5], p[1] if p else 0, p[2] if p else 0])
    with open(f'{out}/walkgrid.json', 'w', encoding='utf-8') as f:
        json.dump({'g': [GLAT, GLON], 'c': rows}, f, separators=(',', ':'))
    return len(rows)


if __name__ == '__main__':
    print(f'walk grid: {build(sys.argv[1] if len(sys.argv) > 1 else "data")} squares')
