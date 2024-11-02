import pandas as pd
import holoviews as hv
hv.extension('bokeh')
from utils.db import *
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
    print(config_section)
    print(config['Locations.{}'.format(config_section)])
    db_file = config['Locations.{}'.format(config_section)]['db_path']
    analysis_ouput = config['Locations.{}'.format(config_section)]['analysis_output']

    db_conn = create_connection(db_file)
    sql = 'SELECT SUBSTRING(cd1.name_first, 1, 1) || SUBSTRING(cd1.name_last, 1, 1) as Mover, ' \
          'SUBSTRING(cd2.name_first, 1, 1) || SUBSTRING(cd2.name_last, 1, 1) as Second, count(*) AS value ' \
          'FROM council_file cf ' \
          'JOIN council_district_member cd1 on cf.MOVER = cd1.mover_name and LENGTH(cd1.end_date) = 0 ' \
          'JOIN council_district_member cd2 on cf.SECOND = cd2.mover_name and LENGTH(cd2.end_date) = 0 ' \
          'GROUP BY  mover, second;'

    df = pd.read_sql(sql, db_conn)
    heatmap = hv.HeatMap(df, label='A Comparison of Los Angeles City Council Member Motion Filing Relationships')
    heatmap.opts(cmap='Greens', height=800, width=800)
    hv.save(heatmap, analysis_ouput + 'mover_second_frequency.html')
    db_conn.close()


if __name__ == "__main__":

    main()
