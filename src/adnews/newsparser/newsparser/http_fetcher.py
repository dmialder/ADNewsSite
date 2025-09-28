import requests
from src.adnews.newsparser.log import *
import time

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

def fetch_html(url: str, src: dict, depth_of_recursion=0) -> str:
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
    )
    try:
        response = scraper.get(url, timeout=15)
        response.raise_for_status()
        # print(f"* HTTP request sent, awaiting response ... {response.status_code} {response.reason}")

        # Логируем успешный запрос
        log_article_parsing(src["name"], url, response.status_code, "Article fetched successfully")
        return response.text
    
    except requests.exceptions.HTTPError as e:
        log_article_parsing(src["name"], url, getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None, f"Failed to fetch article: {str(e)}")
        
        if response.status_code == 404:
            # print(f"404 Not Found: {url}")
            return "404 Page doesn't exist!"
        elif response.status_code == 403:
            time.sleep(15)
            depth_of_recursion += 1
            if depth_of_recursion == 2:
                return "403 Forbidden!"
            return fetch_html(url, src, depth_of_recursion)
        else:
            # print(f"HTTP error ({response.status_code}) on {url}: {e}")
            raise

    except Exception as e:
        # print(f"Error fetching {url}: {e}")
        raise