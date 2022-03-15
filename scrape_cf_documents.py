from db import *
import requests
import os
from bs4 import BeautifulSoup
from pathlib import Path

docs_base = './documents/'
chunk_size = 2048

def retrieve_cf_document(cf_number, path):

    r = requests.get(path, stream=True)

    cf_year = '20' + cf_number[:2]
    filename=os.path.basename(path)
    Path(docs_base + cf_year + '/' + cf_number).mkdir(parents=True, exist_ok=True)

    with open(docs_base + cf_year + '/' + cf_number + '/' + filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


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