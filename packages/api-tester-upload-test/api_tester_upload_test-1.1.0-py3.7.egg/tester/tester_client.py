# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""

from tester.decorators import lazy_property
from tester.configuration import Configuration
from tester.controllers.response_types_controller\
    import ResponseTypesController
from tester.controllers.form_params_controller import FormParamsController
from tester.controllers.body_params_controller import BodyParamsController
from tester.controllers.error_codes_controller import ErrorCodesController
from tester.controllers.query_param_controller import QueryParamController
from tester.controllers.echo_controller import EchoController
from tester.controllers.header_controller import HeaderController
from tester.controllers.template_params_controller\
    import TemplateParamsController
from tester.controllers.query_params_controller import QueryParamsController


class TesterClient(object):

    @lazy_property
    def response_types(self):
        return ResponseTypesController(self.config)

    @lazy_property
    def form_params(self):
        return FormParamsController(self.config)

    @lazy_property
    def body_params(self):
        return BodyParamsController(self.config)

    @lazy_property
    def error_codes(self):
        return ErrorCodesController(self.config)

    @lazy_property
    def query_param(self):
        return QueryParamController(self.config)

    @lazy_property
    def echo(self):
        return EchoController(self.config)

    @lazy_property
    def header(self):
        return HeaderController(self.config)

    @lazy_property
    def template_params(self):
        return TemplateParamsController(self.config)

    @lazy_property
    def query_params(self):
        return QueryParamsController(self.config)

    def __init__(self, config=Configuration()):
        self.config = config
