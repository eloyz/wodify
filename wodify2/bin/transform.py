import codecs
import csv
import logging
import os
import re
import uuid
import xlrd
from collections import namedtuple
from datetime import datetime, date
from os import getcwd, listdir

import click

from ..utils import connect_db, configure_log


configure_log('INFO')
logger = logging.getLogger(__name__)
date_mode = None


def get_1rep_max(weight, reps=1):
    """Reduces weight and rep combination
    to 1-rep-max weight.
    """
    return int(weight * (reps-1) * .033 + weight)


def read_excel(file_path):
    """Returns a generator which can
    be looped through to get the rows
    of the file.
    """
    wb = xlrd.open_workbook(file_path)

    global date_mode
    date_mode = wb.datemode

    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open('{}.csv'.format(os.path.splitext(file_path)[0]), 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(1, sh.nrows):
        yield sh.row_values(rownum)


def save_athlete(name):
    """Save athlete in database
    """
    athlete_id = uuid.uuid5(uuid.NAMESPACE_URL, unicode(name).encode('utf-8'))

    sql_query = """
        INSERT INTO athlete
        (id, name)
        VALUES (?, ?)"""

    db = connect_db()

    db.execute(sql_query, [unicode(athlete_id), name])
    db.commit()

    if db is not None:
        db.close()

    return athlete_id


def save_weight(name):
    """Save weight in database
    """
    weight_id = uuid.uuid5(uuid.NAMESPACE_URL, unicode(name).encode('utf-8'))
    sql_query = """
        INSERT INTO weight
        (id, name)
        VALUES (?, ?)"""

    db = connect_db()
    db.execute(sql_query, [unicode(weight_id), name])
    db.commit()

    if db is not None:
        db.close()

    return weight_id


def save_record(params):
    """Save weight in database
    """
    sql_query = """
        INSERT INTO record
        (athlete_id, weight_id, sets, reps, weight, max_weight, accomplished_on)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""

    db = connect_db()
    db.execute(sql_query, params)
    db.commit()

    if db is not None:
        db.close()




@click.command()
@click.option('--logging', default='INFO', help='Logging level', show_default=True)
def main(logging):
    """Download weight lifting information
    """

    Weight = namedtuple('Weight', ['name', 'weight_name', 'sets', 'reps', 'weight', 'max_weight', 'accomplished_on'])

    for file_path in listdir(getcwd()):
        if file_path.endswith('.xlsx'):
            rows = read_excel(file_path)

            for row in rows:

                name = row[0]
                accomplished_on = datetime(*xlrd.xldate_as_tuple(row[4], date_mode))
                result = row[17]
                weight_name = row[20]

                try:
                    sets, reps, weight = re.search('(\d*) x (\d*) @ (\d*)', result).groups()
                except AttributeError:
                    logger.info('Pattern "sets x reps @ weight" not found --> %s', result)

                max_weight = get_1rep_max(int(weight), int(reps))

                weight_object = Weight(
                    name=name,
                    weight_name=weight_name,
                    sets=sets,
                    reps=reps,
                    weight=weight,
                    max_weight=max_weight,
                    accomplished_on=accomplished_on)

                logger.debug(weight_object)

                athlete_id = save_athlete(name)
                weight_id = save_weight(weight_name)

                save_record([
                    unicode(athlete_id),
                    unicode(weight_id),
                    sets,
                    reps,
                    weight,
                    max_weight,
                    accomplished_on])


