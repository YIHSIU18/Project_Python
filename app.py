import os
import sqlite3 
from flask import Flask, render_template, request, redirect, session, flash, g
from pathlib import Path

#Defining Flask ap
app = Flask(__name__)
app.secret_key = "key"

#User credentials
#users = ('admin', 'admin')

#Flask-SQLit
DATABASE = 'database.db'

#Connect to database SQLite3
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

#Disconnect from database SQLite
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#
@app.route('/')
def home():
    if 'username' not in session:
        return redirect('/login')
    cur = get_db().cursor()
    #Execute the SQL auery to retrieve tasks from database
    cur.execute("SELECT * FROM todos")
    #Fetch all the rows from database
    tasks = cur.fetchall()
        # Create a dictionary to store tasks categorized by status
    todos = {'todo': [], 'In Progress': [], 'complete': []}
    for task in tasks:
        # Append each task to the corresponding status list in the dictionary
        todos[task['status']].append(task)
    
    return render_template('home.html', todos=todos)

#Login page    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = get_db().cursor()
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password));
        user = cur.fetchone()
        # Validation user = admin password = admin
        if user:
            session['username'] = username
            flash('Logged in ok', 'success')
            return redirect('/')
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')
#Logout page
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect('/login')

@app.route('/add', methods=['POST'])
def add_todo():
    if 'username' not in session:
        return redirect('/login')
    todo = request.form.get('todo')
    status = request.form.get('status')
    if todo and status:
        #Get database cursor
        cur = get_db().cursor()
        try:
            #Execute SQL auery to insert todo into the database
            cur.execute("INSERT INTO todos(taskname, status) VALUES(?,?)", (todo, status))
            #Commit changes
            get_db().commit()
            flash('Todo added okay', 'Success')
        except Exception as e:
            # Rollback the transaction if an error occurs
            get_db().rollback()
            flash(f'Error: {e}', 'error')
    else:
        flash('Todo or status cannot be empty!', 'error')
    return redirect('/')

@app.route('/remove/<string:status>/<int:index>')
def remove_todo(status, index):
    if 'username' not in session:
        return redirect('/login')
    if status in session['todos'] and 0 <= index < len(session['todos'][status]):
        del session['todos'][status][index]
        flash('Todo removed successfully!', 'success')
    else:
        flash('Invalid todo index!', 'error')
    return redirect('/')

@app.route('/erro')
def other_page(page_name):
    response = make_response('The page named %s does not exist.' \
                            % page_name, 404)
    return response

#Chekc if the database is NULL then create one
if not Path('database.db').exists():
    #Read SQL file from todo.sql
    sql = Path('todo.sql').read_text()
    with app.app_context():
        db = get_db() #connect to db
        db.cursor().executescript(sql)
        db.commit()