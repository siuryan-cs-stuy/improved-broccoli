import os
import db
import hashlib
from flask import session

def encrypt(string):
    return hashlib.sha224(string).hexdigest()

def add_user(username,password):#creates a new account
    db.adduser(username,encrypt(password))

def match(username,password):#checks if password matches username
    return encrypt(password) == db.get_pass(username)

def logged_in():#checks to see of user is already logged in
    return 'username' in session

def login(username, password): #creates a new session if username and password match
    #this function excepts the password in its non-encrypted form
    encrypted_password = encrypt(password)
    if(match(username,encrypted_password)):
        session['username'] = username
        return True
    else:
        return False

def logout():
    if logged_in():
        session.pop('username')
