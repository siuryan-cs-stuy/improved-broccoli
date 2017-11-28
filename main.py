from flask import Flask, render_template, request, redirect, url_for, session, flash
import api
import config
import auth
import os
import db
import requests, requests_cache

app = Flask(__name__)

requests_cache.install_cache('college_api_cache', backend='sqlite', expire_after=600)
#creates secret key for session encryption
def make_secret_key():
    return "test"
    #return os.urandom(32)

app.secret_key = make_secret_key()

def format_currency(value):
    return "${:,}".format(value)

def format_url(value):
    return ''.join(['http://', value])

def format_percent(value):
    if value:
        return str(value * 100) + '%'
    return 'N/A'

app.jinja_env.filters['currency'] = format_currency
app.jinja_env.filters['external_url'] = format_url
app.jinja_env.filters['format_percent'] = format_percent
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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    school_id = request.args.get('school_id')
    place = None
    if 'place' in request.args:
        place = request.args.get('place')

    if request.method == 'POST':
        return redirect(url_for('toggle_fave', school_id = school_id))

    college = {}
    college['school_id'] = school_id
    college['name'] = api.get_name(school_id)
    college['city'] = api.get_city(school_id)
    college['state'] = api.get_state(school_id)
    college['website'] = api.get_url(school_id)
    college['netPriceSite'] = api.get_price_url(school_id)
    college['gender'] = api.get_gender(school_id)
    college['completion'] = api.get_completion(school_id)
    college['admRate'] = api.get_adm_rate(school_id)
    #satInfo and actInfo are lists of overall and section averages
    college['satInfo'] = api.get_sat(school_id)
    college['actInfo'] = api.get_act(school_id)
    college['size'] = api.get_size(school_id)
    college['avgPrice'] = api.get_price(school_id)
    college['debt'] = api.get_debt(school_id)
    college['pell'] = api.get_pell_grant(school_id)

    degrees = api.get_degrees(school_id)

    degrees_labels = []
    degrees_data = []
    for deg in degrees:
        degrees_labels.append(str(deg.replace('_', ' ').capitalize()))
        degrees_data.append(round(float(degrees[deg]), 2))

    college['degrees_labels'] = degrees_labels
    college['degrees_data'] = degrees_data

    eth = api.get_ethnicity(school_id)

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

    favorited = None
    if auth.logged_in():
        s_id = db.get_ID(session['username'])
        favorited = db.school_in_favs(int(school_id), s_id)
        
    return render_template('profile.html', college = college, GOOGLE_API_KEY = config.GOOGLE_API_KEY, search_page = True, favorited = favorited, place = place)


#renders results.html and passes list of ids and list of names 
@app.route('/results')
def results():
    query = request.args.get('search')
    ids = api.get_id(query)
    if len(ids) == 0:
        return render_template('results.html', noMatch = True)
                        
    if len(ids) == 1:
        return redirect(url_for('profile', school_id = ids[0]))

    schools = {}
    school_locations = {}
    for school_id in ids:
        schools[school_id] = api.get_name(school_id)
        school_locations[school_id] = api.get_city(school_id) + ', ' + api.get_state(school_id)

    return render_template('results.html', schools = schools, school_locations = school_locations, search_page = True, noMatch = False)

@app.route('/favorites')
def favorites():
    fave_list = []
    if auth.logged_in():
        s_id = db.get_ID(session['username'])
        for school in db.get_favs(s_id):
            fave_list.append(school[0])
        schools = {}
        for school_id in fave_list:
            schools[school_id] = api.get_name(school_id)
        if len(schools) == 0:
            return render_template('favorites.html', no_faves = True, username = session['username'].capitalize())
        return render_template('favorites.html', schools = schools, search_page = True, username = session['username'].capitalize(), no_faves = False)
    else:
        flash('You must be logged in to view this page.')
        return redirect('index')

@app.route('/toggle_fave')
def toggle_fave():
    school_id = int(request.args.get('school_id'))
    self_id = db.get_ID(session['username'])
    if db.school_in_favs(school_id, self_id):
        db.remove_fave(school_id, self_id)
    else:
        db.add_fav(school_id, self_id)
    return redirect(url_for('profile', school_id = school_id))


if __name__ == '__main__':
    app.debug = True
    app.run()
