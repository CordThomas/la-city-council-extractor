import pandas as pd
import holoviews as hv
hv.extension('bokeh')
from utils.db import *
from las_utils import database_utils as dbu
from las_utils import system_utils as sysu
import configparser
import socket

def main():
    """
    Create a Sankey chart of the Mover to Seconder relationships for active council members
    """
    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('config/base.ini')
    config_section = sysu.get_config_section(hostname)
    db_file = config['Locations.{}'.format(config_section)]['db_path']
    analysis_ouput = config['Locations.{}'.format(config_section)]['analysis_output']

    db_conn = create_connection(db_file)
    sql = 'SELECT mover as source, lt.topic_label as target, count(*) AS value ' \
          'FROM council_file cf ' \
          'JOIN council_district_member cd1 on cf.MOVER = cd1.mover_name and LENGTH(cd1.end_date) = 0 ' \
          'JOIN council_file_legislative_topic flt ON flt.cf_number = cf.cf_number ' \
          'JOIN  legislative_topic lt on flt.topic_id = lt.topic_id ' \
          'GROUP BY source, target;'

    df = pd.read_sql(sql, db_conn)
    sankey = hv.Sankey(df, label='A Comparison of Los Angeles City Council Member Motion Filing')
    sankey.opts(label_position='left', edge_color='target', node_color='index', cmap='tab20')
    hv.save(sankey, analysis_ouput + 'mover_legislative_topic.html')
    db_conn.close()


if __name__ == "__main__":

    main()
