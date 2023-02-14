__author__ = 'Administrator'

from trg.sql_blocks.tblcol_match import TableColMatch



class QueryCombo:
    def __init__(self):
        self.tcm = TableColMatch()

    def querycombo_list_(self,trgtlist, tbllist, tblcolslist, clist):
        combo_list = []
        for q in trgtlist:                                       # for each select col ......
            combined = False
            hascondition = False
            for t in tbllist:                                    # for each from table ......
                if q[0] == t[0]:                                 # a select col and a from table are in the same query
                    for c in clist:                              # for each condition ......
                        if q[0] == c[0]:                         # a select col and a condition are in the same query
                            hascondition = True
                            if t[2] == c[4] or t[2] == c[8]:     # a query table matches cond left table or right table
                                combo = [q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], "t=",\
                                         t[1], t[2], t[3], t[4], [], "c=",\
                                         c[1], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], q[11], q[12]]
                                combined = True
                                if combo_list.count(combo) == 0:
                                    combo_list.append(combo)
            if not hascondition:
                for t in tbllist:
                    if q[0] == t[0]:                             # a select col and a from table are in the same query
                        if self.tcm.tblcol_match_(tblcolslist, q[5], t[2]):   # q[5]=col,  t[2]=tbl
                            combo = [q[0], q[2], q[3], q[4], q[5], q[6], q[7],  0, "", q[10], "t=",\
                                     t[1], t[2], t[3], t[4], [], "c=",\
                                       0,   "",   "",   "",   "", "", "", "", "", q[11], q[12]]
                            combined = True
                            if combo_list.count(combo) == 0:
                                combo_list.append(combo)
            if combined == False:
                combo = [q[0], q[2], q[3], q[4], q[5], q[6], q[7], 0, "", q[10], "t=",\
                         0, "", 0, "", [], "c=", \
                         0, "", "", "", "", "", "", "", "", q[11], q[12]]
                if combo_list.count(combo) == 0:
                    combo_list.append(combo)
        return combo_list

        #  combo= (in same combo means in the same query block)
        #  q[4] != "" means in the select clause, a column is in the form of "table.column"
        # [q[0],  q[2],    q[3],    q[4],  q[5],     q[6],      q[7],     q[8],     q[9],    q[10],     "t=",
        #  qid, col-id, disply col, tbl,   col,  repld tblid, repld tbl, insrt id,insrtcol,  order,     "t=",
        #   0     1       2          3      4         5          6         7         8        9          10

        #   t[1],  t[2], t[3],  t[4],  [],           "c=",
        #  tblid,  tbl,  aid,  alias, subquerycols   "c=",
        #    11     12    13     14    15             16

        #    c[1],   c[3],  c[4],  c[5], c[6], c[7], c[8] , c[9], c[10]],  q[11],      q[12]
        #   conid, con txt, tbl,  alias, col,  comp, tbl,  alias,  col,  parent id,  union or not
        #     17      18     19    20    21     22   23     24     25,       26,         27
