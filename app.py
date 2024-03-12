from flask import Flask, make_response
app = Flask(__name__)
@app.route('/')
def home():
    return 'First app in Python'
@app.route('/about')
def about():
    return 'about page'
@app.route('/register')
def register():
    return 'register page'
@app.route('/login')
def login():
    return 'login page'
@app.route('/<page_name>')
def other_page(page_name):
    response = make_response('The page named %s does not exist.' \
                            % page_name, 404)
    return response
if __name__ == '__main__':
    app.run(debug=True)