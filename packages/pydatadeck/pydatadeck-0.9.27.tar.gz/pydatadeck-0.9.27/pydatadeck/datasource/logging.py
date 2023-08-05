"""Logging related classes and functions"""

import json
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
from datetime import datetime
from urllib.parse import urlparse

from flask import g, request

class RequestFormatter(logging.Formatter):
    """
    Log record formatter which prepends log messages with timestamp, trace_id,
    HTTP method and request path
    """

    def __init__(self, logFormat=None, timeFormat=None,
                 json_output=False, service_name='Undefined'):
        super(RequestFormatter, self).__init__(logFormat, timeFormat)
        self.json_output = json_output
        self.service_name = service_name

    def format(self, record):
        rec = logging.makeLogRecord(record.__dict__)
        try:
            rec.path = urlparse(request.url).path
            rec.trace_id = g.trace_id if 'trace_id' in g else ''
            rec.method = request.method
            rec.service_name = self.service_name
            rec.user_id = g.user_id if 'user_id' in g else request.headers.get("UID")
        except RuntimeError:
            rec.path = ''
            rec.trace_id = ''
            rec.method = ''
            rec.service_name = ''
            rec.user_id = ''
        return super().format(rec)


class JsonFormatter(RequestFormatter):
    """
    Setting the log output format conforms to the trace log specification
    """
    def __init__(self, service_name='Undefined'):
        log_format = {
            "log_create_time": "%(asctime)s",
            "traceid": "%(trace_id)s",
            "userid": "%(user_id)s",
            "level": "%(levelname)s",
            "service": "%(service_name)s",
            "method": "%(method)s",
            "process": "%(process)d",
            "path": "%(path)s",
            "log": "%(message)s"
        }
        time_format = '%Y-%m-%dT%H:%M:%S.000+00:00'
        super(JsonFormatter, self).__init__(
            json.dumps(log_format), time_format, True, service_name)

    def formatTime(self, record, datefmt=None):
        record_time = datetime.utcfromtimestamp(int(record.created))
        if datefmt:
            return record_time.strftime(datefmt)
        else:
            return record_time.isoformat()

    def formatMessage(self, record):
        # Make message a json valid string
        record.message = json.dumps(record.message).strip('"')
        return self._style.format(record)


def _init_directory(filename):
    dirs_path = os.path.dirname(filename)
    if dirs_path:
        os.makedirs(dirs_path, exist_ok=True)


def _filename_format(filename):
    return datetime.now().strftime(filename)


class MakeFileHandler(RotatingFileHandler):
    """
    Subclass RotatingFileHandler to call init method during initialization
    """
    def __init__(self, filename, mode='a', maxBytes=0,
                 backupCount=0, encoding=None, delay=False):
        filename = _filename_format(filename)
        _init_directory(filename)
        super(MakeFileHandler, self).__init__(filename, mode, maxBytes,
                                              backupCount, encoding, delay)


class TraceLogTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Subclass TimedRotatingFileHandler to call init method during initialization"""
    def __init__(self, filename, when='D', interval=1, backupCount=2,
                 encoding='UTF-8', delay=False, utc=False, atTime=None):
        filename = _filename_format(filename)
        _init_directory(filename)
        super(TraceLogTimedRotatingFileHandler, self).__init__(
            filename, when, interval, backupCount, encoding, delay, utc, atTime)
