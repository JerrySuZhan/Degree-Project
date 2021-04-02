from flask import Flask, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/listing')
def listing():
    return render_template('listing-1-full.html')


@app.route('/single')
def single():
    return render_template('single-property-1.html')


@app.route('/new')
def new():
    return render_template('post.html')


@app.route('/login')
def login():
    return render_template('login-1.html')


@app.route('/signup')
def signup():
    return render_template('signup-1.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


if __name__ == '__main__':
    app.run()
