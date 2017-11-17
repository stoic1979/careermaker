from pymongo import MongoClient
from flask import jsonify
import traceback
import json
import datetime
from bson import ObjectId


class Mdb:

    def  __init__(self):
        # conn_str = "mongodb://%s:%s@%s:%d/%s" \
        #           % (DB_USER, DB_PASS,
        #            DB_HOST, DB_PORT, AUTH_DB_NAME)
        # print "-------", conn_str
        conn_str = 'mongodb://cmuser:cmpass@ds135689.mlab.com:35689/careermaker'
        client = MongoClient(conn_str)
        self.db = client['careermaker']

        print "[Mdb] connected to database :: ", self.db

############################################################################
#                                                                          #
#                               CANDIDATE PANNEL                           #
#                                                                          #
############################################################################
    # CHECK EMAIL USER ALREADY REGISTERED OR NOT
    def check_email(self, email):
        return self.db.candidate.find({'email': email}).count() > 0

    # REGITRATION CANDIDATE IN DATABASE
    def add_candidate(self, user_id, name, email, pw_hash, age, phone, address, gender):
        try:
            rec = {
                'user_id': user_id,
                'name': name,
                'email':email,
                'password': pw_hash,
                'age': age,
                'phone': phone,
                'address': address,
                'gender': gender
            }
            self.db.candidate.insert(rec)

        except Exception as exp:
            print "add_candidate() :: Got exception: %s", exp
            print(traceback.format_exc())

    # CHECK EMAIL EXIST OR NOT IN DATABASE BEFORE LOGIN CANDIDATE
    def user_exists(self, email):
        return self.db.candidate.find({'email': email}).count() > 0

    # MATCH PASSWORD AND EMAIL THEN LOGIN
    def get_password(self, email):
        result = self.db.candidate.find({'email': email})
        name = ''
        password = ''
        if result:
            for data in result:
                name = data['name']
                password = data['password']
                print 'password in db class', password
        return password

    # GET NAME AND EMAILID VIA EMAIL ADDRESS
    def get_name(self, email):
        result = self.db.candidate.find({'email': email})
        name = ''
        email = ''
        if result:
            for data in result:
                name = data['name']
                email = data['email']
        return name

    # CANDIDATE SESSION INFORMATION
    def save_login_info(self, user_email, mac, ip, user_agent, type):
        LOGIN_TYPE = 'User Login'
        try:
            # ts = datetime.datetime.utcnow()
            # ts = datetime.datetime.now().strftime("%d-%m-%G  %H:%M:%S")
            ts = datetime.datetime.today().strftime("%a %b %d %X  %Y ")

            rec = {
                'user_id': user_email,
                'mac': mac,
                'ip': ip,
                'user_agent': user_agent,
                'user_type': type,
                'timestamp': ts
            }

            self.db.candidate_session.insert(rec)
        except Exception as exp:
            print "save_login_info() :: Got exception: %s", exp
            print(traceback.format_exc())


############################################################################
#                                                                          #
#                               COMPANY PANNEL                             #
#                                                                          #
############################################################################
    # CHECK EMAIL USER ALREADY REGISTERED OR NOT
    def check_company_email(self, email):
        return self.db.company.find({'email': email}).count() > 0

    # REGITRATION CANDIDATE IN DATABASE
    def add_company(self, user_id, name, website, email, pw_hash, mobile, telno, address, city, state, country, pin):
        try:
            rec = {
                'user_id': user_id,
                'name': name,
                'website': website,
                'email':email,
                'password': pw_hash,

                'mobile': mobile,
                'telno': telno,
                'address': address,
                'city': city,
                'state': state,
                'country': country,
                'pin': pin
            }
            self.db.company.insert(rec)
        except Exception as exp:
            print "add_company() :: Got exception: %s", exp
            print(traceback.format_exc())

  # CHECK EMAIL EXIST OR NOT IN DATABASE BEFORE LOGIN CANDIDATE
    def user_exists1(self, email):
        return self.db.company.find({'email': email}).count() > 0

    # MATCH PASSWORD AND EMAIL THEN LOGIN
    def get_password1(self, email):
        result = self.db.company.find({'email': email})
        name = ''
        password = ''
        if result:
            for data in result:
                name = data['name']
                password = data['password']
                print 'password in db class', password
        return password

    # GET NAME AND EMAILID VIA EMAIL ADDRESS
    def get_name1(self, email):
        result = self.db.company.find({'email': email})
        name = ''
        email = ''
        if result:
            for data in result:
                name = data['name']
                email = data['email']
        return name

    # CANDIDATE SESSION INFORMATION
    def save_login_info1(self, user_email, mac, ip, user_agent, type):
        LOGIN_TYPE = 'User Login'
        try:
            # ts = datetime.datetime.utcnow()
            # ts = datetime.datetime.now().strftime("%d-%m-%G  %H:%M:%S")
            ts = datetime.datetime.today().strftime("%a %b %d %X  %Y ")

            rec = {
                'user_id': user_email,
                'mac': mac,
                'ip': ip,
                'user_agent': user_agent,
                'user_type': type,
                'timestamp': ts
            }

            self.db.company_session.insert(rec)
        except Exception as exp:
            print "save_login_info1() :: Got exception: %s", exp
            print(traceback.format_exc())

############################################################################
#                                                                          #
#                               ADMIN PANNEL                               #
#                                                                          #
############################################################################
    def add_admin(self, email, password):
        try:
            rec = {
                'email': email,
                'password': password
            }
            self.db.admin.insert(rec)
        except Exception as exp:
            print "add_admin() :: Got exception: %s", exp
            print(traceback.format_exc())


    def admin_exists(self, email, password):

        return self.db.admin.find({'email': email, 'password': password}).\
                   count() > 0

    def get_companies(self):
        collection = self.db["company"]
        # result = collection.find().skip(self.db.survey.count()-1)
        result = collection.find({})
        ret = []
        for data in result:
            ret.append(data)
        return ret

    def get_candidates(self):
        collection = self.db["candidate"]
        # result = collection.find().skip(self.db.survey.count()-1)
        result = collection.find({})
        ret = []
        for data in result:
            ret.append(data)
        return ret

    def get_python_jobs(self):
        collection = self.db["job_vacancy_python"]
        # result = collection.find().skip(self.db.survey.count()-1)
        result = collection.find({})
        ret = []
        for data in result:
            ret.append(data)
        return ret

    def get_android_jobs(self):
        collection = self.db["job_vacancy_python"]
        # result = collection.find().skip(self.db.survey.count()-1)
        result = collection.find({})
        ret = []
        for data in result:
            ret.append(data)
        return ret
        # print'==========================',ret

    def get_php_jobs(self):
        collection = self.db["job_vacancy_android"]
        # result = collection.find().skip(self.db.survey.count()-1)
        result = collection.find({})
        ret = []
        for data in result:
            ret.append(data)
        return ret

if __name__ == "__main__":
    mdb = Mdb()
    mdb.add_admin('john@gmail.com', '123')
    # mdb.add_candidate('1', 'tom', 'tom@gmail.com', '123', '25', '7845698745', 'mohali', 'male')

