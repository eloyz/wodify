import os

ROOT = os.path.abspath(os.path.dirname(__file__))

# Chrome driver
DRIVER_PATH = os.path.join(ROOT, 'driver', 'chromedriver')

# Implicitly wait X seconds for DOM to load
SELENIUM_WAIT = 15

# Database files
DATABASE = os.path.join(ROOT, '..', 'wodify.db')
SCHEMAFILE = os.path.join(ROOT, '..', 'sql', 'schema.sql')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s %(levelname)s %(name)s %(lineno)d %(processName)s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'level': 'INFO',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'selenium.webdriver.remote.remote_connection': {
            'level': 'CRITICAL',
            'propagate': False
        }
    }
}

DEBUG = False
EMAIL = None
PASSWORD = None

try:
    import settings_local
except:
    pass