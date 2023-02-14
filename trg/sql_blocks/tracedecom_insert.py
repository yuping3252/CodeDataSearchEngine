__author__ = 'Administrator'

from trg.sql_tool.table_columns_db import TableColumns


class TraceDecomInsert:
    def __init__(self):
        self.tc = TableColumns()

    def tracedecom_insert_(self, query_id, tree_ssql, select_cols, insert_type_, param_, glo):
        insert_ = []
        # if insert statement, without parameter list, then, list all to be inserted columns from left to right
        # and match as many select columns as possible
        table_insert = ""
        tt = []
        for t in tree_ssql:
            if t[6] == "table":
                tbl_insert_id = t[1]
                tbl_insert = t[7]
                tt = t

        if len(tree_ssql) == 2: 
            cols = self.tc.cols_(tbl_insert, glo)
            if cols:
                i = 0
                for c in cols:
                    for sc in select_cols:
                        if int(sc[5]) == i:
                            insert_.append([query_id, sc[5], tbl_insert_id, tbl_insert, c, sc[0], sc[1], sc[3]])
                            # col pos, table id,  insrt table,  insrt col,   query id,  src table, src col
                    i += 1
            else:
                return "tracedecom_insert.py,   No database relevance"
        else:
            for q in tree_ssql:
                for sc in select_cols:
                    if q[10] == sc[5]:
                        insert_.append([query_id, sc[5], tbl_insert_id, tbl_insert, q[7], sc[0], sc[1], sc[3]])
        return insert_
