import sqlite3
from src.adnews.analysis.analysis_maker import *
from src.adnews.analysis.nothing.advizer import *
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
        advice = row[5]
        
        if summary is None:
            summary_prompt_text = get_summarization_prompt(init_text)
            summary = gpt_process(summary_prompt_text)
        if advice is None:
            adv_prompt_text = get_advice_prompt(summary)
            advice = gpt_process(adv_prompt_text)
        
        cursor.execute("""UPDATE posts SET summary = ?, advice = ? WHERE id = ?""", (summary, advice, id))

    conn.commit()
    conn.close()

    return True


    



