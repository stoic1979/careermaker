from flask import Flask, request, make_response, render_template, jsonify,\
    session, url_for, redirect, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required,\
                        logout_user, current_user
from flask_admin import Admin, BaseView, expose
import uuid
from uuid import getnode as get_mac
from flask.ext.bcrypt import Bcrypt
from bson.objectid import ObjectId
from functools import wraps
import time
from datetime import datetime, timedelta
import datetime
import traceback
import flask_login
import flask
import json
import jwt
import os
from db import Mdb
# from werkzeug.utils import secure_filename
# from wtforms.fields import SelectField

from eve import Eve

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'templates')

# app = Eve('', template_folder=tmpl_dir)

app = Flask(__name__)

bcrypt = Bcrypt(app)
mdb = Mdb()


#############################################
#                                           #
#              WORKING  SESSION             #
#                                           #
#############################################
@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)
    flask.session.modified = True
    flask.g.user = flask_login.current_user


app.config['secretkey'] = 'some-strong+secret#key'
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

# setup login manager
login_manager = LoginManager()
login_manager.init_app(app)


#############################################
#                                           #
#        _id of mongodb record was not      #
#           getting JSON encoded, so        #
#           using this custom one           #
#                                           #
#############################################
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


#############################################
#                                           #
#                SESSION COUNTER            #
#                                           #
#############################################
def sumSessionCounter():
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1


##############################################
#                                            #
#           Login Manager                    #
#                                            #
##############################################
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/')


#############################################
#                                           #
#              TOKEN REQUIRED               #
#                                           #
#############################################
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
############################################################################
#                                                                          #
#            CHECK EMAIL USER ALREADY REGISTERED OR NOT                    #
#                                                                          #
############################################################################

        return f(*args, **kwargs)

    return decorated


@app.route('/admin1')
def admin1():
    templateData = {'title': 'index page'}
    return render_template('admin1/home.html', **templateData)


@app.route('/admin1/index')
def index():
    templateData = {'title': 'index page'}
    return render_template('admin1/index.html', **templateData)


###########################################################################################################
#                                                                                                         #
#                                                                                                         #
#                                                                                                         #
#                                         CANDIDATE PANNEL                                                #
#                                                                                                         #
#                                                                                                         #
#                                                                                                         #
###########################################################################################################
############################################################################
#                                                                          #
#                              CANDIDATE ROUTE                             #
#                                                                          #
############################################################################
@app.route('/candidate')
@app.route('/')
def candidate():
    templateData = {'title': 'Login Page'}
    return render_template('candidate/home.html', session=session, **templateData)


############################################################################
#                                                                          #
#                              CANDIDATE SIGNUP                            #
#                                                                          #
############################################################################
@app.route('/candidate/signup')
def candidate_signup():
    templateData = {'title': 'Signup page'}
    return render_template('candidate/signup.html', session=session, **templateData)


