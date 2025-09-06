import sqlite3

conn = sqlite3.connect('web_database.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        init_text TEXT NOT NULL,
        short_text TEXT NOT NULL,
        analysis_text TEXT NOT NULL,
        num_views INTEGER,
        url TEXT NOT NULL,
        dt TEXT NOT NULL,
        hashtag TEXT
    )
''')

conn.commit()
conn.close()