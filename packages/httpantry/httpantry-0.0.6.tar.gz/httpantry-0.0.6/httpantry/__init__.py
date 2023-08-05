import httpantry.parse_configuration as parse_configuration
import requests
from .requests_wrapper import handle_request
import httpantry.http_proxy_server as http_proxy_server
import os
import stat


CACHE_PATH = "__httpantry_cache__"
DEPLOYABLE_PATH = "deployable_database.py"
INIT = False

def __getattr__(name):
    """
    Handle method calls
    """

    print(name)

    known_methods = ["get", "post", "put", "delete", "patch"]
    
    def call_unknown_method(*args, **kwargs):
        try:
            method_to_call = getattr(requests, name)
            return method_to_call(*args, **kwargs)
        except:
            raise

    def call_known_method(*args, **kwargs):
        try:
            if not INIT:
                validate_cache_dir()
            return handle_request(name, *args, **kwargs)
        except:
            raise
    
    if name in known_methods:
        return call_known_method
    else:
        return call_unknown_method

def validate_cache_dir():
    ''' Validates that the cache directory has been set up correctly '''
    if not os.path.isdir(CACHE_PATH):
        os.mkdir(CACHE_PATH) 
    INIT = True
    parse_configuration.userConfiguration()

