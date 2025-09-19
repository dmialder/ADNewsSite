import requests

def fetch_feed_bytes(src: dict) -> bytes:
    """Простой GET RSS. Возвращает байты ленты."""
    r = requests.get(
        src["feed_url"],
        headers=src.get("headers"),
        timeout=int(src.get("http_timeout", 15)),
    )
    r.raise_for_status()
    return r.content

import cloudscraper

def fetch_html(url: str, src: dict) -> str:
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
    )
    response = scraper.get(url, timeout=15)
    response.raise_for_status()

    print(f"* HTTP request sent, awaiting response ... {response.status_code} {response.reason}")
    return response.text