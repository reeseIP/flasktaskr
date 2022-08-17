from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime 

with sqlite3.connect(DATABASE_PATH) as conn:
    
    # create a cursor
    c = conn.cursor()
    
    # temporarily change the name of tasks table
    c.execute('ALTER TABLE tasks RENAME TO old_tasks')
    
    # recreate a new tasks table with updated schema
    db.create_all()
    
    # get the old data
    c.execute('SELECT name, due_date, priority, status FROM old_tasks ORDER BY task_id ASC')
    
    # save all rows as a list of tuples with added fields
    data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in c.fetchall()]
    
    # insert the data back into the tasks table
    c.executemany('INSERT INTO tasks(name, due_date, priority, status, posted_date, user_id)\
                        VALUES(?,?,?,?,?,?)', data)
            
    # drop the temp table
    c.execute('DROP TABLE old_tasks')
    