1. initially launch db_creator.py to create database

2. database consists of 8 parameters:
"id" (creates automatically, doesn't have to do anything with it); 
"init_text", "short_text", "analysis_text", "url" - TEXT format;
"num_views" - integer;
"dt" - TEXT. It means datatime, but sqlite3 doesn't provide datetime format. In order to make it so, have to use posgreSQL;
"hashtag" - TEXT. Can add multiple, but has to be in "smth1, smth2, smth3" format, so still the text format. Or have to use postgreSQL

3. in essential_funcs.py stored functions "single_insert_web", "multiple_insert_web", "multiple_extract_web", "clear_database_web"

4. To add single raw, have to pass (init_text, short_text, analysis_text, num_views, url, dt, hashtag) in "single_insert_web" function. Same with "multiple_insert_web", but passing parameter is list

5. To extract info from db, use "multiple_extract_web" function, passing no parameters. Will give you a list of rows

6. To clear database, use function "clear_database_web"