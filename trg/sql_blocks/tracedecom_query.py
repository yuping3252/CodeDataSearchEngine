__author__ = 'Administrator'

from trg.sql_blocks.querytarget_list   import QueryTarget
from trg.sql_blocks.querytable_list    import QueryTable
from trg.sql_blocks.querycombo_list    import QueryCombo
from trg.sql_blocks.tblcol_match       import TableColMatch
from trg.sql_blocks.typed_block_lists  import TypedBlocks
from trg.sql_blocks.cond_decom         import CondDecom
from trg.sql_blocks.tracedecom_selcols import TraceSelectCol
from trg.sql_blocks.col_src_trace      import ColumnSourceTrace
from trg.sql_tool.table_columns_db     import TableColumns

class TraceDecomQuery:
    def __init__(self):
        self.qt = QueryTarget()
        self.qtb = QueryTable()
        self.qco = QueryCombo()
        self.tcm = TableColMatch()
        self.tb = TypedBlocks()
        self.cd = CondDecom()
        self.tc = TableColumns()
        self.sc = TraceSelectCol()

    def tracedecom_query_(self, tree, query, glo):
        [query_list, query_nested, select_list, column_list,\
         from_list, from_alias_table_list, from_alias_alias_list, from_only_table_list,\
         join_list, join_table_list, join_alias_table_list, join_alias_alias_list,\
         join_only_table_list, where_list, join_on_list, condition_list] \
            = self.tb.typed_block_lists_(tree, query)
        query_id = self.query_id_(query_list, query)
        querytrgt_list  = self.qt.querytarget_list_(query_list, select_list, column_list)
        [querytable_list, cond_list] = self.qtb.querytable_list_(query_list,\
                    from_list, from_alias_table_list, from_alias_alias_list, from_only_table_list, \
                    join_list, join_table_list, join_alias_table_list, join_alias_alias_list,\
                    join_only_table_list, where_list, join_on_list, condition_list)

        table_cols_list_with_None = self.tc.table_columns_db_(querytable_list, glo)
        table_cols_list = []
        for tbl in table_cols_list_with_None:
            if tbl[3]:
                table_cols_list.append(tbl)                                          #-------- selective --------
        
        if len(table_cols_list) < len(table_cols_list_with_None):
            print("tracedecom_query.py,   table_cols_list=", table_cols_list)
            return "tracedecom_query.py,  No access to database"

        conddecom_list  = self.cd.cond_decom_(querytable_list, cond_list, table_cols_list, glo)

        combo_list      = self.qco.querycombo_list_(querytrgt_list, querytable_list, table_cols_list, conddecom_list)
        traced_cols     = self.trace_multi_level_(combo_list, query_nested, table_cols_list)

        [cols_their_src, traced_sel_cols] = self.column_match_(tree, traced_cols, query_nested)

        self.colsrc_trace = ColumnSourceTrace()
        [src_traced, filter_block_list]   = self.colsrc_trace.cols_src_trace_(cols_their_src)
        # src_traced:        [complex query id,   qid,   selcolpos,   colpos,   table,   col]

        return query_id, conddecom_list, traced_cols, cols_their_src, traced_sel_cols, src_traced, filter_block_list

#   output columns (9 element now):
#   [12,       'test_t2', 't2', 'c21',       [],            '0',          10,           'union',        33]
#    query id,   table,  alias, column, lower blocks id,  col pos order, upper block, type of query,  union pos

#    reverse tracing:
#    col [ [query, col, colpos], [query, col, colpos], ... ]

    def query_id_(self, query_list, query):
        for q in query_list:
            if q[7] == query:
                this_query_block = q
        return this_query_block[0]
        return src_traced

    def column_match_(self, tree, traced_cols, query_nested):
        upper_blocks = []
        for col in traced_cols:
            if upper_blocks.count(col[6]) == 0:
                upper_blocks.append(col[6])
        traced_cols = self.query_order_in_union_(tree, upper_blocks, traced_cols)

        traced_sel_cols = self.sc.trace_sel_cols_(query_nested, traced_cols)
        traced_sel_cols.sort(key=lambda x: x[5])

        cols_their_src = []
        for upid in upper_blocks:
            union_ = self.union_or_query_(upper_blocks, upid, traced_cols)
            colpos_num_ = self.col_pos_count_(upid, traced_cols)
            cols_at_pos_lists = self.allcolpos_(upid, colpos_num_, traced_cols)

            # double list, represents all queries within a block (upper block)
            # within a block may be a query, or unioned queries
            # each inner list represents one select column position in one block,

            for col_tables in cols_at_pos_lists:
                col_its_src = []
                for c in col_tables:
                    col_its_src.append(c)
                col_its_src.sort(key=lambda x:x[8])
                cols_their_src.append(col_its_src)
