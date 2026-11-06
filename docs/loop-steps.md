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


## Step 3: A*, the start's connected part of the map, load radius D/2.2 + 1.5 km — not kept

What was tried:

- **A\*** instead of Dijkstra, with the estimate "straight-line distance × lowest cost per metre on the map".
- **Only the part of the map connected to the start** for the start and the waypoints. When the nearest point lies on a small isolated piece, the nearest point on a large connected part is used instead.
- **Load radius D/2.2 + 1.5 km** (6 km loop: 4.2 km instead of 2.8 km; 10 km: 6.05 instead of 4.1).

Correctness check: on 30 random pairs of points in Laeken and Meerdaalwoud, A* found routes exactly as cheap as Dijkstra in all 30. It was barely faster (Laeken 5.3 s vs 5.8 s, Meerdaalwoud 2.0 vs 1.9 s for 15 routes). The estimate must use the cheapest price on the map (forest path near water, about 0.78), far below a typical street, so A* can't skip much.

Measured on the four cases (same seeds as step 2):

- Zoniënwoud, Meerdaalwoud, Woluwe: identical loops.
- Laeken run 2: one option changed for the worse, 9.71 km (21% out & back, roundness 0.47) → 10.50 km (26%, 0.33).
- Slower everywhere: Zoniënwoud 5 → 7 s, Woluwe 4 → 6 s, Laeken 7–8 → 9–12 s, because of the much larger area to load and process.

Verdict: **not kept** (no improvement, slower). The code is on the branch `experiment/step3-astar`. The larger radius belongs to the 36-attempt generator's geometry, so it will be tried again inside step 4 and only kept if it helps there.


## Step 4: loop generator from the method — on hold until step 5

What was built:

- **Junction map:** every stretch between two junctions becomes one link, stored as numbered arrays (Laeken: 114,000 junctions instead of 447,000 map points). Same routes, much less work.
- **36 independent attempts:** 12 directions × 3 shapes (triangle, square, wide), side = D / (legs × 1.35), × 0.8 for the square. Each waypoint is snapped to the nearest junction within 0.6 × side, otherwise the attempt is given up.
- **Penalties so the walk doesn't retrace its steps:** a link already used costs ×6 per use; links within ~20 m of earlier legs (outside 150 m of the start and 100 m of the leg's end) cost up to ×5; retaking the first link out of the start costs ×20.
- **Cleanup:** dead ends (a → b → a) and "antennas" (out and back the same way within 30 m) are removed; real loops stay.
- **Length:** up to 3 tries; when more than 5% off, side × (D / length)^0.9.
- **Start:** the nearest junction on a large connected part of the map.
- **"Show 3 more":** next unseen options; when used up, 36 new attempts with the directions turned 15°.
- **Choice of the 3 options unchanged** (closest to the distance, as before), so only the generator is measured here.

The generator has no randomness, so both runs give the same result; one run per case is shown.

| Case | Options: km (out & back, roundness) | Time |
|---|---|---|
| A Zoniënwoud 5 km | 5.08 (2%, 0.61) · 5.09 (2%, 0.50) · 4.84 (3%, 0.26) | 10 s |
| B Meerdaalwoud 10 km | 10.05 (0%, 0.28) · 10.00 (1%, 0.36) · 10.10 knooppunten (5%, 0.38) | 12 s |
| C Woluwe 5 km | 4.97 (19%, 0.33) · 5.05 (14%, 0.37) · 4.93 (17%, 0.41) | 8 s |
| D Laeken 10 km | 10.04 (16%, 0.18) · 10.03 (21%, 0.53) · 9.95 (22%, 0.28) | 17 s |

Compared with step 2:

- **Distance:** every option within ±3% (step 2: up to 7%). In Zoniënwoud the official routes at −24% and +34% are no longer shown.
- **Out & back:** Laeken better (16–22% vs 21–26%); Woluwe the same (14–19%); forests still very low.
- **Roundness:** mixed (some 0.5–0.6, some 0.18–0.28).
- **Time:** 2–3× slower (8–17 s vs 4–8 s).

What all 36 loops look like (Woluwe 5 km): out & back median 14%, best 9%; roundness median 0.37; 7 of 36 are within 5% of the distance **and** at most 10% out & back. The current choice (closest distance only) doesn't pick those; the method's score in step 5 does exactly that.

What was learned while building it:

- **The "near earlier legs" penalty** helps a little in Laeken (median out & back 21% → 18%) and not in Woluwe (15% → 14%), and was the most expensive part. It was made 3× cheaper by preparing each link's points once and marking the 20 m zone in advance.
- **Timing pitfall:** browsers stretch setTimeout pauses to a second or more in background tabs, which inflated early timings. The generator now pauses with a message channel, which isn't slowed down.
- **Choosing the 3 options took 12.8 s** in Laeken because every loop was checked against every lead-only area (all nature reserves since step 1). Checking outline boxes first brought it to 1 s, with the same dog labels.
- **Building the junction map** was sped up by counting neighbours directly.

Verdict: **not published on its own** (2–3× slower for a modest gain). Kept on the branch `experiment/step4-generator`, to be measured together with step 5; if steps 4 + 5 together don't clearly beat step 2, both go.


## Step 5: score and selection (measured together with step 4) — kept

What changed:

