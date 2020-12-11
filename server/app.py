from grabber import Grabber
from flask import Flask, jsonify, request, Response
import json
import os.path
import re

# Variables
URL = "https://cat-fact.herokuapp.com/facts"
FILENAME = "data.json"

if not os.path.isfile(FILENAME):    
    g = Grabber()
    g.grab(URL, FILENAME)

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return "Welcome to cat facts"

@app.route('/api/v1/catfacts', methods=["GET"])
def get_catfacts():

    # Create a params dict to hold query parameters
    params = {}
    params['firstname'] = request.args.get('firstname')
    params['lastname'] = request.args.get('lastname')
    params['id'] = request.args.get('id')
    print("params is ", params)

    # Create a pattern_search dict to hold corresponding regex patterns
    pattern_search = {}
    for key in params:
        if params[key] is None:
            pattern_search[key] = "[a-zA-Z]*"
        else:
            pattern_search[key] = "^"+params[key]+"$"
    print("pattern_search is ", pattern_search)

    with open(FILENAME, 'r') as file:
        catfacts = json.load(file) # list of dict

    data = []
    for catfact in catfacts:
        if re.match(pattern_search['firstname'], catfact['user']['name']['first']) and \
            re.match(pattern_search['lastname'], catfact['user']['name']['last']) and \
            re.match(pattern_search['id'], catfact['_id']):
            data.append(catfact)

    print("INFO: No of catfacts with firstname, lastname and id as {}, {} and {} = {}".format(params['firstname'], params['lastname'], params['id'], len(data)))
    if len(data) > 0:
        return jsonify(data), 200
    else:
        return {"msg": "No catfact found"}, 404


@app.route('/api/v1/catfacts', methods=["DELETE"])
def delete_catfact():
    params = {}

    params['id'] = request.args.get('id')
    print("INFO: params id is ", params['id'])

    with open(FILENAME, 'r') as file:
        catfacts = json.load(file) # list of dict

    # only id
    if params['id'] is not None:
        catfact = [catfact for catfact in catfacts if catfact['_id'] == params['id']]
        print("INFO: {} catfact found!".format(len(catfact)))
        if len(catfact) > 0:
            print("INFO: The catfacts with id {} will be deleted".format(params['id']))
            catfacts = [catfact for catfact in catfacts if catfact['_id'] != params['id']]
            print("No of catfacts after successful delete operation = {}".format(len(catfacts)))
            with open(FILENAME, 'w') as writer:
                json.dump(catfacts, writer)
            return {"msg": "Catfact ID {} deleted successfully".format(params['id'])}, 202
        else:
            # 404 Record not found
            print("No catfact present with the id specified : {}".format(params['id']))
            return {"msg": "Catfact ID {} not found".format(params['id'])}, 404
    else:
        # 400 Bad Request
        return {"msg": "Invalid Request. Please provide a catfact ID."}, 400

app.run()
