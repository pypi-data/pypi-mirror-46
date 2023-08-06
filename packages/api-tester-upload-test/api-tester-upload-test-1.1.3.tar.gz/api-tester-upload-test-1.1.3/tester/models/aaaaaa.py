# -*- coding: utf-8 -*-

"""
    tester

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

import dateutil.parser
from tester.api_helper import APIHelper

class Aaaaaa(object):

    """Implementation of the '_aaaaaa' model.

    TODO: type model description here.

    Attributes:
        address (string): TODO: type description here.
        age (int): TODO: type description here.
        birthday (list of date): TODO: type description here.
        birthtime (list of datetime): TODO: type description here.
        name (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address":'address',
        "age":'age',
        "birthday":'birthday',
        "birthtime":'birthtime',
        "name":'name'
    }

    def __init__(self,
                 address=None,
                 age=None,
                 birthday=None,
                 birthtime=None,
                 name=None,
                 additional_properties = {}):
        """Constructor for the Aaaaaa class"""

        # Initialize members of the class
        self.address = address
        self.age = age
        self.birthday = birthday
        self.birthtime = APIHelper.RFC3339DateTime(birthtime) if birthtime else None
        self.name = name

        # Add additional model properties to the instance
        self.additional_properties = additional_properties


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        address = dictionary.get('address')
        age = dictionary.get('age')
        birthday = None
        if dictionary.get('birthday') != None:
            birthday = list()
            for date_string in dictionary.get('birthday'):
                birthday.append(dateutil.parser.parse(date_string).date())
        birthtime = None
        if dictionary.get('birthtime') != None:
            birthtime = list()
            for datetime_string in dictionary.get('birthtime'):
                birthtime.append(APIHelper.RFC3339DateTime.from_value(datetime_string).datetime)
        name = dictionary.get('name')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(address,
                   age,
                   birthday,
                   birthtime,
                   name,
                   dictionary)


