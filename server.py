from flask import Flask, render_template, request
import traceback
import os
import json

app = Flask(__name__)


@app.route("/")
def index():
	templateData = {'title' : 'Home Page'}
	return render_template("index.html", **templateData )

@app.route("/candi_form")
def candidate_form():
	templateData = {'title' : 'Home Page'}
	return render_template("api_demo.html", **templateData )

@app.route("/save_candidates", methods=['POST'])
def home():
	return "hiiiiii"




#################################################################
#																#
#							Main Server							#
#																#
#################################################################
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True, threaded=True)