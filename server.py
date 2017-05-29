from flask import Flask, render_template, request
from models import Candidate, Company, Vacancy, JobCategory, Skill, db, app
import md5
import traceback
import os
import json


@app.route("/")
def index():
	templateData = {'title' : 'Home Page'}
	return render_template("index.html", **templateData )

@app.route("/api_demo")
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
		encodepassword = md5.new(pswd).hexdigest()
		
		# save candidate in db
		candidate = Candidate(name, email, encodepassword, age, phone, address, gender)
		db.session.add(candidate)
		db.session.commit()
	except Exception as exp:
		print "save_candidate(): : Got Exception: %s" % exp
		print(traceback.format_exc())
	return "Candidate Data Saved"



@app.route("/save_company", methods=['POST'])
def save_company():
	try:
		name = request.form['name']
		website = request.form['website']
		email = request.form['email']
		pswd = request.form['pswd']
		mobile = request.form['mobile']
		telno = request.form['telno']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		pin = request.form['pin']
		encodepswd = md5.new(pswd).hexdigest()
		
		# saving company in db
		company = Company(name, website, email, encodepswd, mobile, telno, address, city, state, country, pin)
		db.session.add(company)
		db.session.commit()
	except Exception as exp:
		print "save_company(): : Got Exception: %s" % exp
		print (traceback.format_exc())
	return "Company Saved"




@app.route("/save_vacancy", methods=['POST'])
def save_vacancy():
	try:
		comp_id = request.form['comp_id']
		cand_id = request.form['cand_id']
		post_date = request.form['post_date']
		expiry_date = request.form['expiry_date']
		sal_min = request.form['sal_min']
		sal_max = request.form['sal_max']
		fulltime = request.form['fulltime']

		# saving vacancy in db
		vacancy = Vacancy(comp_id, cand_id, post_date, expiry_date, sal_min, sal_max, fulltime)
		db.session.add(vacancy)
		db.session.commit()
	except Exception as exp:
		print "save_vacancy() :: Got Exception: %s" % exp
		print (traceback.format_exc())
	return "Vacancy saved"

@app.route("/save_JobCategory", methods=['POST'])
def save_JobCategory():
	try:
		title = request.form['title']

		# savin Job Category in db
		jbcategory = JobCategory(title)
		db.session.add(jbcategory)
		db.session.commit()
	except Exception as exp:
		print "save_JobCategory() :: Got Exception: %s" % exp
		print (traceback.format_exc())
	return "Save Job Category"


@app.route("/save_skill", methods=['POST'])
def save_skill():
	try:
		cat_id = request.form['cat_id']
		title = request.form['title']

		# saving skill in db
		skill = Skill(cat_id, title)
		db.session.add(skill)
		db.session.commit()
	except Exception as exp:
		print "save_skill() :: Got Excetion: %s" % exp
		print (traceback.format_exc())
	return "Save Skill"

	@app.route("/search", methods=['POST'])
	def search():
		try:
			print "search() :: %s", request.form
		except Exception as exp:
			print "search() :: Got Exception: %s" % exp
			print (traceback.format_exc())
		return "Job Search"



#################################################################
#																#
#							Main Server							#
#																#
#################################################################
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
