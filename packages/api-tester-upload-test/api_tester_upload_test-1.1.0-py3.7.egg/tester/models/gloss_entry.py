# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.gloss_def


class GlossEntry(object):

    """Implementation of the 'GlossEntry' model.

    TODO: type model description here.

    Attributes:
        id (string): TODO: type description here.
        sort_as (string): TODO: type description here.
        gloss_term (string): TODO: type description here.
        acronym (string): TODO: type description here.
        abbrev (string): TODO: type description here.
        gloss_def (GlossDef): TODO: type description here.
        gloss_see (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "abbrev": 'Abbrev',
        "acronym": 'Acronym',
        "gloss_def": 'GlossDef',
        "gloss_see": 'GlossSee',
        "gloss_term": 'GlossTerm',
        "id": 'ID',
        "sort_as": 'SortAs'
    }

    def __init__(self,
                 abbrev=None,
                 acronym=None,
                 gloss_def=None,
                 gloss_see=None,
                 gloss_term=None,
                 id=None,
                 sort_as=None,
                 additional_properties={}):
        """Constructor for the GlossEntry class"""

        # Initialize members of the class
        self.id = id
        self.sort_as = sort_as
        self.gloss_term = gloss_term
        self.acronym = acronym
        self.abbrev = abbrev
        self.gloss_def = gloss_def
        self.gloss_see = gloss_see

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
        abbrev = dictionary.get('Abbrev')
        acronym = dictionary.get('Acronym')
        gloss_def = tester.models.gloss_def.GlossDef.from_dictionary(dictionary.get('GlossDef')) if dictionary.get('GlossDef') else None
        gloss_see = dictionary.get('GlossSee')
        gloss_term = dictionary.get('GlossTerm')
        id = dictionary.get('ID')
        sort_as = dictionary.get('SortAs')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(abbrev,
                   acronym,
                   gloss_def,
                   gloss_see,
                   gloss_term,
                   id,
                   sort_as,
                   dictionary)
