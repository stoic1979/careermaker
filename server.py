from flask import Flask, render_template, request, redirect, jsonify, make_response
from models import User, Candidate, \
      Company, Vacancy, JobCategory, Skill, db, app
import md5
from flask_pymongo import PyMongo
import traceback
import os

import jwt
import datetime
from functools import wraps
import json

from scraper.config import *
from scraper.db import Mdb

app = Flask(__name__)
mongo = PyMongo(app)

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from bson import ObjectId
mdb = Mdb()


######################################################
#                                                    #
# Since mongodb's _id of each record was not getting #
# json encoded, so this custom JSONEncoder is needed #
#                                                    #
######################################################
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)




# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)


class ChildView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('category', 'title', 'created_at')

admin = Admin(app, name='CareerMaker Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Candidate, db.session))
admin.add_view(ModelView(Company, db.session))
admin.add_view(ModelView(Vacancy, db.session))
admin.add_view(ModelView(JobCategory, db.session))
# admin.add_view(ModelView(Skill, db.session))
# admin.add_view(ChildVinameew(Skill, db.session))
admin.add_view(ModelView(User, db.session))


@app.route("/")
@login_required
def index():
    templateData = {'title': 'Home Page'}
    return render_template("index.html", **templateData )


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route("/api_demo")
def candidate_form():
    templateData = {'title' : 'Home Page'}
    return render_template("api_demo.html", **templateData )


@app.route("/find_company_data", methods=['POST'])
def find_company_data():
    ret = {"err": 0}
    try:
        ret = []
        print "find_company_data() ::", request.form
        login()
        cname = request.form['cname']
        # ret['Company Name'] = cname
        collection_android = mdb.db["job_vacancy_android"]
        collection_python = mdb.db["job_vacancy_python"]
        result = collection_android.find({"title": cname})
        print result
        # ret.append(result)
        for data in result:
            ret.append(data)

        result = collection_python.find({"title": cname})
        print result
        # ret.append(result)
        for data in result:
            ret.append(data)
        # testing code
        print JSONEncoder().encode({'job_vacancy %s ': ret})

        # mdb.retrieve_data(cname)
    except Exception as exp:
        print "find_company_data() :: Got exception: %s" % exp
        print(traceback.format_exc())
    # return json.dumps(ret)
    return JSONEncoder().encode({'job_vacancy': ret})


@app.route("/save_candidate", methods=['POST'])
def save_candidate():
    try:
        print "save_candidate(): :", request.form
        user_id = request.form['user_id']
        name = request.form['name']
        email = request.form['email']
        pswd = request.form['pswd']
        age = request.form['age']
        phone = request.form['phone']
        address = request.form['address']
        gender = request.form['gender']
        encodepassword = md5.new(pswd).hexdigest()

        # save candidate in db
        candidate = Candidate(user_id, name, email, encodepassword, age, phone, address, gender)
        db.session.add(candidate)
        db.session.commit()
    except Exception as exp:
        print "save_candidate(): : Got Exception: %s" % exp
        print(traceback.format_exc())
    return "Candidate Data Saved"


@app.route("/save_company", methods=['POST'])
def save_company():
    try:
        print "save_company() :: ", request.form
        user_id = request.form['user_id']
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
        company = Company(user_id, name, website, email, encodepswd, mobile, telno, address, city, state, country, pin)
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
        title = request.form['indextitle']

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
        print(traceback.format_exc())
    return "Save Skill"


@app.route("/search", methods=['POST'])
def search():
    try:
        print "search() :: %s", request.form
    except Exception as exp:
        print "search() :: Got Exception: %s" % exp
        print (traceback.format_exc())
    return "Job Search"


@app.route("/user_register", methods=['POST'])
def user_register():
    try:
        print "user_register() :: ", request.form
        username = request.form['username']
        pswd = request.form['pswd']
        encodepswd = md5.new(pswd).hexdigest()

        user = User(username, encodepswd)
        db.session.add(user)
        db.session.commit()
    except Exception as exp:
        print "user_register() :: Got Exception: %s" % exp
        print(traceback.format_exc())
        return "user Register Successfully"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        print "login GET"
        templateData = {'title' : 'Login To Career Maker'}
        return render_template("index.html", **templateData)
    else:
        username = request.form['username']
        pswd = request.form['pswd']
        encodepswd = md5.new(pswd).hexdigest()
        
        user = User.query.filter_by(username=username).filter_by(pswd=encodepswd).first()
        if not user:
            print "The username and Password is invalid"
            return "Invalid Username and Password"
        else:
            print "login is successfull"
            templateData = {'title' : 'Home Page'}
            return render_template("index.html", **templateData)
"""
# token authentication
app.config['secretkey'] = 'some-strong+secret#key'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        # ensure that token is specified in the request
        if not token:
            return jsonify({'message': 'Missing token!'})

        # ensure that token is valid
        try:
            data = jwt.decode(token, app.config['secretkey'])
        except:
            return jsonify({'message': 'Invalid token!'})

        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():
    return 'unprotected'

@app.route('/protected')
@token_required
def protected():
    return 'protected'


@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({'user': auth.username, 'exp': expiry}, app.config['secretkey'], algorithm='HS256')
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
"""

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

#################################################################
#																#
#							Main Server							#
#																#
#################################################################

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
