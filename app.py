from flask import Flask, render_template, jsonify
import csv
from threading import Lock

application = Flask(__name__)
news_lock = Lock()
rotation_index = [0]  # используем список для изменения внутри функции

def load_news():
    news = []
    try:
        with open("news.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                if i >= 5:
                    break
                news.append(row)
    except Exception as e:
        print(f"Ошибка при чтении news.csv: {e}")
    return news

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/news")
def get_news():
    with news_lock:
        news = load_news()
        if not news:
            return jsonify({"error": "No news available"}), 500
        selected = news[rotation_index[0] % len(news)]
        rotation_index[0] = (rotation_index[0] + 1) % len(news)
    return jsonify({"news": news, "selected": selected})

@application.route("/select/<int:index>")
def select_news(index):
    news = load_news()
    if 0 <= index < len(news):
        return jsonify(news[index])
    else:
        return jsonify({"error": "Invalid index"}), 400

if __name__ == "__main__":
    application.run(debug=True)
