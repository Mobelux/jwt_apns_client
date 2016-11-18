#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_jwt_apns_client
----------------------------------

Tests for `jwt_apns_client` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from jwt_apns_client import jwt_apns_client
from jwt_apns_client import cli



class TestJwt_apns_client(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'jwt_apns_client.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output