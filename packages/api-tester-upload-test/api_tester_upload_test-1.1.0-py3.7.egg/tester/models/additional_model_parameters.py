# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.job


class AdditionalModelParameters(object):

    """Implementation of the 'AdditionalModelParameters' model.

    TODO: type model description here.

    Attributes:
        name (string): TODO: type description here.
        field (string): TODO: type description here.
        address (string): TODO: type description here.
        job (Job): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "job": 'Job',
        "address": 'address',
        "field": 'field',
        "name": 'name'
    }

    def __init__(self,
                 job=None,
                 address=None,
                 field=None,
                 name=None,
                 additional_properties={}):
        """Constructor for the AdditionalModelParameters class"""

        # Initialize members of the class
        self.name = name
        self.field = field
        self.address = address
        self.job = job

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
        job = tester.models.job.Job.from_dictionary(dictionary.get('Job')) if dictionary.get('Job') else None
        address = dictionary.get('address')
        field = dictionary.get('field')
        name = dictionary.get('name')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(job,
                   address,
                   field,
                   name,
                   dictionary)
