# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""

from enum import Enum
from tester.api_helper import APIHelper
from tester.http.requests_client import RequestsClient


class Environment(Enum):
    """An enum for SDK environments"""
    PRODUCTION = 0
    TESTING = 1


class Server(Enum):
    """An enum for API servers"""
    DEFAULT = 0
    AUTH_SERVER = 1


class Configuration(object):

    """A class used for configuring the SDK by a user.
    """

    @property
    def http_client(self):
        return self._http_client

    @property
    def timeout(self):
        return self._timeout

    @property
    def array_serialization(self):
        return self._array_serialization

    @property
    def environment(self):
        return self._environment

    @property
    def port(self):
        return self._port

    @property
    def suites(self):
        return self._suites

    def __init__(self, timeout=60, array_serialization='indexed',
                 environment=Environment.TESTING, port='80', suites=1):
        # The value to use for connection timeout
        self._timeout = timeout

        # Set the array parameter serialization method.
        # (allowed: indexed, unindexed, plain, csv, tsv, psv)
        self._array_serialization = array_serialization

        # Current API environment
        self._environment = environment

        # port value
        self._port = port

        # suites value
        self._suites = suites

        # The Http Client to use for making requests.
        self._http_client = self.create_http_client()

    def clone_with(self, timeout=None, array_serialization=None,
                   environment=None, port=None, suites=None):

        timeout = timeout or self.timeout
        array_serialization = array_serialization or self.array_serialization
        environment = environment or self.environment
        port = port or self.port
        suites = suites or self.suites

        return Configuration(timeout=timeout,
                             array_serialization=array_serialization,
                             environment=environment, port=port, suites=suites)

    def create_http_client(self):
        return RequestsClient(timeout=self.timeout)

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

    def get_base_uri(self, server=Server.DEFAULT):
        """Generates the appropriate base URI for the environment and the
        server.

        Args:
            server (Configuration.Server): The server enum for which the base
            URI is required.

        Returns:
            String: The base URI.

        """
        parameters = {
            "port": self.port,
            "suites": self.suites,
        }

        return APIHelper.append_url_with_template_parameters(
            self.environments[self.environment][server], parameters, False
        )
