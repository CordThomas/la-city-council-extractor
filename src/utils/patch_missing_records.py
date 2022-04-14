from bs4 import BeautifulSoup
import requests
import urllib3
from src.scrape_cf_votes import *

cf_url_base = 'https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber={}'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

missing_council_files = ['10-1806', '19-1600', '19-1601', '19-1602', '19-1603',
                         '19-1604', '19-1605', '19-1606', '19-1608', '19-1609',
                         '19-1610', '19-1611', '19-1612', '19-1613', '19-1614', '19-1615',
                         '19-1616', '19-1618', '22-0271', '22-0274']

missing_council_files = ['05-2714', '06-0080', '06-3114', '07-1271', '08-1824']


def patch_missing_cfs(db_conn, url_base, missing_cfs):

    for missing_cf in missing_cfs:
        cf_url = url_base.format(missing_cf)
        print('Processing: {}'.format(cf_url))
        html_text = requests.get(cf_url, verify=False).text
        soup = BeautifulSoup(html_text, 'html.parser')
        insert_new_council_file(db_conn, missing_cf)
        # process_cf_votes(soup, db_conn, missing_cf, True)


def patch(url_base, missing_cfs):

    db_file = '../../data/city-council.db'
    db_conn = create_connection(db_file)
    patch_missing_cfs(db_conn, url_base, missing_cfs)
    db_conn.close()


if __name__ == "__main__":

    patch(cf_url_base, missing_council_files)