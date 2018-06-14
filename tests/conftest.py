#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest

@pytest.fixture(scope="session")
def fixture_path():
    pwd = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pwd, 'fixtures')