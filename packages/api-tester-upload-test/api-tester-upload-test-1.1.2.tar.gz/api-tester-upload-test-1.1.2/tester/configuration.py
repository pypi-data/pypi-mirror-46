# -*- coding: utf-8 -*-

"""
    tester

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

import sys
import logging

from tester.api_helper import APIHelper

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Configuration(object):

    """A class used for configuring the SDK by a user.

    This class need not be instantiated and all properties and methods
    are accessible without instance creation.

    """

    # Set the array parameter serialization method
    # (allowed: indexed, unindexed, plain, csv, tsv, psv)
    array_serialization = "indexed"

    # An enum for SDK environments
    class Environment(object):
        PRODUCTION = 0
        TESTING = 1

    # An enum for API servers
    class Server(object):
        DEFAULT = 0
        AUTH_SERVER = 1

    # The environment in which the SDK is running
    environment = Environment.TESTING

    # TODO: Set an appropriate value
    port = '80'

    # TODO: Set an appropriate value
    suites = 1

    # The username to use with basic authentication
    # TODO: Set an appropriate value
    basic_auth_user_name = 'TODO: Replace'

    # The password to use with basic authentication
    # TODO: Set an appropriate value
    basic_auth_password = 'TODO: Replace'

    # The username to use with HMAC authentication
    # TODO: Set an appropriate value
    hmac_auth_user_name = None

    # The password to use with HMAC authentication
    # TODO: Set an appropriate value
    hmac_auth_password = None

    # All the environments the SDK can run in
    environments = {
        Environment.PRODUCTION: {
            Server.DEFAULT: 'http://apimatic.hopto.org:{suites}',
            Server.AUTH_SERVER: 'http://apimaticauth.hopto.org:3000',
        },
        Environment.TESTING: {
            Server.DEFAULT: 'http://localhost:3000',
            Server.AUTH_SERVER: 'http://apimaticauth.xhopto.org:3000',
        },
    }

    @classmethod
    def get_base_uri(cls, server=Server.DEFAULT):
        """Generates the appropriate base URI for the environment and the server.

        Args:
            server (Configuration.Server): The server enum for which the base URI is required.

        Returns:
            String: The base URI.

        """
        parameters = {
            "port": cls.port,
            "suites": cls.suites,
        }
        return APIHelper.append_url_with_template_parameters(
            cls.environments[cls.environment][server], parameters, False)

    @classmethod
    def disable_logging(cls):
        """Disable all logging in the SDK
        """
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

    @classmethod
    def enable_logging(cls, filename=None, filemode='a',
                       stream=sys.stdout, level=logging.INFO):
        """Enable logging in the SDK

        Args:
            filename: Specifies that a FileHandler be created, using the specified
                filename, rather than a StreamHandler.
            filemode: If filename is specified, open the file in this mode.
                Defaults to 'a'.
            stream: Use the specified stream to initialize the StreamHandler.
            level: Set the root logger level to the specified level.
        """

        cls.disable_logging()   # clear previously set logging info

        if filename is None:
            logging.basicConfig(stream=stream, level=level)
        else:
            logging.basicConfig(filename=filename, filemode=filemode,
                                level=level)
