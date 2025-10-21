import sqlite3


# inserts if data is different
def single_insert_web(info):
    conn = sqlite3.connect('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/database/web_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT datetime FROM posts")
    datetimes = [row[0] for row in cursor.fetchall()]

    if str(info[1]) in datetimes:
        conn.close()
        return False
    else:
        # Insert a single record
        cursor.execute("INSERT INTO posts (title, datetime, init_text, summary, advice, source, source_url) VALUES (?, ?, ?, ?, ?, ?, ?)", info)
        conn.commit()
        conn.close()

        return True


def multiple_insert_web(info):
    conn = sqlite3.connect('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/database/web_database.db')
    cursor = conn.cursor()

    # Insert multiple record
    cursor.executemany("INSERT INTO posts (title, datetime, init_text, summary, advice, source, source_url) VALUES (?, ?, ?, ?, ?, ?, ?)", info)
    conn.commit()
    conn.close()

    return True


# extraction of all info from database for website
def multiple_extract_web():
    conn = sqlite3.connect('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/database/web_database.db')
    cursor = conn.cursor()

    # select 5 last news from db
    cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()

    return rows



def clear_database_web():
    conn = sqlite3.connect('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/database/web_database.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM posts;')
    conn.commit()

    conn.close()
    return True
