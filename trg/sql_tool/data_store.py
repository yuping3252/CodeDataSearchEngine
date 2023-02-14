__author__ = 'Administrator'

from trg.tool.insert_stmt_val_quoted import insert_stmt_val_quoted_

def data_store_db_(tblname, listtobestored, glo):
    if len(listtobestored) == 0:
        return

    if tblname == "public.TR_File": 
        print("data_store.py,   tblname=", tblname)
        for s in listtobestored: 
            if s == "mssql_addresses.sql": 
                print("data_store.py,     s=", s) 


    insert_stmt = glo.tables_tr.get_sql_stmt_(tblname, "insert")
    i_ = insert_stmt.index("values")
    insert_head_ = insert_stmt[:i_].strip() + " "
    values_ = insert_stmt[i_:].strip()
    i = 0
    for node in listtobestored:
        if i == 0:
            insert_head_ += insert_stmt_val_quoted_(values_, node)
        else:
            v_ = insert_stmt_val_quoted_(values_, node)
            j_ = v_.index("values")
            v_ = v_[j_ + 6:]
            insert_head_ += ", " + v_
        i += 1
    insert_head_ += ";"
    glo.dbserver_[0].sqlexec(insert_head_)


