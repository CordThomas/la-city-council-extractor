"""
Utility script written to extrude the council_district IDs from the council_file
table into a many:many bridge table. The format in the council file system
allows for having multiple council districts associated with a single council file
such as 1,3,5,9,11,15. This script will find those and create 6 records in the
council_file_district table
"""
import configparser
import socket
from las_utils.database_utils import *
from las_utils import system_utils as sysu


def update_data(db_conn):

    sql = 'SELECT cf_number, council_district ' \
          'FROM council_file ' \
          'WHERE council_district IS NOT NULL AND LENGTH(council_district) > 0;'

    sql_insert = 'INSERT INTO council_file_district (cf_number, district_n) VALUES (?, ?)'

    cf_districts = {}
    records = select(db_conn, sql)
    for record in records:
        cf_districts[record[0]] = record[1]

    for cf, districts in cf_districts.items():
        district_list = str(districts).split(',')
        for district in district_list:
            values = (cf, district, )
            execute_sql_params(db_conn, sql_insert, values)


def main():
    """ Process the records
    """
    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('config/base.ini')
    config_section = sysu.get_config_section(hostname)
    db_file = config['Locations.{}'.format(config_section)]['db_path']

    db_conn = create_connection(db_file)

    update_data(db_conn)

    db_conn.commit()
    db_conn.close()


if __name__ == "__main__":
    main()