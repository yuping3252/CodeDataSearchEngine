__author__ = 'Administrator'


class TableColumns:
    def __init__(self):
        i = 1
        #self.tblinfo = TableInfo()

    def table_columns_db_(self, querytable_list, glo):
        tables_cols_list = []
        for q in querytable_list:                                 # q = [query id, tbl id, tbl, xxx, xxx, xxx]
            if q[2].strip()[0] != "(":                            # q[2] is table name
                cols = self.cols_(q[2], glo)
                tables_cols_list.append([q[0], q[1], q[2], cols]) # [query id, tbl id, tbl, cols]
        return tables_cols_list

    def cols_(self, tablename, glo):


        print("table_columns_db.py,   cols_(),  tablename=", tablename)

        query = "select * from query_tr_sql(\'public.\"" + tablename + "\"\')"
        try:                                                      # PostgreSQL
            cds = glo.dbserver_[0].sqlexec(query)
            cols = []
            for rows in cds:
                i = 0
                for col in rows:
                    if i==2:
                        cols.append(col)
                    i += 1
            return cols                                           # return
        except:
            cds = None

        #print("table_columns_db.py,   cols_(),  glo.dbconn_ is a list of database connections that user selected before travel db")
        #print("without these connections, you won't be able to see table icons in the central plot area")

        if cds == None:
            for conn_db in glo.dbconn_:
                if   conn_db.dbtype == "PostgreSQL":
                    query = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = '" + tablename + "'"
                elif conn_db.dbtype == "SQL Server": 
                    query = "SELECT NAME FROM SYS.COLUMNS WHERE object_id = object_id(\'" + tablename +"\')"

                print("table_columns_db_.py,   cols_(),   " + conn_db.dbtype, ",  ",   conn_db.dbnm, ",   query=", query)

                try: 
                    cur = conn_db.conn.cursor() 
                    cur.execute(query) 
                    cds = cur.fetchall()

                    cols = [] 
                    for row in cds: 
                        cols.append(row[0])
                except:
                    cds = None
                finally:
                    if cols != []:
                        print("table_columns_db_()     column finding success,   cols=", cols)
                        return cols

            print("table_columns_db_()     column finding failed")

            return None




