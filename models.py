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


class Candidates(db.Model):
	__tablename__ = 'candidates'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(60))
	email = db.Column(db.String(60), unique=True)
	age = db.Column(db.Integer)
	phone = db.Column(db.Integer, unique=True)
	address = db.Column(db.String(60))
	gender = db.Column(db.String(60))
	ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

	def __init__(self, name, email, age, phone, address, gender):
		self.name = name
        self.email = email
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
	mobile = db.Column(db.Integer, unique=True)
	address = db.Column(db.String(60))
	city = db.Column(db.String(60))
	state = db.Column(db.String(60))
	country = db.Column(db.String(60))
	zip_code = db.Column(db.Integer)
	ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

	def __init__(self,name, website, email, mobile, address, city, state, country, zip_code):
		self.name = name
		self.website = website
		self.email = email
		self.mobile = mobile
		self.address = address
		self.city = city
		self.state = state
		self.country = country
		self.zip_code = zip_code
	
class Vocancy(db.Model):
	__tablename__ = 'vocancy'

	id = db.Column(db.BigInteger, primary_key=True)
	comp_id = db.Column(db.BigInteger, ForeignKey('company.id'))
	candi_id = db.Column(db.BigInteger, ForeignKey('candidates.id'))
	post_date = db.Column(db.String(60))
	expiry_date = db.Columndb(db.String(60))
	sal_min = db.Column(db.Integer)
	sal_max = db.Column(db.Integer)
	fullTime_parttime = db.Column(db.String(60))
	ts = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

	def __init__(self, comp_id, candi_id, post_date, expiry_date, sal_min, sal_max, fullTime_parttime):
		self.comp_id = comp_id
		self.candi_id = candi_id
		self.post_date = post_date
		self.expiry_date = expiry_date
		self.sal_min = sal_min
		self.sal_max = sal_max
		self.fullTime_parttime = fullTime_parttime

try:
    print ("================================= create_all ===================================")
    db.create_all()
except:
    pass