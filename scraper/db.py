#
# Database manager for handling transactions with mongodb
#

from pymongo import MongoClient
from config import *
import traceback
import json


class Mdb:

    def  __init__(self):
        # conn_str = "mongodb://%s:%s@%s:%d/%s" \
        #          % (DB_USER, DB_PASS,
        #           DB_HOST, DB_PORT, AUTH_DB_NAME)
        conn_str = 'mongodb://cmuser:cmpass@ds135689.mlab.com:35689/careermaker'
        client = MongoClient(conn_str)
        self.db = client['careermaker']

        print "[Mdb] connected to database :: ", self.db

    def add_user(self, name, email, password):
        try:
            rec = {
                'name': name,
                'email': email,
                'password': password
            }
            self.db.user.insert(rec)
            return True, "Success"
        except Exception as exp:
            print 'add_user() :: Got exception: %s' % exp
            print(traceback.format_exc())
            return False, "Exception: %s" % exp

    def user_exist(self, email, password):
        """
        function checks if a user with given email and password
        exists in database
        :param email: email of the user
        :param password: password of the user
        :return: True, if user exists,
                False, otherwise
        """
        return self.db.user.find({'email': email,
                                  'password': password}).count() > 0

    def add_vacancy_python(self, title, location, salary, summary):
        try:
            rec = {
                'title': title,
                'location': location,
                'salary': salary,
                'summary': summary
            }
            self.db.job_vacancy_python.insert(rec)
        except Exception as exp:
            print "add_vacancy() :: Got exception: %s" % exp
            print(traceback.format_exc())

    def add_vacancy_android(self, title, location, salary, summary):
        try:
            rec = {
                'title': title,
                'location': location,
                'salary': salary,
                'summary': summary
            }
            self.db.job_vacancy_android.insert(rec)
        except Exception as exp:
            print "add_vacancy() :: Got exception: %s" % exp
            print(traceback.format_exc())

    def add_vacancy_php(self, title, location, salary, summary):
        try:
            rec = {
                'title': title,
                'location': location,
                'salary': salary,
                'summary': summary
            }
            self.db.job_vacancy_php.insert(rec)
        except Exception as exp:
            print "add_vacancy() :: Got exception: %s" % exp
            print(traceback.format_exc())

    def retrieve_data(self, cname):
        collection = self.db["job_vacancy_android"]
        result = collection.find({"title": cname})
        print result
        for data in result:
            print "<<======Got the >>"
            print "<<======Got the data>> :: %s" % data
            return data


if __name__ == "__main__":
    # quick test connecting to localdb
    mdb = Mdb('127.0.0.1', 27017, 'admin', 'carrermaker', 'admin', '123')
    # mdb.add_vacancy('weaveBytes', 'kharar', '10000', 'its python job')
    # mdb.retrieve_data('LuminoGuru Pvt. Ltd.')


    # LuminoGuru Pvt. Ltd.
