__author__ = 'Administrator'


class QueryTarget:
    def __init__(self):
        i = 0

    def querytarget_list_(self, query_list, select_list, column_list):
        querytrgt_list = []
        for q in query_list:
            for s in select_list:
                if s[1] == q[0]:
                    splited_col_list = s[7].split(",")
                    splist = []
                    for sp in splited_col_list:
                        sp = sp.strip().replace("select ", "")
                        splist.append(sp)
                    for c in column_list:
                        if c[1] == s[0]:
                            tblcol = c[7].split(".")
                            if len(tblcol) > 1:
                                [tbl, col] = tblcol
                            else:
                                tbl   = ""
                                [col] = tblcol
                            i = 0
                            order = "0"
                            for sp in splist:
                                if sp == col:
                                    order = str(i)
                                i += 1
                            querytrgt = [q[0], "selectcol", c[0], c[7], tbl, col, 0, "", 0, "", order, q[1], q[6]]
                            querytrgt_list.append(querytrgt)

        return querytrgt_list
    #  querytrgt=[q[0],"selectcol",c[0], c[7],  tbl,col,   0,        "",        0,       "",    order,parentid, union]
    #             qid,   "xxx",  col id,dispcol,tbl,col,repl tblid,repl tbl,insrtcolid,insrtcol,order
    #              0      1        2      3      4   5     6         7          8        9       10    11        12
    # tbl may be empty initially, or may be an alias         ^
    # repld tbl is the matching table from "from", "join" clause

