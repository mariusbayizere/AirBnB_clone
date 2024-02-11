#!/usr/bin/python3
"""model we have BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """represent the BaseModel"""

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        datefun = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for x, v in kwargs.items():
                if x == "created_at" or x == "updated_at":
                    self.__dict__[x] = datetime.strptime(v, datefun)
                else:
                    self.__dict__[x] = v
        else:
            models.storage.new(self)

    def save(self):
        """save updated_at with current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """this module will Return the Dictionary of the BaseModel class.
        """
        rdict = self.__dict__.copy()
        rdict["created_at"] = self.created_at.isoformat()
        rdict["updated_at"] = self.updated_at.isoformat()
        rdict["__class__"] = self.__class__.__name__
        return rdict

    def __str__(self):
        """this module will Return String representation of the BaseModel"""
        finalResilt = self.__class__.__name__
        return "[{}] ({}) {}".format(finalResilt, self.id, self.__dict__)
