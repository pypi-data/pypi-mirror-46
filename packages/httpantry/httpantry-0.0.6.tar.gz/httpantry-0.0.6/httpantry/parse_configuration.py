import configparser
import sys
import json
import httpantry.proxy_database as pr_db
from pathlib import Path
from flask import Response

CONFIGURE_FILE = "__httpantry_cache__/config"
TIME_DELTA = {"days": 86400000, "hours": 3600000, "minutes": 60000, "seconds": 1000, "milliseconds": 1}

class Configurations:
    def __init__(self):
        self.port_number = None
        self.custom_response_file = None
        self.persistence = None
        self.uncached_apis = list()
        self.timeout = None
        self.store = None
        self.retrieve = None

def userConfiguration():
    """ Initializes the configuration """ 
    configure_file = Path(CONFIGURE_FILE)
    if not configure_file.is_file():
        initConfigureFile()
    readConfigFile()

def readConfigFile():
    """ Reads a configuration file """
    config = configparser.ConfigParser()
    config.read(CONFIGURE_FILE)

    for key in config['GENERAL']:
        evaluate_default_parameters(key, config['GENERAL'][key])
    user_params.timeout = 0

    for key in config['TIMEOUT']:
        if key in TIME_DELTA: 
            user_params.timeout += TIME_DELTA[key] * int(config['TIMEOUT'][key])
    
    if config['CUSTOM_RESPONSES']['use_custom_responses'] == "True":
        evaluate_custom_responses_parameters(config['CUSTOM_RESPONSES']['file_name'])

def dynamically_config(request_json):
    """ Configures user_parameters with the specified parameter, json body, and user params """
    for key in request_json.keys():
        if key == "TIMEOUT" or key == "timeout":
            user_params.timeout = 0
            for segment in request_json[key].keys():
                if segment in TIME_DELTA.keys():
                    user_params.timeout += TIME_DELTA[segment] * int(request_json[key][segment])
                else:
                    return False
        elif key == "persistence":
            if request_json[key] == "True" or request_json[key] == "true":
                user_params.persistence = True
            elif request_json[key] == "False" or request_json[key] == "false":
                user_params.persistence = False
            else:
                return False
        elif key == "uncached_apis":
            user_params.uncached_apis.append(request_json[key])
        else:
            return False
    return True

def evaluate_default_parameters(key, string):
    """ Converts from user-defined strings to parameters """
    if key == "port_number":
        user_params.port_number = int(string)
    elif key == "persistence":
        if string == "True":
            user_params.store = pr_db.store
            user_params.retrieve = pr_db.retrieve
        else:
            user_params.store = pr_db.temp_store
            user_params.retrieve = pr_db.temp_retrieve
    elif key == "uncached_apis":
        user_params.uncached_apis = string.split(' ')

def evaluate_custom_responses_parameters(file_name):
    ''' stores files from custom responses file'''
    custom_responses_file = Path(file_name)
    user_params.custom_response_file = file_name
    if not custom_responses_file.is_file():
        # if file does not already exist, create it with some example data
        example_data = [{
            "method": "GET",
            "url": "http://fakeurl.org/get",
            "content": {
                "args": {},
                "headers": {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate",
                    "Host": "fakeurl.org",
                    "User-Agent": "python-requests/2.21.0"
                },
                "url": "http://fakeurl.org/get"
            }
        }]
        with open(file_name, 'x') as outfile:
            json.dump(example_data, outfile, indent=4)
    # read from file, format as response, store in database
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
        for custom_response in data:
            response = Response()
            response.content = json.dumps(custom_response["content"])
            response.headers = custom_response["content"]["headers"]
            user_params.store(custom_response["method"], custom_response["url"], response)


def initConfigureFile():
    """ Creates a configuration file with default parameters """
    config = configparser.ConfigParser()
    config.add_section('GENERAL') 
    config.set('GENERAL', 'port_number', '5000')
    config.set('GENERAL', 'persistence', 'True')
    config.set('GENERAL', 'uncached_apis', 'yourmom.com http://httpbin.org/image/jpeg')
    config.add_section('CUSTOM_RESPONSES')
    config.set('CUSTOM_RESPONSES', 'use_custom_responses', 'True')
    config.set('CUSTOM_RESPONSES', 'file_name', '__httpantry_cache__/custom_responses.json')
    config.add_section('TIMEOUT')
    config.set('TIMEOUT', 'days', '0')
    config.set('TIMEOUT', 'hours', '1')
    config.set('TIMEOUT', 'minutes', '0')
    config.set('TIMEOUT', 'seconds', '0')
    config.set('TIMEOUT', 'milliseconds', '0')
    with open(CONFIGURE_FILE, 'w') as configfile:
        config.write(configfile)
        configfile.close()

user_params = Configurations()
