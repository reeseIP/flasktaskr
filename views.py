import sqlite3
from functools import wraps

from flask import Flask, flash, redirect, render_template, \
    request, session, url_for, g
    
# set up app and config
app = Flask(__name__)
app.config.from_object('_config')

# helper functions

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])
    
def login_required():
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap
    
# route handlers

@app.route('/add/')
@login_required
def new_task():
    g.db = connect_db()
    name = request.form['name']
    due_date = request.form['due_date']
    priority = request.form['priority']
    if not name or not due_date or not priority:
        flash('All fields are required. Please try again.')
        return redirect(url_for('tasks'))
    else:
        cursor = g.db.execute('INSERT INTO tasks(name, due_date, priority, status) VALUES(?,?,?,1)', [ 
            request.form['name'],
            request.form['due_date'],
            request.form['priority']
            ])
        g.db.commit()
        g.db.close()
        flash('New entry has been created.')
        return redirect(url_for('tasks'))
        
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    g.db = connect.db()
    g.db.execute('UPDATE tasks SET status=0 WHERE task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('Task '+str(task_id)+' has been marked complete.')
    return redirect(url_for('tasks'))
    
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    g.db = connect_db()
    g.db.execute('DELETE FROM tasks WHERE task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('Task '+str(task_id)+' has been deleted.')
    return redirect(url_for('tasks'))

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Goodbye!')
    return redirect(url_for('login'))
    
@app.route('/', methods =['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
          or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid credentials. Please try again'
            return render_template('login.html',error=error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('tasks'))
    return render_template('login.html')
    
@app.route('/tasks/')
@login_required
def tasks():
    g.db = connect_db()
    cursor = g.db.execute('SELECT name, due_date, priority, task_id FROM tasks WHERE status=1')
    open_tasks = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in \ cursor.fetchall()]
    
    cursor = g.db.execute('SELECT name, due_date, priority, task_id FROM tasks WHERE status=0')
    closed_tasks = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in \
    cursor.fetchall()]
    g.db.close()
    
    return render_template(
        'tasks.html'
        form = AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks)