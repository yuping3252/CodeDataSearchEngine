from PyQt4.QtCore        import *
from PyQt4.QtGui         import *
from tables.tabledb      import TableDB
from tables.tablesize    import TableSize
from tables.tabledata    import TableData
from tables.tablerelate  import TableRelate
from tables.table_op     import Table_OP
from trg.sql_client.tblcolumns  import TableColumns


class ProcCombo(QWidget):
    def __init__(self, procnm, glo):
        QWidget.__init__(self)
        self.dbnm        = ""
        self.conn_db     = ""
        self.routine_def = ""

        for conn_db in glo.dbconn_:
            cursor = conn_db.conn.cursor()
            if cursor: 
                query = "SELECT ROUTINE_DEFINITION FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME = \'" + procnm + "\'"

                try: 
                    cursor.execute(query)
                    data = cursor.fetchall()
                    data_tuple = data[0]
                    self.routine_def = data_tuple[0]
                    self.dbnm = conn_db.dbnm
                    self.conn_db = conn_db
                    break
                except:
                    # print("t_proc.py,   __init__,   ",    conn_db.dbnm,"    query failed")
                    i = 1


    def definition_of_procnm(self):
        return self.routine_def


    def dbnm_of_procnm(self):
        return self.dbnm


    def conn_db_(self):
        return self.conn_db


if __name__ == '__main__':

    import sys

    app  = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    frm  = ProcCombo(50, 30)
    r, c = frm.size_()
    frm.setGeometry(500, 100, c, r)
    frm.show()
    sys.exit(app.exec_())

