# -*- coding: utf-8 -*-

"""
    tester

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

import tester.models.query_parameter

class EchoResponse(object):

    """Implementation of the 'EchoResponse' model.

    Raw http Request info

    Attributes:
        body (dict<object, object>): TODO: type description here.
        headers (dict<object, string>): TODO: type description here.
        method (string): TODO: type description here.
        path (string): relativePath
        query (dict<object, QueryParameter>): TODO: type description here.
        upload_count (int): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "body":'body',
        "headers":'headers',
        "method":'method',
        "path":'path',
        "query":'query',
        "upload_count":'uploadCount'
    }

    def __init__(self,
                 body=None,
                 headers=None,
                 method=None,
                 path=None,
                 query=None,
                 upload_count=None,
                 additional_properties = {}):
        """Constructor for the EchoResponse class"""

        # Initialize members of the class
        self.body = body
        self.headers = headers
        self.method = method
        self.path = path
        self.query = query
        self.upload_count = upload_count

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
        body = dictionary.get('body')
        headers = dictionary.get('headers')
        method = dictionary.get('method')
        path = dictionary.get('path')
        query = tester.models.query_parameter.QueryParameter.from_dictionary(dictionary.get('query')) if dictionary.get('query') else None
        upload_count = dictionary.get('uploadCount')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(body,
                   headers,
                   method,
                   path,
                   query,
                   upload_count,
                   dictionary)


