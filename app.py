import os
from flask import Flask, render_template, request, redirect, session, flash
from datetime import date

#Defining Flask ap
app = Flask(__name__)
app.secret_key = "key"

#User credentials
users = ('admin', 'admin')

#Flask-SQLit
import sqlite3

#, make_response
@app.route('/')
def home():
    if 'username' not in session:
        return redirect('/login')
    if 'todos' not in session:
        session['todos'] = {'todo': [], 'In Progress': [], 'complete': []}  # Initialize as a dictionary
    return render_template('home.html', todos=session['todos'])
#Login page    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validation user = admin password = admin
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect('/')
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')
#Logout page
@app.route('/logout')
def logout():
    session.pop('username',None)
    flash('You have been logged out.', 'success')
    return redirect('/login')

@app.route('/add', methods=['POST'])
def add_todo():
    if 'username' not in session:
        return redirect('/login')
    todo = request.form.get('status')
    if todo and status:
        session['todos'][status].append(todo)
        flash('You have added a toto list', 'success')
    else:
        flash('Please add a todo list', 'error')
    return redirect('/')

@app.route('/remove/<int:index>')
def remove_todo(index):
    if 'username' not in session:
        return redirect('/login')
    if 'todos' in session and 0 <= index < len(session['todos'][status]):
        del session['todos'][status][index] 
        flash('Todo removed!','success')
    else:
        flash('Error removing todo','error')
    return redirect("/")

@app.route('/erro')
def other_page(page_name):
    response = make_response('The page named %s does not exist.' \
                            % page_name, 404)
    return response
if __name__ == '__main__':
    app.run(debug=True)