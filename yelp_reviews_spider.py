from curl_cffi import requests as cf_requests
import pandas as pd
import time

def fetch_reviews(enc_biz_id, after_cursor=None):
    payload = [{
        "operationName": "GetBusinessReviewFeed",
        "variables": {
            "encBizId": enc_biz_id,
            "reviewsPerPage": 25,
            "selectedReviewEncId": "",
            "hasSelectedReview": False,
            "sortBy": "DATE_DESC",
            "languageCode": "en",
            "ratings": [1, 2, 3, 4, 5],
            "queryText": "",
            "isSearching": False,
            "after": after_cursor,
            "isTranslating": False,
            "translateLanguageCode": "en",
            "reactionsSourceFlow": "businessPageReviewSection",
            "guv": "DED5288FF03B1A04",
            "minConfidenceLevel": "HIGH_CONFIDENCE",
            "highlightType": "",
            "highlightIdentifier": "",
            "isHighlighting": False
        },
        "extensions": {
            "operationType": "query",
            "documentId": "691087a117482fc6d72e9549a7a23834bc35f578b0c161319eb1f9b20c0d92c0"
        }
    }]

    resp = cf_requests.post(
        "https://www.yelp.com/gql/batch",
        json=payload,
        impersonate="chrome120",
        timeout=15
    )
    resp.raise_for_status()
    result   = resp.json()[0].get("data", {})
    business = result.get("business", {})
    edges    = business.get("reviews", {}).get("edges", [])
    pageinfo = business.get("reviews", {}).get("pageInfo", {})
    return edges, pageinfo


def parse_reviews(edges, biz_id, name, city, state):
    rows = []
    for edge in edges:
        node = edge["node"]
        rows.append({
            "business_id":   biz_id,
            "business_name": name,
            "city":          city,
            "state":         state,
            "review_id":     node.get("encid"),
            "rating":        node.get("rating"),
            "text":          node.get("text", {}).get("full") if node.get("text") else None,
            "date":          node.get("createdAt", {}).get("localDateTimeForBusiness") if node.get("createdAt") else None,
        })
    return rows


all_reviews = []
errors      = []

for i, row in df.iterrows():
    biz_id = row["id"]
    name   = row["name"]
    city   = row["city"]
    state  = row["state"]
    after  = None
    biz_reviews = []

    try:
        while len(biz_reviews) < 500:
            edges, pageinfo = fetch_reviews(biz_id, after)
            if not edges:
                break
            biz_reviews.extend(parse_reviews(edges, biz_id, name, city, state))
            if not pageinfo.get("hasNextPage"):
                break
            after = pageinfo.get("endCursor")
            time.sleep(0.8)

        all_reviews.extend(biz_reviews)

    except Exception as e:
        errors.append(biz_id)

    if i % 50 == 0:
        print(f"  [{i}/{len(df)}] {len(all_reviews)} reviews so far")

    time.sleep(0.5)

reviews_df = pd.DataFrame(all_reviews).drop_duplicates(subset="review_id")
reviews_df["date"] = pd.to_datetime(reviews_df["date"], errors="coerce")

print(f"\nTotal reviews: {len(reviews_df)}")
print(f"Date range: {reviews_df['date'].min().date()} → {reviews_df['date'].max().date()}")
print(f"Errors: {len(errors)}")

reviews_df.to_csv("/users/zacharyburnside/desktop/removal/yelp_tattoo_reviews.csv", index=False)