############################################################################
#                                                                          #
#          CHECK CANDIDATE ALREADY REGISTERED OR NOT THEN REGISTER         #
#                            PASSWORD BCRYBY                               #
#                                                                          #
############################################################################
@app.route('/candidate/add_candidate', methods=['POST'])
def add_candidate():
    try:
        user_id = request.form['user_id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        phone = request.form['phone']
        address = request.form['address']
        gender = request.form['gender']
        # print'----------------', request.form

        # password bcrypt  #
        pw_hash = bcrypt.generate_password_hash(password)
        passw = bcrypt.check_password_hash(pw_hash, password)

        check = mdb.check_email(email)
        if check:
            print"This Email Already Used"
            templateData = {'title': 'Signup Page'}
            return render_template('candidate/signup.html', **templateData)

        else:
            mdb.add_candidate(user_id, name, email, pw_hash, age, phone, address, gender)
            print('User Is Added Successfully')

            return render_template('candidate/home.html', session=session)

    except Exception as exp:
        print('add_user() :: Got exception: %s' % exp)
        print(traceback.format_exc())


############################################################################
#                                                                          #
#                              CANDIDATE LOGIN                             #
#        STORED INFORMATION[SESSION_ID, MAC_ADDRESS, IP OR BROWSER]        #
#     SEESION TIME 30 MIN (SEESION LOGOUT AUTOMATICALLY AFTER 30 MINs      #
#                                                                          #
############################################################################
@app.route('/candidate/login', methods=['POST'])
def candidate_login():
    ret = {'err': 0}
    try:
        sumSessionCounter()
        email = request.form['email']
        password = request.form['password']

        if mdb.user_exists(email):
            pw_hash = mdb.get_password(email)
            print 'password in server, get from db class', pw_hash
            passw = bcrypt.check_password_hash(pw_hash, password)

            if passw == True:
                name = mdb.get_name(email)
                session['name'] = name
                session['email'] = email

                # Login Successful!
                expiry = datetime.datetime.utcnow() + datetime.\
                    timedelta(minutes=30)

                token = jwt.encode({'user': email, 'exp': expiry},
                                   app.config['secretkey'], algorithm='HS256')
                # flask_login.login_user(user, remember=False)
                ret['msg'] = 'Login successful'
                ret['err'] = 0
                ret['token'] = token.decode('UTF-8')
                templateData = {'title': 'singin page'}
            else:
                return render_template('candidate/home.html', session=session)

        else:
            # Login Failed!
            return render_template('candidate/home.html', session=session)

            ret['msg'] = 'Login Failed'
            ret['err'] = 1

        LOGIN_TYPE = 'Candidate Login'
        email = session['email']
        user_email = email
        mac = get_mac()
        ip = request.remote_addr

        agent = request.headers.get('User-Agent')
        mdb.save_login_info(user_email, mac, ip, agent, LOGIN_TYPE)

    except Exception as exp:
        ret['msg'] = '%s' % exp
        ret['err'] = 1
        print(traceback.format_exc())
    # return jsonify(ret)
    return render_template('candidate/home.html', session=session)


############################################################################
#                                                                          #
#                       CANDIDATE SESSION LOGOUT                           #
#     STOREED CANDIDATES INFORMATION WHEN CANDIDATE LOGOUT ALL DEATAILS.   #
#                                                                          #
############################################################################
@app.route('/clear')
def clearsession():
    try:
        LOGIN_TYPE = 'Candidate Logout'
        sumSessionCounter()
        email = session['email']
        user_email = email
        mac = get_mac()
        ip = request.remote_addr
        agent = request.headers.get('User-Agent')
        mdb.save_login_info(user_email, mac, ip, agent, LOGIN_TYPE)
        session.clear()
        return render_template('candidate/home.html', session=session)
    except Exception as exp:
        return 'clearsession() :: Got Exception: %s' % exp


###########################################################################################################
#                                                                                                         #
#                                                                                                         #
#                                                                                                         #
#                                         CANDIDATE PANNEL                                                #
#                                                                                                         #
#                                                                                                         #
#                                                                                                         #
###########################################################################################################
############################################################################
#                                                                          #
#                               COMPANY ROUTE                              #
#                                                                          #
############################################################################
@app.route('/company')
def company():
    templateData = {'title': 'Home page'}
    return render_template('company/home.html', **templateData)

############################################################################
#                                                                          #
#                         COMPANY SIGNUP ROUTE                             #
#                                                                          #
############################################################################
@app.route('/company/signup')
def company_signup():
    templateData = {'title': 'Signup page'}
    return render_template('company/signup.html', session=session, **templateData)


############################################################################
#                                                                          #
#           CHECK COMPANY ALREADY REGISTERED OR NOT THEN REGISTER          #
#                            PASSWORD BCRYBY                               #
#                                                                          #
############################################################################
@app.route('/company/add_company', methods=['POST'])
def add_company():
    try:
        user_id = request.form['user_id']
        name = request.form['name']
        website = request.form['website']
        email = request.form['email']
        password = request.form['password']

        mobile = request.form['mobile']
        telno = request.form['telno']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        pin = request.form['pin']

        # password bcrypt  #
        pw_hash = bcrypt.generate_password_hash(password)
        passw = bcrypt.check_password_hash(pw_hash, password)

        check = mdb.check_company_email(email)
        if check:
            print"This Email Already Used"
            templateData = {'title': 'Signup Page'}
            return render_template('company/signup.html', **templateData)

        else:
            mdb.add_company(user_id, name, website, email, pw_hash, mobile, telno, address, city, state, country, pin)

            print('User Is Added Successfully')

            return render_template('company/home.html', session=session)

    except Exception as exp:
        print('add_company() :: Got exception: %s' % exp)
        print(traceback.format_exc())


############################################################################
#                                                                          #
#                              COMPANY LOGIN                               #
#        STORED INFORMATION[SESSION_ID, MAC_ADDRESS, IP OR BROWSER]        #
#     SEESION TIME 30 MIN (SEESION LOGOUT AUTOMATICALLY AFTER 30 MINs      #
#                                                                          #
############################################################################
@app.route('/company/login', methods=['POST'])
def company_login():
    ret = {'err': 0}
    try:
        sumSessionCounter()
        email = request.form['email']
        password = request.form['password']

        if mdb.user_exists1(email):
            pw_hash = mdb.get_password1(email)
            print 'password in server, get from db class', pw_hash
            passw = bcrypt.check_password_hash(pw_hash, password)

            if passw == True:
                name = mdb.get_name1(email)
                session['name'] = name
                session['email'] = email

                # Login Successful!
                expiry = datetime.datetime.utcnow() + datetime.\
                    timedelta(minutes=30)

                token = jwt.encode({'user': email, 'exp': expiry},
                                   app.config['secretkey'], algorithm='HS256')
                # flask_login.login_user(user, remember=False)
                ret['msg'] = 'Login successful'
                ret['err'] = 0
                ret['token'] = token.decode('UTF-8')
                templateData = {'title': 'singin page'}
            else:
                return render_template('company/home.html', session=session)

        else:
            # Login Failed!
            return render_template('company/home.html', session=session)

            ret['msg'] = 'Login Failed'
            ret['err'] = 1

        LOGIN_TYPE = 'Company Login'
        email = session['email']
        user_email = email
        mac = get_mac()
        ip = request.remote_addr

        agent = request.headers.get('User-Agent')
        mdb.save_login_info1(user_email, mac, ip, agent, LOGIN_TYPE)

    except Exception as exp:
        ret['msg'] = '%s' % exp
        ret['err'] = 1
        print(traceback.format_exc())
    # return jsonify(ret)
    return render_template('company/home.html', session=session)


############################################################################
#                                                                          #
#                       CANDIDATE SESSION LOGOUT                           #
#     STOREED CANDIDATES INFORMATION WHEN CANDIDATE LOGOUT ALL DEATAILS.   #
#                                                                          #
############################################################################
@app.route('/clear1')
def clearsession1():
    try:
        LOGIN_TYPE = 'Company Logout'
        sumSessionCounter()
        email = session['email']
        user_email = email
        mac = get_mac()
        ip = request.remote_addr
        agent = request.headers.get('User-Agent')
        mdb.save_login_info1(user_email, mac, ip, agent, LOGIN_TYPE)
        session.clear()
        return render_template('company/home.html', session=session)
    except Exception as exp:
        return 'clearsession() :: Got Exception: %s' % exp


###########################################################################################################
#                                                                                                         #
#                                                                                                         #
#                                                                                                         #
#                                             ADMIN PANNEL                                                #
#                                                                                                         #
#                                                                                                         #
#                                                                                                         #
###########################################################################################################
##############################################################################
#                                                                            #
#                                    ADMIN ROUTE                             #
#                                                                            #
##############################################################################
@app.route('/admin')
def admin():
    templateData = {'title': 'index page'}
    return render_template('admin/login.html', **templateData)


##############################################################################
#                                                                            #
#                        GET ALL COMPANIES DETAILS                           #
#                                                                            #
##############################################################################
@app.route('/admin/companies', methods=['GET'])
def admin_companies():
    data = mdb.get_companies()
    templateData = {'title': 'Get companies', 'data': data}
    return render_template('admin/companies.html', **templateData)


##############################################################################
#                                                                            #
#                        GET ALL CANDIDATES DETAILS                          #
#                                                                            #
##############################################################################
@app.route('/admin/candidates')
def admin_candidates():
    data = mdb.get_candidates()
    templateData = {'title': 'Get candidates', 'data': data}
    return render_template('admin/candidates.html', **templateData)


##############################################################################
#                                                                            #
#                         GET ALL PYTHON VACANCIES                           #
#                                                                            #
##############################################################################
@app.route('/admin/python')
def admin_python():
    data = mdb.get_python_jobs()
    templateData = {'title': 'python page', 'data': data}
    return render_template('admin/python.html', **templateData)


##############################################################################
#                                                                            #
#                         GET ALL ANDROID VACANCIES                          #
#                                                                            #
##############################################################################
@app.route('/admin/android')
def admin_android():
    data = mdb.get_android_jobs()
    # print'--------------------', data
    templateData = {'title': 'android page', 'data': data}
    return render_template('admin/android.html', **templateData)


##############################################################################
#                                                                            #
#                            GET ALL PHP VACANCIES                           #
#                                                                            #
##############################################################################
@app.route('/admin/php')
def admin_php():
    data = mdb.get_php_jobs()
    templateData = {'title': 'php page', 'data': data}
    return render_template('admin/php.html', **templateData)


##############################################################################
#                                                                            #
#                       EMAIL ROUTE SHOW LIST OF INBOX EMAIL                 #
#                                                                            #
##############################################################################
@app.route('/admin/email')
def admin_email():
    templateData = {'title': 'email page'}
    return render_template('admin/email.html', **templateData)


##############################################################################
#                                                                            #
#                         SHOW LIST OF INBOX EMAIL                           #
#                                                                            #
##############################################################################
@app.route('/admin/inbox')
def admin_inbox():
    templateData = {'title': 'inbox page'}
    return render_template('admin/inbox.html', **templateData)


##############################################################################
#                                                                            #
#                            SHOW LIST OF SEND BOX                           #
#                                                                            #
##############################################################################
@app.route('/admin/sent')
def admin_sent():
    templateData = {'title': 'send page'}
    return render_template('admin/sent.html', **templateData)


##############################################################################
#                                                                            #
#                            SHOW LIST OF DRAFT BOX                          #
#                                                                            #
##############################################################################
@app.route('/admin/draft')
def admin_draft():
    templateData = {'title': 'draft page'}
    return render_template('admin/draft.html', **templateData)


##############################################################################
#                                                                            #
#                            SHOW LIST OF TRASH BOX                          #
#                                                                            #
##############################################################################
@app.route('/admin/trash')
def admin_trash():
    templateData = {'title': 'trash page'}
    return render_template('admin/trash.html', **templateData)


##############################################################################
#                                                                            #
#                                   ADMIN LOGIN                              #
#                                                                            #
##############################################################################
@app.route('/admin/admin_login', methods=['POST'])
def admin_login():
    ret = {'err': 0}
    try:

        sumSessionCounter()
        email = request.form['email']
        password = request.form['password']

        if mdb.admin_exists(email, password):
            # name = mdb.get_admin_name(email)
            session['email'] = email

            expiry = datetime.datetime.utcnow() + datetime.\
                timedelta(minutes=30)
            token = jwt.encode({'user': email, 'exp': expiry},
                               app.config['secretkey'], algorithm='HS256')
            ret['msg'] = 'Login successful'
            ret['err'] = 0
            ret['token'] = token.decode('UTF-8')
            return render_template('admin/home.html', session=session)
        else:
            templateData = {'title': 'singin page'}
            # Login Failed!
            return render_template('/admin/login.html', session=session)
            # return "Login faild"
            ret['msg'] = 'Login Failed'
            ret['err'] = 1

    except Exception as exp:
        ret['msg'] = '%s' % exp
        ret['err'] = 1
        print(traceback.format_exc())
        # return jsonify(ret)
        # return render_template('admin/home.html', session=session)


##############################################################################
#                                                                            #
#                              ADMIN SESSION LOGOUT                          #
#                                                                            #
##############################################################################
@app.route('/clear2')
def clearsession2():
    session.clear()
    return render_template('/admin/login.html', session=session)


##############################################################################
#                                                                            #
#                    HADDLE THE ERROR AND SHOW THE 404 PAGE                  #
#                                                                            #
##############################################################################
@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s', (request.path))
    return render_template('admin/404.html'), 404


###########################################################################################################
#                                                                                                         #
#                                                                                                         #
#                                                                                                         #
#                                              MAIN SERVER                                                #
#                                                                                                         #
#                                                                                                         #
#                                                                                                         #
###########################################################################################################
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
