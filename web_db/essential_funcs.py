import sqlite3

def single_insert_web(info):
    conn = sqlite3.connect('web_database.db')
    cursor = conn.cursor()

    # Insert a single record
    cursor.execute("INSERT INTO posts (init_text, short_text, analysis_text, num_views, url, dt, hashtag) VALUES (?, ?, ?, ?, ?, ?, ?)", info)
    conn.commit()
    conn.close()

    return True


def multiple_insert_web(info):
    conn = sqlite3.connect('web_database.db')
    cursor = conn.cursor()

    # Insert multiple record
    cursor.executemany("INSERT INTO posts (init_text, short_text, analysis_text, num_views, url, dt, hashtag) VALUES (?, ?, ?, ?, ?, ?, ?)", info)
    conn.commit()
    conn.close()

    return True


# extraction of all info from database for website
def multiple_extract_web():
    conn = sqlite3.connect('web_database.db')
    cursor = conn.cursor()

    # Select all data from the users table
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    conn.close()

    return rows


def clear_database_web():
    conn = sqlite3.connect('web_database.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM posts;')
    conn.commit()

    conn.close()
    return True
