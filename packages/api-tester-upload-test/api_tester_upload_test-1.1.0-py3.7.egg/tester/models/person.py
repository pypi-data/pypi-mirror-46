# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import dateutil.parser
from tester.api_helper import APIHelper
import tester.models.person


class Person(object):

    """Implementation of the 'Person' model.

    TODO: type model description here.

    Attributes:
        address (string): TODO: type description here.
        age (long|int): TODO: type description here.
        birthday (date): TODO: type description here.
        birthtime (datetime): TODO: type description here.
        name (string): TODO: type description here.
        uid (string): TODO: type description here.
        person_type (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address": 'address',
        "age": 'age',
        "birthday": 'birthday',
        "birthtime": 'birthtime',
        "name": 'name',
        "uid": 'uid',
        "person_type": 'personType'
    }

    def __init__(self,
                 address=None,
                 age=None,
                 birthday=None,
                 birthtime=None,
                 name=None,
                 uid=None,
                 person_type=None,
                 additional_properties={}):
        """Constructor for the Person class"""

        # Initialize members of the class
        self.address = address
        self.age = age
        self.birthday = birthday
        self.birthtime = APIHelper.RFC3339DateTime(birthtime) if birthtime else None
        self.name = name
        self.uid = uid
        self.person_type = person_type

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
            'Empl': Employee.from_dictionary,
            'Boss': Boss.from_dictionary
        }
        unboxer = discriminators.get(dictionary.get('personType'))

        # Delegate unboxing to another function if a discriminator
        # value for a child class is present.
        if unboxer:
            return unboxer(dictionary)

        # Extract variables from the dictionary
        address = dictionary.get('address')
        age = dictionary.get('age')
        birthday = dateutil.parser.parse(dictionary.get('birthday')).date() if dictionary.get('birthday') else None
        birthtime = APIHelper.RFC3339DateTime.from_value(dictionary.get("birthtime")).datetime if dictionary.get("birthtime") else None
        name = dictionary.get('name')
        uid = dictionary.get('uid')
        person_type = dictionary.get('personType')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(address,
                   age,
                   birthday,
                   birthtime,
                   name,
                   uid,
                   person_type,
                   dictionary)


class Employee(Person):

    """Implementation of the 'Employee' model.

    TODO: type model description here.
    NOTE: This class inherits from 'Person'.

    Attributes:
        department (string): TODO: type description here.
        dependents (list of Person): TODO: type description here.
        hired_at (datetime): TODO: type description here.
        joining_day (Days): TODO: type description here.
        salary (int): TODO: type description here.
        working_days (list of Days): TODO: type description here.
        boss (Person): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address": 'address',
        "age": 'age',
        "birthday": 'birthday',
        "birthtime": 'birthtime',
        "department": 'department',
        "dependents": 'dependents',
        "hired_at": 'hiredAt',
        "joining_day": 'joiningDay',
        "name": 'name',
        "salary": 'salary',
        "uid": 'uid',
        "working_days": 'workingDays',
        "boss": 'boss',
        "person_type": 'personType'
    }

    def __init__(self,
                 address=None,
                 age=None,
                 birthday=None,
                 birthtime=None,
                 department=None,
                 dependents=None,
                 hired_at=None,
                 joining_day='Monday',
                 name=None,
                 salary=None,
                 uid=None,
                 working_days=None,
                 boss=None,
                 person_type=None,
                 additional_properties={}):
        """Constructor for the Employee class"""

        # Initialize members of the class
        self.department = department
        self.dependents = dependents
        self.hired_at = APIHelper.HttpDateTime(hired_at) if hired_at else None
        self.joining_day = joining_day
        self.salary = salary
        self.working_days = working_days
        self.boss = boss

        # Add additional model properties to the instance
        self.additional_properties = additional_properties

        # Call the constructor for the base class
        super(Employee, self).__init__(address,
                                       age,
                                       birthday,
                                       birthtime,
                                       name,
                                       uid,
                                       person_type)

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
            'Boss': Boss.from_dictionary
        }
        unboxer = discriminators.get(dictionary.get('personType'))

        # Delegate unboxing to another function if a discriminator
        # value for a child class is present.
        if unboxer:
            return unboxer(dictionary)

        # Extract variables from the dictionary
        address = dictionary.get('address')
        age = dictionary.get('age')
        birthday = dateutil.parser.parse(dictionary.get('birthday')).date() if dictionary.get('birthday') else None
        birthtime = APIHelper.RFC3339DateTime.from_value(dictionary.get("birthtime")).datetime if dictionary.get("birthtime") else None
        department = dictionary.get('department')
        dependents = None
        if dictionary.get('dependents') is not None:
            dependents = [tester.models.person.Person.from_dictionary(x) for x in dictionary.get('dependents')]
        hired_at = APIHelper.HttpDateTime.from_value(dictionary.get("hiredAt")).datetime if dictionary.get("hiredAt") else None
        joining_day = dictionary.get("joiningDay") if dictionary.get("joiningDay") else 'Monday'
        name = dictionary.get('name')
        salary = dictionary.get('salary')
        uid = dictionary.get('uid')
        working_days = dictionary.get('workingDays')
        boss = tester.models.person.Person.from_dictionary(dictionary.get('boss')) if dictionary.get('boss') else None
        person_type = dictionary.get('personType')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(address,
                   age,
                   birthday,
                   birthtime,
                   department,
                   dependents,
                   hired_at,
                   joining_day,
                   name,
                   salary,
                   uid,
                   working_days,
                   boss,
                   person_type,
                   dictionary)


