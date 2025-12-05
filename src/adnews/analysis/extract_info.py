import sqlite3
from .analysis_maker import *
from .add_analysis_funcs import *


def refill_empty_summary_advice():
    conn = sqlite3.connect('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/database/web_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT * 
                        FROM posts 
                        WHERE summary IS NULL OR summary = '' 
                            OR advice IS NULL OR advice = '';""")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        init_text = row[3]
        summary = row[4]
        advice = row[5]
        
        if summary is None or summary == '':
            summary_prompt_text = get_summarization_prompt(init_text)
            summary = gpt_process(summary_prompt_text)
        if advice is None or advice == '':
            adv_prompt_text = get_advice_prompt(summary)
            advice = gpt_process(adv_prompt_text)
        
        cursor.execute("""UPDATE posts SET summary = ?, advice = ? WHERE id = ?""", (summary, advice, id))

    conn.commit()
    conn.close()

    return True


    



