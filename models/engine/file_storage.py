#!/usr/bin/python3
"""
It's the business layer
that serves to store and retrieve objects using JSON format from a file
"""
import json
import os
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.review import Review


class FileStorage:
    """
    This class serves as an ORM interface to store and retrieve objects <- JSON
    """

    __objects = {}
    __file_path = 'file.json'

    def all(self):
        """Return all instances stored"""
        return FileStorage.__objects

    def new(self, obj):
        """Stores a new Object"""
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes objects stored and persists them in a file"""
        serialized = {}
        for key, value in FileStorage.__objects.items():
            serialized[key] = value.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)

    def reload(self):
        """reload method 'deserialized from JSON file' """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as js_f:
                for key, obj in json.loads(js_f.read()).items():
                    obj = eval(obj['__class__'])(**obj)
                    FileStorage.__objects[key] = obj
