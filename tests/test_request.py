# -*- coding: utf-8 -*-

import pytest

from unittest.mock import MagicMock, patch
from resolver.request import Request
from resolver.request import InvalidResolverArgumentValueError

fake_response = '{"fake", "data"}'


class TestRequestResolver:
    resolver = Request(argument=None)

    @pytest.mark.parametrize(
        "arg",
        [
            (None),
            (""),
            ("invalid"),
            ("foo://acme.org/invalid"),
        ],
    )
    def test_resolve_with_invalid_args(self, arg):
        with pytest.raises(InvalidResolverArgumentValueError):
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
