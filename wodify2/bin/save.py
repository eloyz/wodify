import codecs
import csv
import glob
import logging
import os
import re
from sqlite3 import ProgrammingError
import uuid
import xlrd
from collections import namedtuple
from datetime import datetime, date
from os import getcwd, listdir

import click

from ..utils import connect_db, configure_log

logger = logging.getLogger(__name__)
date_mode = None


def get_1rep_max(weight, reps=1):
    """Reduces weight and rep combination
    to 1-rep-max weight.
    """
    return int(weight * (reps-1) * .033 + weight)

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
    # This decodes to unicode and ignores the funny characters
    # It then encodes them to bytes/str in order to go to the database
    name = unicode(name, errors='ignore').encode('utf-8')

    weight_id = uuid.uuid5(uuid.NAMESPACE_URL, name)

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

def to_machine_label(l):

    new_list = []
    for i in l:
        i = i.lower()
        i = i.replace(' ', '_')
        i = i.replace('(', '_')
        i = i.replace(')', '')
        new_list.append(i)

    return new_list

@click.command()
@click.option('--csv-file', default='.', help='CSV file to save to database', show_default=True)
@click.option('--log-level', default='INFO', help='Logging level', show_default=True)
def main(log_level, csv_file):
    """Merge downloaded files. 
    Files are converted from an XLSX to a CSV.
    """
    excel_date_mode = 0
    configure_log(log_level)

    Weight = namedtuple('Weight', ['name', 'weight_name', 'sets', 'reps', 'weight', 'max_weight', 'accomplished_on'])

    with open(csv_file, 'rb') as f:
        csv_reader = csv.reader(f)

        header_row = csv_reader.next()
        CSVFile = namedtuple('CSV', to_machine_label(header_row))

        for row in csv_reader:

            csv_file = CSVFile(*row)

            name = csv_file.name
            accomplished_on = datetime(*xlrd.xldate_as_tuple(float(csv_file.date), excel_date_mode))
            result = csv_file.formatted_result
            weight_name = csv_file.name_21

            try:
                sets, reps, weight = re.search('(\d*) x (\d*) @ (\d*)', result).groups()
            except AttributeError:
                logger.warning('Pattern "sets x reps @ weight" not found --> %s', result)

            max_weight = get_1rep_max(int(weight), int(reps))

            weight_object = Weight(
                name=name,
                weight_name=weight_name,
                sets=sets,
                reps=reps,
                weight=weight,
                max_weight=max_weight,
                accomplished_on=accomplished_on)

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



