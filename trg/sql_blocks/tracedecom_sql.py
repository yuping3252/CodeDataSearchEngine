__author__ = 'Administrator'

from trg.sql_blocks.identify_sql        import IdentifySQL
from trg.sql_blocks.insert_blocks       import Insert_Blocks
from trg.sql_blocks.tracedecom_query    import TraceDecomQuery
from trg.sql_blocks.tracedecom_selcols  import TraceSelectCol
from trg.sql_blocks.tracedecom_insert   import TraceDecomInsert
from trg.sql_blocks.src_filter_separate import SourceOrFilter
from trg.sql_blocks.tracedecom_store_db import TraceDecomStoreDB

class TraceDecomSQL:
    def __init__(self):
        self.identify = IdentifySQL()
        self.insert = Insert_Blocks()
        self.trace_query  = TraceDecomQuery()
        self.trace_selcol = TraceSelectCol()
        self.trace_insert = TraceDecomInsert()
        self.srcfilter = SourceOrFilter()
        self.trace_store = TraceDecomStoreDB()

    def tracedecom_sql_(self, tree, glo):
        stmt = tree[0][7].strip()
        sql_type = self.identify.identify_sql_(stmt)
        insert_ = []
        if sql_type[1] == "insert":
            query_id = 0
            cond     = 0
            filter_block_list = []
            traced_sel_cols   = []
            src_traced        = []

            [insert_type_, param_, tree_ssql, query] = self.insert.insert_blocks_(stmt, 1, glo)

            traced_cols = []
            cols_their_src = []
            if insert_type_=="insert select":
                trace_query_result = self.trace_query.tracedecom_query_(tree, query, glo)

                if type(trace_query_result) == type(""):
                    return trace_query_result
                [query_id, cond, traced_cols, cols_their_src, traced_sel_cols, src_traced, filter_block_list] = \
                    trace_query_result

                insert_ = self.trace_insert.tracedecom_insert_(query_id, tree_ssql, traced_sel_cols, insert_type_, param_, glo)
            else:
                return "SQL statement of type:  Insert into (...) values (...), skip processing for now"
        elif sql_type[1] == "select":
            trace_query_result = self.trace_query.tracedecom_query_(tree, tree[0][7], glo)

            if type(trace_query_result) == type(""):
                return trace_query_result
            [query_id, cond, traced_cols, cols_their_src, traced_sel_cols, src_traced, filter_block_list] = \
                trace_query_result

        [src_tbl_list, filter_relation] = \
            self.srcfilter.src_filter_separate_(query_id, cond, traced_cols, cols_their_src, filter_block_list, glo)

        # ------------------ store sql to database --------------------------
        # ------------------ store sql to database --------------------------
        self.trace_store.tracedecom_store_db_(query_id, insert_, traced_cols, cols_their_src, traced_sel_cols, \
                                              src_traced, src_tbl_list, filter_relation, glo)
        return tree