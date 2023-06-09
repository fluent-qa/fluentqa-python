from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import object  # noqa: F401

import logging
import logging.config
from io import IOBase

import settings


DEBUG_A = 9
DEBUG_B = 8
DEBUG_C = 7
logging.addLevelName(DEBUG_A, "DEBUG_A")
logging.addLevelName(DEBUG_B, "DEBUG_B")
logging.addLevelName(DEBUG_C, "DEBUG_C")


def get_logger(name, *args):
    return logging.getLogger('.'.join(['pytui', name] + list(args)))


class LogWriter(IOBase):
    def __init__(self, logger):
        self.logger = logger
        self._data = []

    def write(self, message):
        # self.logger.debug('STDOUT: (%s)\n', message.strip('\n'))
        self._data.append(message)


def configure(filename, debug):
    logging_dict = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'process': {
                'format':
                    '%(created)f %(msecs)25.19f %(name)-25s  %(levelname)-7s  %(message)s',
            }
        },
        'handlers': {
            'default': {
                'class': 'logging.NullHandler'
            },
            'logfile': {
                'class': 'logging.FileHandler',
                'formatter': 'process',
                'filename': filename,
                'mode': 'w+',
            }
        },
        'loggers': {
            'pytui': {
                'handlers': ['logfile'],
                'level': 'DEBUG' if debug else 'INFO',
            },
            'pytui.runner.pipe': {
                'level': 'INFO',
            },
            'pytui.runner.stdout': {
                'level': 'INFO',
            },
            'pytui.runner.stderr': {
                'level': 'INFO',
            },
        },
        'root': {
            'handlers': ['default'],
            'level': 'CRITICAL',
        }
    }

    for module in settings.DEBUG_MODULES:
        logging_dict['loggers'].setdefault(module, {})
        logging_dict['loggers'][module]['level'] = 'DEBUG'
        # logging_dict['loggers'][module]['handlers'] = ['logfile']
        # logging_dict['loggers'][module]['propagate'] = False

    logging.config.dictConfig(logging_dict)
