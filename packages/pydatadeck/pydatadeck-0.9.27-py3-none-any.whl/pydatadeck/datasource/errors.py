"""
Helpers for making Flask error response.
"""
import os
from http import HTTPStatus

from flask import jsonify
from .translation import get_translator

locale_dir = os.path.join(os.path.dirname(__file__), 'locales')

ERROR_PREFIX = 'ERROR_PREFIX'

class ErrorCodes:
    """
    Datasource service error codes,
    """
    INVALID_REQUEST = 'INVALID_REQUEST'
    NOT_AUTHORIZED = 'NOT_AUTHORIZED'
    FETCH_DATA_ERROR = 'FETCH_DATA_ERROR'
    INVALID_FIELD_COMBINATION = 'INVALID_FIELD_COMBINATION'
    THROTTLED = 'THROTTLED'

    """
    For custom error , data source need to provide the localized error message.
    """
    CUSTOM_ERROR = 'CUSTOM_ERROR'

def _error_response(status, code, message, debug_message=None):
    """
    Makes a customized error response.

    Args:
        status (int): HTTP status code
        code (str): error code
        message (str): error message
        debug_message(str): detail error message for debug purpose

    Returns:
        object: Flask json response
    """

    return jsonify({'errorCode': code, 'message': message, 'debugMessage':debug_message}), status


def predefined_error(code, app_display_name, exception_msg, extra_error_msg=None, locale='en_US'):
    """
    Make a predefined error response
    Args:
        code (ErrorCodes): Predefined error code
        app_display_name(str): app name dispayed to user, like Google Analytics
        exception_msg (str): error message used for debug purpose
        extra_error_msg (str): extra error message wants to displayed to user
        locale (str): en_US, ja_JP, zh_CN

    Returns:
        object: Flask json response with localized error message
    """
    _ = get_translator(locale, 'errors', locale_dir)

    error_msg = _(code) if code != ErrorCodes.CUSTOM_ERROR else ""

    if extra_error_msg:
        error_msg = '{}, {}'.format(error_msg, extra_error_msg)

    message = _(ERROR_PREFIX).format(app_display_name=app_display_name)
    if error_msg:
        message += f' Detailed error: {error_msg}'

    return _error_response(HTTPStatus.BAD_REQUEST,
                           code=code, message=message, debug_message=exception_msg)


def custom_error(app_display_name, exception_msg, error_msg, locale='en_US'):
    """
    Make a predefined error response
    Args:
        app_display_name(str): app name dispayed to user, like Google Analytics
        exception_msg (str): error message used for debug purpose
        error_msg (str):  localized error message displayed to user
        locale (str): en_US, ja_JP, zh_CN

    Returns:
        object: Flask json response with localized error message
    """
    return predefined_error(ErrorCodes.CUSTOM_ERROR,
                            app_display_name, exception_msg, error_msg, locale)


class ServiceErrorBase(Exception):
    """
    Base error type

    Attributes:
        inner_exception (exception) -- inner exception
        locale (str): en_US, ja_JP, zh_CN
    """

    def __init__(self, message=None, inner_exception=None, locale='en_US'):
        """
        Creates a new instance.
            message (str, optional): Defaults to None. Error message.
            inner_exception (Exception, optional): Defaults to None.
                Inner exception.
            locale (str, optional): Defaults to 'en_US'. Locale.
        """

        super().__init__(message)
        self.inner_exception = inner_exception
        self.locale = locale


class ServiceBadRequestError(ServiceErrorBase):
    """Error representing a bad request"""


class ServiceAuthError(ServiceErrorBase):
    """Error representing an authorization failure"""


class ServiceFetchDataError(ServiceErrorBase):
    """Error representing data fetching failure"""

class ServiceThrottledError(ServiceErrorBase):
    """Error representing request being throttled by provider"""
