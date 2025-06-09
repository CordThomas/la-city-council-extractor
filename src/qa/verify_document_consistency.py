"""
This script verifies the following:
- council_document table has a record for every document downloaded from the council file system
- there is a PDF document for every record in the council_document table
- there is a txt document for every record in the council_document table
- we start with what we know - that if there is a record in council_document_text
  then there must have been a PDF and txt.

"""
import configparser
import socket

from las_utils import system_utils as sysu
from utils.db import *



def main():

    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('config/base.ini')
    config_section = sysu.get_config_section(hostname)
    db_file = config['Locations.{}'.format(config_section)]['db_path']

    db_conn = create_connection(db_file)

    cf_url_base = 'https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber='
    cf_item_pattern = '{year}-{item}'
    process_cf_records(db_conn, cf_url_base, cf_item_pattern)

    db_conn.close()


if __name__ == "__main__":
    main()
