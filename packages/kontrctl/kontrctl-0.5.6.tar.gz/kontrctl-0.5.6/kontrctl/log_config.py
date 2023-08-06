"""
Logging configuration module
"""

from logging.config import dictConfig

FORMATTERS = {
    'verbose': {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },

    'simple': {
        'format': '%(levelname)s %(message)s'
    },
    'colored_console': {
        '()': 'coloredlogs.ColoredFormatter',
        'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 'datefmt': '%H:%M:%S'
    },

}

HANDLERS = {
    'console': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'colored_console'
    },
}

LOGGERS = {
    'tests': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
    'kontrctl': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
    'kontr_api': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
}

LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': FORMATTERS,
    'handlers': HANDLERS,
    'loggers': LOGGERS,
}


def load_logger(conf_type=None):
    """Loads config based on the config type
    Args:
        conf_type(str): Config type available (dev, test, prod)

    """
    if conf_type is not None:
        print("Not implemented yet!")
    dictConfig(LOGGING_CONF)
