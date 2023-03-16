# -*- coding: utf-8 -*-

import requests
from validator_collection import checkers

from sceptre.resolvers import Resolver


class Request(Resolver):
    """
    Resolve data from a REST API endpoint.
    """

    def _make_request(self, url):
        """
        Make a request to a REST API endpoint
        :param url: The url endpoint reference
        """
        content = None
        try:
            response = requests.get(url)
            content = response.text
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err
        except requests.exceptions.RequestException as e:
            raise e

        return content

    def resolve(self):
        """
        This method is invoked by Sceptre

        :returns: Response from the request
        :rtype: str
        """

        arg = self.argument
        if checkers.is_url(arg):
            response = self._make_request(arg)
        else:
            raise ValueError(f"Invalid argument: {arg}")

        return response
