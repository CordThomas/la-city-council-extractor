from bs4 import BeautifulSoup
import bs4
import requests
import urllib3

from scrape_cf_file import *
from scrape_cf_votes import *
from db import *

# tell urllib to ignore SSL warnings - another approach would be to
# setup your python environment to trust the SSL certificate of the target website
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def process_cf_records(conn, cf_url_base, cf_item_pattern):
    """ Loop over the collection of years of interest (we ran from 2010 to
    2021 inclusive) and the number of council file records (varies considerably
    from year to year with nearly 2,200 in 2012 (?) to only 1,400 in other years).
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
    for year in range(10, 22):
        for cf in range(1800):
            cf_number = cf_item_pattern.format(year=str(year), item=str(cf).zfill(4))
            cf_url = cf_url_base + cf_number
            print(cf_url)
            html_text = requests.get(cf_url, verify=False).text
            soup = BeautifulSoup(html_text, 'html.parser')

            for linebreak in soup.find_all('br'):
                linebreak.extract()

            # insert_new_council_file(conn, cf_number)
            process_cf_council_file(soup, meta_words, conn, cf_number)
            # process_cf_votes(soup, conn, cf_number)

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
    db_file = 'data/city-council.db'
    db_conn = create_connection(db_file)

    cf_url_base = 'https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber='
    cf_item_pattern = '{year}-{item}'
    process_cf_records(db_conn, cf_url_base, cf_item_pattern)


if __name__ == "__main__":
    main()