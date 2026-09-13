"""Regenerate the static fallback map images in assets/images/maps/.

These PNGs are NOT used by itinerary-leaflet.html itself -- that file renders
live, interactive Leaflet maps (OpenStreetMap tiles, free, no API key) via
the <script> block near the end of <body>. The PNGs here exist only as a
fallback for contexts that can't run that JavaScript, e.g. an embedded copy
published as a Claude Artifact for offline/phone viewing, where live map-tile
fetches are blocked by the sandbox.

Requires Google Chrome (or Chromium) on PATH in headless-screenshot mode --
no API key, no billing account, no signup of any kind. Coordinates below
must be kept in sync with the MAPS object in itinerary-leaflet.html.

Usage:
    python3 generate_maps.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "assets" / "images" / "maps"
TMP_DIR = ROOT / ".map_render_tmp"

MAPS = {
    "overview": {
        "center": [-39, -64], "zoom": 4, "route": True, "size": (1280, 1000),
        "stops": [
            {"n": 1, "name": "Buenos Aires", "coords": [-34.6037, -58.3816]},
            {"n": 2, "name": "Puerto Iguazú", "coords": [-25.5996, -54.5795]},
            {"n": 3, "name": "Ushuaia", "coords": [-54.8019, -68.3030]},
            {"n": 4, "name": "El Chaltén", "coords": [-49.3310, -72.8855]},
            {"n": 5, "name": "El Calafate", "coords": [-50.3388, -72.2688]},
            {"n": 6, "name": "Bariloche", "coords": [-41.1335, -71.3103]},
        ],
    },
    "buenos_aires": {
        "center": [-34.6037, -58.3816], "zoom": 12, "size": (1280, 800),
        "stops": [
            {"label": "B", "name": "Buenos Aires (city)", "coords": [-34.6037, -58.3816]},
            {"label": "A", "name": "Ezeiza International Airport (EZE)", "coords": [-34.8222, -58.5358]},
        ],
    },
    "iguazu": {
        "center": [-25.68, -54.44], "zoom": 11, "size": (1280, 800),
        "stops": [
            {"label": "T", "name": "Puerto Iguazú (town)", "coords": [-25.5996, -54.5795]},
            {"label": "P", "name": "Parque Nacional Iguazú (Argentine side)", "coords": [-25.6869, -54.4453]},
            {"label": "G", "name": "Garganta del Diablo", "coords": [-25.6953, -54.4367]},
        ],
    },
    "ushuaia": {
        "center": [-54.78, -68.38], "zoom": 10, "size": (1280, 800),
        "stops": [
            {"label": "U", "name": "Ushuaia (town)", "coords": [-54.8019, -68.3030]},
            {"label": "P", "name": "Tierra del Fuego National Park", "coords": [-54.8475, -68.5514]},
            {"label": "L", "name": "Lapataia Bay (end of Ruta 3)", "coords": [-54.8612, -68.5978]},
        ],
    },
    "el_calafate": {
        "center": [-50.42, -72.66], "zoom": 9, "size": (1280, 800),
        "stops": [
            {"label": "C", "name": "El Calafate (town)", "coords": [-50.3388, -72.2688]},
            {"label": "G", "name": "Perito Moreno Glacier", "coords": [-50.4934, -73.0479]},
        ],
    },
    "el_chalten": {
        "center": [-49.32, -72.91], "zoom": 11, "size": (1280, 800),
        "stops": [
            {"label": "C", "name": "El Chaltén (town)", "coords": [-49.3310, -72.8855]},
            {"label": "F", "name": "Fitz Roy / Laguna de los Tres", "coords": [-49.2734, -72.9581]},
            {"label": "T", "name": "Cerro Torre / Laguna Torre", "coords": [-49.3098, -72.9875]},
        ],
    },
    "bariloche": {
        "center": [-41.19, -71.42], "zoom": 10, "size": (1280, 800),
        "stops": [
            {"label": "B", "name": "Bariloche (town)", "coords": [-41.1335, -71.3103]},
            {"label": "C", "name": "Circuito Chico / Cerro Campanario", "coords": [-41.0887, -71.5068]},
            {"label": "L", "name": "Llao Llao", "coords": [-41.0622, -71.5336]},
            {"label": "T", "name": "Cerro Tronador", "coords": [-41.3447, -71.8867]},
        ],
    },
}


def render_html(cfg: dict, w: int, h: int) -> str:
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  html,body {{ margin:0; padding:0; }}
  #map {{ width: {w}px; height: {h}px; }}
  .stop-badge {{
    background:#00205b;color:#fff;border-radius:50%;width:26px;height:26px;
    display:flex;align-items:center;justify-content:center;font-weight:700;
    font-size:13px;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.35);
    font-family: system-ui, sans-serif;
  }}
  .leaflet-control-zoom, .leaflet-control-attribution {{ display:none !important; }}
</style></head>
<body>
<div id="map"></div>
<script>
  var cfg = {json.dumps(cfg)};
  var map = L.map('map', {{ zoomControl:false, attributionControl:false }}).setView(cfg.center, cfg.zoom);
  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);
  cfg.stops.forEach(function(stop) {{
    var label = stop.n !== undefined ? stop.n : stop.label;
    var icon = L.divIcon({{ className: '', html: '<div class="stop-badge">' + label + '</div>', iconSize:[26,26], iconAnchor:[13,13] }});
    L.marker(stop.coords, {{ icon: icon }}).addTo(map);
  }});
  if (cfg.route) {{
    L.polyline(cfg.stops.map(function(s){{ return s.coords; }}), {{ color:'#00205b', weight:3, dashArray:'6 6', opacity:0.7 }}).addTo(map);
  }}
</script>
</body></html>
"""


def find_chrome() -> str:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    raise SystemExit(
        "No Chrome/Chromium found on PATH. Install Google Chrome or Chromium "
        "to regenerate map images (no API key needed, just the browser)."
    )


def main() -> None:
    chrome = find_chrome()
    TMP_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for key, cfg in MAPS.items():
        w, h = cfg["size"]
        html_path = TMP_DIR / f"{key}.html"
        html_path.write_text(render_html(cfg, w, h), encoding="utf-8")

        png_path = OUT_DIR / f"map_{key}.png"
        print(f"Rendering {png_path.name} ...")
        subprocess.run(
            [
                chrome, "--headless", "--disable-gpu", "--no-sandbox",
                f"--window-size={w},{h}", f"--screenshot={png_path}",
                "--virtual-time-budget=6000", "--hide-scrollbars",
                html_path.resolve().as_uri(),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Palette-quantize to keep file size reasonable (map tiles have few
        # distinct colors, so this loses no visible quality).
        im = Image.open(png_path).convert("RGB")
        im.quantize(colors=256, method=Image.MEDIANCUT).save(png_path, optimize=True)
        kb = png_path.stat().st_size / 1024
        print(f"  OK ({kb:.0f} KB)")

    shutil.rmtree(TMP_DIR, ignore_errors=True)
    print("\nAll maps regenerated.")


if __name__ == "__main__":
    main()
