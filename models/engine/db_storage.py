#!/usr/bin/Python3
"""Defines the engine for the MySQL database"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


username = getenv('HBNB_MYSQL_USER')
password = getenv('HBNB_MYSQL_PWD')
hostname = getenv('HBNB_MYSQL_HOST')
databse = getenv('HBNB_MYSQL_DB')
environment = getenv('HBNB_ENV')
all_classes = [State, City, User, Place, Review, Amenity]


class DBStorage:
    """Defining the class DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize a connection with MySQL and create tables"""
        db_url = 'mysql+mysqldb://{}:{}@{}/{}'.format(
                 username, password, hostname, databse)
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if environment == "test":
            Base.MetaData.drop_all()


    def all(self, cls=None):
        """Returns a dictionary of objects"""
        my_dict = dict()

        if cls in all_classes:
            return self.get_data_from_table(cls, my_dict)

        for cl in all_classes:
            my_dict = self.get_data_from_table(cl, my_dict)

        return my_dict

    def new(self, obj):
        """Adds a new object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Method to commit all changes to the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Method to delete a new object to the current database"""
        self.__session.delete(obj)

    def reload(self):
        """Method to create the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get_data_from_table(self, cls, structure):
        """Get the data from a MySQL Table"""
        if type(structure) is dict:
            query = self.__session.query(cls)
            for _row in query.all():
                key = "{}.{}".format(cls.__name__, _row.id)
                structure[key] = _row

            return structure

    def close(self):
        """public methodto to call remove method"""
        self.__session.close()
