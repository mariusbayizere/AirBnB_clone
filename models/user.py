#!/usr/bin/python3
"""Define class user"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    Represent class user.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
