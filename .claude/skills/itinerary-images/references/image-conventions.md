# Image Conventions

Reference for the `itinerary-images` skill. Contains all format templates, naming rules, and destination mappings.

---

## Folder Structure

```
assets/
└── images/
    ├── buenos-aires/
    ├── iguazu/
    ├── peninsula-valdes/
    ├── ushuaia/
    ├── el-calafate/
    ├── el-chalten/
    ├── bariloche/
    ├── mendoza/
    └── maps/            ← fallback map screenshots (not used by the live page — see below)
```

---

## Destination Slug Mapping

| Destination name (itinerary)  | Folder slug          | HTML section id      |
|-------------------------------|----------------------|----------------------|
| Buenos Aires                  | `buenos-aires`       | `buenos-aires`       |
| Puerto Iguazú / Iguazú Falls  | `iguazu`             | `iguazu`             |
| Buenos Aires (transit day)    | `buenos-aires`       | `ba-transit`         |
| Puerto Madryn / Península Valdés | `peninsula-valdes` | `madryn`           |
| Ushuaia                       | `ushuaia`            | `ushuaia`            |
| El Calafate                   | `el-calafate`        | `calafate`           |
| El Chaltén                    | `el-chalten`         | `chalten`            |
| Bariloche                     | `bariloche`          | `bariloche`          |
| Mendoza                       | `mendoza`            | `mendoza`            |
| Overview / trip-wide map      | `maps`               | n/a                  |

---

## File Naming Rules

1. Use the **last path segment** of the source URL as the filename
2. Lowercase the entire filename: `Skyline_Puerto_Madero.jpg` → `skyline_puerto_madero.jpg`
3. Replace spaces with underscores if any remain
4. Preserve the original extension (`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`)
5. If two images from different sources would produce the same filename, prefix with a short descriptor: `ba_skyline_puerto_madero.jpg`

### Examples

| Source URL | Downloaded path |
|---------------------------------------------------------------------------|--------------------------------------|
| `https://commons.wikimedia.org/wiki/Special:FilePath/Skyline_Puerto_Madero.jpg` | `assets/images/buenos-aires/skyline_puerto_madero.jpg` |
| `https://commons.wikimedia.org/wiki/Special:FilePath/Casa_rosada_2.jpg` | `assets/images/buenos-aires/casa_rosada_2.jpg` |

> Map images under `assets/images/maps/` are not downloaded from a source URL at all — they're rendered locally by `generate_maps.py` (see below). These naming rules don't apply to them.

---

## HTML Format Templates

`itinerary-leaflet.html` is hand-authored HTML (not generated) — photo
galleries are plain `<table>` grids of `<img>` tags. Maps ARE real, live,
interactive Leaflet.js maps rendering free OpenStreetMap tiles (no API key,
no billing) — not static images. Do not revert this to static `<img>` maps.

### Photo grid (after the destination tagline, before the map block)
```html
<table width="100%" border="0" cellspacing="4" cellpadding="0"><tr>
<td colspan="3"><img src="./assets/images/<slug>/image1.jpg" alt="Alt text 1" width="100%" /></td>
<td colspan="3"><img src="./assets/images/<slug>/image2.jpg" alt="Alt text 2" width="100%" /></td>
</tr><tr>
<td colspan="2"><img src="./assets/images/<slug>/image3.jpg" alt="Alt text 3" width="100%" /></td>
<td colspan="2"><img src="./assets/images/<slug>/image4.jpg" alt="Alt text 4" width="100%" /></td>
<td colspan="2"><img src="./assets/images/<slug>/image5.jpg" alt="Alt text 5" width="100%" /></td>
</tr></table>
```
Rows commonly mix a 2-wide top row (`colspan="3"` each) with a 3-wide bottom row (`colspan="2"` each) for 5 images total; adjust colspans to fit however many images the section has, keeping each row's colspans summing to 6.

### Interactive map (Leaflet)
```html
<div id="map-<slug>" class="leaflet-map" data-map="<key>" role="img" aria-label="Destination city map"></div>
<p><a href="<google-maps-or-other-map-link>">View on Google Maps ↗</a></p>
```
`<slug>` is a unique DOM id (e.g. `map-el-chalten`; the two Buenos Aires
sections use `map-buenos-aires-arrival` and `map-buenos-aires-departure`
since a page can't have duplicate ids). `<key>` is the lookup key into the
`MAPS` JS object defined in the `<script>` block near the end of `<body>` —
it must match one of `MAPS`' top-level keys (`overview`, `buenos_aires`,
`iguazu`, `ushuaia`, `el_calafate`, `el_chalten`, `bariloche`). Multiple divs
can share the same `data-map` key (both Buenos Aires divs use `buenos_aires`).

To add a stop to an existing map or add a whole new destination map, edit the
`MAPS` object directly — each entry is `{ center: [lat, lon], zoom, stops: [{ label, name, coords: [lat, lon] }, ...] }`
(the `overview` entry additionally has `route: true` to draw the dashed line
connecting stops in visiting order, and its stops use `n` — a number — instead
of `label`). The `initMaps()` function below it iterates every
`.leaflet-map[data-map]` element and instantiates a Leaflet map for it
automatically — no other code needs to change.

### Fallback map images (`assets/images/maps/`)
These PNGs are **not referenced by the live page** — `itinerary-leaflet.html`
always renders real Leaflet maps. They exist only for contexts that can't run
JavaScript or fetch live map tiles, specifically the embedded copy published
as a Claude Artifact for phone viewing (that sandbox blocks OSM tile fetches
and the `unpkg.com` CDN Leaflet loads from). Regenerate them with:
```
python3 generate_maps.py
```
This requires Chrome/Chromium on PATH — no API key, no signup, free forever.
Run it whenever the `MAPS` object in `itinerary-leaflet.html` changes (new
stop, reordered route, moved marker) and keep the two in sync manually; the
script has its own copy of `MAPS` that must match.

---

## Sync Checklist

After every image update, verify:

- [ ] Every `./assets/images/<slug>/<filename>` path exists on disk
- [ ] Each row's `colspan` values sum to 6 (the table is a 6-column grid)
- [ ] No external `http://` or `https://` URLs remain in the photo grid
- [ ] If a map's stops changed, the `MAPS` object in `itinerary-leaflet.html` AND in `generate_maps.py` were both updated, and `generate_maps.py` was re-run
- [ ] Load `itinerary-leaflet.html` locally and confirm both the photos and the interactive maps render
