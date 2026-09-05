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
    └── maps/            ← static map images
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
| `https://staticmap.openstreetmap.de/staticmap.php?center=-34.6...` | `assets/images/maps/map_buenos_aires.png` ← use a descriptive name for query-string URLs |

> **Note**: OpenStreetMap static map URLs use query strings with no filename in the path. Generate a descriptive filename: `map_<destination-slug>.png`

---

## HTML Format Templates

`itinerary-leaflet.html` is hand-authored HTML (not generated) — photo
galleries are plain `<table>` grids of `<img>` tags, and maps are static PNG
images, not an interactive map widget. Match this structure exactly; do not
introduce `.photo-tiles` divs or a JS map library.

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

### Static map image
```html
<img alt="Destination city map" src="./assets/images/maps/map_<slug>.png">
<a href="<google-maps-or-other-map-link>">View on Google Maps ↗</a>
```

---

## Sync Checklist

After every image update, verify:

- [ ] Every `./assets/images/<slug>/<filename>` path exists on disk
- [ ] Each row's `colspan` values sum to 6 (the table is a 6-column grid)
- [ ] No external `http://` or `https://` URLs remain in the photo grid or map `<img src>`
- [ ] Load `itinerary-leaflet.html` locally and confirm the images render
