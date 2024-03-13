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
from .errors import *
import datetime


class FileStorage:
    """
    This class serves as an ORM interface to store and retrieve objects <- JSON
    """

    __objects = {}
    __file_path = 'file.json'
    models = ("BaseModel", "User", "Place", "State\
", "City", "Amenity", "Review")

    def all(self):
        """Return all instances stored"""
        return FileStorage.__objects

    def new(self, obj):
        """Stores a new Object"""
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes objects stored and persist in file"""
        serialized = {
                key: val.to_dict()
                for key, val in self.__objects.items()
            }
        with open(FileStorage.__file_path, "w") as f:
            f.write(json.dumps(serialized))

    def reload(self):
        """de-serialize persisted objects"""
        try:
            deserialized = {}
            with open(FileStorage.__file_path, "r") as f:
                deserialized = json.loads(f.read())
            FileStorage.__objects = {
                key:
                    eval(obj["__class__"])(**obj)
                    for key, obj in deserialized.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            # No need for error
            pass

    def find_by_id(self, model, obj_id):
        """Find and return an elemt of model by its id"""
        F = FileStorage
        if model not in F.models:
            # Invalid Model Name
            # Not yet Implemented
            raise ModelNotFoundError(model)

            key = model + "." + obj_id
            if key not in F.__objects:
                # invalid id
                # Not yet Implemented
                raise InstanceNotFoundError(obj_id, model)

            return F.__objects[key]

    def delete_by_id(self, model, obj_id):
        """Find and return an elemt of model by its id"""
        F = FileStorage
        if model not in F.models:
            raise ModelNotFoundError(model)

        key = model + "." + obj_id
        if key not in F.__objects:
            raise InstanceNotFoundError(obj_id, model)

        del F.__objects[key]
        self.save()

    def find_all(self, model=""):
        """Find all instances or instances of model"""
        if model and model not in FileStorage.models:
            raise ModelNotFoundError(model)
        results = []
        for key, val in FileStorage.__objects.items():
            if key.startswith(model):
                results.append(str(val))
        return results

    def update_one(self, model, iid, field, value):
        """Updates an instance"""
        F = FileStorage
        if model not in F.models:
            raise ModelNotFoundError(model)

        key = model + "." + iid
        if key not in F.__objects:
            raise InstanceNotFoundError(iid, model)

        if field in ("id", "updated_at", "created_at"):
            # not allowed to be updated
            return
        inst = F.__objects[key]
        try:
            # if instance has that value
            # cast it to its type
            vtype = type(inst.__dict__[field])
            inst.__dict__[field] = vtype(value)
        except KeyError:
            # instance doesn't has the field
            # assign the value with its type
            inst.__dict__[field] = value
        finally:
            inst.updated_at = datetime.utcnow()
            self.save()
