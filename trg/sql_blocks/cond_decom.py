__author__ = 'Administrator'

from trg.sql_tool.col_search_table import ColSearchTable


class CondDecom:
    def __init__(self):
        self.cst = ColSearchTable()

    def cond_decom_(self, querytable_list, cond_list, table_cols_list, glo):
        cond_decom_list  = self.cond_decom2_(cond_list)
        cond_decom_list  = self.col_to_table_(cond_decom_list, querytable_list, table_cols_list)
        return cond_decom_list

    # cond_list = [qid, cid, w/j id, w/j type, c txt]
    def cond_decom2_(self, cond_list):
        cond_decom_list = []
        for c1 in cond_list:
            cc = c1[4].split(" and ")
            for c in cc:
                comp1 = c.find(" like ")
                comp2 = c.find(">=")
                comp3 = c.find("<=")
                comp4 = c.find("=")
                comp5 = c.find(">")
                comp6 = c.find("<")
                if comp1 > 0:
                    comp = comp1
                elif comp2 > 0:
                    comp = comp2
                elif comp3 > 0:
                    comp = comp3
                elif comp4 > 0:
                    comp = comp4
                elif comp5 > 0:
                    comp = comp5
                elif comp6 > 0:
                    comp = comp6
                left = c[:comp]
                dot = left.find(".")
                if dot > 0:
                    colleft = [left[:dot], left[dot:]]
                else:
                    colleft = ["", left]
                if comp1 > 0:
                    compsign = c[comp1:comp1 + 6].strip()
                    colright = ["expr", c[comp1 + 6:].strip()]
                else:
                    le = comp
                    if comp2 > 0 or comp3 > 0:
                        right = c[comp + 2].strip()
                        ri = comp + 2
                    else:
                        right = c[comp + 1:].strip()
                        ri = comp + 1
                    compsign = c[le:ri]
                    dot = right.find(".")
                    if dot > 0:
                        colright = [right[:dot], right[dot + 1:]]
                    else:
                        colright = ["", right]
                cleft  = self.trimcolumn_(colleft[1])
                cright = self.trimcolumn_(colright[1])
                cond = [c1[0], c1[1], c1[2],  c,    "",   colleft[0],  cleft, compsign, "", colright[0], cright]
                # cond = [qid, cond id, wid, c txt, tbl, alias, col, comp, tbl, alias, col]
                cond_decom_list.append(cond)
        return cond_decom_list

    #    c[1],   c[3],  c[4],  c[5], c[6], c[7], c[8] , c[9], c[10]]
    #   conid, con txt, tbl,  alias, col,  comp, tbl,  alias,  col
    #     17      18     19    20    21     22   23     24     25


    def col_to_table_(self, cond_decom_list, querytable_list, tables_cols_list):
        for cond in cond_decom_list:
            if cond[4] == "" and cond[5] == "":
                cond[4] = self.cst.col_search_table(tables_cols_list, cond[0], cond[6])
            else:
                for t in querytable_list:
                    if cond[0] == t[0]:
                        if cond[5] == t[2]:
                            cond[4] = cond[5]
                            cond[5] = t[4]
                            break
                        elif  cond[5] == t[4] and cond[5] != "":
                            cond[4] = t[2]
                            break
            if cond[9] == "expr":
                cond[8] = "expr"
                cond[9] = ""
            elif cond[8] == "" and cond[9] == "":
                cond[8] = self.cst.col_search_table(tables_cols_list, cond[0], cond[10])
            else:
                for t in querytable_list:
                    if cond[0] == t[0]:
                        # cond = [qid, cond id, wid, c txt, tbl, alias, col, comp, tbl, alias, col]
                        # t = [query id, tbl id, tbl, alias id, alias]
                        if cond[9] == t[2]:
                            cond[8] = cond[9]
                            cond[9] = t[4]
                            break
                        elif cond[9] == t[4] and cond[9] != "":
                            cond[8] = t[2]
                            break
        return cond_decom_list

    def trimcolumn_(self, column):
        column = column.strip().strip(".").strip(";")
        return column


