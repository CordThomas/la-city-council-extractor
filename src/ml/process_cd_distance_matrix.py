import openpyxl
from utils import db

source_file_path = '../../data/council district proximity.xlsx'
db_path = '../../data/city-council.db'

wrkbk = openpyxl.load_workbook(source_file_path)
wrksh = wrkbk.active

db_conn = db.create_connection(db_path)

for row in wrksh.iter_rows(min_row = 2, min_col=2,
                           max_row = 16, max_col=16):
    for cell in row:
        if cell.value is not None:
            council_district_1 = cell.row - 1
            council_district_2 = cell.column - 1
            db.insert_council_distance_entry(db_conn, council_district_1,
                                             council_district_2, cell.value)