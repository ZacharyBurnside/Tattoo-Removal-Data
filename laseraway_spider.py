from curl_cffi import requests
import json, time, math
import pandas as pd

BASE_URL = "https://www.laseraway.com/api/locations/search"
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://www.laseraway.com/locations/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

def build_us_grid(lat_start=25, lat_end=50, lng_start=-125, lng_end=-65, step=3):
    """Generate a lat/lng grid covering the continental US."""
    points = []
    lat = lat_start
    while lat <= lat_end:
        lng = lng_start
        while lng <= lng_end:
            points.append((round(lat, 2), round(lng, 2)))
            lng += step
        lat += step
    return points

GRID = build_us_grid()
print(f"Grid size: {len(GRID)} anchor points | radius: 150 miles each")

# ── Scrape ─────────────────────────────────────────────────────────────────
seen_ids = set()
all_locations = []
capped_calls = []  # track any calls that still hit 100

for i, (lat, lng) in enumerate(GRID):
    try:
        resp = requests.get(
            BASE_URL,
            headers=HEADERS,
            params={"lat": lat, "lng": lng, "max_results": 100, "search_radius": 150},
            impersonate="chrome120",
            timeout=15,
        )
        if resp.status_code != 200:
            time.sleep(1.5)
            continue

        data = resp.json()
        results = data if isinstance(data, list) else data.get("locations", data.get("results", []))

        if len(results) == 100:
            capped_calls.append((lat, lng))  # flag — might be missing some

        new = 0
        for loc in results:
            loc_id = loc.get("id") or loc.get("slug")
            if loc_id not in seen_ids:
                seen_ids.add(loc_id)
                all_locations.append(loc)
                new += 1

        if new > 0:
            print(f"  ({lat}, {lng})  +{new} new | {len(all_locations)} total  {'⚠️ CAPPED' if len(results)==100 else ''}")

    except Exception as e:
        print(f"  ({lat}, {lng}) Error: {e}")

    time.sleep(0.8)

# ── Results ────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"Total unique locations: {len(all_locations)}")

if capped_calls:
    print(f"\n⚠️  {len(capped_calls)} calls hit the 100-result cap — may need tighter radius:")
    for lat, lng in capped_calls:
        print(f"   ({lat}, {lng})")
else:
    print("✓ No calls hit the cap — collection is complete")

# Save
with open("laseraway_locations_complete.json", "w") as f:
    json.dump(all_locations, f, indent=2)
print("\nSaved → laseraway_locations_complete.json")

# Quick summary by state
from collections import Counter
state_counts = Counter(loc["state"] for loc in all_locations)
print("\nLocations by state:")
for state, count in sorted(state_counts.items(), key=lambda x: -x[1]):
    print(f"  {state}: {count}")