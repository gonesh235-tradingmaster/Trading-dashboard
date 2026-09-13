import feedparser
import json
import time
from datetime import datetime

FEEDS = [
    ("Reuters Business", "https://feeds.reuters.com/reuters/businessNews"),
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
    ("Investing Forex", "https://www.investing.com/rss/news_1.rss"),
    ("Investing Crypto", "https://www.investing.com/rss/news_301.rss"),
    ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
    ("FXStreet", "https://www.fxstreet.com/rss/news"),
    ("MarketWatch", "https://feeds.marketwatch.com/marketwatch/topstories/"),
]

MAX_PER_FEED = 10
MAX_TOTAL = 60


def fetch_all():
    items = []
    for source_name, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:MAX_PER_FEED]:
                items.append({
                    "source": source_name,
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "ts": int(time.mktime(entry.published_parsed)) if entry.get("published_parsed") else 0,
                })
        except Exception as e:
            print(f"Failed: {source_name} -> {e}")

    seen = set()
    unique = []
    for it in items:
        key = it["title"].lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(it)

    unique.sort(key=lambda x: x["ts"], reverse=True)
    return unique[:MAX_TOTAL]


if __name__ == "__main__":
    news = fetch_all()
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump({
            "updated": datetime.utcnow().isoformat() + "Z",
            "count": len(news),
            "items": news,
        }, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(news)} news items.")
