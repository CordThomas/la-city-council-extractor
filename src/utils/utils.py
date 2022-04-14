from datetime import date


def iso_format_date(last_changed_date):
    """
    Format a date of various formats into an ISO formatted
    date:  yyyy-mm-dd
    :param last_changed_date:  input date to format (e.g., 01/01/2010)
    :return: ISO formated date
    """

    if len(last_changed_date) == 12 and last_changed_date[2:3] == '/' \
        and last_changed_date[5:6] == '/':

        return date(int(last_changed_date[6:10]), int(last_changed_date[0:2]),
                    int(last_changed_date[3:5])).isoformat()

