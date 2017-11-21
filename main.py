from flask import Flask, render_template, request
import api
import config

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#if there is an exact match, redirects to profile with the id passed as a parameter; if not, redirects to result page with list of all ids passed
@app.route('/search')
def search():
    query = ""
    if request.method == 'GET':
        query = request.get('search')
    ids = api.getId(query)
    if len(ids) == 1:
        return redirect(url_for('/profile', school_id = ids[1]))
    else:
        return redirect(url_for('/results', schoolIds = ids))

@app.route('/profile')
def profile():
    college = {}
    school_id = request.args.get('school_id')
    college['school_id'] = school_id
    college['name'] = api.getName(school_id)
    college['city'] = api.getCity(school_id)
    college['state'] = api.getState(school_id)
    website = api.getUrl(school_id)
    netPriceSite = api.getPriceUrl(school_id)
    gender = api.getGender(school_id)
    admRate = api.getAdmRate(school_id)
    #satInfo and actInfo are lists of overall and section averages
    satInfo = api.getSat(school_id)
    actInfo = api.getAct(school_id)
    avgPrice = api.getPrice(school_id)
    return render_template('profile.html', college = college, website = website, netPriceSite = netPriceSite, gender = gender, admRate = admRate, satInfo = satInfo, actInfo = actInfo, avgPrice = avgPrice, GOOGLE_API_KEY = config.GOOGLE_API_KEY)

#renders results.html and passes list of ids and list of names 
@app.route('/results', methods=["POST", "GET"])
def results():
    idList = request.form('school_ids')
    nameList = []
    for school in ids:
        nameList.append(api.getName(school))
    return render_template('results.html', ids = idList, names = nameList)

if __name__ == '__main__':
    app.debug = True
    app.run()
