__author__ = 'Administrator'

class QueryTable:
    def __init__(self):
        i = 0

    def querytable_list_(self, query_list, \
                         from_list, from_alias_table_list, from_alias_alias_list, from_only_table_list,\
                         join_list, join_table_list, join_alias_table_list, join_alias_alias_list,\
                         join_only_table_list, where_list, join_on_list, condition_list):
        querytable_list = []
        cond_list = []
        for q in query_list:
            for f in from_list:
                if f[1] == q[0]:
                    for t in from_alias_table_list:
                        if t[1] == f[0]:
                            for a in from_alias_alias_list:
                                if a[1] == f[0] and a[2] == t[2]:
                                    querytable = [f[1], t[0], t[7], a[0], a[7]]
                                    querytable_list.append(querytable)
                    for t in from_only_table_list:
                        if t[1] == f[0]:
                            querytable = [f[1], t[0], t[7], 0, ""]
                            querytable_list.append(querytable)
                    for j in join_list:
                        if j[1] == f[0]:
                            for jt in join_table_list:
                                if jt[1] == j[0]:
                                    for jtt in join_alias_table_list:
                                        if jtt[1]==jt[0]:
                                            for jta in join_alias_alias_list:
                                                if jta[1]==jt[0] and jta[2]==jtt[2]:
                                                    querytable = [q[0], jtt[0], jtt[7], jta[0], jta[7]]
                                                    querytable_list.append(querytable)
                                    for jto in join_only_table_list:
                                        if jto[1]==jt[0]:
                                            querytable = [q[0], jto[0], jto[7], 0, ""]
                                            querytable_list.append(querytable)
                            for jo in join_on_list:
                                if jo[1] == j[0]:
                                    for c in condition_list:
                                        if c[1] == jo[0]:
                                            cond = [q[0], c[0], jo[0], jo[5], c[7]]
                                            if cond_list.count(cond)==0:
                                                cond_list.append(cond)
                    for w in where_list:
                        if w[1] == f[0]:
                            for c in condition_list:
                                if c[1] == w[0]:
                                    cond = [q[0], c[0], w[0], w[5], c[7]]
                                    if cond_list.count(cond) == 0:
                                        cond_list.append(cond)
        return querytable_list, cond_list

    #  querytrgt = [q[0], "selectcol", c[0],     c[7],      tbl,  col,      0,         "",          0,        ""]
    #               qid,     "xxx",   col id, display col,  tbl,  col, repld tblid, replid tbl, insrtcolid, insrtcol
    #                0         1         2        3          4     5        6           7           8          9
    #
    # tbllist    t =  [q[0], t[0], t[7], a[0], a[7]]    <-- querytable_list
    #                 qid, tblid, tbl,  a id,  alias
    # tblcolslist= { [query id,  tbl id, tbl,     cols] }
    #                   qid,     tblid,  tbl,  [col, col, ...]
    #
    # clist      c = [qid, cond id, wid, c txt, tbl, alias, col, comp, tbl, alias, col]
    #                  0     1       2     3     4     5     6    7     8     9     10
