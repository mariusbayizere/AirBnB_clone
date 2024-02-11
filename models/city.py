#!/usr/bin/python3

"""Defines the City class."""

from models.base_model import BaseModel


class City(BaseModel):
    """
    Represent a city.

    Attributes:
        state_id (str): The ID of the state where the city is located.
        name (str): The name of the city.
    """

    state_id = ""
    name = ""
