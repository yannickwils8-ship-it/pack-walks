# Loop method: results per step

Every step is measured with `tools/measure-loops.js` (`await runAllCases(2)` on the live site), with a fixed seed per case and run (1011–1042), so "before" and "after" make the same random choices. Each cell lists the options as **km (out & back %, roundness)**. Changed options are in bold.

Definitions follow the method: **path** = path, track, bridleway, steps or any unpaved way; **small street** = other walkable ways (including paved footways and sidewalks); **road** = tertiary to trunk.

## Seeded baseline (data version 1, before step 1)

| Case | Run 1 | Run 2 |
|---|---|---|
| A Zoniënwoud 5 km | 4.91 (7%, 0.14) · 3.81 route (3%, 0.16) · 6.72 route (1%, 0.29) | 5.19 (1%, 0.26) · 3.81 route · 6.72 route |
| B Meerdaalwoud 10 km | 10.10 knp (5%, 0.38) · 10.30 (0%, 0.32) · 10.32 (0%, 0.57) | 9.91 (4%, 0.49) · 10.10 knp (5%, 0.38) · 9.81 knp (2%, 0.47) |
| C Woluwe 5 km | 5.07 (17%, 0.41) · 4.70 (17%, 0.14) | 5.05 (15%, 0.44) · 4.93 (14%, 0.28) · 4.46 (16%, 0.27) |
| D Laeken 10 km | 10.00 (21%, 0.53) · 10.04 (28%, 0.43) · 10.47 (26%, 0.42) | 9.80 (22%, 0.31) · 9.81 (24%, 0.45) · 10.40 (30%, 0.24) |

Time: A 5.5–10 s, B 4–6 s, C 5 s, D 10 s.

## Step 1: richer path data (data version 2)

What changed: car park aisles, driveways, drive-throughs and emergency access are no longer walkable; paths with `access=no/private` but `foot=yes/designated/permissive` are now walkable; each way records paved/unpaved, sidewalk, difficulty and lead; water taps, toilets and water for dogs were added. Bigger roads are stored but stay out of route making until step 2.

| Case | Run 1 | Run 2 |
|---|---|---|
| A Zoniënwoud 5 km | **5.11 (4%, 0.44)** · 3.81 route · 6.72 route | **5.06 (1%, 0.27)** · 3.81 route · 6.72 route |
| B Meerdaalwoud 10 km | unchanged | unchanged |
| C Woluwe 5 km | **4.95 (10%, 0.17)** · 5.07 (17%, 0.41) | 5.05 (15%, 0.44) · 4.93 (14%, 0.28) · **4.88 (8%, 0.16)** |
| D Laeken 10 km | unchanged | unchanged |

Time: about the same (3–10 s).

New information now measurable (examples): Zoniënwoud trail loops 66–76% unpaved; Meerdaalwoud loops 66–76% unpaved; Woluwe 3–23% unpaved; Laeken 4–15% unpaved. Sidewalks are rarely mapped (0–7% of streets in Woluwe and Laeken), so sidewalk information will have little effect for now.

Verdict: **kept.** Five loops changed. Out & back fell in each of them (Zoniënwoud 7% → 4%, Woluwe 17% → 10% and 16% → 8%), and distance got closer (Woluwe −11% → −2%, Zoniënwoud −2%/+4% → +2%/+1%). Roundness went up in Zoniënwoud (0.14 → 0.44) but down in two Woluwe loops (0.27 → 0.16, 0.14 → 0.17); the new score in step 5 targets that. Nothing got slower. Above all, steps 2 and 7 need this data (surface, water, lead).


## Step 2: cost per metre (method table plus dog settings)

What changed: every link now costs length × the method's cost per metre (path 1.0, track 1.1, footway 1.15, residential 1.7, tertiary 3.0, primary 6.0, trunk not walkable; unpaved footway/track/cycleway at most 1.05; difficult ×1.2). Quiet roads up to tertiary, primary and secondary are now part of the walking graph, so a loop can cross one where needed. Two settings were measured:

- **M, method only:** nature preference p = 0, nothing else.
- **D, with dog settings:** p = +0.5 (paths and unpaved ×0.825, roads ×1.3), big roads (trunk to secondary) ×8, lead-only ways ×1.1, links within about 30 m of water ×0.95.

Forest cases (A, B): nearly unchanged with both settings; the loops were already 77–100% on paths. The knooppunten loop in Meerdaalwoud now shows its 13% on roads as "road" instead of "not on the graph".

Urban cases, trail loops only, averages (individual loops in the measurement output):

| | Step 1 | M | D |
|---|---|---|---|
| Unpaved, Laeken (D) | 11% | 11% | **16%** |
| Unpaved, Woluwe (C) | 13% | 9% | 12% |
| Out & back, Laeken | 25% | 23% | 24% |
| Out & back, Woluwe | 13% | 15% | 14% |
| Roundness, Laeken | 0.40 | 0.44 | 0.43 |
| Roundness, Woluwe | 0.29 | 0.30 | 0.33 |
| Junctions passed twice, Laeken | 5.5 | 6.3 | 4.5 |
| Distance off target, Laeken | 2.2% | 1.2% | 2.7% |
| Distance off target, Woluwe | 1.2% | 3.5% | 3.8% |

Time: unchanged (3–9 s).

Verdict: **kept, with the dog settings (D).** They raise the unpaved share in town by about half (Laeken 11% → 16%), make loops a little rounder, and pass fewer junctions twice; out & back is about the same. Distance accuracy is a little worse in Woluwe (one loop +7%); step 4's length correction addresses that. The main out-and-back problem in towns is still open and is step 4's job.
