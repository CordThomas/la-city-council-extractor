from las_utils import database_utils as dbu
from las_utils import system_utils as sysu
import argparse
import configparser
import os
from os.path import isdir, join
import socket
import sys


def load_document_list(db_conn, year):
    """
    Load a list of documents that have been loaded so we know what to process.
    :param db_conn: Active database connection
    :param year: Year to load documents for
    :return: list of documents that have been loaded to the council_document table.
    """

    sql = 'SELECT file_name ' \
          'FROM council_document ' \
          'WHERE cf_number LIKE ?;'

    document_list = []
    documents = dbu.select_params(db_conn, sql, [year, ])
    for document in documents:
        document_list.append(document[0])

    return document_list


def insert_document_text(db_conn, cf_document_id, text):

    sql = 'INSERT INTO council_document_text (cf_document_id, cf_document_text) VALUES (?, ?)'
    params = (cf_document_id, text, )
    dbu.execute_sql_params(db_conn, sql, params)


def process_documents(db_conn, document_list, base_path, year):
    """

    :param db_conn:
    :param document_list:
    :param base_path:
    :param year:
    :return:
    """
    for root, subdirs, files in os.walk(join(base_path, '20' + str(year))):
        for file in files:
            file_path = join(root, file)
            print(file_path)

            cf_number = root.split('/')[-1]
            print (cf_number + '   ' + file)
            if file not in document_list:

                if pathlib.Path(file_path).suffix.lower() == '.pdf':
                    insert_new_council_document(db_conn, cf_number, '',
                                                title, file_name)

                if pathlib.Path(file_path).suffix.lower() == '.txt':
                    with open(file_path, 'r') as f:
                        f_text = f.read()
                        cf_document_id = file_path.split('/')[-1].split('.')[0]
                        insert_document_text(db_conn, cf_document_id, f_text)


def main(args):
    """
    Identify council files that have alrady been processed for a given year, then loop
    over the directory of documents for that year and if it's not already been processed, then
    process it.
    """
    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('config/base.ini')
    config_section = sysu.get_config_section(hostname)
    print(config_section)
    print(config['Locations.{}'.format(config_section)])
    db_file = config['Locations.{}'.format(config_section)]['db_path']
    documents_base = config['Locations.{}'.format(config_section)]['documents_base']

    db_conn = dbu.create_connection(db_file)
    documents_already_loaded = load_document_list(db_conn, args.year)
    process_documents(db_conn, documents_already_loaded, documents_base, args.year)
    db_conn.commit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Enter the year to process, 2 digits')
    parser.add_argument('--year', dest='year', type=str, help='Year to process')
    args = parser.parse_args()
    main(args)
