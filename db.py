import sqlite3

f = "app.db"
db = sqlite3.connect(f)
c = db.cursor()
c.execute('CREATE TABLE IF NOT EXISTS favorites (college_id INTEGER, user_id INTEGER);')
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username TEXT, password TEXT);')
db.close()

#returns the id of the user given the username
def getID(user):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT id FROM users WHERE username = "%s";' %(user))
    result = c.fetchall()
    db.close()
    return result[0][0]

#adds the user to the database
#do NOT use this function since the password is not encrypted
#to add a user with encryption look at the add_user(username,password) method in auth
def adduser(username,password):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    if empty():
         c.execute('INSERT INTO users VALUES(1,"%s", "%s");' %(username, password))
         db.commit()
         db.close()
         return True
    if get_pass(username) is None:
        c.execute('SELECT max(id) FROM users;')
        result = c.fetchall()
        result = result[0][0] + 1
        c.execute('INSERT INTO users VALUES("%d","%s", "%s");' %(result,username, password))
        db.commit()
        db.close()
        return True
    db.close()
    return False

#checks if the there are any existing users in the database
def empty():
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM users;')
    result = c.fetchall()
    return result == []

#returns the password of the user    
def get_pass(username):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT password FROM users WHERE username= "%s";' %(username))
    result = c.fetchall()
    if result == []:
        db.close()
        return None
    else:
        db.close()
        return result[0][0]
   
#set a college as a favorite of the user
#accepts c_id as college id and s_id as user id which you can get with getID(<username>)
def addfav(c_id, s_id):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM favorites WHERE college_id == "%d" AND user_id == "%d";'%(c_id, s_id))
    result = c.fetchall()
    if result == []:
        c.execute('INSERT INTO favorites VALUES("%d","%d");'%(c_id,s_id))
        db.commit()
        db.close()
        return True
    db.close()
    return False

#returns a dictionary of the user's favorite collegs
#s_id is user id
def getfavs(s_id):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT college_id FROM favorites WHERE user_id == "%d";' %(s_id))
    result = c.fetchall()
    db.close()
    return result

#removes a school from a user's favorite list
#removeFave(<college id>,<user id>)
def removeFave(school_id, s_id):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('DELETE FROM favorites WHERE college_id == "%d" AND user_id == "%d";' %(school_id, s_id))
    db.close()
