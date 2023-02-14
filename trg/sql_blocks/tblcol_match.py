__author__ = 'Administrator'


class TableColMatch:
    def __init__(self):
        i = 0

        # tblcols = [query id, tbl id, tbl, cols]
    def tblcol_match_(self, table_cols_list, column, table):
        table_column_match = False
        for tblcols in table_cols_list:
            if tblcols[2] == table:
                cols = tblcols[3]
                for col in cols:
                    if col == column:
                        table_column_match = True
        return table_column_match





