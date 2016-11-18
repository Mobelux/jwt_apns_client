# -*- coding: utf-8 -*-
"""
jwt_apns_client/utils

General utility classes and functions
"""
from __future__ import absolute_import, unicode_literals, print_function, division


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
