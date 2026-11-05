// Measures the loops that "Create a walk" produces, for before/after comparisons.
// Paste into the browser console on the live site, then run:  await runAllCases(2)
// Reads results only; it doesn't change the app or saved data.
//
// Per option it reports:
//   km / offTarget   length and difference from the asked distance
//   pathPct          share on path, track, footway, bridleway, cycleway or steps
//   streetPct        share on residential, service, unclassified, living street or pedestrian
//   otherPct         share not on the walking graph (e.g. bigger roads used by marked routes)
//   outAndBackPct    share within 20 m of a part already walked (more than 150 m from the start)
//   junctionsTwice   points passed a second time (more than 150 m from the start)
//   crossings        segments that cross between map points (rare: crossing paths share a point)
//   compact          4π × area / length²: 1 = circle, low = stretched, star or figure-eight
//   startToParkingM  distance from the loop's start to the chosen parking or point

function measureOptions(){
  const A = cr.ctx.area, S = cr.ctx.origin;
  const key = p => Math.round(p[0] * 1e5) * 1e6 + Math.round(p[1] * 1e5);
  const xy = (p, o) => [(p[1] - o[1]) * 111.32 * Math.cos(o[0] * Math.PI / 180) * 1000, (p[0] - o[0]) * 111.32 * 1000];
  return cr.options.map(o => {
    const pts = o.pts, s0 = pts[0];
    let len = 0, lp = 0, ls = 0, lu = 0;
    for (let i = 1; i < pts.length; i++) {
      const d = km(P(pts[i - 1]), P(pts[i])); len += d;
      const e = (A.G.get(key(pts[i - 1])) || []).find(x => x.to === key(pts[i]));
      if (!e) lu += d; else if (e.cost / e.len <= 1.5) lp += d; else ls += d;
    }
    // Resampled every 10 m so the out-and-back share doesn't depend on how densely the map is drawn
    const rs = [];
    for (let i = 1; i < pts.length; i++) {
      const d = km(P(pts[i - 1]), P(pts[i])) * 1000, n = Math.max(1, Math.ceil(d / 10));
      for (let k = 0; k < n; k++) rs.push([pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * k / n, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * k / n]);
    }
    const grid = new Map(), ck = (a, b) => a + ':' + b;
    let back = 0;
    rs.forEach((p, i) => {
      const a = Math.round(p[0] / 0.0002), b = Math.round(p[1] / 0.0003);
      if (km(P(p), P(s0)) > 0.15) {
        let hit = false;
        for (let da = -1; da <= 1 && !hit; da++) for (let db = -1; db <= 1 && !hit; db++)
          for (const j of grid.get(ck(a + da, b + db)) || []) if (j < i - 4 && km(P(p), P(rs[j])) < 0.02) { hit = true; break; }
        if (hit) back++;
      }
      const k2 = ck(a, b); if (!grid.has(k2)) grid.set(k2, []); grid.get(k2).push(i);
    });
    const q = pts.map(p => xy(p, s0));
    const ccw = (a, b, c) => (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0]);
    let cross = 0;
    for (let i = 1; i < q.length; i++) for (let j = i + 2; j < q.length; j++) {
      if (i === 1 && j === q.length - 1) continue;
      const a = q[i - 1], b = q[i], c = q[j - 1], d = q[j];
      const d1 = ccw(a, b, c), d2_ = ccw(a, b, d), d3 = ccw(c, d, a), d4 = ccw(c, d, b);
      if (((d1 > 0 && d2_ < 0) || (d1 < 0 && d2_ > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0))) cross++;
    }
    let ar = 0;
    for (let i = 0; i < q.length; i++) { const a = q[i], b = q[(i + 1) % q.length]; ar += a[0] * b[1] - b[0] * a[1]; }
    const seen = new Set(); let twice = 0, prev = null;
    pts.forEach((p, i) => {
      const id = Math.round(p[0] * 1e5) + ',' + Math.round(p[1] * 1e5);
      if (id === prev) return;   // route shapes stitched from pieces repeat the join point
      if (i < pts.length - 1 && seen.has(id) && km(P(p), P(s0)) > 0.15) twice++;
      seen.add(id); prev = id;
    });
    return {kind:o.kind, name:createdTitle(o).slice(0, 40), km:+len.toFixed(2),
      offTarget:Math.round((len - cr.ctx.L) / cr.ctx.L * 100) + '%',
      pathPct:Math.round(lp / len * 100), streetPct:Math.round(ls / len * 100), otherPct:Math.round(lu / len * 100),
      outAndBackPct:Math.round(back / rs.length * 100), junctionsTwice:twice, crossings:cross,
      compact:+(4 * Math.PI * Math.abs(ar / 2) / Math.pow(len * 1000, 2)).toFixed(2),
      startToParkingM:Math.round(km(P(s0), S) * 1000)};
  });
}

async function runCase(label, setup, kmTarget){
  cr.km = kmTarget; cr.current = null; cr.options = []; setup(); setView('create');
  const t0 = performance.now();
  await createLoop();
  return {label, secs:+((performance.now() - t0) / 1000).toFixed(1), options:cr.options.length ? measureOptions() : []};
}

async function runAllCases(runs = 2){
  const anb = await anbData(), area = n => 'anb:' + anb.areas.findIndex(a => a.n === n);
  const cases = [
    ['A forest 5 km (Zoniënwoud)', () => { cr.mode = 'area'; $('#cSearch').value = ''; $('#cArea').value = area('Zoniënwoud'); }, 5],
    ['B forest 10 km (Meerdaalwoud)', () => { cr.mode = 'area'; $('#cSearch').value = ''; $('#cArea').value = area('Meerdaalwoud en Heverleebos'); }, 10],
    ['C urban 5 km (Sint-Lambrechts-Woluwe)', () => { cr.mode = 'point'; cr.point = {lat:50.8479, lon:4.4316}; cr.pointName = 'Sint-Lambrechts-Woluwe'; }, 5],
    ['D urban 10 km (Laeken)', () => { cr.mode = 'point'; cr.point = {lat:50.8881, lon:4.3508}; cr.pointName = 'Laeken'; }, 10],
  ];
  const out = [];
  for (let run = 1; run <= runs; run++) for (const [l, f, k] of cases) out.push({run, ...(await runCase(l, f, k))});
  console.table(out.flatMap(c => c.options.map(o => ({run:c.run, case:c.label, secs:c.secs, ...o}))));
  return out;
}
