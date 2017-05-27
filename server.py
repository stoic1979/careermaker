from flask import Flask, render_template, request
from models import Candidate, Company, Vacancy, db, app
from flask_restful import Resource, Api, reqparse
#from utils import *
import traceback
import os
import json

# app = Flask(__name__)


@app.route("/")
def index():
	templateData = {'title' : 'Home Page'}
	return render_template("index.html", **templateData )

@app.route("/candi_form")
def candidate_form():
	templateData = {'title' : 'Home Page'}
	return render_template("api_demo.html", **templateData )

@app.route("/save_candidate", methods=['POST'])
def save_candidate():
	try:
		print "Candidate Data(): :", request.form
		name = request.form['name']
		email = request.form['email']
		pswd = request.form['pswd']
		age = request.form['age']
		phone = request.form['phone']
		address = request.form['address']
		gender = request.form['gender']
		candidate = Candidate(name, email, password, age, phone, address, gender)
		db.session.add(candidate)
		db.session.commit()
	except Exception as exp:
		print "save_candidate(): : Got Exception: %sd" % exp
		print(traceback.format_exc())
	return "Candidate Data Saved"




#################################################################
#																#
#							Main Server							#
#																#
#################################################################
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True, threaded=True)