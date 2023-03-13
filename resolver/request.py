# -*- coding: utf-8 -*-

import requests
from validator_collection import checkers

from sceptre.resolvers import Resolver

def make_request(url):
  """
  Make a request to a REST API endpoint
  :param url: The url endpoint reference
  """
  content = None
  try:
    response = requests.get(url)
    content = response.text
    if response.status_code != requests.codes.ok:
      raise response.raise_for_status()
  except requests.exceptions.RequestException as e:
    raise e

  return content

class Request(Resolver):
  """
  Resolve data from a REST API endpoint.
  """

  def __init__(self, *args, **kwargs):
    super(Request, self).__init__(*args, **kwargs)

  def resolve(self):
    """
    This method is invoked by Sceptre

    :returns: Response from the request
    :rtype: str
    """

    arg = self.argument
    if checkers.is_url(arg):
      response = make_request(arg)
    else:
      raise ValueError(f'Invalid argument: {arg}')

    return response
