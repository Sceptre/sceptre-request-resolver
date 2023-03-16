# sceptre-request-resolver

A Sceptre resolver to make requests from REST API endpoints.

## Motivation

There are some pretty useful REST API endpoints on the internet.  The endpoints
can return lots of different types of data, typically in JSON format.
This simple resolver can retrieve that data and pass it to Sceptre parameters
or scepter_user_data parameters.

## Installation

To install directly from PyPI
```shell
pip install sceptre-request-resolver
```

To install from this git repo
```shell
pip install git+https://github.com/Sceptre/sceptre-request-resolver.git
```

## Usage/Examples

```yaml
parameters|sceptre_user_data:
  <name>: !request <API ENDPOINT>
```

## Example

Simple request:
```yaml
parameters:
  wisdom: !request 'https://ron-swanson-quotes.herokuapp.com/v2/quotes'
```
__Note__: request returns a string.


Request data and convert the response string to a JSON object:
```yaml
sceptre_user_data:
   hounds: !from_json_string {response}
     response: !request 'https://dog.ceo/api/breed/hound/list'
```
