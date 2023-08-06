# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.time_to_live


class Advanced(object):

    """Implementation of the 'Advanced' model.

    TODO: type model description here.

    Attributes:
        tags (list of string): TODO: type description here.
        attachments (int): TODO: type description here.
        required_signatures (int): TODO: type description here.
        get_social_security_number (bool): TODO: type description here.
        time_to_live (TimeToLive): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "attachments": 'attachments',
        "get_social_security_number": 'getSocialSecurityNumber',
        "required_signatures": 'requiredSignatures',
        "tags": 'tags',
        "time_to_live": 'timeToLive'
    }

    def __init__(self,
                 attachments=None,
                 get_social_security_number=None,
                 required_signatures=None,
                 tags=None,
                 time_to_live=None,
                 additional_properties={}):
        """Constructor for the Advanced class"""

        # Initialize members of the class
        self.tags = tags
        self.attachments = attachments
        self.required_signatures = required_signatures
        self.get_social_security_number = get_social_security_number
        self.time_to_live = time_to_live

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
        attachments = dictionary.get('attachments')
        get_social_security_number = dictionary.get('getSocialSecurityNumber')
        required_signatures = dictionary.get('requiredSignatures')
        tags = dictionary.get('tags')
        time_to_live = tester.models.time_to_live.TimeToLive.from_dictionary(dictionary.get('timeToLive')) if dictionary.get('timeToLive') else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(attachments,
                   get_social_security_number,
                   required_signatures,
                   tags,
                   time_to_live,
                   dictionary)
