import sqlite3


def single_insert(info):
    conn = sqlite3.connect('smth.db')
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
    

# extraction of all info from database for website
def multiple_extract():
    conn = sqlite3.connect('smth.db')
    cursor = conn.cursor()

    # select 5 last news from db
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    conn.close()

    return rows


def insert_smth_keke():
    for i in range(5):
        info = ("kek", i, "init_text", "summary", "advice", "source", "source_url")
        single_insert(info)


# main function
if __name__ == "__main__":
    conn = sqlite3.connect('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/database/web_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()

    print(rows)
    print(len(rows))
