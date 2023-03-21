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
        
        if isinstance(args, str):
            url = args
            
        if isinstance(args, dict):
            if not "url" in args.keys:
                raise InvalidResolverArgumentValueError(f"Missing required argument: url")

            url = args.get("url")
                
            if "auth" in args.keys():
                auth_type = args.get("auth_type")
                if not auth_type in self.VALID_AUTHENTICATION_METHODS:
                    raise InvalidResolverArgumentValueError(f"Invalid authentication method: {auth_type}")
                
                if auth_type == 'BASIC':
                    if not "user" in args.keys and not "password" in args.keys:
                        raise InvalidResolverArgumentValueError(f"{auth_type} authentication requires: user and password parameters")
                        
                    user = args.get("user")
                    password = args.get("password")    
                    
        if not checkers.is_url(url):
            raise InvalidResolverArgumentValueError(f"Invalid argument: {url}")
        
        
        response = self._make_request(url, auth_type=auth_type, user=user, password=password)
        
        return response
