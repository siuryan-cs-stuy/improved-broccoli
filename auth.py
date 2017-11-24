import os
import db
import hashlib
from flask import session
def make_secret_key():
	return os.urandom(32)

def encrypt(string):
	return hashlib.sha224(string).hexdigest()

def adduser(username,password):#creates a new account
	db.adduser(username,encrypt(password))

def match(username,password):#checks if password matches username
	return encrypt(password) == db.get_pass(username)

def in_session():#checks to see of user is already logged in
	return ('username' in session and 'password' in session and match(session.get('username'),session.get('password')))

def login(username, password): #creates a new session if username and password match
	#this function excepts the password in its non-encrypted form
	encrypted_password = encrypt(password)
	if(match(username,encrypted_password)):
		session['username'] = username
		session['password'] = encrypted_password
		return True
	else:
		return False
