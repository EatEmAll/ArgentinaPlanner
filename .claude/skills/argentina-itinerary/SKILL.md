---
name: argentina-itinerary
description: 'Day-by-day travel itinerary generation for Argentina. Use when planning a trip to Argentina, creating a travel schedule, routing between regions (Buenos Aires, Patagonia, Mendoza, Bariloche, El Calafate, El Chaltén, Ushuaia, Iguazu Falls, Salta, Jujuy, Peninsula Valdes), recommending how many days per region, or adapting a plan for specific interests, pace, and budget. Adaptable to other international destinations. Triggers: plan my trip, itinerary, day-by-day schedule, what to do in, how many days, route Argentina, Patagonia trip, wine region.'
---

# Argentina Itinerary Generator

## When to Use
- Planning a trip to any Argentine region or multi-region circuit
- Requesting a day-by-day schedule with activities, meals, and logistics
- Optimising routing between cities to minimise backtracking
- Adapting a trip for specific travel style, budget tier, or group type

## Procedure

### Step 1: Gather Requirements
Collect or infer from context:
- **Destinations**: Specific cities, or open to recommendations
- **Duration**: Total days available
- **Travel dates / season**: Critical for Patagonia access, whale watching, harvest festivals
- **Interests**: Tango & culture | Food & wine | Nature & wildlife | Adventure trekking | History & archaeology | Photography
- **Pace**: Relaxed (1–2 activities/day) | Moderate (3–4) | Packed (5+)
- **Budget tier**: Budget | Mid-range | Luxury
- **Group type**: Solo | Couple | Family with kids | Group

### Step 2: Select Regions and Build Route
Consult [regions.md](./references/regions.md) for:
- Minimum recommended nights per region
- Seasonal access windows (Patagonia: Oct–Apr; Iguazu: year-round; Mendoza harvest: Mar–Apr)
- Which regions pair efficiently together
- Internal transport links between regions

Routing priority — cluster geographically to minimise backtracking:
1. **Buenos Aires** — gateway, usually start/end
2. **Northwest**: Salta → Jujuy → Quebrada de Humahuaca
3. **Cuyo**: Mendoza → Uco Valley wine route
4. **Patagonia South**: Bariloche → El Calafate → El Chaltén → Ushuaia
5. **Northeast**: Puerto Iguazu → Iberá Wetlands (optional)
6. **Atlantic**: Peninsula Valdes (whale watching, Sep–Nov)

### Step 3: Build the Day-by-Day Plan
Structure each day:
```
Day N — [Location]
Morning   : [Activity + logistics tip]
Afternoon : [Activity]
Evening   : [Dinner area + style]
Stay      : [Neighbourhood / accommodation tier]
Move      : [Transport to next stop if changing location that day or next morning]
```

Guidelines:
- Cluster high-energy days before rest/flex days in packed schedules
- Flag advance-booking requirements: Perito Moreno ice trekking, Iguazu boat tour, Tren a las Nubes, Aconcagua permits, premium winery tastings
- Add 1 flex/rest day per 5–6 days for trips longer than 10 days
- Note early-start days (glacier treks, boat departures, overnight buses)

### Step 4: Use Sample Templates as Starting Points
Load [sample-itineraries.md](./references/sample-itineraries.md) for proven route templates:
- Classic Grand Tour (14 days)
- Patagonia Focus (8–10 days)
- Buenos Aires + Wine Country (6–7 days)
- Northern Adventure: Salta + Iguazu (9 days)
- Short Break: Buenos Aires Only (3–4 days)

### Step 5: Finalize Output
Deliver:
1. **Route summary** — regions in order with total days per stop
2. **Day-by-day schedule** — using the structure from Step 3
3. **Advance booking checklist** — what to reserve and how far ahead
4. **Practical logistics note** — arrival airport, inter-region transport method

### Step 6: Apply Repository Itinerary Changes
When applying any change to this repository's itinerary, edit
`itinerary-leaflet.html` directly — it is the only itinerary file, hand-authored,
with no separate Markdown source or render step. See
`../itinerary-images/references/image-conventions.md` for the HTML structure
conventions (photo-grid tables, static map images) if the change touches images.

## Adapting for Other Destinations
Replace Argentine regions with target-country equivalents. The gathering, routing, and day-structure procedures apply universally to any international trip.
