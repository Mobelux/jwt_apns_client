# -*- coding: utf-8 -*-
"""
jwt_apns_client/jwt_apns_client

Client for handling HTTP/2 and JWT based connections to Apple's APNs.
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import json
import time

from hyper import HTTPConnection

from .utils import APNSReasons, make_provider_token

ALGORITHM = 'ES256'
PROD_API_HOST = 'api.push.apple.com'
DEV_API_HOST = 'api.development.push.apple.com'
API_PORT = '443'


class APNSEnvironments(object):
    PROD = 'prod'
    DEV = 'dev'


class Alert(object):
    """
    An APNs Alert.  APNs Payloads can take a dict, which will be built from this object
    or just a single string.
    """

    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop('title', None)
        self.body = kwargs.pop('body', None)
        self.title_loc_key = kwargs.pop('title_loc_key', None)
        self.title_loc_args = kwargs.pop('title_loc_args', None)
        self.action_loc_key = kwargs.pop('action_loc_key', None)
        self.loc_key = kwargs.pop('loc_key', None)
        self.loc_args = kwargs.pop('loc_args', None)
        self.launch_image = kwargs.pop('launch_image', None)
        super(Alert, self).__init__(*args, **kwargs)

    def get_payload_dict(self):
        payload = {}
        props = ['title', 'body', 'title_loc_key', 'title_loc_args', 'action_loc_key', 'loc_key', 'loc_args',
                 'launch_image']
        for k in props:
            val = getattr(self, k, None)
            apns_key = k.replace('_', '-')
            if val is not None:
                payload[apns_key] = val
        return payload


class APNSConnection(object):

    def __init__(self, *args, **kwargs):
        """
        params:
            :param algorithm: (str) The algorithm to use for the jwt.  Defaults to ES256.
            :param team_id: (str) The app team id
            :param apns_key_id: (str) The apns key id
            :param apns_key_path: (str) Path to file with the apns auth key
            :param api_version: (int) The API version.  Default is 3
            :param topic: (str) The APNs topic
            :param environment: (str) development or production. Default is development.
            :param api_host: (str) The host for the API.  If not specified then defaults to the standard host for
                the specified environment.
            :param api_port: (int) The port to make the http2 connection on.  Default is 443.
            :param provider_token: (str) The base64 encoded jwt provider token
        """
        self.algorithm = kwargs.pop('algorithm', ALGORITHM)
        self.topic = kwargs.pop('topic', None)
        self.team_id = kwargs.pop('team_id', None)
        self.apns_key_id = kwargs.pop('apns_key_id', None)
        self.apns_key_path = kwargs.pop('apns_key_path', None)
        self.api_version = kwargs.pop('api_version', 3)
        self.secret = self.get_secret()
        self.environment = kwargs.pop('environment', APNSEnvironments.DEV)
        self.api_host = kwargs.pop('api_host',
                                   PROD_API_HOST if self.environment == APNSEnvironments.PROD else DEV_API_HOST)
        self.api_port = kwargs.pop('api_port', 443)
        self.provider_token = kwargs.pop('provider_token', None)

        if not self.provider_token and self.apns_key_id and self.team_id:
            self.provider_token = self.make_provider_token()

        self._conn = None
        super(APNSConnection, self).__init__(*args, **kwargs)

    @property
    def connection(self):
        if not self._conn:
            self._conn = HTTPConnection(host=self.api_host, port=self.api_port)
        return self._conn

    def get_payload_data(self, alert=None, badge=None, sound=None, content=None, category=None, thread=None):
        """
        Builds the payload dict.

        :param alert: May be a `Alert` instance or a string
        :param badge:
        :param sound:
        :param content:
        :param category:
        :param thread:

        :returns: The payload as a dict ready for conversion to json in a request.
        """

        aps_dict = {}
        if alert is not None:
            if hasattr(alert, 'get_payload_dict'):
                aps_dict['alert'] = alert.get_payload_dict()
            else:
                aps_dict['alert'] = alert
        if badge is not None:
            aps_dict['badge'] = badge
        if sound is not None:
            aps_dict['sound'] = sound
        if content is not None:
            aps_dict['content-available'] = content
        if category is not None:
            aps_dict['category'] = category
        if thread is not None:
            aps_dict['thread-id'] = thread

        data = {
            'aps': aps_dict
        }
        return data

    def get_request_headers(self, token=None, topic=None, priority=10, expiration=0):
        """
        See details on topic, expiration, priority values, etc. at
        https://developer.apple.com/library/content/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/CommunicatingwithAPNs.html#//apple_ref/doc/uid/TP40008194-CH11-SW1

        :param token: the jwt token
        :param topic: the message topic
        :param priority (int): the message priority.  10 for immediate, 5 to consider power consumption. Default is 10.
        :param expiration (int): The message expiration.  Default is 0.
        :returns: A dict of the http request headers
        """
        if topic is None:
            topic = self.topic

        if token is None:
            token = self.provider_token

        request_headers = {
            'apns-expiration': u'%s' % expiration,
            'apns-priority': u'%s' % priority,
            'apns-topic': u'%s' % topic,
            'authorization': 'bearer %s' % token.decode('ascii')
        }

        return request_headers

    def get_request_payload(self, alert=None, badge=None, sound=None, content=None, category=None, thread=None):
        """
        Returns the request payload as utf-8 encoded json

        :param alert: May be a `Alert` instance or a string
        :param badge:
        :param sound:
        :param content:
        :param category:
        :param thread:
        :returns: The JSON encoded request payload
        """
        data = self.get_payload_data(alert, badge, sound, content, category, thread)
        return json.dumps(data).encode('utf-8')

    def make_provider_token(self, issuer=None, issued_at=None, algorithm=None, secret=None, headers=None):
        """
        Build the jwt token for the connection.

        Apple returns an error if the provider token is updated too often, so we don't want to constantly build
        new ones.

        :returns: JWT encoded token
        """
        issuer = issuer or self.team_id
        issued_at = issued_at or time.time()
        algorithm = algorithm or self.algorithm
        secret = secret or self.secret
        headers = headers or self.get_token_headers(algorithm=algorithm)

        return make_provider_token(issuer=issuer, issued_at=issued_at, secret=secret, headers=headers)

    def get_secret(self):
        secret = ''
        if self.apns_key_path:
            with open(self.apns_key_path) as f:
                secret = f.read()
        return secret

    def get_token_headers(self, algorithm=None, apns_key_id=None):
        """
        Build headers for the JWT token

        :returns: Dict of headers for the JWT token
        """
        algorithm = algorithm or self.algorithm
        apns_key_id = apns_key_id or self.apns_key_id

        headers = {
            'alg': algorithm,
            'kid': apns_key_id,
        }

        return headers

    def send_notification(self, device_registration_id, **kwargs):
        """
        Send a push notification using http2.  Creates a new connection or reuses an existing connection
        if possible.

        :param device_registration_id: The registration id of the device to send the notification to
        :param alert: May be a `Alert` instance or a string
        :param badge:
        :param sound:
        :param content:
        :param category:
        :param thread:
        :returns: A :class:`jwt_apns_client.jwt_apns_client.NotificationResponse`
        """
        # TODO: Should we accept ALL params which the various chain of methods accept too allow for full
        # customization on send_notification() call?
        headers = self.get_request_headers()
        payload = self.get_request_payload(**kwargs)
        path = u'/%d/device/%s' % (self.api_version, device_registration_id)

        conn = self.connection
        conn.request(
            'POST',
            path,
            payload,
            headers=headers
        )
        resp = conn.get_response()
        status = resp.status
        reason = ''
        data = resp.read()
        if not status == 200:
            data_dict = json.loads(data)
            reason = data_dict.get('reason', '')

        notification_response = NotificationResponse(status=status, reason=reason, host=conn.host, port=conn.port,
                                                     path=path, payload=payload, headers=headers)

        if reason == APNSReasons.IDLE_TIMEOUT:
            self.close()

        return notification_response

    def close(self, error_code=None):
        """
        Close the HTTP/2 connection with optional error code
        """
        if self._conn:
            self._conn.close(error_code=error_code)
        self._conn = None


class NotificationResponse(object):
    """
    Encapsulate a response to sending a notification using the API.
    """

    def __init__(self, status=200, reason='', host='', port=443, path='', payload=None, headers=None, *args, **kwargs):
        super(NotificationResponse, self).__init__(*args, **kwargs)
        self.status = status
        self.reason = reason
        self.payload = payload
        self.headers = headers
        self.host = host
        self.port = port
        self.path = path
