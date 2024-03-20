import os
import sqlite3 
from flask import Flask, render_template, request, redirect, session, flash, g
from pathlib import Path

#Defining Flask ap
app = Flask(__name__)
app.secret_key = "key"

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


#Home page
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
        #todos[task['status']].append(task)
        task_dict = {'id': task[0], 'taskname': task[1], 'status': task[2]}  # Assuming id, taskname, and status are in positions 0, 1, and 2 respectively
        todos[task[2]].append(task_dict)

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
    return redirect('/login')

#Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password =  request.form['confirm_password']

        #Check if the user already exists
        cur = get_db().cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        exisited_user = cur.fetchone() #Retrieves the user dans
        if exisited_user:
            flash('Username already exists. Please create a different username.', 'error')
            return redirect('/register')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please re-enter your passwords.', 'error')
            return redirect('/register')

        #Insert new user into the database
        try:
           cur.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, password))
           get_db().commit()
           flash('Registration successful! You can login' , 'success')
           return redirect ('/login')
        except Exception as e:
            # Rollback the transaction if an error occurs
            get_db().rollback()
            flash(f'Error: {e}', 'error')

    return render_template('register.html')

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
            # Execute SQL query to insert todo into the database
            cur.execute("INSERT INTO todos(taskname, status) VALUES(?,?)", (todo, status))
            # Commit changes
            get_db().commit() 
            flash('Todo added successfully', 'success')
        except Exception as e:
            # Rollback the transaction if an error occurs
            get_db().rollback()
            flash(f'Error: {e}', 'error')
    else:
        flash('Todo or status cannot be empty!', 'error')
    return redirect('/')

@app.route('/update/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    if 'username' not in session:
        return redirect('/login')
    
    # Get database cursor
    cur = get_db().cursor()

    try:
        #Extract data from the reauest
        new_taskname = request.form.get('new_taskname')
        new_status = request.form.get('new_status')

        # Execute SQL query to update the status of the todo item
        cur.execute("UPDATE todos SET taskname=?, status=? WHERE id=?", (new_taskname, new_status, todo_id,))
        # Commit changes
        get_db().commit()
        flash('Todo updated successfully', 'success')
    except Exception as e:
        # Rollback the transaction if an error occurs
        get_db().rollback()
        flash(f'Error: {e}', 'error')

    return redirect('/')

@app.route('/remove/<int:todo_id>', methods=['POST'])
def remove_todo(todo_id):
    if 'username' not in session:
        return redirect('/login')
    
    # Get database cursor
    cur = get_db().cursor()
    
    try:
        # Execute SQL query to delete todo from the database
        cur.execute("DELETE FROM todos WHERE id=?", (todo_id,))
        # Commit changes
        get_db().commit()
        flash('Todo removed successfully', 'success')
    except Exception as e:
        # Rollback the transaction if an error occurs
        get_db().rollback()
        flash(f'Error: {e}', 'error')

    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

#Chekc if the database is NULL then create one
if not Path('database.db').exists():
    #Read SQL file from todo.sql
    sql = Path('todo.sql').read_text()
    with app.app_context():
        db = get_db() #connect to db
        db.cursor().executescript(sql)
        db.commit()