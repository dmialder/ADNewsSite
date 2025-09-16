import sqlite3

conn = sqlite3.connect('web_database.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        datetime TEXT NOT NULL,
        init_text TEXT NOT NULL,
        summary TEXT NOT NULL,
        advice TEXT NOT NULL,
        num_views INTEGER,
        source_url TEXT NOT NULL,
        hashtag TEXT
    )
''')

conn.commit()
conn.close()