__author__ = 'Administrator'

from   trg.tool             import tree_strip
from   trg.tool.tree_strip  import tree_strip


class From_After_Blocks:
    def __init__(self):
        i = 0

    def from_after_blocks_(self, tree, block, clauseflg, glo):
        pairs = self.clause_blocks_find_(tree, block, clauseflg, glo)
        tree.extend(pairs)
        tree_strip(tree)
        return tree

    # search for all blocks of type clauseflg
    def clause_blocks_find_(self, tree, block, clauseflg, glo):  # block is one of union_paren_list, no columns, select, from

        pairs = []  # each complex select, have one tree, which have multiple parens and unions, and select, from, and columns
        for frm in tree:
            if ((block[3] <= frm[3] and frm[4] < block[4]) or (block[3] < frm[3] and frm[4] <= block[4])) == False \
                    or frm[5] != "from":
                continue
            ss = frm[7]
            cnt_clause = ss.count(clauseflg)
            if cnt_clause == 0:
                return pairs
            # frm is a "from", inside the block (, paren and unioned select, hopefully select ... from ...)
            # frm contains at least one clauseflg, such as order by
            if clauseflg == "from":
                pairs = self.from_cut_short_(tree, frm)
                break
            list_clause_ = []
            base = glo.offset + glo.offset_select + glo.offset_from
            for i in range(cnt_clause):
                clause = ss.find(clauseflg)  # offset from "from" to the beginning of clauseflg
                list_clause_.append(base + clause)
                ss = ss[clause + 1:]
                base += clause + 1

            # list of clauses, each in the list is start position of a clauseflg

            # remove every clauseflg that lies inside lower level blocks which are in frm block
            list_remove = []

            for clause in list_clause_:
                for b in tree:
                    if (frm[3] < b[3] and b[4] <= frm[4]) and (b[3] <= clause and clause < b[4]):
                        list_remove.append(clause)
                        break
            # list of clauseflg to be removed
            list_clause = []
            for clause in list_clause_:
                if list_remove.count(clause) == 0:
                    list_clause.append(clause)
            # list of top level clauseflg, hopefully only one element
            base = glo.offset + glo.offset_select + glo.offset_from

            for clause in list_clause:                    # clauses are in global positions
                endpoint1 = frm[4]
                for b in tree:
                    #  frm[  clause  b[ ] ]   endpoint
                    if  b[1] == frm[0] and (frm[3] < b[3] and b[4] <= frm[4]) and clause < b[3] < endpoint1:
                        endpoint = b[3]
                for later_clause in list_clause:
                    if clause < later_clause < endpoint1:
                        endpoint1 = later_clause - 1
                ss = frm[7][clause - base:endpoint1 - base]
                pair = [glo.sqlid, frm[0], "", clause, endpoint1, clauseflg, "clause", ss, False, frm[9] + 1, ""]
                pairs.append(pair)
                glo.sqlid += 1
        return pairs

    def from_cut_short_(self, tree, block):
        pairs = []
        if block[5] == "from":
            endpoint = 1000000
            for b in tree:
                if b[1] == block[0] and b[6] != "parenthensis" and endpoint > b[3]:
                    endpoint = b[3] - 1
            if endpoint < 1000000:
                block[4] = endpoint
                block[7] = block[7][:endpoint - block[3]]
                pairs.append(block)
        return pairs

