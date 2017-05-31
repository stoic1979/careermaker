#
# script for various ORM models for project
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boatdb.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost/careermaker'

# set as part of the config
SECRET_KEY = 'many random bytes'

# or set directly on the app
app.secret_key = SECRET_KEY

db = SQLAlchemy(app)

# UserMixin provides features for handling login etc
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(60), unique=True)


class Candidate(db.Model):
	__tablename__ = 'candidate'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(60))
	email = db.Column(db.String(60), unique=True)
	pswd = db.Column(db.String(60))
	age = db.Column(db.Integer)
	phone = db.Column(db.String(16))
	address = db.Column(db.String(60))
	gender = db.Column(db.String(60))
	created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

	def __init__(self, name, email, pswd, age, phone, address, gender):
		self.name = name
		self.email = email
		self.pswd = pswd
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
	pswd = db.Column(db.String(60))
	mobile = db.Column(db.String(16), unique=True)
	telno = db.Column(db.String(16), unique=True)  # landline No
	address = db.Column(db.String(60))
	city = db.Column(db.String(60))
	state = db.Column(db.String(60))
	country = db.Column(db.String(60))
	pin = db.Column(db.Integer)
	created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

	def __init__(self, name, website, email, pswd, mobile, telno, address, city, state, country, pin):
		self.name = name
		self.website = website
		self.email = email
		self.pswd = pswd
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
	created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

	def __init__(self, comp_id, cand_id, post_date, expiry_date, sal_min, sal_max, fulltime):
		self.comp_id = comp_id
		self.cand_id = cand_id
		self.post_date = post_date
		self.expiry_date = expiry_date
		self.sal_min = sal_min
		self.sal_max = sal_max
		self.fulltime = fulltime


class JobCategory(db.Model):
	__tablename__ = 'jobcategory'

 	id = db.Column(db.BigInteger, primary_key=True)
 	title = db.Column(db.String(120))
 	created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

        #########################################################
        #                                                       #
        # Flask admin needs a model constructor with no params, #
        # So using default params here to fix error             #
        #                                                       #
        #########################################################
 	def __init__(self, title="", created_at=None):
 		self.title = title
                if created_at:
                    self.created_at = created_at

        def __str__(self):
            return self.title


class Skill(db.Model):
 	__tablename__ = 'skill'
 	
 	id = db.Column(db.BigInteger, primary_key=True)
 	category = db.Column(db.BigInteger, ForeignKey('jobcategory.id'))
 	title = db.Column(db.String(120))
 	created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
	
	def __init__(self, category, title):
		self.category = category
		self.title = title


if __name__ == '__main__':
	try:
		print ("CREATING ALL TABLES")
		db.create_all()
	except Exception as exp:
		print "create_all() :: Got Excetion: %s" % exp
