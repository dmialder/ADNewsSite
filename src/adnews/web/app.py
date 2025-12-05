from flask import Flask, render_template, jsonify, send_from_directory
import csv
import sqlite3
import json
import os
import logging
from threading import Lock
from src.adnews.database.essential_funcs import multiple_extract_web

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
SP500_DATA_PATH = os.path.join(STATIC_DIR, "js", "sp500_data.json")
LOG_PATH = os.path.join(BASE_DIR, "app.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

application = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
news_lock = Lock()
rotation_index = [0]

def fetch_sp500_once():
    """Однократная загрузка данных S&P500 из локального JSON."""
    try:
        if not os.path.exists(SP500_DATA_PATH):
            logging.warning(f"Файл {SP500_DATA_PATH} не найден.")
            return []

        with open(SP500_DATA_PATH, "r", encoding="utf-8") as f:
            candles = json.load(f)

        if not isinstance(candles, list) or not candles:
            logging.warning("Пустые или некорректные данные в sp500_data.json.")
            return []

        logging.info(f"Загружено {len(candles)} свечей из локального JSON.")
        return candles
    except Exception as e:
        logging.exception(f"Ошибка при загрузке sp500_data.json: {e}")
        return []

CANDLES_CACHE = fetch_sp500_once()

def load_news_csv():
    """Резервная загрузка новостей из CSV."""
    news = []
    try:
        with open("news.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                if i >= 5:
                    break
                news.append(row)
        logging.info(f"Загружено {len(news)} новостей из CSV.")
    except Exception as e:
        logging.exception(f"Ошибка при чтении news.csv: {e}")
    return news


def load_news_db():
    """Основная загрузка новостей из БД."""
    news = []
    try:
        load = multiple_extract_web() or []
    except Exception as e:
        logging.exception(f"multiple_extract_web failed: {e}")
        return news

    for item in load[:5]:
        try:
            news.append({
                "title": str(item[1]) if len(item) > 1 else "",
                "datetime": str(item[2]) if len(item) > 2 else "",
                "summary": str(item[4]) if len(item) > 4 else "",
                "advice": str(item[5]) if len(item) > 5 else "",
                "source_url": str(item[8]) if len(item) > 8 else "",
            })
        except Exception as e:
            logging.warning(f"Пропущена некорректная запись: {e}")
            continue
    return news


@application.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        logging.exception(f"Ошибка при рендеринге index.html: {e}")
        return "<h1>Index render error</h1>", 200


@application.route("/news")
def get_news():
    with news_lock:
        news = load_news_db()
        if not news:
            news = load_news_csv()

        if not news:
            logging.warning("Нет доступных новостей.")
            return jsonify({"news": [], "selected": None}), 200

        selected = news[rotation_index[0] % len(news)]
        rotation_index[0] = (rotation_index[0] + 1) % len(news)

    return jsonify({"news": news, "selected": selected})


@application.route("/select/<int:index>")
def select_news(index):
    news = load_news_db() or load_news_csv()
    if 0 <= index < len(news):
        return jsonify(news[index])
    else:
        return jsonify({"error": "Invalid index"}), 400


@application.route("/candles")
def get_candles():
    """Отдаёт кэшированные данные S&P500."""
    if not CANDLES_CACHE:
        return jsonify({"error": "No candle data available"}), 200
    return jsonify(CANDLES_CACHE)


@application.route("/favicon.ico")
def favicon():
    ico_dir = application.static_folder
    ico_path = os.path.join(ico_dir, "favicon.ico")
    if os.path.exists(ico_path):
        return send_from_directory(ico_dir, "favicon.ico", mimetype="image/vnd.microsoft.icon")
    return ("", 204)

if __name__ == "__main__":
    logging.info("Запуск Flask приложения")
    application.run(debug=True)
