# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.medication
import tester.models.lab
import tester.models.imaging


class Complex1(object):

    """Implementation of the 'complex1' model.

    TODO: type model description here.

    Attributes:
        medications (list of Medication): TODO: type description here.
        labs (list of Lab): TODO: type description here.
        imaging (list of Imaging): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "imaging": 'imaging',
        "labs": 'labs',
        "medications": 'medications'
    }

    def __init__(self,
                 imaging=None,
                 labs=None,
                 medications=None,
                 additional_properties={}):
        """Constructor for the Complex1 class"""

        # Initialize members of the class
        self.medications = medications
        self.labs = labs
        self.imaging = imaging

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
        imaging = None
        if dictionary.get('imaging') is not None:
            imaging = [tester.models.imaging.Imaging.from_dictionary(x) for x in dictionary.get('imaging')]
        labs = None
        if dictionary.get('labs') is not None:
            labs = [tester.models.lab.Lab.from_dictionary(x) for x in dictionary.get('labs')]
        medications = None
        if dictionary.get('medications') is not None:
            medications = [tester.models.medication.Medication.from_dictionary(x) for x in dictionary.get('medications')]

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(imaging,
                   labs,
                   medications,
                   dictionary)
