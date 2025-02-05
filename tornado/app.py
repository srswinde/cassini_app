import tornado.ioloop
import tornado.web
import base64
import os
from api.handlers import main_handlers
import logging
logging.basicConfig(level=logging.DEBUG)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name =  os.environ.get('POSTGRES_DB')
        self.write(f"Hello, world {name}!")

def make_app():
    return tornado.web.Application([
        (r"/", main_handlers.HelloWorldHandler),
        (r"/recreate", main_handlers.RecreateDatabaseHandler),
        (r"/lazyload", main_handlers.LazyLoadHandler),
        (r"/process", main_handlers.ProcessHandler),
    ], debug=True, logging='debug')

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
