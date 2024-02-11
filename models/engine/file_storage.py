#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent the FileStorage  class which is the abstract engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        this function will return the dictionary __object.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the internal storage dictionary.

        Args:
            obj: The object to be added to the storage.

        Returns:
            None
        """
        xx1 = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(xx1, obj.id)] = obj

    def save(self):
        """
        Serialize objects stored in the internal storage to a JSON file.
        """
        module = FileStorage.__objects
        diction_object = {obj: module[obj].to_dict() for obj in module.keys()}
        
    def reload(self):
        """
        Reload objects from a JSON file into the internal storage.
        """
        try:
            with open(FileStorage.__file_path) as file:
                diction_object = json.load(file)
                for obj_key, obj_value in diction_object.items():
                    p = obj_value["__class__"]
                    del obj_value["__class__"]
                    self.new(eval(p)(**obj_value))
        except FileNotFoundError:
            return
