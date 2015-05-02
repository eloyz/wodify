import logging
from datetime import datetime, date

import click
from selenium.webdriver.common.keys import Keys

from ..utils import get_driver, configure_log
from ..settings import DRIVER_PATH


logger = logging.getLogger(__name__)


@click.command()
@click.option('--logging', default='INFO', help='Logging level', show_default=True)
def main(logging):
    """Download weight lifting information
    """
    from ..base import WeightDownload

    configure_log(logging)
    driver = get_driver(DRIVER_PATH)

    try:
        weight_download = WeightDownload(driver)
        weight_download.run()
    except KeyboardInterrupt:
        driver.close()
    except Exception:
        # driver.close()
        raise
