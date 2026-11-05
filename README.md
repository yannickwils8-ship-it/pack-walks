# Pack Walks: documentation

Pack Walks helps a small group of dog owners in Belgium pick a green walk every two weeks that suits everyone. It shows each person's driving distance, the weather, and the route, and lets people answer Join / Maybe / Can't.

## Files in this folder

| File | What it is |
|---|---|
| `index.html` | The app. Open it in a browser (Chrome, Edge or Firefox). |
| `pack-walks-group-belgium.json` | Eleven test members around Brussels (Kampenhout, Sterrebeek, Woluwe, Perk, Jette, Elsene, Tervuren, Overijse, Steenokkerzeel, Zaventem, Melsbroek). Not real people. |
| `pack-walks-test-group.json` | Four older test members (Gent, Leuven, Mechelen, Hasselt). |
| `README.md` | This documentation. |
| `manifest.webmanifest`, `icon.svg`, `icon-192.png`, `icon-512.png` | Let phones install the app on the home screen. |
| `tools/build_data.py` | Builds the walk data the app uses (see "Walk data" below). |
| `.github/workflows/pages.yml` | Publishes the site and rebuilds the walk data every week. |

## Walk data

To be fast and reliable, the app doesn't ask public map servers for paths every time. Every Monday, GitHub builds a compact copy of Belgium's walking data from OpenStreetMap:

- walking paths and forest tracks,
- knooppunten and the links between them,
- marked walking routes,
- dog places (off-leash zones, lead-only and no-dog areas, drinking water),
- parkings, villages, and green or built-up areas.

It also includes from **Agentschap Natuur en Bos**:

- the official **off-leash zones** (hondenzones) in Flanders,
- the official **nature areas** with their outlines.

The data is split into map squares of about 10 × 10 km, and the app only downloads the squares it needs. It's published with the website but not stored in the repository, so the repository stays small. Code changes go live in about a minute; a full data rebuild takes longer.

If the data isn't available (for example when `index.html` is opened as a file on your computer), the app falls back to the live public map servers, which can be slow.

## Online with GitHub Pages

GitHub Pages publishes `index.html` as a website, for example `https://yannickwils8-ship-it.github.io/pack-walks/`.

1. On GitHub, open the repository → **Settings** → **Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**, branch **main**, folder **/ (root)**, and save.
3. After a minute or two the page shows the site's address.

Pages for a **private** repository needs a paid GitHub plan (Pro, Team or Enterprise). On a free account the repository must be public. Either way, the published site itself can be opened by anyone who has the link, so never put real members' data files in the repository.

## Install on your phone

Open the site on your phone, then:

- **iPhone (Safari):** tap Share → **Add to Home Screen**.
- **Android (Chrome):** tap ⋮ → **Add to Home screen** or **Install app**.

The app then opens full screen like a normal app. This works only from the online site, not from a file opened on the computer.

## Before you start

- You need an internet connection. The map, walking network, weather and distances come from online services.
- The app runs in one browser on one computer. Your data stays in that browser.
- The public map-data servers are sometimes slow or busy. If planning fails, wait a minute and try again.

## The screen

On a computer you see three parts side by side:

- **Left: navigation.** Walks, Group, Me and Settings. At the bottom, the name you're using the app as.
- **Middle: the page you chose.**
- **Right: the map.** Home towns appear as coloured initials. The selected walk is drawn in orange with a "Start" label, and dashed lines show each person's drive to the start. **Show whole group** zooms back out.

On a phone the navigation sits at the bottom, and the map has its own **Map** tab.

## Quick start with the test group

1. Double-click `index.html`.
2. Go to **Settings → Import file** and pick `pack-walks-group-belgium.json`. This replaces everything saved in that browser.
3. Still in Settings, press **Re-locate towns**. It looks up each town by name so the map shows the right places. It takes about a minute.
4. Go to **Me** and tap a name under **Who are you?**
5. Go to **Walks** and press **Plan walks**. A progress bar shows each step.

## Walks

- **The big card** shows the selected walk. By default this is the next planned walk. It contains:
  - date, start time and a countdown,
  - a weather label: good, windy, hot, wet, or cancelled,
  - for knooppunten loops, the **numbered junctions to follow** in order,
  - length, how green the route is, the weather, and your own drive,
  - **Join / Maybe / Can't** buttons (tap the same answer again to clear it),
  - who is coming, which dogs are coming, and any dog notes,
  - **Driving distances** for everyone (tap Show), with anyone over their maximum marked,
  - **Show route on map**, **Directions to start** (opens Google Maps), **Share on WhatsApp**, and **Download GPX** for a GPS or walking app.
- **Coming up** lists all planned walks. Tap one to show it in the big card and on the map. The label on the right shows your answer.
- **Past walks** are kept at the bottom.
- **Plan walks** replaces planned walks from the first walk date onward, and clears the answers given to those walks.

## How walks are chosen

