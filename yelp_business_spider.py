import requests
import pandas as pd
import time

API_KEY = "_API_Key"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

CITIES = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX",
    "Phoenix, AZ", "Dallas, TX", "Miami, FL", "San Francisco, CA",
    "Seattle, WA", "Denver, CO", "Austin, TX", "Atlanta, GA",
]

results = []

for city in CITIES:
    print(f"→ {city}")
    offset = 0

    while True:
        resp = requests.get(
            "https://api.yelp.com/v3/businesses/search",
            headers=HEADERS,
            params={
                "term": "tattoo removal",
                "location": city,
                "limit": 50,
                "offset": offset,
            }
        )

        data = resp.json()
        businesses = data.get("businesses", [])
        if not businesses:
            break

        for b in businesses:
            results.append({
                "id":           b["id"],
                "alias":        b["alias"],       # <-- added
                "name":         b["name"],
                "city":         b["location"].get("city"),
                "state":        b["location"].get("state"),
                "zip":          b["location"].get("zip_code"),
                "rating":       b.get("rating"),
                "review_count": b.get("review_count"),
                "latitude":     b["coordinates"].get("latitude"),
                "longitude":    b["coordinates"].get("longitude"),
                "categories":   ", ".join(c["title"] for c in b.get("categories", [])),
                "url":          b.get("url"),
            })

        offset += 50
        if offset >= 1000 or len(businesses) < 50:
            break
        time.sleep(0.5)

df = pd.DataFrame(results).drop_duplicates(subset="id")
print(f"\nTotal: {len(df)} businesses")
print(df.head(2))