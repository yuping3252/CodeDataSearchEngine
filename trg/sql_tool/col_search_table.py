__author__ = 'Administrator'

class ColSearchTable:
    def __init__(self):
        i = 0

    def col_search_table(self, tables_cols_list, qid, column):
        match = 0
        table = ""
        for tbl_cols in tables_cols_list:     # tbl_cols = [query id, tbl id, tbl, cols], cols = [...]
            if qid == tbl_cols[0]:
                for col in tbl_cols[3]:
                    if column.strip() == col.strip():
                        table = tbl_cols[2]
                        match += 1
        if match > 1:
            table = ""
        return table