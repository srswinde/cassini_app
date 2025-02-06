from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, Float, String, Enum, insert, desc, and_
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
import enum
import os
import datetime
import requests
import logging



def get_dburi():
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_user = os.environ.get('POSTGRES_USER')
    db_name = os.environ.get('POSTGRES_DB')
    host = os.environ.get('POSTGRES_HOST')
    uri = f'postgresql+psycopg2://{db_user}:{db_password}@{host}:5432/{db_name}'
    return uri
    
def get_session():
    uri = get_dburi()
    maker = sessionmaker(bind=create_engine(uri))
    return maker

Base = declarative_base()
TEST_CASE = True



class conditions(Base):

    __tablename__="conditions"

    timestamp=Column(Integer, primary_key=True)
    temperature_F=Column(Float)
    relative_humidity=Column(Float)

    def to_dict(self):
        return {
                'timestamp':self.timestamp,
                "temperature_F":self.temperature_F,
                "relative_humidity":self.relative_humidity
                }


class HAS_TURTLE(enum.Enum):
    YES = 1
    NO = 0
    NULL = -1
    
class HAS_HUMAN(enum.Enum):
    YES = 1
    NO = 0
    NULL = -1
    
class HAS_MOTION(enum.Enum):
    YES = 1
    NO = 0
    NULL = -1

class LazyLoader:
    
        
    @classmethod
    def clean_data(cls, row):
        """Handle special data types

        Parameters
        ----------
        row : dict
            A dictionary of row data from the database

        Returns
        -------
        dict
            The cleaned row data
        """
        
        if 'hasTurtle' in row:
            row['hasTurtle'] = HAS_TURTLE(row['hasTurtle']['value'])
            
        return row
    
        

class images(Base):
    
    __tablename__="images"
    timestamp=Column(Integer, primary_key=True)
    path=Column(String(255))
    hasTurtle=Column(Enum(HAS_TURTLE), default=HAS_TURTLE.NULL)
    
class probabilities(Base):
    
    __tablename__="probabilities"
    timestamp=Column(Integer, primary_key=True)
    prob=Column(Float)

class pretrained(Base):
    __tablename__="pretrained"
    timestamp=Column(Integer, primary_key=True)
    model_file=Column(String(255), default="")
    prob=Column(Float)

class detections(Base):
    
    __tablename__="detections"
    timestamp=Column(Integer, primary_key=True)
    hasTurtle=Column(Enum(HAS_TURTLE), default=HAS_TURTLE.NULL)

class pretrained_models(Base):
    __tablename__="pretrained_models"
    id=Column(Integer, primary_key=True, autoincrement=True)
    timestamp=Column(Integer)
    model_file=Column(String(255), default="")
    prob=Column(Float)

class pretrained_20240311_0221(Base):
    __tablename__="pretrained_20240311_0221"
    timestamp=Column(Integer, primary_key=True)
    model_file=Column(String(255), default="")
    prob=Column(Float)

class temp_sensors(Base):
    
    __tablename__="temp_sensors"
    timestamp = Column(Integer, primary_key=True)
    address = Column(String(255))
    temp = Column(Float)
    

class hole_camera(Base, LazyLoader):
    __tablename__="hole_camera"
    timestamp = Column(BigInteger, primary_key=True)
    path = Column(String(512))
    hasTurtle = Column(Enum(HAS_TURTLE), default=HAS_TURTLE.NULL)
    xpos = Column(Float, default=-1.0)
    ypos = Column(Float, default=-1.0)
    model_name = Column(String(512), default="")
    prob = Column(Float, default=-1.0)

class hole_camera_metadata(Base):
    
    __tablename__="hole_camera_metadata"
    timestamp = Column(BigInteger, primary_key=True)
    is_human_detected = Column(Enum(HAS_HUMAN), default=HAS_HUMAN.NULL)
    is_motion_detected = Column(Enum(HAS_MOTION), default=HAS_MOTION.NULL)
    
class hole_camera_resnet_detection(Base):
        
    __tablename__="hole_camera_resnet_detection"
    index = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(BigInteger)
    model_name = Column(String(512))
    path = Column(String(512))
    prob = Column(Float)
    class_name = Column(String(100))
    class_number = Column(Integer)
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)


class notifications(Base):
    
    __tablename__="notifications"
    timestamp = Column(BigInteger, primary_key=True)
    notification_type = Column(String(128))
    detection_start = Column(BigInteger)
    detection_end = Column(BigInteger)
    message = Column(String(512))
    start_notified = Column(Integer, default=0)
    end_notified = Column(Integer, default=0)
    

class cassini_orientation(Base):
    
    __tablename__="cassini_orientation"
    timestamp = Column(BigInteger, primary_key=True)
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
    
    orientation = Column(Integer)

class Loader:
    """A class to load data into the database
    """
    
    def __init__(self, table, data):
        
        self.table = table
        self.data = data

    def load(self):
        """Load data into the database
        The method blocks until the data is loaded into the database. 
        """
        
        session = get_session()()
        db_process_ = db_process()
        db_process_.process_name = "load"
        db_process_.status = "start"
        db_process_.table_name = self.table.__tablename__
        db_process_.data_time = self.data[0]['timestamp']
        db_process_.data_length = len(self.data)
        db_process_.processed_rows = 0
        session.add(db_process_)
        session.commit()
        length = len(self.data)
        new_rows = []
        for ii, row in enumerate(self.data):
            new_rows.append(self.table(**self.table.clean_data(row)))
            if ii % 100 == 0:
                db_process_.processed_rows = ii
                session.add_all(new_rows)
                session.commit()
                new_rows = []
                
        session.add_all(new_rows)
        db_process_.processed_rows = length
        db_process_.status = "complete"
        session.add(db_process_)
        session.commit()
        session.close()

class db_process(Base):
    
    __tablename__="db_process"
    timestamp = Column(BigInteger, primary_key=True)
    process_name = Column(String(128))
    status = Column(String(128))
    message = Column(String(512))
    table_name = Column(String(128))
    data_time = Column(BigInteger)
    data_length = Column(Integer)
    processed_rows = Column(Integer)
  
def recreate():
    md = Base.metadata
    s = get_session()()
    md.bind = s.bind
    md.create_all(s.bind)
    s.close()