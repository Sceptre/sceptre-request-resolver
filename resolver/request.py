# -*- coding: utf-8 -*-

import requests

from validator_collection import checkers
from sceptre.resolvers import Resolver
from sceptre.exceptions import SceptreException
from jsonschema import validate
from requests.auth import HTTPBasicAuth


args_schema = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "auth": {"type": "string"},
        "auth_type": {"enum": ["basic"]},
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["url"],
    "dependentRequired": {"auth": ["auth_type"]},
    "anyOf": [
        {
            "properties": {"auth_type": {"const": "basic"}},
            "required": ["username", "password"],
        }
    ],
}


class InvalidResolverArgumentValueError(SceptreException):
    """
    Error raised if a resolver's argument value is invalid.
    """

    pass


class Request(Resolver):
    """
    Resolve data from a REST API endpoint.
    """

    VALID_AUTHENTICATION_METHODS = ["basic"]

    def _make_request(self, args=None):
        """
        Make a request to a REST API endpoint
        :param url: The url endpoint reference
        """
        content = None
        url = args.get("url")
        if not checkers.is_url(url):
            raise InvalidResolverArgumentValueError(f"Invalid argument: {url}")

        if args.get("auth_type") == "basic":
            username = args.get("username")
            password = args.get("password")
            response = requests.get(url, auth=HTTPBasicAuth(username, password))
        else:
            response = requests.get(url)

        response.raise_for_status()
        content = response.text
        return content

    def resolve(self):
        """
        This method is invoked by Sceptre

        :returns: Response from the request
        :rtype: str
        """

        args = self.argument
        validate(instance=args, schema=args_schema)
        response = self._make_request(args)

        return response
