from flask import Flask, render_template, request, redirect, url_for
import api
import config

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
    return render_template('index.html')

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
    college['admRate'] = api.getAdmRate(school_id)
    #satInfo and actInfo are lists of overall and section averages
    college['satInfo'] = api.getSat(school_id)
    college['actInfo'] = api.getAct(school_id)
    college['avgPrice'] = api.getPrice(school_id)

    #testing
    college['degrees_labels'] = ['Computer Science', 'Engineering', 'Mathematics', 'Science', 'Social Science', 'English', 'History', 'Other']
    college['degrees_data'] = [0.35, 0.2, 0.15, 0.2, 0.05, 0.03, 0.01, 0.01]

    return render_template('profile.html', college = college, GOOGLE_API_KEY = config.GOOGLE_API_KEY)

#renders results.html and passes list of ids and list of names 
@app.route('/results')
def results():
    query = request.args.get('search')
    ids = api.getId(query)
    if len(ids) == 1:
        return redirect(url_for('profile', school_id = ids[1]))

    schools = {}
    for school_id in ids:
        schools[school_id] = api.getName(school_id)

    return render_template('results.html', schools = schools)

if __name__ == '__main__':
    app.debug = True
    app.run()
