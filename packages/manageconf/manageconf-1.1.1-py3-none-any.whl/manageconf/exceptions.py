class BotoRequestFailureError(Exception):
    """Raised when a Boto request to SSM fails"""


class RemoteConfigurationJSONDecodeError(Exception):
    """Raised when a Parameter Store item fails to be deserialised"""
