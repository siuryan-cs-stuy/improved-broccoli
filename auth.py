import os
import db
import hashlib
from flask import session

#encrypts the string
def encrypt(string): 
    return hashlib.sha224(string).hexdigest()

#creates a new account
def add_user(username,password):
    return db.adduser(username,encrypt(password))

#checks if password matches username
def match(username,password):
    return encrypt(password) == db.get_pass(username)

#checks if the user exists on not
def user_exists(username): 
    return db.get_pass(username) is not None

#checks to see of user is already logged in
def logged_in():
    return 'username' in session

#creates a new session if username and password match
#this function excepts the password in its non-encrypted form
def login(username, password):
    if(match(username,password)):
        session['username'] = username
        return True
    else:
        return False

#removes login cookie
def logout(): 
    if logged_in():
        session.pop('username')
