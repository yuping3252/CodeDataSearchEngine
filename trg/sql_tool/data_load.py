__author__ = 'Administrator'

from trg.sql_tool.data_retrieve  import data_retrieve_db_
from trg.tool.print_space_layout import Print_Layout

class DataLoad:
    def __init__(self, glo):
        self.glo = glo
        self.glo.list_tr_sqlquerysrctables = data_retrieve_db_("TR_SQLQuerySrcTables", glo)
        self.glo.list_tr_sqlqueryselcols   = data_retrieve_db_("TR_SQLQuerySelCols",   glo)
        self.glo.list_tr_sqlquerytrace     = data_retrieve_db_("TR_SQLQueryTrace",     glo)
        self.glo.list_tr_sqlinsertselcls   = data_retrieve_db_("TR_SQLInsertSelCols",  glo)
        self.glo.list_tr_sqlqueryfilter    = data_retrieve_db_("TR_SQLQueryFilter",    glo)

        self.glo.list_tr_node = data_retrieve_db_("TR_Node", glo)
        self.glo.list_tr_file = data_retrieve_db_("TR_File", glo)
        self.glo.list_tr_sql  = data_retrieve_db_("TR_SQL",  glo)

        for node in self.glo.list_tr_node:
            for file_ in self.glo.list_tr_file:
                if node[4] == file_[0]:
                    node[5] = file_ + ['','','','','']
                    break


    def mouseDoubleClickEvent(self, event):
        print(" event=", event)

    def list_node(self):
        return self.glo.list_tr_node

    def list_file(self):
        return self.glo.list_tr_file

    def list_sql(self):
        return self.glo.list_tr_sql

    def list_sqlquerysrctables(self):
        return self.glo.list_tr_sqlquerysrctables

    def list_sqlqueryselcols(self):
        return self.glo.list_tr_sqlqueryselcols


    def list_sqlquerytrace(self):
        return self.glo.list_tr_sqlquerytrace

    def list_sqlinsertselcls(self):
        return self.glo.list_tr_sqlinsertselcls

    def list_sqlqueryfilter(self):
        return self.glo.list_tr_sqlqueryfilter

    def list_sql(self):
        return self.glo.list_tr_sql











