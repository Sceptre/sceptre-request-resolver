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
            ({"url": None}),
            ({"url": "invalid"}),
        ],
    )
    def test_resolve_with_invalid_args(self, arg):
        with pytest.raises(InvalidResolverArgumentValueError):
            self.resolver.argument = arg
            self.resolver.resolve()

    @pytest.mark.parametrize(
        "arg",
        [("https://fake-endpoint.org"), ({"url": "https://fake-endpoint.org"})],
    )
    @patch(
        "resolver.request.Request._make_request", MagicMock(return_value=fake_response)
    )
    def test_resolve_with_valid_args(self, arg):
        self.resolver.argument = arg
        response = self.resolver.resolve()
        assert response == fake_response
