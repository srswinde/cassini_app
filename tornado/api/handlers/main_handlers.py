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
        self.write("Hello, World!")
        
        
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
        <img src={url}>
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
    
