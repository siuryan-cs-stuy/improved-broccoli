import db
import hashlib

def encrypt(string):
	return hashlib.sha224(string).hexdigest()

def adduser(username,password):
	db.adduser(username,encrypt(password))

def login(username,password):
	return encrypt(password) == db.get_pass(username)


