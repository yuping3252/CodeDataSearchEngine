__author__ = 'Administrator'

import copy

from trg.tool               import tree_strip, select_from_paren_strip
from trg.tool.lefts_rights  import Lefts_Rights
from trg.tool.make_pairs    import Make_Pairs
from trg.tool.merge_2_lists import Merge_2_Lists
from trg.tool.tree_strip    import tree_strip
from trg.tool.select_from_paren_strip import select_from_paren_strip



class Select_From_Blocks:
    def __init__(self):
        self.sqlid_p = 0
        self.mp = Make_Pairs()
        self.lr = Lefts_Rights()
        self.merge = Merge_2_Lists()

    def select_from_blocks_(self, tree_union, block, level, glo):    # tree_union starts from a top "select",
        tree2 = copy.deepcopy(tree_union)
        select_sql = block[7]                                        # block contains a "select ... from ..."
        tree_ = self.select_from_pairs_(tree2, select_sql, level, glo)
        tree_ = select_from_paren_strip(tree_)
        tree_strip(tree_)
        return tree_

    def select_from_pairs_(self, tree2, stmt, level, glo):   # left and right lists, respectively
        stmt = stmt.lower()
        [lst_left, lst_right] = self.lr.get_lefts_rights_(stmt,"select", "from")
        len_ = len(lst_left)
        lst_left.sort()
        lst_right.sort()
        lst_pairs_ = []
        for i in range(len_):
            le = lst_left.pop()
            for ri in lst_right:
                if le < ri:
                    lst_pairs_.append([le,ri])
                    lst_right.remove(ri)
                    break
        b0 = self.min_pair_(lst_pairs_)
        lst_pairs = []
        le = glo.offset + glo.offset_select + b0[0]     # offset to sql + offset from beginning of sql to select + ...
        ri = glo.offset + glo.offset_select + b0[1]
        glo.offset_from = b0[1]
        pair = [glo.sqlid, glo.sqlid_p, "", le, ri,  "select", "block", stmt[b0[0]:b0[1]], False, level, ""]
        lst_pairs.append(pair)
        glo.sqlid += 1
        ri2= ri + len(stmt) - b0[1]
        pair = [glo.sqlid, glo.sqlid_p, "", ri, ri2, "from","block", stmt[b0[1]:ri2], False, level, ""]
        lst_pairs.append(pair)                                       # list of "select ... from ..." pairs
        tree2.extend(lst_pairs)                                      # merge to a copy of tree_union
        glo.sqlid += 1
        return tree2

    def min_pair_(self, lst_pairs):
        max_ = 1000000
        bb = 0
        for b in lst_pairs:
            if max_ > b[0]:
                max_ = b[0]
                bb = b
        return bb
