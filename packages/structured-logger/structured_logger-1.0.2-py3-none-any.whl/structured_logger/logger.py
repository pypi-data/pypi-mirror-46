import json
import logging
import sys
import traceback


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    @staticmethod
    def prepare_message(message, params):
        obj = params
        obj["message"] = message
        return json.dumps(obj)

    def set_level(self, level):
        self.logger.setLevel(level)

    def debug(self, message, params={}):
        self.logger.debug(self.prepare_message(message, params))

    def info(self, message, params={}):
        self.logger.info(self.prepare_message(message, params))

    def warning(self, message, params={}):
        self.logger.warning(self.prepare_message(message, params))

    def error(self, message, params={}):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        params["errorName"] = repr(exc_type)
        params["errorMessage"] = repr(exc_value)
        params["errorStackTrace"] = traceback.format_exc()
        obj = self.prepare_message(message, params)
        self.logger.error(obj)
