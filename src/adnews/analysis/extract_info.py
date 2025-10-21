import sqlite3
from summarizer import *
from advizer import *
from add_analysis_funcs import *


def refill_empty_summary_advice():
    conn = sqlite3.connect('/var/www/u3198937/data/www/neuro-express.ru/src/adnews/database/web_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE summary IS NOT NULL OR advice IS NOT NULL")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        init_text = row[3]
        summary = row[4]
        
        if summary is None:
            summ_prompt_text = get_summarization_prompt(init_text)
            summary = YGPT_analysis(init_text, summ_prompt_text)
        
        adv_prompt_text = get_advice_prompt(summary)
        advice = YGPT_analysis(summary, adv_prompt_text)
        
        cursor.execute("""UPDATE posts SET summary = ?, advice = ? WHERE id = ?""", (summary, advice, id))

    conn.commit()
    conn.close()

    return True


    



