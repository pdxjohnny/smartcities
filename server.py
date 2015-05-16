import os
import json
import argparse
import tornado.ioloop
import tornado.web
import traceback

import calc

__version__ = "0.0.1"
__description__ = "GuardJog server to calculate results"


DIRECTORY = os.path.join(os.path.dirname(__file__))
INDEX_PAGE = "site/index.html"
DEFUALT_PORT = 80

class BaseHandler(tornado.web.RequestHandler):
    """
    A Basic class to derive from
    """
    pass


class Index_Handler(BaseHandler):
    """
    Render the index page
    """
    def get(self):
        self.render(DIRECTORY + INDEX_PAGE)


class API_Handler(BaseHandler):
    """
    Calls functions in the calc.py file.
    Passed get query parameters that specify what data is needed.
    Example:
    score: crime, air, park
    station: station_id
    time: morning, afternoon, night
    Returns the intiger scores in a json from use by client.
    Example:
    {
        "OK": true,
        "morning": {
            "nonviolent": 18,
            "violent": 0
            },
        "afternoon": {
            "nonviolent": 31,
            "violent": 3
        },
        "night": {
            "nonviolent": 42,
            "violent": 6
        }
    }
    """
    def get(self, slug):
        # The result that will be sent to the client as a json
        # Basic return value
        result = {"OK": False}
        # Get he query parameters
        score = self.get_argument('score', False)
        station = self.get_argument('station', False)
        time = self.get_argument('time', False)
        # Use the score parameter to get result of the
        # function with that name in calc.
        if score:
            # Try to call the function
            try:
                # Update the result dict with the returned dict
                result.update( getattr(calc, score)(station, time) )
                # It worked so say OK
                result["OK"] = True
            # If the function fails say why
            except Exception, error:
                # Add the error to the return
                error = unicode(traceback.format_exc())
                result["ERROR"] = error
        # Say that a score is needed
        else:
            result["ERROR"] = u"No score given"
        # json dump and return the results
        result = json.dumps(result)
        # Return the result to the client
        self.write(unicode(result))


class SC_Server(tornado.web.Application):
    """
    The tornado server process that binds to port
    and handles requests.
    """
    def __init__(self):
        # The settings that tell how to server the static files
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "site"),
            "cookie_secret": "KNSDF23HRGBBE8D",
            "xsrf_cookies": True,
        }
        # Spectify the handlers for the urls
        handlers = [
            (r"/", Index_Handler),
            (r"/api/([^/]*)", API_Handler),
            (r'/(.*)', tornado.web.StaticFileHandler, \
                dict(path=settings['static_path']) ),
        ]
        # Call init on tornado.web.Application
        super(SC_Server, self).__init__(handlers, **settings)


def start(port=DEFUALT_PORT, key=False, crt=False):
    application = SC_Server()
    application.listen(port)
    print "Serving on port", port
    tornado.ioloop.IOLoop.instance().start()


def arg_setup():
    arg_parser = argparse.ArgumentParser(description=__description__)
    arg_parser.add_argument("--port", "-p", type=int, \
        help="Port to host or connect to GuardJog server")
    arg_parser.add_argument("--key", "-k", type=unicode, \
        help="Key file to use")
    arg_parser.add_argument("--crt", "-c", type=unicode, \
        help="Cert file to use")
    arg_parser.add_argument("--version", "-v", action="version", \
        version=u"GuardJog " + unicode(__version__) )
    initial = vars(arg_parser.parse_args())
    args = {}
    for arg in initial:
        if initial[arg]:
            args[arg] = initial[arg]
    return args

def main():
    args = arg_setup()
    start(**args)
    return 0

if __name__ == "__main__":
    main()