- **Walk types:** official knooppunten loops (the numbered walking network) and GR/PR routes that return to their start.
- **Length:** always **5 to 8 km**, and preferably no longer than the shortest maximum in the group. Lengths vary from walk to walk across that range.
- **Nature first:** at least 45% of the route must run through woods, fields, meadows, heath, parks or nature reserves, and the greener the better. Routes with more than a quarter of their length in built-up land are skipped, and so are walks starting within 1.5 km of a town or 700 m of a village centre (hamlets don't count). Woods such as Zoniënwoud or Meerdaalwoud rank highest.
- **Distance:** at least half the group must be within their maximum drive.
- **Variety:**
  - Starting points are spread over the whole area around the group, and up to three different loops are tried from each junction.
  - Two walks in one batch never share more than 40% of their paths.
  - Walks that overlap recent walks, or start within 2.5 km of one, rank lower.
  - The final choice is made at random from the best few, so pressing **Plan walks** again gives a different set.
- **Fair driving:** over a batch, the app keeps track of how far each person has driven and favours places that are close for whoever has driven most so far.
- **Weather** at the start point, for the walk's time:
  - gusts of **60 km/h or more** cancel the walk, and the card says why,
  - gusts of **45 km/h or more** steer walks away from woods,
  - forecasts reach 16 days ahead, so later walks say "Forecast not out yet".

## Create a walk

Make a loop yourself, for any day.

1. Open **Create**.
2. Choose where:
   - **Nature area:** pick one of the 300+ Natuur en Bos areas, listed nearest to the group first with their distance, or a Walloon area at the bottom. You can also type the name of any other area. The chosen area's outline is shown on the map.
   - **Point on map:** click the map where the walk should start. On a phone, tap **Choose on map** and then tap the map.
3. Set the **distance** with the slider (3–15 km).
4. Press **Create loop**. This takes from a few seconds to about a minute, depending on how busy the public map servers are.

You always get **three options**, each with its own colour on the map (orange, blue, purple). They come from:

- **Official routes:** marked regional and local walking routes that come back to their start, starting at the point closest to where you chose. Follow their signs.
- **Knooppunten loops:** signposted loops on the numbered junction network, with the junctions to follow.
- **Trail loops:** built along paths and forest tracks, using roads only to connect them. They aren't signposted, so follow them on your phone or download the GPX.

Each option shows its length and walking time, and whether it **matches your distance** or is shorter or longer. If no route of the exact distance exists there, the app says so and shows the three closest alternatives. **Show 3 more** gives three different routes from the same place.

**Dog-friendly information**, for walking with a big group of dogs:

- Paths where dogs are banned are left out of trail loops. Official and knooppunten routes that cross a no-dog area are labelled and ranked last.
- On the map: **off-leash zones** in green, **lead-only** areas with an orange dashed edge, **no-dog** areas and paths in red, and **drinking water** as blue dots.
- Each option is labelled when it passes an off-leash zone, needs a lead on part of the way, passes water points, or runs mostly on wide tracks (easier with 5–10 dogs).
- Off-leash zones come from Natuur en Bos (official, Flanders) and from OpenStreetMap. The other dog information comes from OpenStreetMap and isn't complete everywhere, so always check the signs at the entrance.
- In Natuur en Bos areas dogs must stay on a lead and on the paths, except inside the marked off-leash zones.

Select an option to see it on the map, get directions, download the GPX, share it on WhatsApp, or **Add walk** to the group calendar on a date. A walk added by hand replaces any walk already planned that day, and **Plan walks** leaves it in place. If the forecast for that day shows gusts above the cancel limit, the app won't add it.

## Group

- **Add member** opens a form: name, town, dog's name, size, lead, notes, longest drive (15/20/25 km) and longest walk (5–8 km).
- Each member card has **Show on map** and **Remove**. Remove asks for a second tap, so nobody is deleted by accident.

## Me

- **Who are you?** chooses whose answers you give on this device.
- **Your details** lets you change your own information. If you change your town, it's looked up again.
- **I'm new** opens the registration form.

## Settings

- **Planning:** first walk date, start time, and how many walks to plan (one every two weeks).
- **Weather:** the gust limits for avoiding woods and for cancelling.
- **Group data:** **Export file** downloads everything as a `.json` file to send to the group. **Import file** loads such a file. **Re-locate towns** looks up all towns again. **Clear all data** deletes everything after a second click.

## Sharing with the group

Everything is saved in your own browser. To share:

1. **Settings → Export file**.
2. Send the file to the group, for example on WhatsApp.
3. Each person opens the app and uses **Settings → Import file**.

An import replaces what is saved in that browser. Answers given on different computers are not merged; the hosted version (planned) will do this automatically.

## Privacy

- Only names, towns, dog details and limits are stored. No addresses or email addresses.
- Town names are sent to the Nominatim service to find their position. Walk searches go to public map servers. Nothing else leaves your computer.
- Clearing your browser's site data deletes everything. Export first if you want to keep it.

## Troubleshooting

| Problem | What to try |
|---|---|
| Homes are in the wrong place | **Settings → Re-locate towns**, then plan again. |
| "Could not find … in Belgium" | Use postcode and town, for example `3070 Kampenhout`. |
| No green loops found | Give some members a larger maximum drive. |
| "The map data server is busy" | Wait a minute and press **Plan walks** again. |
| A date says "No walk on this date" | Too windy, or no route fits most people's maximum drive. The card says which. |
| Weather missing | The walk is more than 16 days away. Plan again closer to the date. |
| Import did nothing | Pick a file exported from Pack Walks. |

## Limits of this version

- No logins, no shared database, no notifications. Sharing is by file.
- The nature and town checks use rectangles around map areas, so they're approximate.
- Dog details are shown for information and don't yet change which walk is chosen.
- Driving distances use the free OSRM road service. If it's unavailable, the app estimates with straight-line distance × 1.3.
