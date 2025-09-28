1. Сначала запустите db_creator.py для создания базы данных.

2. База данных состоит из 8 параметров:
"id" (создаётся автоматически, с ней ничего не нужно делать);
"init_text", "short_text", "analysis_text", "url" - текстовый формат;
"num_views" - целое число;
"dt" - текстовый формат. Это означает datatime, но в SQLite3 формат datetime не поддерживается. Для этого необходимо использовать posgreSQL;
"hashtag" - текстовый формат. Можно добавить несколько параметров, но они должны быть в формате "smth1, smth2, smth3", то есть текстовый формат остаётся текстовым. Или придётся использовать PostgreSQL.

3. В essential_funcs.py хранятся функции "single_insert_web", "multiple_insert_web", "multiple_extract_web", "clear_database_web".

4. Чтобы добавить один элемент, необходимо передать (init_text, short_text, analysis_text, num_views, url, dt, hashtag) в функцию "single_insert_web". То же самое с "multiple_insert_web", но передаётся список параметров.

5. Для извлечения информации из базы данных используйте функцию "multiple_extract_web" без параметров. В результате вы получите список строк.

6. Для очистки базы данных используйте функцию "clear_database_web".