# -*- coding: utf-8 -*-

"""
    tester

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
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
        "imaging":'imaging',
        "labs":'labs',
        "medications":'medications'
    }

    def __init__(self,
                 imaging=None,
                 labs=None,
                 medications=None,
                 additional_properties = {}):
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
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        imaging = None
        if dictionary.get('imaging') != None:
            imaging = list()
            for structure in dictionary.get('imaging'):
                imaging.append(tester.models.imaging.Imaging.from_dictionary(structure))
        labs = None
        if dictionary.get('labs') != None:
            labs = list()
            for structure in dictionary.get('labs'):
                labs.append(tester.models.lab.Lab.from_dictionary(structure))
        medications = None
        if dictionary.get('medications') != None:
            medications = list()
            for structure in dictionary.get('medications'):
                medications.append(tester.models.medication.Medication.from_dictionary(structure))

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(imaging,
                   labs,
                   medications,
                   dictionary)


