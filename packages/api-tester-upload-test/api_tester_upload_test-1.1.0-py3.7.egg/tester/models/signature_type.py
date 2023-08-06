# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class SignatureType(object):

    """Implementation of the 'SignatureType' model.

    TODO: type model description here.

    Attributes:
        mechanism (string): TODO: type description here.
        on_eaccept_use_hand_written_signature (bool): TODO: type description
            here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "mechanism": 'mechanism',
        "on_eaccept_use_hand_written_signature": 'onEacceptUseHandWrittenSignature'
    }

    def __init__(self,
                 mechanism=None,
                 on_eaccept_use_hand_written_signature=None,
                 additional_properties={}):
        """Constructor for the SignatureType class"""

        # Initialize members of the class
        self.mechanism = mechanism
        self.on_eaccept_use_hand_written_signature = on_eaccept_use_hand_written_signature

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
        mechanism = dictionary.get('mechanism')
        on_eaccept_use_hand_written_signature = dictionary.get('onEacceptUseHandWrittenSignature')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(mechanism,
                   on_eaccept_use_hand_written_signature,
                   dictionary)
