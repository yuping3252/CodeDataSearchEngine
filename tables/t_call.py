from PyQt4.QtCore        import *
from PyQt4.QtGui         import *
from tables.tabledb      import TableDB
from tables.tablesize    import TableSize
from tables.tabledata    import TableData
from tables.tablerelate  import TableRelate
from tables.table_op     import Table_OP
from trg.sql_client.tblcolumns  import TableColumns


class TableCombo(QWidget):
    def __init__(self, rows, columns, tblnm, mw, glo):
        QWidget.__init__(self)
        self.dbnm    = ""
        self.conn_db = ""
        self.t_op    = ""
        self.mw      = mw
        self.tblvw_  = ""

        # ------------------------------------- loop over db connections
        for conn_db in glo.dbconn_:
            cursor = conn_db.conn.cursor()
            if cursor:
                query_test = "select count(*) from tr_fk_pk_table"

                try: 
                    cursor.execute(query_test)
                except:
                    print("t_call.py,   __init__(),   database ",    conn_db.dbnm," does not have table tr_fk_pk_table")
                    continue

                sz        = TableSize() 
                tdata     = TableData  (conn_db, sz) 
                trelate   = TableRelate(conn_db, sz) 
                self.t_op = Table_OP(conn_db, sz, tdata, trelate, self.mw, self)
                self.r    = 0
                self.c    = 0

                # ------------------------------------- test db connection
                success   = self.one_db_1_table(self.t_op, tdata, tblnm, conn_db, glo)
                if success: 
                    self.dbnm    = conn_db.dbnm
                    self.conn_db = conn_db
                    print("t_call.py,   __init__(),   database ",    conn_db.dbnm," have table ", tblnm)
                    break
                else:
                    print("t_call.py,   __init__(),   database ",    conn_db.dbnm," does not have table ", tblnm)



    def one_db_1_table(self, t_op, tdata, tblnm, conn_db, glo):
        dbtype    =  conn_db.dbtype
        dbnm      =  conn_db.dbnm
        tbl_lst   = [tblnm]
        q = TableColumns()
        cols    = [0, tblnm]

        print("")
        print("t_call.py,    one_db_1_table(),    cols=", cols)

        cols = q.a_query(cols, conn_db, glo)

        print("t_call.py,    one_db_1_talbe(),    q.a_query(cols, conn_db, glo)=", cols)

        if cols[2] != []:
            cols2 = []
            for col_ in cols[2]:
                col = col_[0]
                cols2.append(col)
            col_lst = [cols2]
            self.tblvw_, self.r, self.c = t_op.tbl_col_rows("populategrid", dbtype, dbnm, tbl_lst, col_lst, self)
            layout = QVBoxLayout()
            layout.addWidget(self.tblvw_)
            self.setLayout(layout)

            print("t_call.py,    one_db_1_table(),    return True")
            return True
        else:
            print("t_call.py,    one_db_1_table(),    sql_client.tblcolumns.py failed, cols=", cols)
            return False



    def dbnm_of_tblnm(self):
        return self.dbnm



    def conn_db_(self):
        return self.conn_db


    def tblvw(self):
        return self.tblvw_


    def size_(self):
        return self.r, self.c



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    frm = TableCombo(50, 30)
    r, c = frm.size_()
    frm.setGeometry(500, 100, c, r)
    frm.show()
    sys.exit(app.exec_())

