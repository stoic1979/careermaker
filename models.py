#
# script for various ORM models for project
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boatdb.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost/careermaker'
db = SQLAlchemy(app)


class Candidate(db.Model):
	__tablename__ = 'candidate'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(60))
	email = db.Column(db.String(60), unique=True)
	password = db.Column(db.String(16))
	age = db.Column(db.Integer)
	phone = db.Column(db.Integer, unique=True)
	address = db.Column(db.String(60))
	gender = db.Column(db.String(60))
	ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

	def __init__(self, name, email, password, age, phone, address, gender):
		self.name = name
		self.email = email
		self.password = password
		self.age = age
		self.phone = phone
		self.address = address
		self.gender = gender 

class Company(db.Model):
	__tablename__ = 'company'
	
	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(60))
	website = db.Column(db.String(60))
	email = db.Column(db.String(60), unique=True)
	password = db.Column(db.String(16))
	mobile = db.Column(db.String(16), unique=True)
	telno = db.Column(db.String(16), unique=True)  # landline No
	address = db.Column(db.String(60))
	city = db.Column(db.String(60))
	state = db.Column(db.String(60))
	country = db.Column(db.String(60))
	pin = db.Column(db.Integer)
	ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

	def __init__(self, name, website, email, password, mobile, telno, address, city, state, country, pin):
		self.name = name
		self.website = website
		self.email = email
		self.password = password
		self.mobile = mobile
		self.telno = telno
		self.address = address
		self.city = city
		self.state = state
		self.country = country
		self.pin = pin
	
class Vacancy(db.Model):
	__tablename__ = 'vacancy'

	id = db.Column(db.BigInteger, primary_key=True)
	comp_id = db.Column(db.BigInteger, ForeignKey('company.id'))
	cand_id = db.Column(db.BigInteger, ForeignKey('candidate.id'))
	post_date = db.Column(db.String(60))
	expiry_date = db.Column(db.String(60))
	sal_min = db.Column(db.Integer)
	sal_max = db.Column(db.Integer)
	fulltime = db.Column(db.Boolean, default=True)
	ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

	def __init__(self, comp_id, cand_id, post_date, expiry_date, sal_min, sal_max, fulltime):
		self.comp_id = comp_id
		self.cand_id = cand_id
		self.post_date = post_date
		self.expiry_date = expiry_date
		self.sal_min = sal_min
		self.sal_max = sal_max
		self.fulltime = fulltime

if __name__ == '__main__':
	try:
		print ("CREATING ALL TABLES")
		db.create_all()
	except Exception as exp:
		print "create_all() :: Got Excetion: %s" % exp