class Boss(Employee):

    """Implementation of the 'Boss' model.

    Testing circular reference.
    NOTE: This class inherits from 'Employee'.

    Attributes:
        promoted_at (datetime): TODO: type description here.
        assistant (Employee): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address": 'address',
        "age": 'age',
        "birthday": 'birthday',
        "birthtime": 'birthtime',
        "department": 'department',
        "dependents": 'dependents',
        "hired_at": 'hiredAt',
        "joining_day": 'joiningDay',
        "name": 'name',
        "promoted_at": 'promotedAt',
        "salary": 'salary',
        "uid": 'uid',
        "working_days": 'workingDays',
        "assistant": 'assistant',
        "boss": 'boss',
        "person_type": 'personType'
    }

    def __init__(self,
                 address=None,
                 age=None,
                 birthday=None,
                 birthtime=None,
                 department=None,
                 dependents=None,
                 hired_at=None,
                 joining_day='Monday',
                 name=None,
                 promoted_at=None,
                 salary=None,
                 uid=None,
                 working_days=None,
                 assistant=None,
                 boss=None,
                 person_type=None,
                 additional_properties={}):
        """Constructor for the Boss class"""

        # Initialize members of the class
        self.promoted_at = APIHelper.UnixDateTime(promoted_at) if promoted_at else None
        self.assistant = assistant

        # Add additional model properties to the instance
        self.additional_properties = additional_properties

        # Call the constructor for the base class
        super(Boss, self).__init__(address,
                                   age,
                                   birthday,
                                   birthtime,
                                   department,
                                   dependents,
                                   hired_at,
                                   joining_day,
                                   name,
                                   salary,
                                   uid,
                                   working_days,
                                   boss,
                                   person_type)

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
        age = dictionary.get('age')
        birthday = dateutil.parser.parse(dictionary.get('birthday')).date() if dictionary.get('birthday') else None
        birthtime = APIHelper.RFC3339DateTime.from_value(dictionary.get("birthtime")).datetime if dictionary.get("birthtime") else None
        department = dictionary.get('department')
        dependents = None
        if dictionary.get('dependents') is not None:
            dependents = [tester.models.person.Person.from_dictionary(x) for x in dictionary.get('dependents')]
        hired_at = APIHelper.HttpDateTime.from_value(dictionary.get("hiredAt")).datetime if dictionary.get("hiredAt") else None
        joining_day = dictionary.get("joiningDay") if dictionary.get("joiningDay") else 'Monday'
        name = dictionary.get('name')
        promoted_at = APIHelper.UnixDateTime.from_value(dictionary.get("promotedAt")).datetime if dictionary.get("promotedAt") else None
        salary = dictionary.get('salary')
        uid = dictionary.get('uid')
        working_days = dictionary.get('workingDays')
        assistant = tester.models.person.Employee.from_dictionary(dictionary.get('assistant')) if dictionary.get('assistant') else None
        boss = tester.models.person.Person.from_dictionary(dictionary.get('boss')) if dictionary.get('boss') else None
        person_type = dictionary.get('personType')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(address,
                   age,
                   birthday,
                   birthtime,
                   department,
                   dependents,
                   hired_at,
                   joining_day,
                   name,
                   promoted_at,
                   salary,
                   uid,
                   working_days,
                   assistant,
                   boss,
                   person_type,
                   dictionary)
