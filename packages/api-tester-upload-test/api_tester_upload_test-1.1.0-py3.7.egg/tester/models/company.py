# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class Company(object):

    """Implementation of the 'Company' model.

    TODO: type model description here.

    Attributes:
        company_name (string): TODO: type description here.
        address (string): TODO: type description here.
        cell_number (string): TODO: type description here.
        company (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address": 'address',
        "cell_number": 'cell number',
        "company_name": 'company name',
        "company": 'company'
    }

    def __init__(self,
                 address=None,
                 cell_number=None,
                 company_name=None,
                 company=None,
                 additional_properties={}):
        """Constructor for the Company class"""

        # Initialize members of the class
        self.company_name = company_name
        self.address = address
        self.cell_number = cell_number
        self.company = company

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

        discriminators = {
            'boss_comp': BossCompany.from_dictionary,
            'empl_comp': EmployeeComp.from_dictionary,
            'Software_Tester': SoftwareTester.from_dictionary
        }
        unboxer = discriminators.get(dictionary.get('company'))

        # Delegate unboxing to another function if a discriminator
        # value for a child class is present.
        if unboxer:
            return unboxer(dictionary)

        # Extract variables from the dictionary
        address = dictionary.get('address')
        cell_number = dictionary.get('cell number')
        company_name = dictionary.get('company name')
        company = dictionary.get('company')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(address,
                   cell_number,
                   company_name,
                   company,
                   dictionary)


class BossCompany(Company):

    """Implementation of the 'Boss_company' model.

    TODO: type model description here.
    NOTE: This class inherits from 'Company'.

    Attributes:
        first_name (string): TODO: type description here.
        last_name (string): TODO: type description here.
        address_boss (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address": 'address',
        "address_boss": 'address_boss',
        "cell_number": 'cell number',
        "company_name": 'company name',
        "first_name": 'first name',
        "last_name": 'last name',
        "company": 'company'
    }

    def __init__(self,
                 address=None,
                 address_boss=None,
                 cell_number=None,
                 company_name=None,
                 first_name=None,
                 last_name=None,
                 company=None,
                 additional_properties={}):
        """Constructor for the BossCompany class"""

        # Initialize members of the class
        self.first_name = first_name
        self.last_name = last_name
        self.address_boss = address_boss

        # Add additional model properties to the instance
        self.additional_properties = additional_properties

        # Call the constructor for the base class
        super(BossCompany, self).__init__(address,
                                          cell_number,
                                          company_name,
                                          company)

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
        address = dictionary.get('address')
        address_boss = dictionary.get('address_boss')
        cell_number = dictionary.get('cell number')
        company_name = dictionary.get('company name')
        first_name = dictionary.get('first name')
        last_name = dictionary.get('last name')
        company = dictionary.get('company')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(address,
                   address_boss,
                   cell_number,
                   company_name,
                   first_name,
                   last_name,
                   company,
                   dictionary)


