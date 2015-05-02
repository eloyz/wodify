import codecs
import csv
import glob
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

logger = logging.getLogger(__name__)
date_mode = None


def get_1rep_max(weight, reps=1):
    """Reduces weight and rep combination
    to 1-rep-max weight.
    """
    return int(weight * (reps-1) * .033 + weight)


def read_excel(file_path):
    """Returns a list of row values

    param: str file_path: Path to file

    :returns: list of rows
    :rtype: generator
    """
    wb = xlrd.open_workbook(file_path)

    # Set date mode as a global variable
    # This variable is used in a separate function
    global date_mode
    date_mode = wb.datemode

    logger.info('%s %s', type(date_mode), date_mode)

    sheet1 = wb.sheet_by_name('Sheet1')

    for rownum in xrange(sheet1.nrows):
        row = [unicode(c).encode('utf8') for c in sheet1.row_values(rownum)]
        yield row

@click.command()
@click.option('--log-level', default='INFO', help='Logging level', show_default=True)
@click.option('-dd --download-directory', default='.', help='Directory with downloaded files', show_default=True)
@click.option('-mf --merged-file', default='merged-filed.csv', help='Path of merged file', show_default=True)
def main(log_level, download_directory, merged_file):
    """Merge downloaded files. 
    Files are converted from an XLSX to a CSV.

    Example use:
        wodify-merge -dd ~/Downloads/ -mf boom.csv
        cat ~/Downloads/*.xls | wodify-merge > boom.csv

    """
    configure_log(log_level)

    # Create our new file
    f = open(os.path.join(merged_file), 'wb')
    csv_writer = csv.writer(f)

    # Expand the tilde symbol if it exists
    download_directory = os.path.expanduser(download_directory)

    # Get list of files we're merging
    path = os.path.join(download_directory, 'PerformanceResult*.xlsx')
    glob_list = glob.iglob(path)

    logger.debug('path %s', glob_list)

    for file_index, file_path in enumerate(sorted(glob_list, key=os.path.getmtime)):

        logger.info(file_path)

        rows = read_excel(file_path)
        for row_index, row in enumerate(rows):

            # Write all rows (including header row)
            if file_index == 0:
                csv_writer.writerow(row)

            # Write only data rows
            if file_index > 0:
                if row_index > 0:
                    csv_writer.writerow(row)

    f.close()
