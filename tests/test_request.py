# -*- coding: utf-8 -*-

import pytest

from unittest.mock import MagicMock, patch
from resolver.request import Request
from resolver.request import InvalidResolverArgumentValueError
from jsonschema import ValidationError

fake_response = '{"fake", "data"}'


class TestRequestResolver:
    resolver = Request(argument=None)

    @pytest.mark.parametrize(
        "arg",
        [(None), (""), ("invalid"), ("foo://acme.org/invalid"), ({"url": "invalid"})],
    )
    def test_resolve_with_invalid_url(self, arg):
        with pytest.raises(InvalidResolverArgumentValueError):
            self.resolver.argument = arg
            self.resolver.resolve()

    @pytest.mark.parametrize(
        "arg",
        [
            ("https://fake-endpoint.org"),
            ({"url": "https://fake-endpoint.org"}),
            (
                {
                    "url": "https://fake-endpoint.org",
                    "auth": "basic",
                    "user": "myuser",
                    "password": "mypwd",
                }
            ),
        ],
    )
    @patch(
        "resolver.request.Request._make_request", MagicMock(return_value=fake_response)
    )
    def test_resolve_with_valid_args(self, arg):
        self.resolver.argument = arg
        response = self.resolver.resolve()
        assert response == fake_response

    @pytest.mark.parametrize(
        "arg",
        [
            ({}),  # url is required
            ({"url": None}),  # url must be a string
            ({"url": "https://fake-endpoint.org", "auth": "invalid"}),  # invalid auth
            (  # basic auth requires user and password
                {"url": "https://fake-endpoint.org", "auth": "basic"}
            ),
            (  # basic auth requires user and password
                {
                    "url": "https://fake-endpoint.org",
                    "auth": "basic",
                    "user": "myuser",
                }
            ),
            (  # basic auth requires user and password
                {
                    "url": "https://fake-endpoint.org",
                    "auth": "basic",
                    "password": "mypasswd",
                }
            ),
        ],
    )
    def test_resolve_with_invalid_schema_rules(self, arg):
        with pytest.raises(ValidationError):
            self.resolver.argument = arg
            self.resolver.resolve()
