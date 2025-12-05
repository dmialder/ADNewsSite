import time
from .extract_info import *

def main():
    while True:
        try:
            refill_empty_summary_advice()
        except Exception as exc:
            print(f"[ERROR] refill_empty_summary_advice failed: {exc}")
        time.sleep(10)


if __name__ == "__main__":
    main()