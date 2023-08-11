#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Scrape the Los Angeles City Council council file and voting history.
   This version starts from the year that is 2 years from this
   year (if 2022, then 2020)and checks each
   council file record for whether the Last Changed Date is greater
   than the date_last_changed in the database record.
"""
from bs4 import BeautifulSoup
import urllib3
import datetime

from scrape_cf_file import *
from scrape_cf_votes import *
from scrape_cf_activity import *
from scrape_cf_documents import *
from utils.db import *

# tell urllib to ignore SSL warnings - another approach would be to
# setup your python environment to trust the SSL certificate of the target website
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
db_file = '../data/city-council.db'


def process_cf_record(conn, cf_number, cf_url, meta_words):

    download_success = False
    attempt_count = 0
    empty_cf_page = 0
    erl = 0

    while not download_success and attempt_count < 5:

        try:
            html_text = requests.get(cf_url, verify=False, timeout=(5, 15)).text
            erl = 1
            soup = BeautifulSoup(html_text, 'html.parser')
            erl = 2
            for linebreak in soup.find_all('br'):
                linebreak.extract()

            insert_new_council_file(conn, cf_number)
            empty_cf_page, is_update = process_cf_council_file(soup, meta_words, conn, cf_number)
            erl = 3
            if empty_cf_page != 0:
                return empty_cf_page
            elif is_update in ['new', 'update']:
                process_cf_votes(soup, conn, cf_number, True)
                erl = 4
                process_cf_activity(soup, conn, cf_number)
                erl = 5
                process_cf_document(soup, conn, cf_number)
                erl = 6

            download_success = True

        except requests.exceptions.ConnectionError:
            print('***** Failed to connect {}'.format(cf_url))
            attempt_count += 1
            time.sleep(5)
        except requests.exceptions.Timeout:
            print('***** Timed out {}'.format(cf_url))
            attempt_count += 1
            time.sleep(5)
        except Exception as exc:
            print(exc)
            print('  At line {}'.format(str(erl)))
            break

    return empty_cf_page


def process_cf_records(conn, cf_url_base, cf_item_pattern):
    """ Loop over the collection of years of interest (we started in 2010 but this
    script starts 1 year ago from this year)
    and the number of council file records (varies considerably
    from year to year with nearly 2,200 in 2012 to only 1,400 in other years).
    Relies on BeautifulSoup to parse the HTML and extract data to insert into
    a SQLite database.

    Note:  The online database starts in 1990.  It looks like there was a change in
    structure from 2008 to 2009, maybe when the system was upgraded or migrated.
    Prior to 2009, there was a Subject field that included a summary of the file
    and the list of file activities at the bottom of the page is a simple text
    list vs the list of files and links.

    :param conn:  Active database connection
    :param cf_url_base:  The base URL for the council file data page
    :param cf_item_pattern:  The year-file pattern compiled in this method to complete the URL
    """
    meta_words = []
    this_year = datetime.date.today().year
    first_year = this_year
    begin_processing = True
    for year in range(first_year, this_year + 1):
        empty_cf_pages = 0
        for cf in range(5000):
            cf_number = cf_item_pattern.format(year=str(year)[2:].zfill(2), item=str(cf).zfill(4))
            cf_url = cf_url_base + cf_number
            # if str(year) == '2022' and str(cf) == '273':
            #     begin_processing = True
            if begin_processing:
                print(cf_url)
                empty_cf_pages += process_cf_record(conn, cf_number, cf_url, meta_words)

            # If we have found more than 20 consecutive empty pages, break for the year, outer loop
            if empty_cf_pages >= 20:
                break

    # This bit should be pulled out into a separate method - it's part of
    # a pre-stage process to identify all the council file summary labels
    for meta_word in meta_words:
        print(meta_word)


def main():
    """ Entry point for processing the LA City Clerk's Council File
    Management System which presents a single page for each council file.  This
    script currently just scrapes the summary information of the file and the
    voting results for files that have been acted on.   Other information
    includes the collection of documents including the original motion, city
    agency reports, community impact statements and communications from the public.
    The CFMS also includes topics that are more administrative such as the council
    recess schedule, the state and federal legislative program, and Commendatory
    Resolutions.
    """
    db_conn = create_connection(db_file)

    cf_url_base = 'https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber='
    cf_item_pattern = '{year}-{item}'
    process_cf_records(db_conn, cf_url_base, cf_item_pattern)

    db_conn.close()

if __name__ == "__main__":
    main()