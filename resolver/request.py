# -*- coding: utf-8 -*-

import requests

from validator_collection import checkers
from sceptre.resolvers import Resolver
from sceptre.exceptions import SceptreException


class InvalidResolverArgumentValueError(SceptreException):
    """
    Error raised if a resolver's argument value is invalid.
    """

    pass


class Request(Resolver):
    """
    Resolve data from a REST API endpoint.
    """

    VALID_AUTHENTICATION_METHODS = ["BASIC"]

    def _make_request(self, url, auth_type=None):
        """
        Make a request to a REST API endpoint
        :param url: The url endpoint reference
        """
        content = None
        if auth_type:
            response = requests.get(url, auth_type)
        else:
            response = requests.get(url)
        content = response.text
        response.raise_for_status()
        return content

    def resolve(self):
        """
        This method is invoked by Sceptre

        :returns: Response from the request
        :rtype: str
        """

        args = self.argument
        url = None
        auth= None

        if not isinstance(args, str):
            url = args.get("url")
            auth = args.get("auth")
            if isinstance(args, dict):
                auth_type = args["auth"]["auth_type"]
                if not auth_type in self.VALID_AUTHENTICATION_METHODS:
                    raise InvalidResolverArgumentValueError(f"Invalid request method: {auth_type}")

                if auth_type == "BASIC":
                    response = self._make_request(args, auth)

        if checkers.is_url(args):
            response = self._make_request(args, auth_type)
        else:
            raise InvalidResolverArgumentValueError(f"Invalid argument: {args}")

        return response
