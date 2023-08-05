# httpantry
Httpantry is a set of tools for caching RESTful API calls in development environments.

The pip package contains two components: a Flask proxy server and a wrapper module for the Python Requests library.

### Running the Proxy Server

You can run the Flask proxy server from the command line using:

```httpantry server```

This command will create a directory named ```__httpantry_cache__``` containing the cache database ```proxy_database.db```, the configuration file ```config```, and the custom responses file ```custom_responses.json```.

To start caching responses, simply point your requests at the proxy server using ```http://localhost:<port_number>```, where ```<port_number>``` is the specified port number in the configuration file.

The server can be killed at any time. To remove the cache directory and all contents, including configurations and custom responses, run:

```httpantry cleanup```

##### Note: the proxy server cannot proxy HTTPS requests. For HTTPS requests, please consider using the wrapper functionality for the Requests library.

To create the ```__httpantry_cache__``` directory and populate it with the default infrastructure without running the proxy server or importing the wrapper functions, run:

```httpantry init```

To flush the cache, run:

```httpantry flush```

### Using the wrapper functions

This package contains wrapper functions for the user-facing API of the Python Requests library. These wrapper functions include:
```
requests.get()
requests.put()
requests.post()
requests.delete()
requests.patch()
```

If your code is using the Requests library, you can simply replace 
```import requests``` with ```import httpantry as requests```.
After switching the imports, all requests and associated responses through the functions enumerated above will be cached, and all other function calls will be forwarded to the correction function in the Requests library.

The wrapper functions will also create the cache directory on import. The directory can be deleted easily using the command:
```httpantry cleanup```

### Configurations

Both the wrapper functions and proxy server will parse configurations from a ```config``` file in the ```__httpantry_cache___``` directory. If one does not exist there, one will be created with the following default configurations:

```
[GENERAL]
port_number = 5000
persistence = True
uncached_apis = yourmom.com http://httpbin.org/image/jpeg

[CUSTOM_RESPONSES]
use_custom_responses = True
file_name = __httpantry_cache__/custom_responses.json

[TIMEOUT]
days = 0
hours = 1
minutes = 0
seconds = 0
milliseconds = 0
```

```port_number``` specifies the port number of the proxy server.
```persistence``` specifies whether the responses should be stored in a persistent database or not.
```uncached apis``` is a space-delimited list of URLs. Any API call to a URL in this list will not be cached.
The ```[TIMEOUT]``` section specifies the length of time for which a response can be considered valid. Responses are not deleted from the database upon timeout. Instead, they will be resolved again, and the new response will be stored.

### Custom Responses

httpantry allows for customized responses. These responses are recorded in ```__httpantry_cache___/custom_responses.json```. They consist of the ```method```, ```url```, and ```content``` of the response. If the file does not exist when the module is imported, it will be created with the following example content:

```json
[
    {
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
    }
]
```

Authors: Rowen Felt and Zebediah Millslagle

