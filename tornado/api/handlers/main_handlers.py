import tornado.web
from database.models import recreate, hole_camera, get_session
from dateutil.parser import parse

class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World!")
        
        
class RecreateDatabaseHandler(tornado.web.RequestHandler):
    def get(self):
        recreate()
        self.write("Database recreated")
        

class LazyLoadHandler(tornado.web.RequestHandler):
    def get(self):
        
        date = self.get_argument("date", None)
        if date is None:
            date = "01-20-2025"
        date = parse(date)
        midnight = date.replace(hour=0, minute=0, second=0, microsecond=0)
        next_midnight = midnight + timedelta(days=1)
        
        maker = get_session()
        session = maker()
        query = session.query(hole_camera)\
            .filter(and_(hole_camera.timestamp*1000 >= midnight.timestamp(), hole_camera.timestamp*1000 < next_midnight.timestamp()))
        CNT = query.count()
       
        self.write(F"Count: {CNT}")
        return
        
    
