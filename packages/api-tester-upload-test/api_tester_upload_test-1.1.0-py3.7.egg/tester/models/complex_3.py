# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.signer
import tester.models.status
import tester.models.data_to_sign
import tester.models.contact_details
import tester.models.advanced


class Complex3(object):

    """Implementation of the 'complex3' model.

    TODO: type model description here.

    Attributes:
        document_id (string): TODO: type description here.
        signers (list of Signer): TODO: type description here.
        status (Status): TODO: type description here.
        title (string): TODO: type description here.
        description (string): TODO: type description here.
        external_id (string): TODO: type description here.
        data_to_sign (DataToSign): TODO: type description here.
        contact_details (ContactDetails): TODO: type description here.
        advanced (Advanced): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "advanced": 'advanced',
        "contact_details": 'contactDetails',
        "data_to_sign": 'dataToSign',
        "description": 'description',
        "document_id": 'documentId',
        "external_id": 'externalId',
        "signers": 'signers',
        "status": 'status',
        "title": 'title'
    }

    def __init__(self,
                 advanced=None,
                 contact_details=None,
                 data_to_sign=None,
                 description=None,
                 document_id=None,
                 external_id=None,
                 signers=None,
                 status=None,
                 title=None,
                 additional_properties={}):
        """Constructor for the Complex3 class"""

        # Initialize members of the class
        self.document_id = document_id
        self.signers = signers
        self.status = status
        self.title = title
        self.description = description
        self.external_id = external_id
        self.data_to_sign = data_to_sign
        self.contact_details = contact_details
        self.advanced = advanced

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
        advanced = tester.models.advanced.Advanced.from_dictionary(dictionary.get('advanced')) if dictionary.get('advanced') else None
        contact_details = tester.models.contact_details.ContactDetails.from_dictionary(dictionary.get('contactDetails')) if dictionary.get('contactDetails') else None
        data_to_sign = tester.models.data_to_sign.DataToSign.from_dictionary(dictionary.get('dataToSign')) if dictionary.get('dataToSign') else None
        description = dictionary.get('description')
        document_id = dictionary.get('documentId')
        external_id = dictionary.get('externalId')
        signers = None
        if dictionary.get('signers') is not None:
            signers = [tester.models.signer.Signer.from_dictionary(x) for x in dictionary.get('signers')]
        status = tester.models.status.Status.from_dictionary(dictionary.get('status')) if dictionary.get('status') else None
        title = dictionary.get('title')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(advanced,
                   contact_details,
                   data_to_sign,
                   description,
                   document_id,
                   external_id,
                   signers,
                   status,
                   title,
                   dictionary)
