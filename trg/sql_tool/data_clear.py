__author__ = 'Administrator'

class DataClear:
    def truncate_all_db_tables_(self, glo):
        self.data_remove_("TR_SQLQuerySrcTables", glo)
        self.data_remove_("TR_SQLQuerySelCols", glo)
        self.data_remove_("TR_SQLQueryTrace", glo)
        self.data_remove_("TR_SQLInsertSelCols", glo)
        self.data_remove_("TR_SQLQueryFilter", glo)

        self.data_remove_("TR_Node", glo)
        self.data_remove_("TR_File", glo)
        self.data_remove_("TR_SQL", glo)

    def data_remove_(self, tblname, glo):
        truncate_stmt = glo.tables_tr.get_sql_stmt_(tblname, "truncate")
        cds = glo.dbserver_[0].sqlexec(truncate_stmt)





