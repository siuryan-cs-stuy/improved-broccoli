from flask import Flask, render_template, request
import api.py

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/index')
def index():
    return redirect(url_for('/'))

#if there is an exact match, redirects to profile with the id passed as a parameter; if not, redirects to result page with list of all ids passed
@app.route('/search', methods=["POST", "GET"])
def search():
    getsearch = ""
    if request.method == 'POST': 
        getSearch = request.form('search')
    if request.method == 'GET':
        getSearch = request.get('search')
    ids = api.getId(getSearch)
    if len(id) == 1:
        return redirect(url_for('/profile', schoolId = ids[1]))
    else:
        return redirect(url_for('/results', schoolIds = ids))

@app.route('/profile', methods=["POST", "GET"])
def profile():
    schoolId = request.form('schoolId')
    name = api.getName(schoolId)
    city = api.getCity(schoolId)
    state = api.getState(schoolId)
    webiste = api.getUrl(schoolId)
    netPriceSite = api.getPriceUrl(schoolId)
    gender = api.getGender(schoolId)
    admRate = api.getAdmRate(schoolId)
    #satInfo and actInfo are lists of overall and section averages
    satInfo = api.getSatInfo(schoolId)
    actInfo = api.getActInfo(schoolId)
    avgPrice = api.getPrice(schoolId)
    return render_template('profile.html', name = name, city = city, state = state, website = website, netPriceSite = netPriceSite, gender = gender, admRate = admRate, satInfo = satInfo, actInfo = actInfo, avgPrice = avgPrice)

#renders results.html and passes list of ids and list of names 
@app.route('/results', methods=["POST", "GET"])
def results():
    idList = request.form('schoolIds')
    nameList = []
    for school in ids:
        nameList.append(api.getName(school))
    return render_template('results.html', ids = idList, names = nameList)
    
    



if __name__ == '__main__':
    app.debug = True
    app.run()
