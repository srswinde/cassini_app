import subprocess
from threading import Thread
from dateutil.parser import parse
from database.models import Loader
from database.models import get_session, hole_camera, hole_camera_resnet_detection
from sqlalchemy import and_
import datetime
import logging
import requests
import pandas as pd


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ThreadManager(metaclass=Singleton):
    """Manage threads for loading data to the database use a singleton pattern
    to only instantiate one instance of the class


    """
    
    
    def __init__(self):
        
        self.threads = []
        
    def start_loader(self, table, data):
        """Start a loader thread to load data into the database

        Parameters
        ----------
        table : database.models.Base
            table from the database ORM.
        data : list
            database data from other website.
        """
        
        loader = Loader(table, data)
        self.add_thread(loader.load, ())
    
    def add_thread(self, target, args):
        """Add a thread to the thread manager"""
        
        thread = Thread(target=target, args=args, daemon=True,)
        self.threads.append(thread)
        
        thread.start()
        
    def __iter__(self):
        return iter(self.threads)
    
    def join(self):
        for thread in self.threads:
            thread.join()
    
    


def get_day(table, date):
    
    database_map = {
        "hole_camera": hole_camera,
        "hole_camera_resnet_detection": hole_camera_resnet_detection
    }
    
    if table.__tablename__ not in database_map:
        raise ValueError(f"Table {table} not found")
    
    if type(date) == str:
        date = parse(date)
        
    if date > datetime.datetime.now():
        raise ValueError("Cannot query future dates")
        
    midnight = date.replace(hour=0, minute=0, second=0, microsecond=0)
    next_midnight = midnight + datetime.timedelta(days=1)
    session = get_session()()
    query = session.query(table).filter(and_(table.timestamp >= midnight.timestamp()*1000, table.timestamp < next_midnight.timestamp()*1000))
    logging.info(f"Querying {table.__tablename__} for {date} found {query.count()} rows")
    if query.count() == 0:
        logging.info(f"No local data found for {date}, lazy loading")
        data = get_from_url(table, date)
        ThreadManager().start_loader(table, data)
        if data is None or len(data) == 0:
            return pd.DataFrame()
        else:
            return pd.DataFrame(data)
        
    else:
        return pd.read_sql(query.statement, query.session.bind)
        

def get_from_url(table, date):
    
    datestr = date.strftime("%m-%d-%Y")
    url = f"https://swahle.org/cassini/db/{table.__tablename__}/{datestr}"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error loading data from {url} {response.text}")
    
    data = response.json()
    return data
    


