import json
import tornado.ioloop
import tornado.web

import calc

calc_methods = [method for method in dir(calc) if callable(getattr(calc, method))]

calc_score = {}
i = 0
for method in calc_methods:
    calc_score[method] = calc_methods[i]
    i += 1

def test(station, time):
    return {"test": "hello test"}

calc_score["test"] = test

class BaseHandler(tornado.web.RequestHandler):
    def user(self):
        return self.get_secure_cookie("user")


class HomeHandler(BaseHandler):
    def get(self):
        self.write("Hello Index!!")


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
        handlers = [
            (r"/", HomeHandler),
            (r"/api/([^/]*)", EntryHandler)
        ]
        super(Application, self).__init__(handlers)


def start():
    application = Application()
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()

def main():
    start()
    return 0

if __name__ == "__main__":
    main()
