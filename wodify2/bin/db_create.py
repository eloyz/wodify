import os
import logging
from datetime import datetime, date
from contextlib import closing

import click

from .. import settings
from ..utils import connect_db, configure_log


logger = logging.getLogger(__name__)


@click.command()
def main():
    """Creates the database tables.
    Not idompotent, will delete existing database tables.
    """
    with closing(connect_db()) as db:
        with open(settings.SCHEMAFILE, 'rb') as f:
            db.cursor().executescript(f.read())
        db.commit()
