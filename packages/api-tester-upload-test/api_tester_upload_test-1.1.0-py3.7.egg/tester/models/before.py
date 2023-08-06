# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class Before(object):

    """Implementation of the 'Before' model.

    TODO: type model description here.

    Attributes:
        use_check_box (bool): TODO: type description here.
        title (string): TODO: type description here.
        message (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "message": 'message',
        "title": 'title',
        "use_check_box": 'useCheckBox'
    }

    def __init__(self,
                 message=None,
                 title=None,
                 use_check_box=None,
                 additional_properties={}):
        """Constructor for the Before class"""

        # Initialize members of the class
        self.use_check_box = use_check_box
        self.title = title
        self.message = message

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
        message = dictionary.get('message')
        title = dictionary.get('title')
        use_check_box = dictionary.get('useCheckBox')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(message,
                   title,
                   use_check_box,
                   dictionary)
