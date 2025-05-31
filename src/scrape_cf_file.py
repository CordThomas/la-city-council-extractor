"""
Script uses BeautifulSoup4 to parse HTML label:value pairs from the City Council motion pages
and loads them in a database. The basis of the script uses a mapping (from data_structures) of
HTML tag IDs to database fields to figure out where to store the data in the database.
"""
import bs4
from utils.data_structures import *
from utils.db import *
from utils.utils import iso_format_date
from datetime import date


def done_processing_sections(section):
    """ Determine whether to stop the serial processing of the council
    file summary section.  If we want to process the File Activities, then
    this would be something to update.  Turns out the format of the file
    page changes dating before 2009 where the transition is to "File History"
    and the file activities are not linked but still linked in the online
    document section in the top right.
    :param section:  The HTML section DIV currently being evaluated
    :return: True if we're at the stopping point, otherwise False
    """
    for element in section:
        if element.string == 'File Activities' or element.string == 'File History':
            return True
    return False


def contains_class(class_list, class_match):
    """ Determines if the class_match is in the class_list.
    Not sure why I didn't just say class_match in class_list but
    think that for some reason the BeautifulSoup list didn't support
    that or there was something else wrong.
    :param class_list:  A list of HTML classes
    :param class_match:  The class we are looking for
    :return: True if the match class is in the list
    """
    for class_val in class_list:
        if class_val == class_match:
            return True

    return False


def process_record(db_conn, cf_number, reclabel, rectext):
    """ Process the council file summary information entry; this is a
    single field label and value from the HTML content.
    :param db_conn:  Active database connection
    :param cf_number:  Council file number, format a zero-padded yy-nnnn
    :param reclabel:  The HTML field label - the label of the section to be mapped
    to the database field.
    :param rectext:  The value of the field to be added to the database
    """

    if reclabel in cf_fields:
        db_field = cf_fields[reclabel]
        rectext = clean_field_for_database(db_field, rectext)
        update_council_file_field(db_conn, cf_number, db_field, rectext)


def get_last_changed_date(cf_number, soup):
    """
    Get the Last Changed Date from the council file
    :param cf_number:  Council file number, format a zero-padded yy-nnnn
    :param soup:  The BeautifulSoup object for the council file page
    :return:  the iso formated last change date for the council file
    """

    sections = soup.find_all('div', {'class': 'section'})
    reclabel = ''
    rectext = ''
    grab_next_text = False
    for section in sections:
        for index, element in enumerate(section.descendants):
            if isinstance(element, bs4.element.Tag):
                if 'class' in element.attrs:
                    if contains_class(element.attrs['class'], 'reclabel'):
                        try:
                            reclabel = element.string.strip()
                        except Exception:
                            pass

                    if grab_next_text:
                        try:
                            for elementitem in element:
                                if isinstance(elementitem, bs4.element.NavigableString):
                                    rectext += str(elementitem.string) + '; '
                                elif isinstance(elementitem, bs4.element.Tag):
                                    rectext = elementitem.string.strip()
                                    break
                            return rectext
                        except Exception:
                            pass

                    if reclabel == 'Last Changed Date':
                        grab_next_text = True


def check_if_update(db_conn, cf_number, soup):
    """
    Check whether this council file is an update because it is
    either a new record or the Last Changed Date is greater than
    the CF's date_last_changed as recorded in the database.
    :param db_conn:   The database connection handle
    :param cf_number:  Council file number, format a zero-padded yy-nnnn
    :param soup:  The BeautifulSoup object for the council file page
    :return:
    """
    council_file_exists, date_last_changed = counfil_file_exists(db_conn, cf_number)
    if not council_file_exists:
        print('==== We have a new record')
        return 'new'
    else:
        cf_last_changed_date = get_last_changed_date(cf_number, soup)
        cf_last_changed_date = iso_format_date(cf_last_changed_date)
        if date_last_changed is None or date.fromisoformat(cf_last_changed_date) > date.fromisoformat(date_last_changed):
            print('==== We have an updated record')
            return 'update'

    return ''


def parse_section(db_conn, cf_number, section, meta_words):
    """ Parse the section of the council file meta information to
    extract the field label and field text.  The HTML has a variety of
    formats.  The method should process all permutations.
    :param db_conn:  The database connection handle
    :param cf_number:  Council file number, format a zero-padded yy-nnnn
    :param section:  The HTML section from which to extract the label and value
    :param meta_words:  The list used to track all the possible field names; should
    be part of a separate method or even preprocesing script to create the structure
    of the database table schema.
    """
    reclabel = ''
    rectext = ''
    for element in section.descendants:
        if isinstance(element, bs4.element.Tag):
            if 'class' in element.attrs:
                if contains_class(element.attrs['class'], 'reclabel'):
                    try:
                        reclabel = element.string.strip()
                    except Exception:
                        pass

                elif contains_class(element.attrs['class'], 'rectext'):
                    if len(element.contents) > 1:
                        for elementitem in element:
                            if isinstance(elementitem, bs4.element.NavigableString):
                                rectext += str(elementitem.string) + '; '
                            elif isinstance(elementitem, bs4.element.Tag):
                                rectext = elementitem.string.strip()
                                break
                    else:
                        try:
                            rectext = element.string.strip()
                        except Exception:
                            pass

            if reclabel is not None and len(reclabel) > 0 and rectext is not None and len(rectext) > 0:
                # if reclabel not in meta_words:
                #     meta_words.append(reclabel)
                # if 'Date' in reclabel:
                process_record(db_conn, cf_number, reclabel, rectext)
                reclabel = ''
                rectext = ''


def process_cf_council_file(soup, meta_words, db_conn, cf_number, process_documents_only=False):
    """ Process the council_file meta data section of the page
    :param soup:  The BeautifulSoup object for the council file page
    :param db_conn:  The database connection handle
    :param cf_number:  Council file number, format a zero-padded yy-nnnn
    :param meta_words:  The list used to track all the possible field names; should
    be part of a separate method or even preprocesing script to create the structure
    of the database table schema.
    :param process_documents_only: To get the historical documents or documents we might have missed, set to True
    :return missing_sections, is_update:  Returns whether the council file page is
     missing sections (1).   If not, this suggests the page was empty - there
     are empty pages in the middle of the year, so cannot assume that the first
     empty page signals the end of the year. is_update
    """

    missing_sections = 1
    is_update = False

    sections = soup.find_all('div', {'class': 'section'})

    if process_documents_only:
        return 0 if len(sections) > 0 else 1, 'update'

    if len(sections) > 0:
        missing_sections = 0

        is_update = check_if_update(db_conn, cf_number, soup)

        if is_update in ['new', 'update']:
            for section in sections:
                if done_processing_sections(section):
                    break
                # If we have a set of children we know we have content
                if len(section) > 1:
                    parse_section(db_conn, cf_number, section, meta_words)

    return missing_sections, is_update
