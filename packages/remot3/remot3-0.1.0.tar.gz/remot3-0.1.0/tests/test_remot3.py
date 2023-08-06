#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `remot3` package."""

import pytest
from remot3 import Remot3


class TestRemot3(object):
    def test_get_apiurl(self):
        test_apiurl = 'https://test-apiurl/api'
        r3 = Remot3('', '', '', test_apiurl)
        assert r3.get_apiurl() == test_apiurl

    def test_login(self):
        r3 = Remot3('', '', '')
        status, token, resp = r3.login()
        assert resp['status'] == 'false'

    def test_parse_server_name(self):
        r3 = Remot3('', '', '')
        name = r3.parse_server_name('id=123', r".*id=(?P<id>\d*)")
        assert name == '123'