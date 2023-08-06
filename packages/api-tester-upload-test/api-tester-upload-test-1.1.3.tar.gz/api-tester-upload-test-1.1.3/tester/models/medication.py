# -*- coding: utf-8 -*-

"""
    tester

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

import tester.models.ace_inhibitor
import tester.models.antianginal
import tester.models.anticoagulant
import tester.models.beta_blocker
import tester.models.diuretic
import tester.models.mineral

class Medication(object):

    """Implementation of the 'Medication' model.

    TODO: type model description here.

    Attributes:
        ace_inhibitors (list of AceInhibitor): TODO: type description here.
        antianginal (list of Antianginal): TODO: type description here.
        anticoagulants (list of Anticoagulant): TODO: type description here.
        beta_blocker (list of BetaBlocker): TODO: type description here.
        diuretic (list of Diuretic): TODO: type description here.
        mineral (list of Mineral): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "ace_inhibitors":'aceInhibitors',
        "antianginal":'antianginal',
        "anticoagulants":'anticoagulants',
        "beta_blocker":'betaBlocker',
        "diuretic":'diuretic',
        "mineral":'mineral'
    }

    def __init__(self,
                 ace_inhibitors=None,
                 antianginal=None,
                 anticoagulants=None,
                 beta_blocker=None,
                 diuretic=None,
                 mineral=None,
                 additional_properties = {}):
        """Constructor for the Medication class"""

        # Initialize members of the class
        self.ace_inhibitors = ace_inhibitors
        self.antianginal = antianginal
        self.anticoagulants = anticoagulants
        self.beta_blocker = beta_blocker
        self.diuretic = diuretic
        self.mineral = mineral

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
        ace_inhibitors = None
        if dictionary.get('aceInhibitors') != None:
            ace_inhibitors = list()
            for structure in dictionary.get('aceInhibitors'):
                ace_inhibitors.append(tester.models.ace_inhibitor.AceInhibitor.from_dictionary(structure))
        antianginal = None
        if dictionary.get('antianginal') != None:
            antianginal = list()
            for structure in dictionary.get('antianginal'):
                antianginal.append(tester.models.antianginal.Antianginal.from_dictionary(structure))
        anticoagulants = None
        if dictionary.get('anticoagulants') != None:
            anticoagulants = list()
            for structure in dictionary.get('anticoagulants'):
                anticoagulants.append(tester.models.anticoagulant.Anticoagulant.from_dictionary(structure))
        beta_blocker = None
        if dictionary.get('betaBlocker') != None:
            beta_blocker = list()
            for structure in dictionary.get('betaBlocker'):
                beta_blocker.append(tester.models.beta_blocker.BetaBlocker.from_dictionary(structure))
        diuretic = None
        if dictionary.get('diuretic') != None:
            diuretic = list()
            for structure in dictionary.get('diuretic'):
                diuretic.append(tester.models.diuretic.Diuretic.from_dictionary(structure))
        mineral = None
        if dictionary.get('mineral') != None:
            mineral = list()
            for structure in dictionary.get('mineral'):
                mineral.append(tester.models.mineral.Mineral.from_dictionary(structure))

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(ace_inhibitors,
                   antianginal,
                   anticoagulants,
                   beta_blocker,
                   diuretic,
                   mineral,
                   dictionary)


