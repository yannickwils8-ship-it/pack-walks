// Test helper (not used by the app): builds the same walking-quality grid as walk_grid.py, in the
// browser, from the published tiles within a box, and hands it to the app instead of walkgrid.json.
// Used to try fair start places before the weekly data build has made the real file.
// Usage in the page console: await buildTestGrid(50.3, 4.0, 51.2, 5.1)
async function buildTestGrid(minLat, minLon, maxLat, maxLon){
  const ix = await dataIndex(), [tlat, tlon] = ix.tile, GLAT = 0.01, GLON = 0.015;
  const PATHS = new Set(['path', 'footway', 'track', 'bridleway', 'steps']), ROADS = new Set(['tertiary', 'secondary', 'primary', 'trunk']);
  const SOFT = new Set(['path', 'track', 'bridleway']);
  const cells = new Map(), cellOf = (la, lo) => Math.floor(la / GLAT) * 100000 + Math.floor(lo / GLON);
  const get = k => { if (!cells.has(k)) cells.set(k, [0, 0, 0, 0, 0, 0, null]); return cells.get(k); };
  const segM = (a, b) => Math.hypot((b[0] - a[0]) * 111320, (b[1] - a[1]) * 111320 * Math.cos((a[0] + b[0]) / 2 * Math.PI / 180));
  const keys = [];
  for (let x = Math.floor(minLon / tlon); x <= Math.floor(maxLon / tlon); x++)
    for (let y = Math.floor(minLat / tlat); y <= Math.floor(maxLat / tlat); y++) keys.push([x, y]);
  for (const [x, y] of keys) {
    const key = x + '_' + y;
    if (!ix.pathSet.has(key)) continue;
    const t = await tileJSON('paths', key); if (!t) continue;
    for (const w of t.w) {
      const hw = ix.walk[w[0]], flags = w[1], kind = PATHS.has(hw) ? 0 : ROADS.has(hw) ? 2 : 1;
      const unpaved = (flags & 2) || (SOFT.has(hw) && !(flags & 1));
      const pts = decode(w, 2);
      for (let i = 1; i < pts.length; i++) {
        const a = pts[i - 1], b = pts[i], mla = (a[0] + b[0]) / 2, mlo = (a[1] + b[1]) / 2;
        if (Math.floor(mlo / tlon) !== x || Math.floor(mla / tlat) !== y) continue;
        const m = segM(a, b), c = get(cellOf(mla, mlo));
        c[kind] += m; if (unpaved) c[3] += m;
      }
    }
  }
  for (const [x, y] of keys) {
    const key = x + '_' + y;
    if (!ix.metaSet.has(key)) continue;
    const t = await tileJSON('meta', key); if (!t) continue;
    for (const flat of t.wt || []) for (const p of decode(flat)) get(cellOf(p[0], p[1]))[4]++;
    for (const it of t.k || []) get(cellOf(it[1] / QD, it[2] / QD))[5]++;
    for (const it of t.pk || []) {
      const la = it[0] / QD, lo = it[1] / QD, k = cellOf(la, lo);
      if (!cells.has(k)) continue;
      const c = cells.get(k), i = Math.floor(la / GLAT), j = Math.floor(lo / GLON);
      const d = (la - (i + 0.5) * GLAT) ** 2 + ((lo - (j + 0.5) * GLON) * 0.64) ** 2;
      if (!c[6] || d < c[6][0]) c[6] = [d, it[0], it[1]];
    }
  }
  const rows = [...cells].map(([k, c]) => [Math.floor(k / 100000), k % 100000, Math.round(c[0] / 10), Math.round(c[1] / 10), Math.round(c[2] / 10),
    Math.round(c[3] / 10), Math.min(c[4], 999), c[5], c[6] ? c[6][1] : 0, c[6] ? c[6][2] : 0]);
  const m = new Map(); rows.forEach(r => m.set(r[0] * 100000 + r[1], r));
  walkGridP = Promise.resolve({g:[GLAT, GLON], cells:m, rows});
  return {tiles:keys.length, squares:rows.length, withParking:rows.filter(r => r[8]).length};
}
