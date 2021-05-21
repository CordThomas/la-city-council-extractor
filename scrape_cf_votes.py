from db import *
import unicodedata


def process_cf_votes(soup, db_conn, cf_number):
    """ Process the Votes section of the council file page.  There are
    two sections of the page we could break out into separate methods.  The
    first is the summary information including the date and type of
    the meeting.  The second is the list of council members and how
    they voted on the issue.
    :param soup:  The BeautifulSoup object for the council file page
    :param db_conn:  The HTML section DIV currently being evaluated
    :param cf_number:  Council file number, format a zero-padded yy-nnnn
    """
    vote_date = vote_type = vote_action = ''
    # The vote summary
    vote_table = soup.find('table', attrs={'class': 'color_d'})
    # If the motion has been voted on, there will be a summary table
    # Going to naively assume that the table structure remains the same
    if vote_table is not None:
        row_number = 0
        vt_rows = vote_table.find_all('tr')
        for vt_row in vt_rows:
            vt_cells = vt_row.find_all('td')
            vt_value = vt_cells[1].string.strip()
            # print("{key}: {val}".format(key=vt_key, val=vt_value))
            if row_number == 0:
                vote_date = vt_value
            elif row_number == 1:
                vote_type = vt_value
            elif row_number == 2:
                vote_action = vt_value

            row_number += 1

        insert_vote(db_conn, cf_number, vote_date, vote_type, vote_action)

    vote_by_council = soup.find('table', attrs={'id': 'inscrolltbl', 'border': '0'})
    # If the motion has been voted on, there will be a summary table
    if vote_by_council is not None:
        vt_rows = vote_by_council.find_all('tr', attrs={'class': ['rowcolor2', 'rowcolor3']})
        for vt_row in vt_rows:
            vt_cells = vt_row.find_all('td')
            vt_member = unicodedata.normalize('NFKD', vt_cells[0].string.strip())
            vt_district = vt_cells[1].string.strip()
            vt_vote = vt_cells[2].string.strip()
            # print("{key}: {dist} {vote}".format(key=vt_key, dist=vt_district, vote=vt_vote))

            insert_vote_result(db_conn, cf_number, vt_member, vt_district, vt_vote)
