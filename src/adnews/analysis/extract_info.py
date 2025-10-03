import sqlite3


def refill_empty_sumirizer():
    conn = sqlite3.connect('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/database/web_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE summary IS NOT NULL")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        init_text = row[3]
        summary = summarizer(init_text)
        cursor.execute("""UPDATE posts SET summary = ? WHERE id = ?""", (summary, id))

    conn.commit()
    conn.close()

    return True


def refill_empty_advise():
    conn = sqlite3.connect('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/database/web_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE advise IS NOT NULL")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        summary = row[3]
        advise = advizer(summary)
        cursor.execute("""UPDATE posts SET advise = ? WHERE id = ?""", (advise, id))

    conn.commit()
    conn.close()

    return True

    