- **Every option gets the method's score** (lower is better): average cost per metre + 2.5 × repeated share (within ~20 m of a part already walked, more than 150 m from the start) + 4 × distance off beyond 5% + 0.12 × crossings + 0.15 × junctions passed twice + 0.5 × roundness shortfall below 0.3. Our dog rule adds 1 when a loop crosses a no-dog area or path. The same score applies to trail loops, knooppunten loops and official routes, on their real shape.
- **Selection:** options in order of score, skipping any that shares 45% or more of its links with an option already kept or already shown (either way round).
- **"Show 3 more"** uses the same rule, so it never shows a loop again or one too close to an earlier one.

Results (one run per case; the generator has no randomness):

| Case | Options: km (off target, out & back, roundness) | Time |
|---|---|---|
| A Zoniënwoud 5 km | 5.17 (+3%, 2%, 0.60) · 4.82 (−4%, 1%, 0.49) · 5.17 (+3%, 1%, 0.60) | 7 s |
| B Meerdaalwoud 10 km | 10.40 (+4%, 0%, 0.48) · 10.28 (+3%, 0%, 0.52) · 10.05 (0%, 0%, 0.28) | 4 s |
| C Woluwe 5 km | 5.18 (+4%, 10%, 0.42) · 4.78 (−4%, 12%, 0.14) · 5.22 (+4%, 11%, 0.22) | 5 s |
| D Laeken 10 km | 10.48 (+5%, 17%, 0.38) · 9.48 (−5%, 15%, 0.46) · 9.70 (−3%, 17%, 0.34) | 12 s |

Compared with step 2 (live until now):

| | Step 2 | Steps 4 + 5 |
|---|---|---|
| Out & back, Laeken | 21–26% (avg 24%) | **15–17% (avg 16%)** |
| Out & back, Woluwe | 8–19% (avg 14%) | **10–12% (avg 11%)** |
| Out & back, forests | 1–5% | **0–2%** |
| Junctions passed twice | 0–16 | **0** |
| Unpaved, Laeken | avg 16% | **avg 25%** |
| Distance off target | −4% to +7% | −5% to +5% |
| Roundness, Woluwe | 0.18–0.44 | 0.14–0.42 |
| Time | 4–8 s | 4–12 s |

"Show 3 more" in Laeken: four rounds gave 12 different loops; no two share more than 45% of their links.

Side effects to handle later:

- **Meerdaalwoud no longer shows a knooppunten loop** among the 3: it scores lower because 13% of it is on roads, and the walk from the parking isn't counted yet. Step 6 handles knooppunten.
- **Laeken takes about 5 s longer** than before.
- **One Woluwe option is thin** (roundness 0.14); the method's roundness penalty is small by design.

Verdict: **steps 4 and 5 kept**. Out & back in town is down by about a third (Laeken 24% → 16%), loops never pass a junction twice, and town loops use more unpaved ground.


## Step 6: knooppunten with the walk from the parking — kept (with a reserved place)

What changed:

- **Cycles start from the knooppunten nearest the parking** (up to 3 within 1.5 km). The walk from the parking to the knooppunt and back is now included, and only cycles whose **total** is within ±10% of the distance are kept (before: 60–150% of the distance, without the access walk).
- **The access walk is routed on the walking map** and is part of the loop's shape, so the GPX and the map show it too.
- **Knooppunten loops get the same score** as every other option, on their real shape.
- **The sequence shows the parking:** "P → 18 → 17 → … → 18 → P" on the card, "Parking → 18 → … → Parking" in the WhatsApp text.
- **When knooppunten are nearby but no cycle fits the distance**, the card says: "No signposted knooppunten loop of about X km starts near here, so these are trail loops along paths and tracks."

Two variants were measured:

- **M, method only:** the score decides all three places.
- **S, reserved place:** when no knooppunten loop makes the top three but one fits the distance (±10%), the best one takes the third place.

Results: Zoniënwoud, Woluwe and Laeken have no knooppunten within 1.5 km of the start, so nothing changes there. Meerdaalwoud 10 km has 3 knooppunten nearby and 75 fitting cycles:

- **M:** three trail loops (as in step 5). The best knooppunten loop scores 2.46 against 0.95 for the best trail loop. Its own route is pleasant (cost 1.01 per metre), but the 605 m from the parking to knooppunt 18 is walked there and back: 8 junctions passed twice and 10% repeated.
- **S:** the third option becomes P → 18 → 17 → 16 → 15 → 604 → 124 → 123 → 110 → 109 → 108 → 100 → 19 → 18 → P, 10.38 km (+4%), 93% paths, 70% unpaved, 6% out & back (the access walk), roundness 0.36. It replaces a trail loop of 10.05 km with 0% out & back and roundness 0.28.

Compared with the knooppunten loop shown before step 5 (10.10 km, 67% paths, 13% roads, start 400–780 m from the parking not counted), the new one is on better paths (93%, 4% roads) and its distance is honest.

Checked: P pills on the card and in the calendar, WhatsApp text, and the "no signposted loop" message. At 3 km two cycles fit in Meerdaalwoud.

Verdict: **kept, with the reserved place (S)**. With 5–10 dogs, a signposted route that can be followed without a phone is worth a little retracing at the start. It can be switched off with `SIGNPOSTED_SLOT = false`.
