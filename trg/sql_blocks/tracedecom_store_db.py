__author__ = 'Administrator'

import copy
from trg.sql_blocks.src_filter_separate import SourceOrFilter
from trg.sql_tool.data_store            import data_store_db_

class TraceDecomStoreDB:
    def __init__(self):
        self.srcfilter = SourceOrFilter()

    def tracedecom_store_db_(self, query_id, insert_, traced_cols, cols_their_src, traced_sel_cols, \
                             src_traced, src_tbl_list, filter_relation, glo):
        src_tbl_list2    = self.lst_add_fileid_(        glo.fileid,           src_tbl_list)
        traced_sel_cols2 = self.lst_add_2_ids_ (        glo.fileid, query_id, traced_sel_cols)
        src_traced2      = self.lst_double_add_2_ids_(  glo.fileid, query_id, src_traced)
        filter_relation2 = self.lst_add_fileid_(        glo.fileid,           filter_relation)
        insert_2         = self.lst_add_fileid_(        glo.fileid,           insert_)

        self.store_singlelist_("TR_SQLQuerySrcTables", src_tbl_list2,     glo)
        self.store_singlelist_("TR_SQLQuerySelCols",   traced_sel_cols2,  glo)
        self.store_doublelist_("TR_SQLQueryTrace",     src_traced2,       glo)
        self.store_singlelist_("TR_SQLQueryFilter",    filter_relation2,  glo)
        if insert_2 != []:
            self.store_singlelist_("TR_SQLInsertSelCols",  insert_2,          glo)

#        print("tracedecom_store_db(),  TR_SQLQuerySrcTables,[0] ", src_tbl_list2[0])
#        print("tracedecom_store_db(),  TR_SQLQuerySelCols,  [0] ", traced_sel_cols2[0])
#        print("tracedecom_store_db(),  TR_SQLQueryTrace     [0] ", src_traced2[0])
#        print("tracedecom_store_db(),  TR_SQLQueryFilter        ", filter_relation2)
#        print("tracedecom_store_db(),  TR_SQLInsertSelCols  [0] ", insert_2[0])
        return traced_sel_cols

    def lst_add_fileid_(self, file_id, cols):
        augmented_cols = copy.deepcopy(cols)
        for c in augmented_cols:
            c.reverse()
            c.append(file_id)
            c.reverse()
        return augmented_cols

    def lst_add_2_ids_(self, file_id, query_id, cols):
        augmented_cols = copy.deepcopy(cols)
        for c in augmented_cols:
            c.reverse()
            c.append(query_id)
            c.append(file_id)
            c.reverse()
        return augmented_cols

    def lst_double_add_2_ids_(self, file_id, query_id, src_traced):
        augmented_cols = copy.deepcopy(src_traced)
        for clist in augmented_cols:
            for c in clist:
                c.reverse()
                c.append(query_id)
                c.append(file_id)
                c.reverse()
        return augmented_cols

    def store_doublelist_(self, tblnm, doublelist, glo):
        merge_list = []
        for lst in doublelist:
            for col in lst:
                merge_list.append(col)
        data_store_db_(tblnm, merge_list, glo)

    def store_singlelist_(self, tblnm, singlelist, glo):
        data_store_db_(tblnm, singlelist, glo)

