import tornado.ioloop
import tornado.web
import base64
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name =  os.environ.get('POSTGRES_DB')
        self.write(f"Hello, world {name}!")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
