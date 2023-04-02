# -*- coding: utf-8 -*-

import requests

from validator_collection import checkers
from sceptre.resolvers import Resolver
from sceptre.exceptions import SceptreException
from jsonschema import validate
from requests.auth import HTTPBasicAuth

VALID_AUTH_TYPES = ["basic"]

RESOLVER_ARGS_SCHEMA = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "auth": {"enum": VALID_AUTH_TYPES},
        "user": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["url"],
    "if": {"properties": {"auth": {"const": "basic"}}, "required": ["auth"]},
    "then": {"required": ["user", "password"]},
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

    def _make_request(self, url, auth=None):
        """
        Make a request to a REST API endpoint
        :param url: The url endpoint reference
        """
        content = None

        if auth:
            response = requests.get(url, auth=auth)
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
        url = args

        if isinstance(args, dict):
            validate(instance=args, schema=RESOLVER_ARGS_SCHEMA)
            url = args.get("url")

        if not checkers.is_url(url):
            raise InvalidResolverArgumentValueError(f"Invalid argument: {url}")

        auth = None
        if isinstance(args, dict) and "auth" in args:
            auth_type = args.get("auth").lower()
            if auth_type == "basic":
                user = args.get("user")
                password = args.get("password")
                auth = HTTPBasicAuth(user, password)

        response = self._make_request(url, auth=auth)
        return response
