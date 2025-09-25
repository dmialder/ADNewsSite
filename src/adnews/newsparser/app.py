from datetime import datetime, timezone

from .newsparser.config import load_config
from .newsparser.scheduler import run_forever
from .newsparser.http_fetcher import fetch_feed_bytes
from .newsparser.rss_parser import parse_feed
from .newsparser.exporter import build_record
from .newsparser.state import get_last_published, set_last_published

from ..database.essential_funcs import *


def make_process_source(out_path: str):
    def process_source(src: dict, cycle_iso: str):
        feed_bytes = fetch_feed_bytes(src)
        entries = parse_feed(feed_bytes, src)




        last_iso = get_last_published(src["name"])
        last_dt = datetime.fromisoformat(last_iso.replace("Z","+00:00")) if last_iso else None

        entries = [e for e in entries if e.get("published")]
        entries.sort(key=lambda e: e["published"])

        new_cnt = 0
        saved_pub_max = None
        for e in entries:
            pub = e["published"]
            if last_dt is not None and pub <= last_dt:
                continue
            rec = build_record(e, src)
            print(rec)
            new_cnt += 1
            if saved_pub_max is None or pub > saved_pub_max:
                saved_pub_max = pub

        if new_cnt and saved_pub_max:
            set_last_published(src["name"], saved_pub_max.isoformat(), cycle_iso)

        return {"new": new_cnt, "skipped": len(entries) - new_cnt}
    return process_source

def main():
    cfg = load_config("../src/adnews/newsparser/config/sources.yaml")
    process_source = make_process_source(cfg["out_path"])
    run_forever(cfg, process_source)

if __name__ == "__main__":
    main()