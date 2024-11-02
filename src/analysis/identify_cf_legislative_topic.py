from utils.db import *
from las_utils import database_utils as dbu
from las_utils import system_utils as sysu
import configparser
import socket


def record_legislative_topic_for_cf(db_conn, cf_number, id):
    """
    Insert a record into council_file_legislative_topic for this cf and topic id
    """
    sql = ''' INSERT INTO council_file_legislative_topic(cf_number, topic_id)
              VALUES(?, ?) '''
    dbu.execute_sql_params(db_conn, sql, (cf_number, id, ))


def process_council_file_topics(db_conn, legislative_topics, cf_number, cf_title):
    """
    Check which legislative topics this CF might be about given the terms in the title
    """
    topic_lower = cf_title.lower()
    for topic in legislative_topics:
        id = topic['id']
        term = topic['topic']
        if term.lower() in topic_lower:
            print('Processing {} for {}'.format(term, cf_title))
            record_legislative_topic_for_cf(db_conn, cf_number, id)


def main():
    """
    Loop through the city council files and identify their legislative topic(s) (e.g., environment or transportation)
    """
    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('config/base.ini')
    config_section = sysu.get_config_section(hostname)
    print(config_section)
    print(config['Locations.{}'.format(config_section)])
    db_file = config['Locations.{}'.format(config_section)]['db_path']

    db_conn = create_connection(db_file)
    council_files = get_council_files(db_conn)
    legislative_topics = get_legislative_topics(db_conn)

    for cf_number in council_files.keys():
        process_council_file_topics(db_conn, legislative_topics, cf_number, council_files[cf_number]['title'])

    db_conn.commit()


if __name__ == "__main__":

    main()

