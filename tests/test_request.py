# -*- coding: utf-8 -*-

import pytest

from unittest.mock import MagicMock, patch
from resolver.request import Request
from resolver.request import InvalidResolverArgumentValueError

fake_response = '{"fake", "data"}'


class TestRequestResolver:
    resolver = Request(argument=None)

    @pytest.mark.parametrize(
        "arg, expected",
        [
            (None, InvalidResolverArgumentValueError),
            ("", InvalidResolverArgumentValueError),
            ("invalid", InvalidResolverArgumentValueError),
            ("foo://acme.org/invalid", InvalidResolverArgumentValueError),
        ],
    )
    def test_resolve_with_invalid_args(self, arg, expected):
        with pytest.raises(expected):
            self.resolver.argument = arg
            self.resolver.resolve()

    @patch(
        "resolver.request.Request._make_request", MagicMock(return_value=fake_response)
    )
    def test_resolve_with_valid_arg(self):
        endpoint = "https://fake-endpoint.org"
        self.resolver.argument = endpoint
        response = self.resolver.resolve()
        assert response == fake_response
