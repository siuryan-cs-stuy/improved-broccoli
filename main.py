from flask import Flask, render_template
import api
import config

app = Flask(__name__)

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    print config.GOOGLE_API_KEY
    return render_template('profile.html', GOOGLE_API_KEY = config.GOOGLE_API_KEY)

if __name__ == '__main__':
    app.debug = True
    app.run()
