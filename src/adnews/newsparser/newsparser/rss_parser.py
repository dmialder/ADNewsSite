import feedparser
import re
from datetime import datetime, timezone                
import calendar                                 # утилиты для работы с временем (конвертация struct_time → timestamp)
from email.utils import parsedate_to_datetime   # парсер строк дат формата RFC2822 → datetime

from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
import calendar

def _parse_pubdate(e: dict):
    v = e.get("published")
    if v:
        try:
            dt = parsedate_to_datetime(v)
        except Exception:
            dt = None

        if dt is None:
            try:
                dt = datetime.fromisoformat(v)
            except ValueError:
                return None

        return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

    pp = e.get("published_parsed")
    if pp:
        return datetime.fromtimestamp(calendar.timegm(pp), tz=timezone.utc)
    return None
                             # даты нет — возвращаем None

def parse_feed(feed_bytes: bytes, src: dict) -> list[dict]:
    parsed = feedparser.parse(feed_bytes)
    out = []                                   # сюда сложим нормализованные записи
    for item in parsed.entries:                     # перебираем элементы ленты
        flag = 1
        if hasattr(item, "category"):
            for i in src.get("category_include"):
                if bool(re.search(i, item.get("category"), flags=re.I)):
                    flag *= 0
                    break
        if bool(flag) ^ hasattr(item, "category"):  #проверка на соответствмие категории
            content_encoded = None                 # сюда поместим полный HTML-текст, если он отдан в ленте
            if src.get("fulltext") != "require_http":
                content_encoded = item.get(src.get("fulltext"))

            out.append({                           # собираем нормализованный словарь записи
                "title": (item.get("title") or "").strip(),   # заголовок без крайних пробелов
                "link": (item.get("link") or "").strip(),     # ссылка на оригинальную статью
                "guid": item.get("id"),                        # GUID/ID элемента, если есть
                "summary": item.get("summary"),                # краткое описание из RSS
                "rss_full": content_encoded,                # полный HTML из ленты, если присутствует
                "published": _parse_pubdate(item)             # дата публикации (UTC) из <pubDate>
            })
    return out                                  # возвращаем список нормализованных записей