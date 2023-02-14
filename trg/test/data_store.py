__author__ = 'Administrator'
from trg.tool.insert_stmt_val_quoted import insert_stmt_val_quoted_

def data_store_db_(tblname, listtobestored, glo):
    insert_stmt = glo.tables_tr.get_sql_stmt_(tblname, "insert")
    for node in listtobestored:
#        insert_stmt_val = insert_stmt % tuple(node)
        insert_stmt_quoted = insert_stmt_val_quoted_(insert_stmt, node)
        glo.dbserver_[0].sqlexec(insert_stmt_quoted)



