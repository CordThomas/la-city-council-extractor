from db import *
import requests
import os
import time
from bs4 import BeautifulSoup
from pathlib import Path

docs_base = './documents/'
chunk_size = 2048

# https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module


def retrieve_cf_document(cf_number, path):

    cf_year = '20' + cf_number[:2]
    file_location = docs_base + cf_year + '/' + cf_number
    filename = os.path.basename(path)
    Path(file_location).mkdir(parents=True, exist_ok=True)

    download_success = False
    attempt_count = 0

    while not download_success and attempt_count < 5:
        try:
            r = requests.get(path, stream=True, timeout=(5, 15))
            with open(file_location + '/' + filename, 'wb') as fd:
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)
            download_success = True
        except requests.exceptions.ConnectionError:
            print('***** Failed to connect {}'.format(path))
        except requests.exceptions.Timeout:
            print('***** Timed out {}'.format(path))
            attempt_count += 1
            time.sleep(5)
        except Exception as exc:
            print(exc)


def process_cf_document(soup, conn, cf_number):

    activity_div = soup.find('div', attrs={'style': 'overflow:auto; height:102px;'})
    if activity_div is not None:
        table_rows = activity_div.findChildren('tr')
        if table_rows is not None:
            table_row_idx = 0
            for table_row in table_rows:
                post_date = ''
                title = ''
                document_file_path = ''
                if table_row_idx > 0:
                    table_cells = table_row.findChildren('td')
                    table_hrefs = table_cells[0].findChildren('a')
                    document_path = table_hrefs[0]['href']
                    title = table_cells[0].text.strip()
                    post_date = table_cells[1].text.strip()

                    retrieve_cf_document(cf_number, document_path)
                    print('Date: {} for title {} with path {}'.format(post_date, title, document_path))

                    file_name = os.path.basename(document_path)
                    insert_new_council_document(conn, cf_number, post_date, title, file_name)
                table_row_idx += 1