# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.redirect_settings
import tester.models.signature_type
import tester.models.ui


class Signer(object):

    """Implementation of the 'Signer' model.

    TODO: type model description here.

    Attributes:
        id (string): TODO: type description here.
        url (string): TODO: type description here.
        links (list of string): TODO: type description here.
        external_signer_id (string): TODO: type description here.
        redirect_settings (RedirectSettings): TODO: type description here.
        signature_type (SignatureType): TODO: type description here.
        ui (Ui): TODO: type description here.
        tags (list of string): TODO: type description here.
        order (int): TODO: type description here.
        required (bool): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "external_signer_id": 'externalSignerId',
        "id": 'id',
        "links": 'links',
        "order": 'order',
        "redirect_settings": 'redirectSettings',
        "required": 'required',
        "signature_type": 'signatureType',
        "tags": 'tags',
        "ui": 'ui',
        "url": 'url'
    }

    def __init__(self,
                 external_signer_id=None,
                 id=None,
                 links=None,
                 order=None,
                 redirect_settings=None,
                 required=None,
                 signature_type=None,
                 tags=None,
                 ui=None,
                 url=None,
                 additional_properties={}):
        """Constructor for the Signer class"""

        # Initialize members of the class
        self.id = id
        self.url = url
        self.links = links
        self.external_signer_id = external_signer_id
        self.redirect_settings = redirect_settings
        self.signature_type = signature_type
        self.ui = ui
        self.tags = tags
        self.order = order
        self.required = required

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
        external_signer_id = dictionary.get('externalSignerId')
        id = dictionary.get('id')
        links = dictionary.get('links')
        order = dictionary.get('order')
        redirect_settings = tester.models.redirect_settings.RedirectSettings.from_dictionary(dictionary.get('redirectSettings')) if dictionary.get('redirectSettings') else None
        required = dictionary.get('required')
        signature_type = tester.models.signature_type.SignatureType.from_dictionary(dictionary.get('signatureType')) if dictionary.get('signatureType') else None
        tags = dictionary.get('tags')
        ui = tester.models.ui.Ui.from_dictionary(dictionary.get('ui')) if dictionary.get('ui') else None
        url = dictionary.get('url')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(external_signer_id,
                   id,
                   links,
                   order,
                   redirect_settings,
                   required,
                   signature_type,
                   tags,
                   ui,
                   url,
                   dictionary)
