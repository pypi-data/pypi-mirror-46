import sys
import os
from shutil import rmtree

CACHE_PATH = '__httpantry_cache__'

def main():
    if len(sys.argv) == 1:
        help_command()
    else:
        arg = sys.argv[1]

        if arg == 'server':
            import httpantry
            httpantry.validate_cache_dir()
            httpantry.http_proxy_server.init_proxy_server()
        elif arg == 'cleanup':
            if os.path.isdir(CACHE_PATH):
                rmtree(CACHE_PATH)
        elif arg == '--help' or arg == 'help':
            help_command()
        elif arg == 'init':
            import httpantry
            httpantry.validate_cache_dir()
        elif arg == 'flush':
            import httpantry
            path = CACHE_PATH + "/proxy_database.db"
            if os.path.isfile(path):
                os.remove(path)
        else:
            print('Usage: httpantry COMMAND\n\n'
                    'try "httpantry --help" for help')


def help_command():
    print("Usage: httpantry COMMAND\n\n"
                "Commands:\n"
                "\t init\n"
                "\t server\n"
                "\t cleanup")
