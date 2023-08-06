# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.entry


class Feed(object):

    """Implementation of the 'Feed' model.

    TODO: type model description here.

    Attributes:
        feed_url (string): TODO: type description here.
        title (string): TODO: type description here.
        link (string): TODO: type description here.
        author (string): TODO: type description here.
        description (string): TODO: type description here.
        mtype (string): TODO: type description here.
        entries (list of Entry): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "author": 'author',
        "description": 'description',
        "entries": 'entries',
        "feed_url": 'feedUrl',
        "link": 'link',
        "title": 'title',
        "mtype": 'type'
    }

    def __init__(self,
                 author=None,
                 description=None,
                 entries=None,
                 feed_url=None,
                 link=None,
                 title=None,
                 mtype=None,
                 additional_properties={}):
        """Constructor for the Feed class"""

        # Initialize members of the class
        self.feed_url = feed_url
        self.title = title
        self.link = link
        self.author = author
        self.description = description
        self.mtype = mtype
        self.entries = entries

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
        description = dictionary.get('description')
        entries = None
        if dictionary.get('entries') is not None:
            entries = [tester.models.entry.Entry.from_dictionary(x) for x in dictionary.get('entries')]
        feed_url = dictionary.get('feedUrl')
        link = dictionary.get('link')
        title = dictionary.get('title')
        mtype = dictionary.get('type')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(author,
                   description,
                   entries,
                   feed_url,
                   link,
                   title,
                   mtype,
                   dictionary)
