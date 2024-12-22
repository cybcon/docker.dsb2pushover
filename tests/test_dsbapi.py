# -*- coding: utf-8 -*-
import dsbapi
from packaging import version


def test_dsbapi_version():
    expected_result = "0.0.14"
    result = version.parse(dsbapi.__version__)

    assert result == expected_result
