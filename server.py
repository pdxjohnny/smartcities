import tornado.ioloop
import tornado.web

class sc_server(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", sc_server),
])

def start():
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()

def main():
	start()
	return 0

if __name__ == "__main__":
	main()
