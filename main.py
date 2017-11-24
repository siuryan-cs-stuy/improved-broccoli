from flask import Flask, render_template, request, redirect, url_for
import api
import config
import sys

app = Flask(__name__)

def format_currency(value):
    return "${:,}".format(value)

def format_url(value):
    return ''.join(['http://', value])

app.jinja_env.filters['currency'] = format_currency
app.jinja_env.filters['external_url'] = format_url

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', homepage = True)

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

    return render_template('profile.html', college = college, GOOGLE_API_KEY = config.GOOGLE_API_KEY)

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

    return render_template('results.html', schools = schools, school_locations = school_locations)

if __name__ == '__main__':
    app.debug = True
    if(len(sys.argv) > 1 and sys.argv[1] == "public"):
        print "\nflask app is now public\n"
        app.run(host='0.0.0.0')
    else:
        app.run()
