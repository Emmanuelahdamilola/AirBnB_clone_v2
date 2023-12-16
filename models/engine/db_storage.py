#!/usr/bin/python3
"""Creating a new engine `DBStorage` for managing database storage"""
import os
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.review import Review

class DBStorage:
    """
    Represents a database storage engine for the HBNB project.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new instance of the DBStorage class.
        """
        # Create a database engine using environment variables
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                       .format(os.environ.get('HBNB_MYSQL_USER'),
                                               os.environ.get('HBNB_MYSQL_PWD'),
                                               os.environ.get('HBNB_MYSQL_HOST'),
                                               os.environ.get('HBNB_MYSQL_DB')),
                                       pool_pre_ping=True)
        
        # If in 'test' environment, drop all tables
        if os.environ.get('HBNB_ENV') == 'test': 
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the database and returns objects as a dictionary.

        Args:
            cls (str): Optional class name to filter objects.

        Returns:
            Dictionary of objects with keys in the format 'ClassName.ID'.
        """
        if cls:
            results = self.__session.query(eval(cls)).all()
        else:
            # Combine results from multiple classes into one list
            results = (self.__session.query(State).all() +
                       self.__session.query(City).all() +
                       self.__session.query(User).all() +
                       self.__session.query(Place).all() +
                       self.__session.query(Review).all())

        return {f"{type(obj).__name__}.{obj.id}": obj for obj in results}

    def new(self, obj):
        """
        Adds the object to the current database session.

        Args:
            obj: Object to be added to the session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes to the database.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session.

        Args:
            obj: Object to be deleted from the session.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and the current database session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """Close scoped session
        """
        self.__session.remove()
