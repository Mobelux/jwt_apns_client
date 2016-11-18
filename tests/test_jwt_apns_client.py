#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function, division

"""
test_jwt_apns_client
----------------------------------

Tests for `jwt_apns_client` module.
"""


import os
import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

try:
    from unittest import mock
except ImportError:
    import mock

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

    def test_module_constants(self):
        assert 'ES256' == jwt_apns_client.ALGORITHM
        assert 'api.push.apple.com' == jwt_apns_client.PROD_API_HOST
        assert 'api.development.push.apple.com' == jwt_apns_client.DEV_API_HOST
        assert '443' == jwt_apns_client.API_PORT


class AlertTest(unittest.TestCase):

    def test_init_params(self):
        """
        Test that the passed in params set the expected object attributes.
        """
        alert = jwt_apns_client.Alert(title='title', body='body', title_loc_key='title_loc_key',
                                      title_loc_args=[1, 2], action_loc_key='action_loc_key', loc_key='loc_key',
                                      loc_args=[3, 4], launch_image='launch_image.png')
        self.assertEqual('title', alert.title)
        self.assertEqual('body', alert.body)
        self.assertEqual('title_loc_key', alert.title_loc_key)
        self.assertEqual([1, 2], alert.title_loc_args)
        self.assertEqual('action_loc_key', alert.action_loc_key)
        self.assertEqual('loc_key', alert.loc_key)
        self.assertEqual([3, 4], alert.loc_args)
        self.assertEqual('launch_image.png', alert.launch_image)

    def test_get_payload_dict(self):
        """
        A dict of the data in the object should be returned.  Paramters with underscores should be converted
        to hyphens in the dict keys.
        """
        alert = jwt_apns_client.Alert(title='title', body='body', title_loc_key='title_loc_key',
                                      title_loc_args=[1, 2], action_loc_key='action_loc_key', loc_key='loc_key',
                                      loc_args=[3, 4], launch_image='launch_image.png')
        expected = {
            'title': 'title', 'body': 'body', 'title-loc-key': 'title_loc_key', 'title-loc-args': [1, 2],
            'action-loc-key': 'action_loc_key', 'loc-key': 'loc_key', 'loc-args': [3, 4],
            'launch-image': 'launch_image.png'
        }
        self.assertEqual(expected, alert.get_payload_dict())


class NotificationResponseTest(unittest.TestCase):
    def test_init_params(self):
        """
        Test that the passed in params set the expected object attributes.
        """
        notification = jwt_apns_client.NotificationResponse(status=400, reason='reason', host='api.example.org', port=80,
                                                            path='/api/3/device/12345asdf', payload='payload',
                                                            headers={'h': '1'})
        self.assertEqual(400, notification.status)
        self.assertEqual('reason', notification.reason)
        self.assertEqual('api.example.org', notification.host)
        self.assertEqual(80, notification.port)
        self.assertEqual('/api/3/device/12345asdf', notification.path)
        self.assertEqual('payload', notification.payload)
        self.assertEqual({'h': '1'}, notification.headers)

    def test_init_params_default(self):
        """
        Test the default init params
        """
        notification = jwt_apns_client.NotificationResponse()
        self.assertEqual(200, notification.status)
        self.assertEqual('', notification.reason)
        self.assertEqual('', notification.host)
        self.assertEqual(443, notification.port)
        self.assertEqual('', notification.path)
        self.assertEqual(None, notification.payload)
        self.assertEqual(None, notification.headers)


class APNSConnectionTest(unittest.TestCase):
    TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
    FILES_DIR = os.path.join(TESTS_DIR, 'test_files')
    KEY_FILE_PATH = os.path.join(FILES_DIR, 'apns_key.p8')

    def test_init_params(self):
        """
        Test that the passed in params set the expected object attributes.
        """

        expected_secret = (
            '-----BEGIN PRIVATE KEY-----\n'
            'INVALID_FAKE_KEY\n'
            '-----END PRIVATE KEY-----\n'
        )
        connection = jwt_apns_client.APNSConnection(algorithm='HS256',
                                                    team_id='TEAMID',
                                                    apns_key_id='asdf1234',
                                                    apns_key_path=self.KEY_FILE_PATH,
                                                    api_version=2, # not a value we would really want to pass
                                                    environment=jwt_apns_client.APNSEnvironments.PROD,
                                                    api_host='api.example.org',
                                                    api_port=442)
        self.assertEqual('HS256', connection.algorithm)
        self.assertEqual('TEAMID', connection.team_id)
        self.assertEqual('asdf1234', connection.apns_key_id)
        self.assertEqual(self.KEY_FILE_PATH, connection.apns_key_path)
        self.assertEqual(2, connection.api_version)
        self.assertEqual('prod', connection.environment)
        self.assertEqual('api.example.org', connection.api_host)
        self.assertEqual(442, connection.api_port)
        self.assertEqual(expected_secret, connection.secret)
        self.assertEqual(None, connection._conn)

    def test_init_params_default(self):
        """
        Test the default init params
        """
        connection = jwt_apns_client.APNSConnection()
        self.assertEqual('ES256', connection.algorithm)
        self.assertEqual(None, connection.team_id)
        self.assertEqual(None, connection.apns_key_id)
        self.assertEqual(None, connection.apns_key_path)
        self.assertEqual(3, connection.api_version)
        self.assertEqual('dev', connection.environment)
        self.assertEqual('api.development.push.apple.com', connection.api_host)
        self.assertEqual(443, connection.api_port)
        self.assertEqual('', connection.secret)
        self.assertEqual(None, connection._conn)

    def test_send_notification(self):
        pass

    def test_get_token_headers(self):
        pass

    def test_get_secret(self):
        pass

    def test_get_request_token(self):
        pass

    def test_get_request_payload(self):
        pass

    def test_get_request_headers(self):
        pass

    def test_get_payload_data(self):
        pass

    def test_connection_not_cached(self):
        """
        Test that if we do not already have a connection, self.connection creates and returns an HTTPConnection
        """
        pass

    def test_connection_cached(self):
        """
        Test that if we already have a connection, self.connection returns the existing HTTPConnection without
        creating a new one
        """
        pass
