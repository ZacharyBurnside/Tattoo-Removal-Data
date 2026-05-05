# 🪡 The Rise of Tattoo Removal — A Multi-Source Data Analysis
 
A data engineering project validating the hypothesis that tattoo removal is experiencing sustained, accelerating growth in the United States. Built entirely from public data sources using Python.
 
---
 
## 📊 The Thesis
 
Tattoos have become increasingly mainstream over the past two decades — and with that growth comes a parallel rise in tattoo regret and removal. This project collects, cleans, and visualizes six independent data signals to confirm and quantify that trend.
 
---
 
## 📁 Data Sources
 
| Source | What it measures | How collected |
|--------|-----------------|---------------|
| **US Census Bureau — County Business Patterns** | Annual establishment count for NAICS 812199 (Other Personal Care Services) | Census API |
| **BLS QCEW** | National establishment + employment counts, 2020–2024 | BLS data downloads |
| **Google Trends** | Search interest for "tattoo removal", "laser tattoo removal", "tattoo regret" | `pytrends` |
| **LaserAway Locations API** | 224 locations with open dates, 2006–2026 | `curl_cffi` (Cloudflare bypass) |
| **Yelp — business listings + reviews** | 1,394 businesses, 77,322 reviews across 12 cities, 2006–2026 | Yelp Fusion API + Yelp GraphQL |
| **Reddit** | Post volume across tattoo removal/regret subreddits | PRAW API |
 
---
 
## 🔑 Key Findings
 
- **+80%** growth in NAICS 812199 establishments from 17,697 (2012) to 31,863 (2023)
- **+166%** increase in Google search interest for "tattoo removal" from 2004 to 2026
- **LaserAway** grew from 1 location in 2006 to 224 by 2026, opening 35 locations in 2024 alone
- **181,112** workers employed in the sector as of 2024, up 56% from 2020
- **77,322 Yelp reviews** across 1,394 businesses — 77% are 5-star, with volume closely tracking Google Trends
- Reddit discussion near-silent pre-2024, exploding to 1,416 posts in 2026
---
 
## 🗂️ Project Structure
 
```
tattoo-removal-analysis/
│
├── data/
│   ├── raw/
│   │   ├── BLS_Data.csv               # BLS QCEW download, 2020–2024
│   │   ├── CBP_Data.csv               # Census County Business Patterns, 2010–2023
│   │   ├── google_trends.csv          # Google Trends keyword data
│   │   ├── LaserAway_Locations.csv    # 224 locations with open_date
│   │   ├── Yelp_Listings.csv          # 1,394 business listings
│   │   ├── yelp_tattoo_reviews.csv    # 77,322 reviews with dates
│   │   └── Subreddit_data.csv         # Reddit posts from 4 subreddits
│
├── scrapers/
│   ├── laseraway_scraper.py           # curl_cffi scraper for LaserAway locations API
│   ├── yelp_business_scraper.py       # Yelp Fusion API business search
│   └── yelp_review_scraper.py         # Yelp GraphQL review scraper
│
├── notebooks/
│   └── analysis.ipynb                 # Full analysis notebook
│
├── output/
│   ├── tattoo_removal_analysis_v2.pdf # Full report with all charts
│   └── laseraway_growth.png           # Cumulative location growth chart
│
└── README.md
```
 
---
 
## ⚙️ Setup
 
```bash
pip install curl-cffi requests praw pandas matplotlib pytrends reportlab
```
 
### Reddit API credentials
Create an app at [reddit.com/prefs/apps](https://reddit.com/prefs/apps) and add your credentials to the PRAW script:
 
```python
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="script:tattoo_research:1.0 (by /u/your_username)"
)
```
 
### Yelp API key
Get a free key at [yelp.com/developers](https://yelp.com/developers) and set it in the business scraper:
 
```python
API_KEY = "YOUR_YELP_API_KEY"
```
 
---
 
## 🚀 Running the scrapers
 
**LaserAway locations** (no API key needed, requires `curl_cffi` for Cloudflare bypass):
```bash
python scrapers/laseraway_scraper.py
```
 
**Yelp business listings:**
```bash
python scrapers/yelp_business_scraper.py
```
 
**Yelp reviews** (slow — ~45 min for 1,394 businesses):
```bash
python scrapers/yelp_review_scraper.py
```
 
**Reddit posts:**
```bash
python scrapers/reddit_scraper.py
```
 
**Census CBP data** (pulls directly from Census API, no key needed):
```python
# In notebook or script
import requests
for year in range(2010, 2024):
    resp = requests.get(f"https://api.census.gov/data/{year}/cbp", params={...})
```
 
---
 
## 📝 Notes
 
- **NAICS 812199** ("Other Personal Care Services") is the official Census classification for tattoo removal. It also includes electrolysis and ear piercing, so establishment counts are an upper bound — Yelp review volume provides a more targeted signal.
- **LaserAway** scraper uses `curl_cffi` with `impersonate="chrome120"` to bypass Cloudflare TLS fingerprinting. Standard `requests` will return 403s.
- **Yelp review scraper** uses the internal GraphQL endpoint (`yelp.com/gql/batch`) rather than the Fusion API, which only returns 3 reviews per business on the free tier.
- **Reddit PRAW** caps at 1,000 posts per search query. The script runs multiple query + time_filter combinations to maximize coverage.
---
 
## 📄 Output
 
The full analysis is compiled into a PDF report (`output/tattoo_removal_analysis_v2.pdf`) including all charts and a data summary table. A v3 with sentiment analysis on the 77k review texts is planned.
 
---