class EmployeeComp(Company):

    """Implementation of the 'employee_comp' model.

    TODO: type model description here.
    NOTE: This class inherits from 'Company'.

    Attributes:
        first_name (string): TODO: type description here.
        last_name (string): TODO: type description here.
        id (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address": 'address',
        "cell_number": 'cell number',
        "company_name": 'company name',
        "first_name": 'first name',
        "id": 'id',
        "last_name": 'last name',
        "company": 'company'
    }

    def __init__(self,
                 address=None,
                 cell_number=None,
                 company_name=None,
                 first_name=None,
                 id=None,
                 last_name=None,
                 company=None,
                 additional_properties={}):
        """Constructor for the EmployeeComp class"""

        # Initialize members of the class
        self.first_name = first_name
        self.last_name = last_name
        self.id = id

        # Add additional model properties to the instance
        self.additional_properties = additional_properties

        # Call the constructor for the base class
        super(EmployeeComp, self).__init__(address,
                                           cell_number,
                                           company_name,
                                           company)

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

        discriminators = {
            'Software_Tester': SoftwareTester.from_dictionary
        }
        unboxer = discriminators.get(dictionary.get('company'))

        # Delegate unboxing to another function if a discriminator
        # value for a child class is present.
        if unboxer:
            return unboxer(dictionary)

        # Extract variables from the dictionary
        address = dictionary.get('address')
        cell_number = dictionary.get('cell number')
        company_name = dictionary.get('company name')
        first_name = dictionary.get('first name')
        id = dictionary.get('id')
        last_name = dictionary.get('last name')
        company = dictionary.get('company')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(address,
                   cell_number,
                   company_name,
                   first_name,
                   id,
                   last_name,
                   company,
                   dictionary)


class SoftwareTester(EmployeeComp):

    """Implementation of the 'Software Tester' model.

    TODO: type model description here.
    NOTE: This class inherits from 'EmployeeComp'.

    Attributes:
        team (string): TODO: type description here.
        designation (string): TODO: type description here.
        role (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address": 'address',
        "cell_number": 'cell number',
        "company_name": 'company name',
        "designation": 'designation',
        "first_name": 'first name',
        "id": 'id',
        "last_name": 'last name',
        "role": 'role',
        "team": 'team',
        "company": 'company'
    }

    def __init__(self,
                 address=None,
                 cell_number=None,
                 company_name=None,
                 designation=None,
                 first_name=None,
                 id=None,
                 last_name=None,
                 role=None,
                 team=None,
                 company=None,
                 additional_properties={}):
        """Constructor for the SoftwareTester class"""

        # Initialize members of the class
        self.team = team
        self.designation = designation
        self.role = role

        # Add additional model properties to the instance
        self.additional_properties = additional_properties

        # Call the constructor for the base class
        super(SoftwareTester, self).__init__(address,
                                             cell_number,
                                             company_name,
                                             first_name,
                                             id,
                                             last_name,
                                             company)

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
        address = dictionary.get('address')
        cell_number = dictionary.get('cell number')
        company_name = dictionary.get('company name')
        designation = dictionary.get('designation')
        first_name = dictionary.get('first name')
        id = dictionary.get('id')
        last_name = dictionary.get('last name')
        role = dictionary.get('role')
        team = dictionary.get('team')
        company = dictionary.get('company')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(address,
                   cell_number,
                   company_name,
                   designation,
                   first_name,
                   id,
                   last_name,
                   role,
                   team,
                   company,
                   dictionary)


class Developer(EmployeeComp):

    """Implementation of the 'developer' model.

    TODO: type model description here.
    NOTE: This class inherits from 'EmployeeComp'.

    Attributes:
        team (string): TODO: type description here.
        designation (string): TODO: type description here.
        role (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address": 'address',
        "cell_number": 'cell number',
        "company_name": 'company name',
        "designation": 'designation',
        "first_name": 'first name',
        "id": 'id',
        "last_name": 'last name',
        "role": 'role',
        "team": 'team',
        "company": 'company'
    }

    def __init__(self,
                 address=None,
                 cell_number=None,
                 company_name=None,
                 designation=None,
                 first_name=None,
                 id=None,
                 last_name=None,
                 role=None,
                 team=None,
                 company=None,
                 additional_properties={}):
        """Constructor for the Developer class"""

        # Initialize members of the class
        self.team = team
        self.designation = designation
        self.role = role

        # Add additional model properties to the instance
        self.additional_properties = additional_properties

        # Call the constructor for the base class
        super(Developer, self).__init__(address,
                                        cell_number,
                                        company_name,
                                        first_name,
                                        id,
                                        last_name,
                                        company)

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
        address = dictionary.get('address')
        cell_number = dictionary.get('cell number')
        company_name = dictionary.get('company name')
        designation = dictionary.get('designation')
        first_name = dictionary.get('first name')
        id = dictionary.get('id')
        last_name = dictionary.get('last name')
        role = dictionary.get('role')
        team = dictionary.get('team')
        company = dictionary.get('company')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(address,
                   cell_number,
                   company_name,
                   designation,
                   first_name,
                   id,
                   last_name,
                   role,
                   team,
                   company,
                   dictionary)
