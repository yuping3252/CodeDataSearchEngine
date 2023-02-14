__author__ = 'Administrator'

from trg.tool.rows_cols  import rows_cols_

def data_retrieve_db_(tblname, glo):
    select_stmt = glo.tables_tr.get_sql_stmt_(tblname, "select")
    cds = glo.dbserver_[0].sqlexec(select_stmt)
    listretrieved = rows_cols_(cds)
    return listretrieved





