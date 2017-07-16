from flask import Flask, request, jsonify
from scraper.db import Mdb
from functools import wraps
from bson import ObjectId
import jwt
import datetime
import json
import traceback


app = Flask(__name__)
mdb = Mdb()

app.config['secretkey'] = 'some-strong+secret#key'


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


@app.route("/protected")
@token_required
def protected():
    return 'you are protected'


@app.route('/add_user', methods=['POST'])
def add_user():
    ret = {"error": 0}
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        status, msg = mdb.add_user(name, email, password)
        ret['msg'] = 'user is added successfully'


        if not status:
            ret['msg'] = msg

    except Exception as exp:
        ret['error'] = 1
        ret['message'] = exp
        print(traceback.format_exc())
    return json.dumps(ret)


@app.route('/home')
@token_required
def home():
    return "home"


@app.route('/login', methods=['POST'])
def login():
    ret = {}
    try:
        email = request.form['email']
        password = request.form['password']
        if mdb.user_exist(email, password):

            # login successfull
            expiry = datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
            token = jwt.encode({'email': email, 'exp': expiry},
                               app.config['secretkey'], algorithm='HS256')
            ret['msg'] = 'login successful'
            ret['error'] = 0
            ret['token'] = token.decode('UTF-8')
        else:

            # login failed
            ret['msg'] = 'Login Failed'
            ret['err'] = 1
    except Exception as exp:
        ret['msg'] = '%s' % exp
        ret['err'] = 2
    return jsonify(ret)


if __name__ == '__main__':
    app.run()
