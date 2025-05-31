from utils.db import *


def process_cf_activity(soup, conn, cf_number, process_documents_only=False):
    """
    Process the council actions information.
    :param soup:  The BeautifulSoup object for the council file page
    :param db_conn:  The database connection handle
    :param cf_number:  Council file number, format a zero-padded yy-nnnn
    :param process_documents_only: To get the historical documents or documents we might have missed, set to True
    :return: None
    """

    if not process_documents_only:
        return None

    activity_div = soup.find('div', attrs={'class': 'rectext rowcolor1'})
    if activity_div is not None:
        table_rows = activity_div.findChildren('tr')
        if table_rows is not None:
            table_row_idx = 0
            for table_row in table_rows:
                action_date = ''
                description = ''
                if table_row_idx > 0:
                    table_cells = table_row.findChildren('td')
                    action_date = table_cells[0].text.strip()
                    description = table_cells[1].text.strip()

                    insert_new_council_action(conn, cf_number, action_date, description)
                table_row_idx += 1