from datetime import datetime, timezone
from src.adnews.database.essential_funcs import *
 
def build_record(e: dict, full_text: str, src: dict) -> dict:
    """Формирует минимальную запись и добавляет в БД."""
    dt = e.get("published")  # datetime или None (UTC/с tz)
    published_iso = dt.isoformat() if dt else None

    record = {
        "source": src["name"],
        "title": (e.get("title") or "").strip(),
        "link": (e.get("link") or "").strip(),
        "guid": e.get("guid"),
        "summary": (e.get("summary") or "").strip(),
        "full_text": full_text or "",
        "published": published_iso,
    }

    # Собираем кортеж данных для базы
    db_row = (
        #id INTEGER PRIMARY KEY AUTOINCREMENT,
        record["title"], #title TEXT NOT NULL,
        record["published"], #datetime TEXT NOT NULL,
        record["full_text"], #init_text TEXT NOT NULL,
        record.get("summary" or ""), #summary TEXT,
        '', #advice TEXT,
        record["source"], #source TEXT NOT NULL,
        record["link"], #source_url TEXT NOT NULL,  
    )

    # Добавляем запись в базу
    single_insert_web(db_row)

    return record