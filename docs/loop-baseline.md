# Loop quality: baseline before the new loop method

Measured on 2026-11-06 on the live site (data built 2026-11-05) with `tools/measure-loops.js`, two runs per case. Trail loops contain some randomness, so the two runs differ slightly. Every later step is compared against these numbers with the same script.

What the columns mean is explained at the top of `tools/measure-loops.js`. In short: **paths** = paths, tracks and footways; **streets** = residential, service and similar small roads; **other** = parts not on the walking graph (bigger roads used by marked routes); **out & back** = share of the walk within 20 m of a part already walked; **twice** = junctions passed a second time; **compact** = how round the loop is (1 = circle, below 0.3 = stretched or star-shaped).

## A. Forest, 5 km: Zoniënwoud (Natuur en Bos area, start at nearest parking)

| Run | Option | km | Off target | Paths | Streets | Other | Out & back | Twice | Compact | Start to parking |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Trail loop | 5.18 | +4% | 78% | 22% | 0% | 3% | 2 | 0.43 | 6 m |
| 1 | Official route "Noord-Amerika West" | 3.81 | −24% | 100% | 0% | 0% | 3% | 2 | 0.16 | 972 m |
| 1 | Official route "Flossendellewandeling" | 6.72 | +34% | 100% | 0% | 0% | 1% | 0 | 0.29 | 132 m |
| 2 | Trail loop | 4.99 | 0% | 80% | 20% | 0% | 3% | 3 | 0.45 | 6 m |
| 2 | (same two official routes) | | | | | | | | | |

Time: 5–7 s.

## B. Forest, 10 km: Meerdaalwoud en Heverleebos

| Run | Option | km | Off target | Paths | Streets | Other | Out & back | Twice | Compact | Start to parking |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Trail loop | 10.03 | 0% | 100% | 0% | 0% | 2% | 5 | 0.30 | 12 m |
| 1 | Trail loop | 10.23 | +2% | 99% | 1% | 0% | 5% | 3 | 0.49 | 12 m |
| 1 | Knooppunten loop | 10.10 | +1% | 67% | 20% | 13% | 5% | 0 | 0.38 | 403 m |
| 2 | Trail loop | 9.91 | −1% | 98% | 2% | 0% | 4% | 3 | 0.49 | 12 m |
| 2 | Trail loop | 10.30 | +3% | 100% | 0% | 0% | 0% | 0 | 0.32 | 12 m |
| 2 | Knooppunten loop | 10.10 | +1% | 67% | 20% | 13% | 5% | 0 | 0.38 | 780 m |

Time: 3–5 s.

## C. Urban, 5 km: Sint-Lambrechts-Woluwe (point on the map)

| Run | Option | km | Off target | Paths | Streets | Out & back | Twice | Compact |
|---|---|---|---|---|---|---|---|---|
| 1 | Trail loop | 4.94 | −1% | 84% | 16% | 16% | 0 | 0.18 |
| 1 | Trail loop | 5.14 | +3% | 96% | 4% | 16% | 3 | 0.43 |
| 1 | Trail loop | 5.16 | +3% | 89% | 11% | 18% | 5 | 0.23 |
| 2 | Trail loop | 5.09 | +2% | 93% | 7% | 17% | 1 | 0.42 |
| 2 | Trail loop | 5.17 | +3% | 81% | 19% | 13% | 5 | 0.35 |
| 2 | Trail loop | 4.63 | −7% | 85% | 15% | 17% | 1 | 0.47 |

Time: 3–5 s. Start 24 m from the chosen point. No knooppunten or official loops found here.

## D. Urban, 10 km: Laeken (point on the map)

| Run | Option | km | Off target | Paths | Streets | Out & back | Twice | Compact |
|---|---|---|---|---|---|---|---|---|
| 1 | Trail loop | 10.10 | +1% | 94% | 6% | 21% | 2 | 0.51 |
| 1 | Trail loop | 10.28 | +3% | 91% | 9% | 27% | 3 | 0.29 |
| 1 | Trail loop | 10.49 | +5% | 90% | 10% | 21% | 3 | 0.34 |
| 2 | Trail loop | 10.12 | +1% | 90% | 10% | 19% | 9 | 0.34 |
| 2 | Trail loop | 10.23 | +2% | 91% | 9% | 28% | 6 | 0.19 |
| 2 | Trail loop | 10.22 | +2% | 95% | 5% | 22% | 0 | 0.51 |

Time: 7–10 s. In an earlier single run one option was only 6.42 km (−36%).

## What stands out

- **Out & back is the main weakness in towns:** 13–18% at 5 km and 19–28% at 10 km. In forests it stays low (0–5%).
- **Shape varies a lot:** compactness from 0.18 to 0.51 for the same request, so some loops are long and thin.
- **Official routes are offered even when far off the distance** (−24% and +34% for 5 km in Zoniënwoud), and one starts almost 1 km from the parking.
- **The walk from the parking to the first knooppunt isn't counted** (400–780 m extra each way in Meerdaalwoud) and isn't shown.
- **"Paths" is overestimated in towns:** the current data can't tell a sidewalk mapped as a footway from a real path, and doesn't know paved from unpaved.
- **Crossings (between map points) are 0 everywhere:** in OpenStreetMap crossing paths share a point, so "junctions passed twice" is the better measure here.
- **Create doesn't look at the participants at all:** it starts where you choose, with no driving times.
