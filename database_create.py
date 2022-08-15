#import sqlite3
#from _config import DATABASE_PATH

#with sqlite3.connect(DATABASE_PATH) as conn:
#
#   cursor = conn.cursor()
#    
#    cursor.execute('CREATE TABLE IF NOT EXISTS tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, due_date #TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL)')
#   
#    cursor.execute("INSERT INTO tasks(name, due_date, priority, status) VALUES('Finish this tutorial', '08/11/2022', 10, 1)")
#    
#   cursor.execute("INSERT INTO tasks(name, due_date, priority, status) VALUES('Finish Real Python Course 2', '08/11/2022', #10, 1)")

from views import db
from models import Task
from datetime import date

#create the db and the db table
db.create_all()

#insert data
db.session.add(Task('Finish this tutorial', date(2022,8,12), 10, 1))
db.session.add(Task('Finish Real Python', date(2023,8,12), 10, 1))

db.session.commit()