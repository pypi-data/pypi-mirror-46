import requests
from requests.models import Response
import sys
import httpantry.proxy_database as pr_db
import httpantry.parse_configuration as pc
from datetime import datetime

def handle_request(method_name, *args, **kwargs):
    """
    If request is in database, return it. Otherwise, retrieve it normally,
    store it, then return it
    """

    url = args[0]
    response, timestamp = pr_db.retrieve(method_name.upper(), url)
    if response == None or invalid_timestamp(timestamp):
        # carry out request, store response database 
        response = resolve_request(method_name, *args, **kwargs)
    else:
        print("\t returned a store response")
    return format_response(response)

def invalid_timestamp(timestamp):
    """
    Returns True if timestamp is invalid, or False otherwise
    """
    if timestamp == None:
        return True
    elif (timestamp + pc.user_params.timeout) < pr_db.unix_time_millis(datetime.now()):
        return True
    else:
        return False

def format_response(resp):
    """
    Correctly formats a request
    """
    # unsure if we need these, sometimes doesn't work without
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.headers.items()
            if name.lower() not in excluded_headers]

    # create and return Response object
    response = Response()
    response._content = resp.content
    response.status_code = resp.status_code
    response.headers = headers
    return response

def resolve_request(method_name, *args, **kwargs):

    """
    Resolves unstored responses
    """
    # get response from given request
    method_to_call = getattr(requests, method_name)
    resp = method_to_call(*args, **kwargs)
    print("\t resolving request")
    if any(api in args[0] for api in pc.user_params.uncached_apis):
        return resp
    else:
        pr_db.store(method_name.upper(), args[0], resp)
        return resp