#            print "---    union cols_their_src=", cols_their_src
            # cols_their_src: double list of output columns, 9 element each
            # query id,table,alias,column,lower blocks id,col pos order,upper block,type of query,union pos

        return cols_their_src, traced_sel_cols

    def query_order_in_union_(self, tree, upper_blocks, traced_cols):
        for upid in upper_blocks:
            this_query = []
            for q in tree:
                if q[0] == upid:
                    this_query = q
            for c in traced_cols:
                if c[6] == upid:
                    for t in tree:
                        if t[0] == c[0]:
                            pos = this_query[7].find(t[7])
                            c.append(pos)
                            break
        return traced_cols

    def allcolpos_(self, upid, colpos_num_, traced_cols):
        allcolpos = []
        for colpos_num in range(colpos_num_):
            colpos = []
            for col in traced_cols:
                if upid == col[6] and colpos_num == int(col[5]):
                    colpos.append(col)
            allcolpos.append(colpos)
        return allcolpos

    def col_pos_count_(self, upid, traced_cols):
        colpos = []
        for col in traced_cols:
            if upid == col[6]:
                if colpos.count(col[5]) == 0:
                    colpos.append(col[5])
        colpos_num_ = len(colpos)
        return  colpos_num_

    def union_or_query_(self, upper_blocks, upid, traced_cols):
        col_blocks = []
        for col in traced_cols:
            if col[6] == upid and col_blocks.count(col) == 0:
                col_blocks.append(col)
        cols = []
        for colblock in col_blocks:
            if cols.count(colblock[3]) == 0:
                cols.append(colblock[3])
        union_ = False
        tablecount = []
        type_ = ""
        for col in cols:
            for c in col_blocks:
                if col == c[3]:
                    if tablecount.count(c[1]) == 0:
                        tablecount.append(c[1])
                    type_ = c[7]
        if len(tablecount) > 1 and type_ == "union":
            union_ = True
        return union_

    def trace_multi_level_(self, combo_list, query_nested, table_cols_list):
        multi_lvl_lst = []
        for combo in combo_list:
            one_lvl_lst = self.trace_one_level_(combo_list, query_nested, table_cols_list, combo)
            for one in one_lvl_lst:
                if multi_lvl_lst.count(one) == 0 and one != []:
                    multi_lvl_lst.append(one)
        for m in multi_lvl_lst:
            if m[1] == "" or m[1][0] == "(" and m[1][-1] == ")":
                m = self.recur_(multi_lvl_lst, m)
        return multi_lvl_lst

    def recur_(self, multi_lvl_lst, m):
        subid = m[4]
        found = False
        for s in subid:
            for m1 in multi_lvl_lst:
                if s == m1[0]:
                    if m[3] == m1[3]:
                        if m1[1] == "" or m1[1][0] == "(" and m1[1][-1] == ")":
                            m1 = self.recur_(multi_lvl_lst, m1)
                            m[1] = m1[1]
                        else:
                            m[1] = m1[1]
        return m

    #  combo= (in same combo means in the same query block)
    #  q[4] != "" means in the select clause, a column is in the form of "table.column"
    # [q[0],  q[2],    q[3],    q[4],  q[5],     q[6],      q[7],     q[8],     q[9],    q[10],     "t=",
    #  qid, col-id, disply col, tbl,   col,  repld tblid, repld tbl, insrt id,insrtcol,  order,     "t=",
    #   0     1       2          3      4         5          6         7         8        9          10

    #   t[1],  t[2], t[3],  t[4],  [],           "c=",
    #  tblid,  tbl,  aid,  alias, subquerycols   "c=",
    #    11     12    13     14    15             16

    #    c[1],   c[3],  c[4],  c[5], c[6], c[7], c[8] , c[9], c[10]], q[11]
    #   conid, con txt, tbl,  alias, col,  comp, tbl,  alias,  col,    union or not
    #     17      18     19    20    21     22   23     24     25      26

    def trace_one_level_(self, combo_list, query_nested, table_cols_list, c):
        one_level_list = []
        if c[3] != "":                                                 # has tbl, select col is in the form of ... tbl.col
            for c1 in combo_list:
                if c[0] == c1[0] and c[1] == c1[1]:                    # query id = query id, col id = col id
                    if c[3] == c1[12] or c[3] == c1[14]:               # tbl = tbl or tbl = alias
                        c[5] = c1[11]                                   # replaced tbl id
                        c[6] = c1[12]                                   # replaced tbl
                        next_lvl_blocks = self.next_lvl_blocks_(query_nested, c)   # find next level blocks
                        a = [c[0], c1[12], c1[14], c[4], next_lvl_blocks, c1[9], c1[26], c1[27]]
                        if one_level_list.count(a) == 0:
                            one_level_list.append(a)
                        break
        else:                                                          # no tbl, select col is in the form of ... col
            matching_table_found = False
            for c1 in combo_list:
                if c[0] == c1[0] and c[1] == c1[1] and c[2] == c1[2] and c[4] == c1[21]:  # c[4] = condition left
                # same query, same col id, same col, select col = condition right col
                    matching_table_found = True
                    c[6] = c1[19]
                    next_lvl_blocks = self.next_lvl_blocks_(query_nested, c)
                    a = [c[0], c1[19],c1[20], c[4], next_lvl_blocks, c1[9], c1[26], c1[27]]
                    if one_level_list.count(a) == 0:
                        one_level_list.append(a)
                    break
            if not matching_table_found:
                for c1 in combo_list:
                    if c[0] == c1[0] and c[1] == c1[1] and c[2] == c1[2] and c[4] == c1[25]: # c[4] = condition right
                    # same query, same col id, same col, select col = condition right col
                        matching_table_found = True
                        c[6] = c1[23]
                        next_lvl_blocks = self.next_lvl_blocks_(query_nested, c)
                        a = [c[0], c1[23], c1[24], c[4], next_lvl_blocks, c1[9], c1[26], c1[27]]
                        if one_level_list.count(a) == 0:
                            one_level_list.append(a)
                        break
            if not matching_table_found:
                for c1 in combo_list:
                    if c[0] == c1[0] and c[1] == c1[1] and c[2] == c1[2]:    # same query, same col id, same col
                        if self.tcm.tblcol_match_(table_cols_list, c[4], c1[12]): # select col is not in condition
                            matching_table_found = True
                            c[6] = c1[12]                                     # select col is a col of table in from
                            next_lvl_blocks = self.next_lvl_blocks_(query_nested, c)
                            a = [c[0], c1[12], c1[14], c[4], next_lvl_blocks, c1[9], c1[26], c1[27]] # [qid, table, alias, sel col]
                            if one_level_list.count(a) == 0:
                                one_level_list.append(a)
                            break
            if not matching_table_found:
                next_lvl_blocks = self.next_lvl_blocks_(query_nested, c)
                a = [c[0], "", "", c[4], next_lvl_blocks, c[9], c[26], c[27]]
                if one_level_list.count(a) == 0:
                    one_level_list.append(a)
        return one_level_list
        # one level =  [ qid,  tbl,  alias, col, [sub query block ids], col order, parent id, union ]

    def next_lvl_blocks_(self, query_nested, combo):
        qid_list = []
        for qlist in query_nested:
            i = 0
            len_ = len(qlist)
            if len_ > 1:
                for i in range(len_):
                    if i < len_ - 1:
                        if qlist[i+1][0] == combo[0]:
                            if qid_list.count(qlist[i][0])==0:
                                qid_list.append(qlist[i][0])
                            break
                    i += 1
        return qid_list
