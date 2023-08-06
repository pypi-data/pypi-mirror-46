import logging
import time
import json


class Logger(object):
    levels = {
        'DEBUG': 100,
        'INFO': 200,
        'WARN': 300,
        'ERROR': 400,
    }
    time_format = '%y-%m-%d %H:%M'

    def __init__(self, obj='root', level='DEBUG'):
        self._level = level
        self._levels = Logger.levels
        self._message = obj.__repr__()
        self._message_bak = obj.__str__()
        self._time_format = Logger.time_format

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        if level in self._levels:
            self._level = level
        else:
            raise ValueError

    @property
    def time_fmt(self):
        return self._time_format

    @time_fmt.setter
    def time_fmt(self, fmt):
        self._time_format = fmt

    def time(self):
        self._message += ' ' + time.strftime(self._time_format)
        return self

    def json(self, dictionary):
        self._message += '\n' + json.dumps(dictionary, indent=2, ensure_ascii=False)
        return self

    def message(self, message):
        self._message += '\n' + message.__str__()
        return self

    def print_message(self, message, level):
        if Logger.levels.get(level) >= Logger.levels.get(self._level):
            self._message = level + ': ' + self._message + ' '
        print(self._message,)
        print('\t', message)
        self._message = self._message_bak

    def info(self, message):
        return self.print_message(message, 'INFO')

    def debug(self, message):
        return self.print_message(message, 'DEBUG')

    def warn(self, message):
        return self.print_message(message, 'WARN')

    def error(self, message):
        return self.print_message(message, 'ERROR')
