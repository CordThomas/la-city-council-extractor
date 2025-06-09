"""
Standardizing on using all lower case file names since we somehow resulted in a mix of
partially upper case file names
"""
import configparser
import os
import socket
from las_utils import system_utils as sysu


def convert_filenames_to_lowercase(directory):
    """Converts all filenames within a directory and its subdirectories to lowercase."""
    for root, _, files in os.walk(directory):
        for filename in files:
            old_filepath = os.path.join(root, filename)
            new_filename = filename.lower()
            new_filepath = os.path.join(root, new_filename)
            if old_filepath != new_filepath:
                os.rename(old_filepath, new_filepath)


if __name__ == '__main__':

    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('config/base.ini')
    config_section = sysu.get_config_section(hostname)

    documents_base = config['Locations.{}'.format(config_section)]['documents_base']

    convert_filenames_to_lowercase(documents_base)
