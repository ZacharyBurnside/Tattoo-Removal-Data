import praw
import pandas as pd

reddit = praw.Reddit(
    client_id="client_id",
    client_secret="client_secret",
    user_agent="user_agent"
)

SUBREDDITS = ["tattooremoval", "tattoos", "tattooadvice", "tifu"]

QUERIES = [
    "tattoo removal",
    "tattoo regret",
    "remove my tattoo",
    "hate my tattoo",
    "laser removal",
]

# Search each time window separately to get past the 1000 cap
TIME_FILTERS = ["all", "year", "month"]

results = []
seen_ids = set()

for sub in SUBREDDITS:
    print(f"\nr/{sub}")
    subreddit = reddit.subreddit(sub)

    for query in QUERIES:
        for time_filter in TIME_FILTERS:
            try:
                posts = subreddit.search(query, limit=1000, sort="new", time_filter=time_filter)
                new = 0
                for post in posts:
                    if post.id not in seen_ids:
                        seen_ids.add(post.id)
                        results.append({
                            "subreddit":    sub,
                            "title":        post.title,
                            "text":         post.selftext,
                            "score":        post.score,
                            "num_comments": post.num_comments,
                            "created_date": pd.to_datetime(post.created_utc, unit="s"),
                            "url":          post.url,
                            "query":        query,
                        })
                        new += 1
                print(f"  '{query}' [{time_filter}]: {new} new posts")
            except Exception as e:
                print(f"  Error: {e}")

df = pd.DataFrame(results).sort_values("created_date", ascending=False)
print(f"\nTotal unique posts: {len(df)}")
print(df["subreddit"].value_counts())
print(f"\nDate range: {df['created_date'].min().date()} → {df['created_date'].max().date()}")
