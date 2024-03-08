import json
import os
from models.base_model import BaseModel


class FileStorage:
    """
    This class serves as an Object-Relation Mapping interface to store and retrieve objects using JSON format.
    """

    __objects = {}
    __file_path = 'file.json'
    
    classManes = ["BaseModel", "Place", "City", "Amenity", "Review"]

    def all(self):
        """Return all instances stored"""
        return FileStorage.__objects

    def new(self, obj):
        """Stores a new Object"""
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes objects stored and persists them in a file"""
        serialized = {key: value.to_dict() for key, value in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)

    def reload(self):
        """reload method that update __objects dictionary 'deserialized from JSON file' """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as js_f:
                for key, obj in json.loads(js_f.read()).items():
                    obj = eval(obj['__class__'])(**obj)
                    FileStorage.__objects[key] = obj
