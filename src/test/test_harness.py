from src.utils.db import *
from src.scrape_cf_activity import process_cf_activity
from src.scrape_cf_documents import process_cf_document
from src.scrape_council_files_with_updates import process_cf_record
from bs4 import BeautifulSoup
import requests
import urllib3

cf_url_base = 'https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber={}'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_delete_votes(db_conn, cf_number):
    delete_vote_records(db_conn, cf_number)


def test_process_cf_document(db_conn, cf_number):

    cf_url = cf_url_base.format(cf_number)
    print('Processing: {}'.format(cf_url))
    html_text = requests.get(cf_url, verify=False).text
    soup = BeautifulSoup(html_text, 'html.parser')
    process_cf_document(soup, db_conn, cf_number)


def test_process_cf_activity(db_conn, cf_number):

    cf_url = cf_url_base.format(cf_number)
    print('Processing: {}'.format(cf_url))
    html_text = requests.get(cf_url, verify=False).text
    soup = BeautifulSoup(html_text, 'html.parser')
    process_cf_activity(soup, db_conn, cf_number)


def test_process_cf_file(db_conn, cf_number):

    meta_words = []
    cf_url = cf_url_base.format(cf_number)
    print('Processing: {}'.format(cf_url))
    process_cf_record(db_conn, cf_number, cf_url, meta_words)

def test():

    db_file = '../../data/city-council.db'
    db_conn = create_connection(db_file)
    # test_process_cf_document(db_conn, '12-1168')
    # 21-0093
    test_process_cf_file(db_conn, '21-0000')
    # test_process_cf_activity(db_conn, '10-0102')
    # test_delete_votes(db_conn, '20-1700')
    db_conn.close()


if __name__ == "__main__":

    test()