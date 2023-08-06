# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class Entry(object):

    """Implementation of the 'Entry' model.

    TODO: type model description here.

    Attributes:
        title (string): TODO: type description here.
        link (string): TODO: type description here.
        author (string): TODO: type description here.
        published_date (string): TODO: type description here.
        content_snippet (string): TODO: type description here.
        content (string): TODO: type description here.
        categories (list of string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "author": 'author',
        "categories": 'categories',
        "content": 'content',
        "content_snippet": 'contentSnippet',
        "link": 'link',
        "published_date": 'publishedDate',
        "title": 'title'
    }

    def __init__(self,
                 author=None,
                 categories=None,
                 content=None,
                 content_snippet=None,
                 link=None,
                 published_date=None,
                 title=None,
                 additional_properties={}):
        """Constructor for the Entry class"""

        # Initialize members of the class
        self.title = title
        self.link = link
        self.author = author
        self.published_date = published_date
        self.content_snippet = content_snippet
        self.content = content
        self.categories = categories

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
        author = dictionary.get('author')
        categories = dictionary.get('categories')
        content = dictionary.get('content')
        content_snippet = dictionary.get('contentSnippet')
        link = dictionary.get('link')
        published_date = dictionary.get('publishedDate')
        title = dictionary.get('title')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(author,
                   categories,
                   content,
                   content_snippet,
                   link,
                   published_date,
                   title,
                   dictionary)
