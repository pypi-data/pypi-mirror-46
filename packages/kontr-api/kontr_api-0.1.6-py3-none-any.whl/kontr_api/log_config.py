"""
Logging configuration module
"""

import logging
from logging.config import dictConfig

FORMATTERS = {
    'verbose': {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },

    'simple': {
        'format': '%(levelname)s %(message)s'
    },
}

HANDLERS = {
    'console': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'verbose'
    },
}

LOGGERS = {
    'tests': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
    'kontr_api': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
}

LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': FORMATTERS,
    'handlers': HANDLERS,
    'loggers': LOGGERS,
}

TRACE_LOG_LVL = 9


def _trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LOG_LVL):
        # Yes, logger takes its '*args' as 'args'.
        self._log(TRACE_LOG_LVL, message, args, **kws)


def add_custom_log_level():
    logging.addLevelName(TRACE_LOG_LVL, 'TRACE')
    logging.Logger.trace = _trace


def load_config(conf_type=None):
    """Loads config based on the config type
    Args:
        conf_type(str): Config type available (dev, test, prod)

    """
    if conf_type is not None:
        print("Not implemented yet!")
    dictConfig(LOGGING_CONF)
    reenable_loggers()


def reenable_loggers():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.disabled = False
