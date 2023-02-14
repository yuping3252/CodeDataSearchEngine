__author__ = 'Administrator'

class SourceOrFilter:
    def __init__(self):
        i = 1

    def src_filter_separate_(self, query_id, conddecoms, traced_cols, cols_their_src, filter_block_list, glo):
        src_table_list = []
        for position_colslist in cols_their_src:
            for col in position_colslist:
                IsSource = True
                for f in filter_block_list:
                    if col[1] == f[1]:
                        IsSource = False
                if IsSource:
                    if src_table_list.count([query_id, col[1]]) == 0:
                        src_table_list.append([query_id, col[1]])
        filter_relation = []

        # filter_block_list:   [qid, tbl, alias, col, [...], colpos, upper id, union, offset]
        # conddecoms:          [qid,  cond id,  wid,  c txt,  tbl,  alias,  col,  comp,  tbl,  alias,  col]

        for b in filter_block_list:
            for c in conddecoms:
                if b[3] == c[6]:
                    filter_relation.append([query_id, c[0], c[1], c[2], c[3], c[7], b[1], b[3], c[4], c[6], c[8], c[10]])
                if b[3] == c[10]:
                    filter_relation.append([query_id, c[0], c[1], c[2], c[3], c[7], b[1], b[3], c[8], c[10], c[4], c[6]])
                    #    qid, cond id, wid, c txt, cmp, tbl, col, tbl, col, tbl, col
        new_relation = []
        for b in filter_block_list:
            has_cond = False
            for fr in filter_relation:
                if b[1] == fr[6] and b[3] == fr[7]:
                    has_cond = True                 # this b is in filter_relation, skip
            if has_cond == False:                   # process [54, 'test_t3', '', 'c32', [], '0', 52, 'union', 1]
                for clist in cols_their_src:
                    this_clist = False
                    for c in clist:                # [50, 'test_t1', 't1', 'c11', [53], '0', 48, 'query', 21]
                        if b == c:
                            this_clist = True       # found the inner list, each in this inner list are unioned
                            break
                    if this_clist:
                        b0 = clist[0]               # 1st, which has the name of columns for all queries in inner list
                        for fr in filter_relation:
                            if b0[1] == fr[6] and b0[3] == fr[7]:
                                new_b = [fr[0], fr[1], 0, 0, fr[4], fr[5],  b[1], b[3], fr[6], fr[7], fr[10], fr[11]]
                                new_relation.append(new_b)
            filter_relation.extend(new_relation)
        return src_table_list, filter_relation
