# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.feed


class ResponseData(object):

    """Implementation of the 'ResponseData' model.

    TODO: type model description here.

    Attributes:
        feed (Feed): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "feed": 'feed'
    }

    def __init__(self,
                 feed=None,
                 additional_properties={}):
        """Constructor for the ResponseData class"""

        # Initialize members of the class
        self.feed = feed

        # Add additional model properties to the instance
        self.additional_properties = additional_properties

    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object
            as obtained from the deserialization of the server's response. The
            keys MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        feed = tester.models.feed.Feed.from_dictionary(dictionary.get('feed')) if dictionary.get('feed') else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(feed,
                   dictionary)
