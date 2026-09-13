# Fetch static map images from the Google Maps Static API
# Coordinates, zoom levels, and markers match itinerary-leaflet.html exactly

Set-Location "c:\Users\Vladi\Dev\ArgentinaPlanner"

# Read the API key from config.js (keeps the key in one place)
$configContent = Get-Content ".\config.js" -Raw
if ($configContent -match "window\.GOOGLE_MAPS_API_KEY\s*=\s*'([^']+)'") {
    $key = $Matches[1]
} else {
    Write-Error "Could not find GOOGLE_MAPS_API_KEY in config.js"; exit 1
}

$base   = "https://maps.googleapis.com/maps/api/staticmap"
$outDir = ".\assets\images\maps"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# $markers is an array of raw marker strings, e.g. "color:red|label:1|-34.6,-58.3"
# scale=2 doubles pixel density (effective 1280x800 / 1280x1000 output)
function Fetch-Map([string]$file, [string]$center, [int]$zoom, [string[]]$markers,
                   [string]$size = "640x400", [int]$scale = 2) {
    $url = "${base}?center=${center}&zoom=${zoom}&size=${size}&scale=${scale}&maptype=roadmap"
    foreach ($m in $markers) { $url += "&markers=$m" }
    $url += "&key=$key"

    $name = [System.IO.Path]::GetFileName($file)
    Write-Host "Fetching $name ..."
    try {
        Invoke-WebRequest -Uri $url -OutFile $file -UseBasicParsing -ErrorAction Stop
        $kb = [math]::Round((Get-Item $file).Length / 1KB, 0)
        Write-Host "  OK ($kb KB)"
    } catch {
        Write-Host "  FAILED: $($_.Exception.Message)"
    }
}

Write-Host "Fetching Google Maps static images...`n"

# ── Overview — all 6 stops, numbered labels ──────────────────────────────────
Fetch-Map "$outDir\map_overview.png" "-39,-64" 4 @(
    "color:0x1d6fa4|label:1|-34.6037,-58.3816",
    "color:0x16a34a|label:2|-25.5996,-54.5795",
    "color:0xea580c|label:3|-54.8019,-68.3030",
    "color:0xea580c|label:4|-49.3310,-72.8855",
    "color:0xea580c|label:5|-50.3388,-72.2688",
    "color:0xdb2777|label:6|-41.1335,-71.3103"
) "640x500"

# ── Buenos Aires ──────────────────────────────────────────────────────────────
Fetch-Map "$outDir\map_buenos_aires.png" "-34.6037,-58.3816" 12 @(
    "color:red|label:B|-34.6037,-58.3816",
    "color:red|label:A|-34.5572,-58.4166"
)

# ── Puerto Iguazú / Iguazú Falls ─────────────────────────────────────────────
Fetch-Map "$outDir\map_iguazu.png" "-25.68,-54.44" 11 @(
    "color:red|label:T|-25.5996,-54.5795",
    "color:red|label:P|-25.6869,-54.4453",
    "color:red|label:G|-25.6953,-54.4367"
)

# ── Península Valdés / Puerto Madryn ─────────────────────────────────────────
Fetch-Map "$outDir\map_peninsula_valdes.png" "-42.35,-64.10" 8 @(
    "color:red|label:M|-42.7714,-65.0264",
    "color:red|label:P|-42.5772,-64.2895",
    "color:red|label:N|-42.0694,-63.7778",
    "color:red|label:T|-44.0219,-65.4347"
)

# ── Ushuaia ───────────────────────────────────────────────────────────────────
Fetch-Map "$outDir\map_ushuaia.png" "-54.78,-68.38" 10 @(
    "color:red|label:U|-54.8019,-68.3030",
    "color:red|label:P|-54.8475,-68.5514",
    "color:red|label:L|-54.8612,-68.5978"
)

# ── El Calafate + Perito Moreno ───────────────────────────────────────────────
Fetch-Map "$outDir\map_el_calafate.png" "-50.42,-72.66" 9 @(
    "color:red|label:C|-50.3388,-72.2688",
    "color:red|label:G|-50.4934,-73.0479"
)

# ── El Chaltén + Fitz Roy ────────────────────────────────────────────────────
Fetch-Map "$outDir\map_el_chalten.png" "-49.32,-72.91" 11 @(
    "color:red|label:C|-49.3310,-72.8855",
    "color:red|label:F|-49.2734,-72.9581",
    "color:red|label:T|-49.3098,-72.9875"
)

# ── Bariloche ─────────────────────────────────────────────────────────────────
Fetch-Map "$outDir\map_bariloche.png" "-41.19,-71.42" 10 @(
    "color:red|label:B|-41.1335,-71.3103",
    "color:red|label:C|-41.0887,-71.5068",
    "color:red|label:L|-41.0622,-71.5336",
    "color:red|label:T|-41.3447,-71.8867"
)

# ── Mendoza ───────────────────────────────────────────────────────────────────
Fetch-Map "$outDir\map_mendoza.png" "-33.08,-68.87" 9 @(
    "color:red|label:M|-32.8908,-68.8272",
    "color:red|label:L|-33.0478,-68.8917",
    "color:red|label:V|-33.5292,-69.0614"
)

Write-Host "`nAll maps downloaded."
Get-ChildItem $outDir | Select-Object Name, @{N='KB';E={[math]::Round($_.Length/1KB,0)}}