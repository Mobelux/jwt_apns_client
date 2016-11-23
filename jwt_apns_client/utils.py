# -*- coding: utf-8 -*-
"""
jwt_apns_client/utils

General utility classes and functions
"""
from __future__ import absolute_import, unicode_literals, print_function, division

import jwt
import time


class APNSReasons(object):
    """
    Constants for the various reason strings returned by APNs on error.

    This is not currently an exhaustive list, this is just the ones we currently care about for handling
    """
    # 400
    BAD_COLLAPSE_ID = 'BadCollapseId'
    BAD_DEVICE_TOKEN = 'BadDeviceToken'
    BAD_EXPIRATION_DATE = 'BadExpirationDate'
    BAD_MESSAGE_ID = 'BadMessageId'
    BAD_PRIORITY = 'BadPriority'
    BAD_TOPIC = 'BadTopic'
    DEVICE_TOKEN_NOT_FOR_TOPIC = 'DeviceTokenNotForTopic'
    DUPLICATE_HEADERs = 'DuplicateHeaders'
    IDLE_TIMEOUT = u'IdleTimeout'
    MISSING_DEVICE_TOKEN = 'MissingDeviceToken'
    MISSING_TOPIC = 'MissingTopic'
    PAYLOAD_EMPTY = 'PayloadEmpty'
    TOPIC_DISALLOWED = 'TopicDisallowed'

    # 403
    BAD_CERTIFICATE = 'BadCertificate'
    BAD_CERT_ENVIRONMENT = 'BadCertificateEnvironment'
    EXPIRED_PROVIDER_TOKEN = 'ExpiredProviderToken'
    FORBIDDEN = 'Forbidden'
    INVALID_PROVIDER_TOKEN = 'InvalidProviderToken'
    MISSING_PROVIDER_TOKEN = 'MissingProviderToken'

    # 404
    BAD_PATH = 'BadPath'

    # 405
    METHOD_NOT_ALLOWED = 'MethodNotAllowed'

    # 410
    UNREGISTERED = 'Unregistered'

    # 413
    PAYLOAD_TOO_LARGE = 'PayloadTooLarge'

    # 429
    PROVIDER_TOKEN_UPDATES = 'TooManyProviderTokenUpdates'
    TOO_MANY_REQUESTS = 'TooManyRequests'

    # 500
    INTERNAL_SERVER_ERROR = 'InternalServerError'

    # 502
    SERVICE_UNAVAILABLE = 'ServiceUnavailable'

    # 503
    SHUTDOWN = 'Shutdown'


def make_provider_token(issuer, secret, issued_at=None, headers=None):
    """
    Build the jwt token for the connection.

    Apple returns an error if the provider token is updated too often, so we don't want to constantly build
    new ones.

    :param issuer: The issuer to use for the jwt token
    :param issued_at: Time as unix epoch the token was issued at.  Defaults to time.time().
    :param headers: The jwt headers to use as a dict.  Includes the algorithm and key id.
    :param algorithm: The hashing algorithm used.  Should be the same as used in the headers.  If not specified
        then the value will be taken from `headers['alg']`
    :returns: JWT encoded token
    """
    issued_at = issued_at or time.time()
    headers = headers if headers is not None else {}
    algorithm = headers['alg']

    token = jwt.encode(
        {
            'iss': issuer,
            'iat': issued_at
        },
        secret,
        algorithm=algorithm,
        headers=headers
    )
    return token
