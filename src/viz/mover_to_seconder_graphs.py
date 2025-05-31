import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from utils.db import *
from las_utils import database_utils as dbu
from las_utils import system_utils as sysu
import configparser
import socket

def load_mover_seconder_data(db_conn):
    """
    Return a dictionary containing the directed graph data for active
    city council members with the mover / seconder frequency as the weight
    of the graph.
    """
    sql = 'SELECT cf.mover as "from", cf.second as "to", count(*) as weight from council_file cf ' \
          'join council_district_member cm on cf.mover = cm.mover_name where LENGTH(cm.end_date) = 0 ' \
          'and mover is not null and second is not null and cast(substr(date_received, 1, 4) as integer) > 2010 ' \
          'and second in (select mover_name from council_district_member cd where LENGTH(end_date) = 0) ' \
          'group by mover, second ' \
          'order by mover;'

    movers_seconders = dbu.select(db_conn, sql)
    ms_dict = {}
    for ms in movers_seconders:
        ms_dict[ms[0] + ':' + ms[1]] = ms[2]

    return ms_dict


def generate_mover_seconder_graph(movers_seconders):
    """
    Given the graph of mover seconders dictionary with weights as values,
    draw a weighted graph using networkx
    """

    G = nx.Graph()

    for key, value in movers_seconders.items():
        f_t = key.split(':')
        G.add_edge(f_t[0], f_t[1], weight=value)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(
        G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    )

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    """ Present some data visualizations on the relationship of mover to seconder in the active City
    Council members based on their city council file records
    """
    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('config/base.ini')
    config_section = sysu.get_config_section(hostname)
    print(config_section)
    print(config['Locations.{}'.format(config_section)])
    db_file = config['Locations.{}'.format(config_section)]['db_path']

    db_conn = create_connection(db_file)
    movers_seconders = load_mover_seconder_data(db_conn)
    generate_mover_seconder_graph(movers_seconders)


if __name__ == '__main__':
    main()
