from utils.db import *


def process_cf_activity(soup, conn, cf_number):

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