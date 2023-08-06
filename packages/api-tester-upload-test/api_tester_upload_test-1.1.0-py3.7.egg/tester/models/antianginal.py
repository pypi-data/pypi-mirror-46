# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class Antianginal(object):

    """Implementation of the 'Antianginal' model.

    TODO: type model description here.

    Attributes:
        name (string): TODO: type description here.
        strength (string): TODO: type description here.
        dose (string): TODO: type description here.
        route (string): TODO: type description here.
        sig (string): TODO: type description here.
        pill_count (string): TODO: type description here.
        refills (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "dose": 'dose',
        "name": 'name',
        "pill_count": 'pillCount',
        "refills": 'refills',
        "route": 'route',
        "sig": 'sig',
        "strength": 'strength'
    }

    def __init__(self,
                 dose=None,
                 name=None,
                 pill_count=None,
                 refills=None,
                 route=None,
                 sig=None,
                 strength=None,
                 additional_properties={}):
        """Constructor for the Antianginal class"""

        # Initialize members of the class
        self.name = name
        self.strength = strength
        self.dose = dose
        self.route = route
        self.sig = sig
        self.pill_count = pill_count
        self.refills = refills

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
        dose = dictionary.get('dose')
        name = dictionary.get('name')
        pill_count = dictionary.get('pillCount')
        refills = dictionary.get('refills')
        route = dictionary.get('route')
        sig = dictionary.get('sig')
        strength = dictionary.get('strength')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(dose,
                   name,
                   pill_count,
                   refills,
                   route,
                   sig,
                   strength,
                   dictionary)
