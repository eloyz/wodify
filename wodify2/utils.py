import logging.config
import sqlite3

from selenium import webdriver
from settings import DATABASE, LOGGING, SELENIUM_WAIT

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    return sqlite3.connect(DATABASE)

def configure_log(level):
    """Configure logging for the application

    :param str level: the level to set logging at
    """
    if level is not None:
        LOGGING['handlers']['console']['level'] = level.upper()
    logging.config.dictConfig(LOGGING)


def get_driver(driver, type='chrome'):
    """Initialize the a web driver

    :param str driver: the path to the driver executable
    :param str type: the type of driver to use
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])

    if type == 'chrome':
        # the webdriver that selenium will use to attach to a browser
        driver = webdriver.Chrome(
            chrome_options=options,
            executable_path=driver
        )

    # wait X seconds for DOM to load
    driver.implicitly_wait(SELENIUM_WAIT)

    return driver
