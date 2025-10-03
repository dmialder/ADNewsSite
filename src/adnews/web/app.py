from flask import Flask, render_template, jsonify
import csv
import sqlite3
from src.adnews.database.essential_funcs import *
from threading import Lock, Thread
import os
import time
import json
import yfinance as yf

application = Flask(__name__)
news_lock = Lock()
rotation_index = [0]  # используем список для изменения внутри функции
SP500_DATA_PATH = os.path.join("static", "js", "sp500_data.json")


def fetch_sp500_loop():
    while True:
        try:
            ticker = yf.Ticker("^GSPC")  # S&P 500 индекс
            data = ticker.history(period="1d", interval="1m")
            data = data.tail(90)

            candles = []
            for timestamp, row in data.iterrows():
                candles.append({
                    "time": str(timestamp),
                    "open": round(row["Open"], 2),
                    "close": round(row["Close"], 2),
                    "high": round(row["High"], 2),
                    "low": round(row["Low"], 2)
                })

            with open(SP500_DATA_PATH, "w") as f:
                json.dump(candles, f)

            print(f"[INFO] Обновлены данные S&P500: {len(candles)} свечей")
        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке данных S&P500: {e}")

        time.sleep(900)  # 15 минут

def load_news():
    news = []
    try:
        with open("news.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                if i >= 5:
                    break
                news.append(row)
        print(news)
    except Exception as e:
        print(f"Ошибка при чтении news.csv: {e}")
    return news


def load_news_db():
    news = []
    load = multiple_extract_web()
    single_dict_load = dict()
    for i in range(min(len(load), 5)):
        single_dict_load["title"] = load[i][1]
        single_dict_load["datetime"] = load[i][2]
        single_dict_load["summary"] = load[i][4]
        single_dict_load["advice"] = load[i][5]
        single_dict_load["source_url"] = load[i][8]
        news.append(single_dict_load)
        single_dict_load = dict()
    return news


@application.route("/")
def index():
    return render_template("index.html")

@application.route("/news")
def get_news():
    with news_lock:
        news = load_news_db()
        print(type(news))
        print(type(news[0]))
        if not news:
            return jsonify({"error": "No news available"}), 500
        selected = news[rotation_index[0] % len(news)]
        rotation_index[0] = (rotation_index[0] + 1) % len(news)
    return jsonify({"news": news, "selected": selected})

@application.route("/select/<int:index>")
def select_news(index):
    news = load_news_db()
    if 0 <= index < len(news):
        return jsonify(news[index])
    else:
        return jsonify({"error": "Invalid index"}), 400

if __name__ == "__main__":
    Thread(target=fetch_sp500_loop, daemon=True).start()
    application.run(debug=True)