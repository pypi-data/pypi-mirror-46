# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.attributes


class ResponseWithEnum(object):

    """Implementation of the 'response with Enum' model.

    TODO: type model description here.

    Attributes:
        param_format (ParamFormat): TODO: type description here.
        optional (bool): TODO: type description here.
        mtype (Type): TODO: type description here.
        constant (bool): TODO: type description here.
        is_array (bool): TODO: type description here.
        is_stream (bool): TODO: type description here.
        is_attribute (bool): TODO: type description here.
        is_map (bool): TODO: type description here.
        attributes (Attributes): TODO: type description here.
        nullable (bool): TODO: type description here.
        id (string): TODO: type description here.
        name (string): TODO: type description here.
        description (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "attributes": 'attributes',
        "constant": 'constant',
        "description": 'description',
        "id": 'id',
        "is_array": 'isArray',
        "is_attribute": 'isAttribute',
        "is_map": 'isMap',
        "is_stream": 'isStream',
        "name": 'name',
        "nullable": 'nullable',
        "optional": 'optional',
        "param_format": 'paramFormat',
        "mtype": 'type'
    }

    def __init__(self,
                 attributes=None,
                 constant=None,
                 description=None,
                 id=None,
                 is_array=None,
                 is_attribute=None,
                 is_map=None,
                 is_stream=None,
                 name=None,
                 nullable=None,
                 optional=None,
                 param_format=None,
                 mtype=None,
                 additional_properties={}):
        """Constructor for the ResponseWithEnum class"""

        # Initialize members of the class
        self.param_format = param_format
        self.optional = optional
        self.mtype = mtype
        self.constant = constant
        self.is_array = is_array
        self.is_stream = is_stream
        self.is_attribute = is_attribute
        self.is_map = is_map
        self.attributes = attributes
        self.nullable = nullable
        self.id = id
        self.name = name
        self.description = description

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
        attributes = tester.models.attributes.Attributes.from_dictionary(dictionary.get('attributes')) if dictionary.get('attributes') else None
        constant = dictionary.get('constant')
        description = dictionary.get('description')
        id = dictionary.get('id')
        is_array = dictionary.get('isArray')
        is_attribute = dictionary.get('isAttribute')
        is_map = dictionary.get('isMap')
        is_stream = dictionary.get('isStream')
        name = dictionary.get('name')
        nullable = dictionary.get('nullable')
        optional = dictionary.get('optional')
        param_format = dictionary.get('paramFormat')
        mtype = dictionary.get('type')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(attributes,
                   constant,
                   description,
                   id,
                   is_array,
                   is_attribute,
                   is_map,
                   is_stream,
                   name,
                   nullable,
                   optional,
                   param_format,
                   mtype,
                   dictionary)
