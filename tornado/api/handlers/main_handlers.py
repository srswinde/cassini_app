import tornado.web
from database.models import recreate, hole_camera, get_session, db_process
from sqlalchemy import and_
from dateutil.parser import parse
import datetime
import pandas as pd
import logging
from api.process_loaders import get_day
from database.models import HAS_TURTLE

class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        
        logging.debug("accessing main!")
        html = """
        <html>
        <head>
        <title>Cassini's Website</title>
        </head>
        <body>
        <h1>Welcome to Cassini's Lazy Loader</h1>
        Let's load a database the cassini way -- lazily.
        <br>
        
        <img src="https://swahle.org/cassini/hole-cam/static/2025/2/5/snapshot_1738786148.59658.jpg" height=300 width=400>
        <br>
        
        <a href="/lazyload?date=08-23-2024">Lazy Load</a>
        <br>
        <a href="/process">Or see a list of the loading processes.</a>
        </body>
        </html>
        """
        self.write(html)
        
class RecreateDatabaseHandler(tornado.web.RequestHandler):
    def get(self):
        logging.debug("recreating database")
        recreate()
        self.write("Database recreated")
        

class LazyLoadHandler(tornado.web.RequestHandler):
    def get(self):
        """
        Lazy load the data from the database and show picture of cassini.
        """
        logging.debug("lazy loading")
        
        date = self.get_argument("date", None)
        if date is None:
            date = "01-20-2025"
        data = get_day(hole_camera, date)
        if data is None or data.empty:
            self.write(f"No images available for this {date}")
            return
        
        if 'hasTurtle' in data.columns:
            data['hasTurtle'] = data['hasTurtle'].apply(lambda x: x == HAS_TURTLE.YES)
        
        ii = data.prob.argmax()
        url = data.iloc[ii].path.replace("/mnt/nfs/hole-cam", "https://swahle.org/cassini/hole-cam/static")
        html = f"""
        <html>
        <head>
        <title>Lazy Load</title>
        </head>
        <body>
        <h1>Lazy Loading cassini's database</h1>
        <img src={url} height=300 width=400>
        <br>
        <a href="https://github.com/srswinde/cassini_app">This project is hosted on github.</a>
        </body>
        </html>
        
        """
        self.write(html)
    
class ProcessHandler(tornado.web.RequestHandler):
    
    def get(self):
        logging.debug("processing")
        
        session = get_session()()
        query = session.query(db_process)
        
        df = pd.read_sql(query.statement, query.session.bind)
        
        df['data_time'] = pd.to_datetime(df['data_time'], unit='ms')
        
        
        self.write(df.to_html())
    
