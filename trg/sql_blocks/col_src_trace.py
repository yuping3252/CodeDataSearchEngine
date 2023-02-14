__author__ = 'Administrator'


class ColumnSourceTrace:
    def __init__(self):
        i = 1

    def cols_src_trace_(self, doublelist):
        src_traced = []
        firstblockid = doublelist[0][0][0]
        i = 0
        for a_sel_col in doublelist:
            if a_sel_col[0][0] == firstblockid:
                a_sel_col_traced = self.trace_a_sel_col_(a_sel_col, doublelist)
                src_traced.append(a_sel_col_traced)

        filter_block_list = []
        for dlist in doublelist:
            for d in dlist:                        # d = [123, 'test_t4', 't41', 'c41', [], '0', 119, 'union', 1]
                filter = True
                for tlist in src_traced:
                    for t in tlist:                # t = [120, '0', 'test_t2', 'c21']
                        if d[1] == t[2]:
                            filter = False
                if filter == True:
                    filter_block_list.append(d)

        selcol_pos = 0
        for a_selcol_col_chain in src_traced:
            for c in a_selcol_col_chain:
                c.insert(1, selcol_pos)
            selcol_pos += 1

        return src_traced, filter_block_list
    # src_traced:            complex query id, qid,     selcolpos, colpos,     table, col
    # filter_block_list:     qid,  table,  alias, col, subquery,  colpos, upperblock, union, offset

    def trace_a_sel_col_(self, a_sel_col, doublelist):    # just process one row (unioned queries) of cols_their_src
        src_cols_traced = []
        for a_src_col in a_sel_col:
            a_src_col_traced = self.trace_a_src_col_(a_src_col, doublelist)
            src_cols_traced.extend(a_src_col_traced)
        return src_cols_traced

    def trace_a_src_col_(self, col, doublelist):    # just process one col in one row (unioned queries) of cols_their_src
        col_traced = [[col[0], col[5], col[1], col[3]]]
        for subblock in col[4]:
            for clist in doublelist:
                for c in clist:
                    if c[0] == subblock:
                        if c[3] == col[3]:
                            col_traced1 = self.trace_a_sel_col_(clist, doublelist)
                            for col_ in col_traced1:
                                if col_traced.count(col_) == 0:
                                    col_traced.append(col_)
        return col_traced