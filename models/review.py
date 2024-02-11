#!/usr/bin/python3
"""Defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Represents a review associated with a place in the application.

    Inherits from:
        BaseModel: Base class for all models, providing attributes
                   and methods for data management.

    Attributes:
        place_id (str): The ID of the place review is associated with.
        user_id (str): The ID of the user who created this review.
        text (str): The text content of the review.
    """
    place_id = ""
    user_id = ""
    text = ""
