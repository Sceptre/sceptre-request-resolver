# -*- coding: utf-8 -*-

import pytest

from resolver.request import Request

class TestRequestResolver():
    resolver = Request(
        argument=None
    )

    @pytest.mark.parametrize("arg, expected", [
        (None, ValueError),
        ("", ValueError),
        ("invalid", ValueError),
        ("foo://acme.org/invalid", ValueError)
    ])
    def test_resolving_with_invalid_args(self, arg, expected):
        with pytest.raises(ValueError):
            self.resolver.argument = arg
            self.resolver.resolve()

    def test_resolving_with_valid_arg(self):
        endpoint = "https://dog.ceo/api/breed/hound/list"
        self.resolver.argument = endpoint
        response = self.resolver.resolve()
        assert response == '{"message":["afghan","basset","blood","english","ibizan","plott","walker"],' \
                           '"status":"success"}'


