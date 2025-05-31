from utils.db import *
from las_utils import database_utils as dbu
from las_utils import system_utils as sysu
import configparser
import os
import socket

def load_document_list(db_conn):

    sql = 'SELECT "20" || SUBSTRING(cf_number, 1, 2), cf_number, file_name, cd.cf_document_id ' \
          'FROM council_document cd ' \
          'LEFT OUTER JOIN council_document_text ct ' \
          '  ON cd.cf_document_id = ct.cf_document_id ' \
          'WHERE LOWER(title) IN ("council action", "motion", "speaker card(s)", "communication(s) from public", ' \
          '"communication from public") or LOWER(title) LIKE "community impact statement submitted by%" ' \
          'AND ct.cf_document_id IS NULL;'

    document_list = []
    documents = dbu.select(db_conn, sql)
    for document in documents:
        doc_path = document[0] + '/' + document[1] + '/' + document[2]
        document_entry = {'doc_id': document[3], 'doc_path': doc_path}
        document_list.append(document_entry)

    return document_list


def insert_document_text(db_conn, cf_document_id, text):

    sql = 'INSERT INTO council_document_text (cf_document_id, cf_document_text) VALUES (?, ?)'
    params = (cf_document_id, text, )
    dbu.execute_sql_params(db_conn, sql, params)


def load_documents(db_conn, document_list, base_path):

    for document in document_list:
        document_path = document['doc_path'][:-4] + '.txt'
        if os.path.exists(base_path + '/' + document_path):
            document_id = document['doc_id']
            with open(base_path + '/' + document_path, 'r') as f:
                f_text = f.read()
                insert_document_text(db_conn, document_id, f_text)


def main():
    """
    Load the te
    """
    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('config/base.ini')
    config_section = sysu.get_config_section(hostname)
    print(config_section)
    print(config['Locations.{}'.format(config_section)])
    db_file = config['Locations.{}'.format(config_section)]['db_path']
    documents_base = config['Locations.{}'.format(config_section)]['documents_base']

    db_conn = create_connection(db_file)
    documents_to_load = load_document_list(db_conn)
    load_documents(db_conn, documents_to_load, documents_base)
    db_conn.commit()


if __name__ == '__main__':
    main()
