"""
Creates a custom JSON logger to MySense spec
Usage:
logger.info('This is an info log')
logger.log(99, 'This is a log of an event', extra=dict(event=event))
"""
import os
import sys
import time
import json
import logging
from collections import OrderedDict


class JSONFormatter(logging.Formatter):
    """
    The JSONFormatter class outputs Python log records in JSON format.
    """
    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)
    def format(self, record):
        """
        Overridden from the ancestor class to take
           a log record and output a JSON formatted string.
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        event = record.__dict__.get('event', {})
        log_message = [('level', record.levelno),
                       ('time', time_ms()),
                       ('msg', record.message),
                       ('logStream', os.environ['AWS_LAMBDA_LOG_STREAM_NAME']),
                       ('version', os.environ['VERSION']),
                       ('stage', os.environ['STAGE']),
                       ('service', os.environ['SERVICE']),
                       ('lambdaName', os.environ['AWS_LAMBDA_FUNCTION_NAME']),
                       ('event', event),
                       ('v', 1)]
        return json.dumps(OrderedDict(log_message))


def mysense_logger():
    """
    Sets up a custom mysense JSON logger
    """
    logger = logging.getLogger()
    logger.setLevel('INFO')
    formatter = JSONFormatter('[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(levelno)s\t%(message)s\n',
                              '%Y-%m-%dT%H:%M:%S')
    if logger.handlers == []:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.handlers[0].setFormatter(formatter)
    return logger


def time_ms() -> str:
    """
    Returns the current UNIX time in milliseconds
    """
    return int(time.time() * 1e3)
