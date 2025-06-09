from las_utils import database_utils as dbu
from las_utils import system_utils as sysu
import configparser
import socket
from os import walk
from os.path import join
from pdf2image import pdfinfo_from_path

years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
         '2012', '2021', '2022', '2023', '2024', '2025']


def set_page_count(db_conn, cf_number, file_name, pages):

    sql = 'UPDATE council_document SET page_count = ? WHERE cf_number = ? AND file_name = ?;'
    params = (pages, cf_number, file_name, )
    dbu.execute_sql_params(db_conn, sql, params)


def process_page_count(db_conn, base_path, years):
    """
    Get the page count and set in database
    :param db_conn: Active database connection
    :param base_path: The base path where the documents are stored
    :param years: List of years to process
    :return: None
    """

    for year in years:
        year_path = base_path + '/' + year
        for root, subdirs, files in walk(year_path):
            if not ('13-0516' in root or '13-0318' in root or '13-1122' in root or '13-0343' in root):
                for file in files:
                    file_path = join(root, file)
                    if file_path[-4:].lower() == '.pdf':
                        try:
                            cf_number = root[-7:]
                            info = pdfinfo_from_path(file_path)
                            maxPages = info["Pages"]
                            print(str(maxPages) + ': ' + file)
                            set_page_count(db_conn, cf_number, file, maxPages)
                        except Exception as e:
                            print(e)


if __name__ == "__main__":
    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('config/base.ini')
    config_section = sysu.get_config_section(hostname)
    db_file = config['Locations.{}'.format(config_section)]['db_path']
    documents_base = config['Locations.{}'.format(config_section)]['documents_base']

    db_conn = dbu.create_connection(db_file)

    process_page_count(db_conn, documents_base, years)

    db_conn.commit()
