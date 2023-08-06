# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class Status(object):

    """Implementation of the 'Status' model.

    TODO: type model description here.

    Attributes:
        document_status (string): TODO: type description here.
        completed_packages (list of string): TODO: type description here.
        attachment_packages (object): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "attachment_packages": 'attachmentPackages',
        "completed_packages": 'completedPackages',
        "document_status": 'documentStatus'
    }

    def __init__(self,
                 attachment_packages=None,
                 completed_packages=None,
                 document_status=None,
                 additional_properties={}):
        """Constructor for the Status class"""

        # Initialize members of the class
        self.document_status = document_status
        self.completed_packages = completed_packages
        self.attachment_packages = attachment_packages

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
        attachment_packages = dictionary.get('attachmentPackages')
        completed_packages = dictionary.get('completedPackages')
        document_status = dictionary.get('documentStatus')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(attachment_packages,
                   completed_packages,
                   document_status,
                   dictionary)
