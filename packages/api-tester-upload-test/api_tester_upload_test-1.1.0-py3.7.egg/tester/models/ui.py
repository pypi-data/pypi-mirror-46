# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.dialogs
import tester.models.styling


class Ui(object):

    """Implementation of the 'Ui' model.

    TODO: type model description here.

    Attributes:
        dialogs (Dialogs): TODO: type description here.
        language (LanguageEnum): TODO: type description here.
        styling (Styling): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "dialogs": 'dialogs',
        "language": 'language',
        "styling": 'styling'
    }

    def __init__(self,
                 dialogs=None,
                 language=None,
                 styling=None,
                 additional_properties={}):
        """Constructor for the Ui class"""

        # Initialize members of the class
        self.dialogs = dialogs
        self.language = language
        self.styling = styling

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
        dialogs = tester.models.dialogs.Dialogs.from_dictionary(dictionary.get('dialogs')) if dictionary.get('dialogs') else None
        language = dictionary.get('language')
        styling = tester.models.styling.Styling.from_dictionary(dictionary.get('styling')) if dictionary.get('styling') else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(dialogs,
                   language,
                   styling,
                   dictionary)
