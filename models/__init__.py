#!/usr/bin/python3
"""Module for managing the storage system for HBNB project"""
import os

# Check the storage type defined in the environment variables
if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
    # If using a database, import and use the DBStorage class
    from models.engine.db_storage import DBStorage
    storage_engine = DBStorage()
else:
    # If using file storage, import and use the FileStorage class
    from models.engine.file_storage import FileStorage
    storage_engine = FileStorage()

# Load or reload the storage system
storage_engine.reload()
