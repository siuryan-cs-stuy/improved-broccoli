import sqlite3

f = "app.db"
db = sqlite3.connect(f)
c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS favorites (college_id INTEGER, user_id INTEGER);')
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username TEXT, password TEXT);')

db.close()

def getID(user):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT id FROM users WHERE username = "%s";' %(user))
    result = c.fetchall()
    db.close()
    return results[0][0]

def adduser(username,password):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    if get_pass(username) is None:
        c.execute('SELECT max(id) FROM users;')
        result = c.fetchall()
        result = result[0][0] + 1
        c.execute('INSERT INTO users VALUES("%d","%s", "%s");' %(result,username, password))
        db.commit()
        db.close()
        return true
    db.close()
    return false
    
def get_pass(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT password FROM users WHERE username=\'%s\';' %(username))
    result = c.fetchall()
    if result == []:
        db.close()
        return None
    else:
        db.close()
        return result[0][0]
