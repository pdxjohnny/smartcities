import os
import json
import tornado.ioloop
import tornado.web

import calc

calc_methods = [method for method in dir(calc) if callable(getattr(calc, method))]

calc_score = {}
i = 0
for method in calc_methods:
    calc_score[method] = getattr(calc, method)
    i += 1

def test(station, time):
    return {"test": "hello test", "station": station, "time": time}

calc_score["test"] = test

class BaseHandler(tornado.web.RequestHandler):
    def user(self):
        return self.get_secure_cookie("user")


class HomeHandler(BaseHandler):
    def get(self):
        self.render(os.path.join(os.path.dirname(__file__)) + "site/index.html")


class EntryHandler(BaseHandler):
    def get(self, slug):
        result = {"OK": False}
        score = self.get_argument('score', False)
        station = self.get_argument('station', False)
        time = self.get_argument('time', False)
        if score:
            result.update( calc_score[score](station, time) )
            result["OK"] = True
        result = json.dumps(result)
        self.write(unicode(result))


class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "site"),
            "cookie_secret": "KNSDF23HRGBBE8D",
            "xsrf_cookies": True,
        }
        handlers = [
            (r"/", HomeHandler),
            (r"/api/([^/]*)", EntryHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path']) ),
        ]
        super(Application, self).__init__(handlers, **settings)


def start():
    application = Application()
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()

def main():
    start()
    return 0

if __name__ == "__main__":
    main()
