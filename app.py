from flask import Flask, render_template, redirect, url_for, request, @login_required
app = Flask(__name__)
#Flask-SQLit
import sqlite3

#, make_response
@app.route('/')
def home():
    return 'Todo List'
@app.route('/about')
def about():
    return 'about page'
@app.route('/register')
def register():
    return 'register page'

#Login page    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session.['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

#Logout page
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in',None)
    flash('You were logged out.')
    return redirect(url_for('login.html'))

@app.route('/erro')
def other_page(page_name):
    response = make_response('The page named %s does not exist.' \
                            % page_name, 404)
    return response
if __name__ == '__main__':
    app.run(debug=True)