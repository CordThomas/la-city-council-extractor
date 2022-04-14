import sqlite3
from sqlite3 import Error


def clean_field_for_database(db_field, rectext):
    """
    Clean a field rectext for proper formet in the database.
    Currently only worried about the date field as we want it
    standard yyyy-mm-dd format
    :param db_field: The database field name
    :param rectext: The text to format
    :return:
    """

    if 'date' in db_field:
        rectext = rectext[6:10] + '-' + rectext[0:2] + '-' + rectext[3:5]
    elif 'subject' in db_field:
        rectext = rectext[0:999]
    return rectext


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: Relative or fully qualified path to the database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def counfil_file_exists(conn, cf_num):
    """
    Check whether we already have this council file
    :param conn:  Active database connection
    :param cf_num:  Council file number, format a zero-padded yy-nnnn
    :return: True if exists
    """
    sql = 'SELECT cf_number, date_last_changed FROM council_file WHERE cf_number = ?'
    cur = conn.cursor()
    cur.execute(sql, (cf_num, ))
    data = cur.fetchone()
    if data is None:
        return False, ''
    else:
        return True, data[1]


def insert_new_council_file(conn, cf_num):
    """
    Create a new council file meta data record
    :param conn:  Active database connection
    :param cf_num:  Council file number, format a zero-padded yy-nnnn
    """

    sql = ''' INSERT OR IGNORE INTO council_file(cf_number)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (cf_num,))
    conn.commit()


def insert_new_council_action(conn, cf_num, action_date, description):
    """
    Insert a council action
    :param conn: Active database connection
    :param cf_num: Council file number, format a zero-padded yy-nnnn
    :param action_date: Date of the action
    :param description: Description of the action
    :return: n/a
    """

    sql = ''' INSERT OR IGNORE INTO council_action(cf_number, action_date, description)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (cf_num, action_date, description))
    conn.commit()


def insert_or_update(conn, cf_num, key, value):
    """
    A method to either insert or replace (update) the value in a
    field.  This way, if the primary key is not already in the
    table, it will create a new record and set the field value, otherwise
    it will update the value of the field.  This way you shortcut the
    legacy approach of a 2 step method to first check the existence of the
    primary key in one request and then insert or update in another.  Also
    this avoids race conditions in the case that another program might
    be making the same decision at the same time.
    :param conn:  Active database connection
    :param cf_num:  Council file number, format a zero-padded yy-nnnn
    :param key:  The field name to be set or update
    :parem value:  The value to set for the field
    """
    sql = ''' INSERT OR REPLACE INTO council_file (cf_number, {field})
              VALUES({cf_num},
              COALLESCE((SELECT {field} FROM meta WHERE cf_number = {cf_num}), 'blank')
              ); '''
    sql.format(field=key, cf_num=cf_num)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def update_council_file_field(conn, cf_num, key, value):
    """
    Update the named field with the value for the given council file
    :param conn:  Active database connection
    :param cf_num:  Council file number, format a zero-padded yy-nnnn
    :param key:  The field name to be set
    :param value:  The value to set for the field
    """
    sql = ''' UPDATE council_file SET {field} = ?
              WHERE cf_number = ? '''
    sql_exec = sql.format(field=key)
    # print(sql_exec)
    cur = conn.cursor()
    cur.execute(sql_exec, (value, cf_num))
    conn.commit()


def delete_vote_records(db_conn, cf_number):
    """
    Delete the vote results and vote record for this CF
    :param db_conn:  Active database connection
    :param cf_number:  Council file number, format a zero-padded yy-nnnn
    :return:  None
    """

    cur = db_conn.cursor()
    sql = '''DELETE FROM vote_results WHERE cf_number=?;'''
    cur.execute(sql, (cf_number, ))

    sql = '''DELETE FROM votes WHERE cf_number=?;'''
    cur.execute(sql, (cf_number, ))
    db_conn.commit()


def insert_vote(conn, cf_num, vote_date, vote_type, vote_action):
    """
    Insert a vote summary record with the date and type of meeting
    :param conn:  Active database connection
    :param cf_num:  Council file number, format a zero-padded yy-nnnn
    :param vote_date:  Date of the council meeting at which the vote was held
    :param vote_type:  Type of meeting, either regular or special
    :param vote_action:  The outcome of the vote - there are 28 values
    """

    sql = ''' INSERT INTO votes(cf_number, meeting_date, meeting_type, vote_action)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (cf_num, vote_date, vote_type, vote_action))
    conn.commit()


def insert_vote_result(conn, cf_num, council_member, council_district, vote):
    """
    Insert a vote result by council member
    :param conn:  Active database connection
    :param cf_num:  Council file number, format a zero-padded yy-nnnn
    :param council_member:  The name of the council member casting the vate
    :param council_district:  The council district number
    :param vote:  The council member's vote, ABSENT, YES, NO
    """

    sql = ''' INSERT INTO vote_results(cf_number, council_district, council_member, vote)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (cf_num, int(council_district), council_member, vote))
    conn.commit()


def document_exists(conn, cf_num, file_name):
    """
    Check whether we already have this council file
    :param conn:  Active database connection
    :param cf_num:  Council file number, format a zero-padded yy-nnnn
    :param file_name:  Document file name
    :return: True if exists
    """
    sql = 'SELECT cf_number, file_name FROM council_document WHERE cf_number = ? and file_name = ?'
    cur = conn.cursor()
    cur.execute(sql, (cf_num, file_name))
    data = cur.fetchone()
    if data is None:
        return False
    else:
        return True


def insert_new_council_document(conn, cf_number, action_date, title, file_name):
    """
    Insert a council document number if it doesn't already exist
    :param conn: Active database connection
    :param cf_number: Council file number, format a zero-padded yy-nnnn
    :param action_date: Data the file was processed
    :param title:
    :param file_name:
    :return:
    """

    if document_exists(conn, cf_number, file_name):
        return True
    else:
        sql = ''' INSERT INTO council_document(cf_number, action_date, title, file_name)
                  VALUES(?, ?, ?, ?) '''
        cur = conn.cursor()
        cur.execute(sql, (cf_number, action_date, title, file_name))
        conn.commit()


def get_council_motion_documents(conn):
    """
    Get the list of council documents as full path entries in a list
    :param conn: Active database connection
    :return: List of motion documents with full year and cf_number path
    """

    motion_documents = []
    sql = 'select cf.cf_number, cf.date_received, replace(cd.file_name, \'.pdf\', \'.txt\') ' \
          'from council_document cd ' \
          'join council_file cf on cd.cf_number = cf.cf_number ' \
          'where cd.title = \'Motion\''

    cur = conn.cursor()
    for row in cur.execute(sql):
        year = ''
        if row[1] is None:
            year = '20' + row[0][:2]
        else:
            year = row[1][:4]

        motion_documents.append(year + '/' + row[0] + '/' + row[2])

    return motion_documents


def insert_council_distance_entry(conn, council_district_1, council_district_2, distance):

    sql = 'insert into council_distance_matrix values (?, ?, ?)'
    cur = conn.cursor()
    cur.execute(sql, (council_district_1, council_district_2, distance))
    conn.commit()
