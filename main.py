from flask import Flask, render_template, request, redirect, url_for, session, flash
import api
import config
import auth
import os
import db

app = Flask(__name__)

def make_secret_key():
    return "test"
    #return os.urandom(32)

app.secret_key = make_secret_key()

def format_currency(value):
    return "${:,}".format(value)

def format_url(value):
    return ''.join(['http://', value])

app.jinja_env.filters['currency'] = format_currency
app.jinja_env.filters['external_url'] = format_url
app.jinja_env.globals.update(logged_in = auth.logged_in)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # check if username exists
        if auth.user_exists(username):
            if auth.login(username, password):
                flash('Welcome %s!' % username)
                return redirect('index')
            else:
                flash('Incorrect username/password combination.')
        else:
            flash('Username does not exist.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if auth.logged_in():
        auth.logout()
        flash('Logged out.')
    else:
        flash('Not logged in.')
    return redirect('index')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 == password2:
            if auth.add_user(username, password1):
                auth.login(username, password1)
                flash('Welcome %s!' % username)
                return redirect('index')
            else:
                flash('Username already exists.')
        else:
            flash('Passwords do not match.')
    return render_template('create.html')

@app.route('/profile')
def profile():
    college = {}
    school_id = request.args.get('school_id')
    college['school_id'] = school_id
    college['name'] = api.getName(school_id)
    college['city'] = api.getCity(school_id)
    college['state'] = api.getState(school_id)
    college['website'] = api.getUrl(school_id)
    college['netPriceSite'] = api.getPriceUrl(school_id)
    college['gender'] = api.getGender(school_id)
    college['completion'] = api.getCompletion(school_id)
    college['admRate'] = api.getAdmRate(school_id)
    #satInfo and actInfo are lists of overall and section averages
    college['satInfo'] = api.getSat(school_id)
    college['actInfo'] = api.getAct(school_id)
    college['size'] = api.getSize(school_id)
    college['avgPrice'] = api.getPrice(school_id)
    college['debt'] = api.getDebt(school_id)
    college['pell'] = api.getPellGrant(school_id)

    degrees = api.getDegrees(school_id)

    degrees_labels = []
    degrees_data = []
    for deg in degrees:
        degrees_labels.append(str(deg.replace('_', ' ').capitalize()))
        degrees_data.append(round(float(degrees[deg]), 2))

    college['degrees_labels'] = degrees_labels
    college['degrees_data'] = degrees_data

    eth = api.getEthnicity(school_id)

    eth_labels = []
    eth_data = []
    for e in eth:
        eth_labels.append(e)
        eth_data.append(round(float(eth[e]), 2))

    college['eth_labels'] = eth_labels
    college['eth_data'] = eth_data

    #testing
    #college['degrees_labels'] = ['Computer Science', 'Engineering', 'Mathematics', 'Science', 'Social Science', 'English', 'History', 'Other']
    #college['degrees_data'] = [0.35, 0.2, 0.15, 0.2, 0.05, 0.03, 0.01, 0.01]

    s_id = db.getID(session['username'])
    favorited = school_id in db.getfavs(s_id)

    return render_template('profile.html', college = college, GOOGLE_API_KEY = config.GOOGLE_API_KEY, search_page = True, favorited = favorited)

#renders results.html and passes list of ids and list of names 
@app.route('/results')
def results():
    query = request.args.get('search')
    ids = api.getId(query)
    if len(ids) == 1:
        return redirect(url_for('profile', school_id = ids[0]))

    schools = {}
    school_locations = {}
    for school_id in ids:
        schools[school_id] = api.getName(school_id)
        school_locations[school_id] = api.getCity(school_id) + ', ' + api.getState(school_id)

    return render_template('results.html', schools = schools, school_locations = school_locations, search_page = True)

@app.route('/favorites')
def favorites():
    faveList = []
    if auth.logged_in():
        s_id = db.getID(session['username'])
        for school in db.getfavs(s_id):
            faveList.append(school)
        schools = {}
        for school_id in faveList:
            schools[school_id] = api.getName(school_id)
        return render_template('favorites.html', schools = schools, search_page = True, username = session['username'])
    else:
        flash('You must be logged in to view this page.')
        return redirect('index')

@app.route('/toggle_fave', methods=['GET', 'POST'])
def toggle_fave():
   school_id = int(request.form.get('favorite'))
   s_id = db.getID(session['username'])
   if school_id in db.getfavs(s_id):
       db.removeFave(school_id, s_id)
   else:
       db.addfav(school_id, s_id)
   return redirect(url_for('profile', school_id = school_id))


if __name__ == '__main__':
    app.debug = True
    app.run()
