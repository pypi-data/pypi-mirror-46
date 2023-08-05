from flask import Flask, flash, request, Response, send_from_directory, redirect, url_for, jsonify, json, make_response
import requests
import httpantry.proxy_database as pr_db
import httpantry.parse_configuration as pc
from datetime import datetime

app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

#catch all URL
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_request(path):
    ''' Returns a stored response if such exists, otherwise returns -1 '''
    # get url and method to store in cache
    response, timestamp = pc.user_params.retrieve(request.method, request.url)
    if response == None or invalid_timestamp(timestamp):
       # carry out request, store response database 
        response = resolve_request(request)
    else:
        print("returned a store response")
    return format_response(response)

@app.route('/config', methods=['POST'])
def config_dynamic():
    """ Sets a user configuration as described in the request body """
    result = pc.dynamically_config(request.json)
    if result:
        print(pc.user_params.persistence)
        print(pc.user_params.custom_response_file)
        return make_response("Success", 200)
    else:
        return make_response("Failure", 404)

def invalid_timestamp(timestamp):
    ''' Returns True if timestamp is invalid, or False otherwise '''
    if timestamp == None:
        return True
    elif (timestamp + pc.user_params.timeout) < pr_db.unix_time_millis(datetime.now()):
        return True
    else:
        return False
    
def format_response(resp):
    ''' correctly formats a request '''
    # unsure if we need these, sometimes doesn't work without
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.headers.items()
               if name.lower() not in excluded_headers]

    # create and return Response object
    response = Response(resp.content, resp.status_code, headers)
    return response

def resolve_request(request):
    # get response from given request
    resp = requests.request(
        method=request.method,
        url=request.url,
        headers={key: value for (key, value) in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    print("resolving request")
    if any(api in request.url for api in pc.user_params.uncached_apis):
        return resp
    else:
        pc.user_params.store(request.method, request.url, resp)
        return resp

def init_proxy_server():
    pc.userConfiguration()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(port=pc.user_params.port_number)
