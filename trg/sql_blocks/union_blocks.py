__author__ = 'Administrator'

from trg.tool                      import print_space_layout, tree_strip

from trg.tool.lefts_rights         import Lefts_Rights
from trg.tool.list_add_num         import list_add_num_
from trg.tool.make_pairs           import Make_Pairs
from trg.tool.print_space_layout   import Print_Layout
from trg.tool.tree_strip           import tree_strip

class Union_Blocks:
    def __init__(self):
        self.lr = Lefts_Rights()
        self.mp = Make_Pairs()
        self.print_ = Print_Layout()

    # union_blocks_() has no offset, it merely breaks into parenthenses and unioned sqls, not individually process them
    def union_blocks_(self, select_sql, level, glo):
        paren_tree = self.parentheses_(select_sql, glo)                      # coordinates in paren_tree are local
        tree1 = self.union_separate_ctr_(paren_tree, select_sql, level, glo) # paren_tree could be "No parenthensis"
        if tree1 == []:
            return tree1
        tree1 = self.nested_paren_(tree1, level, glo)
        tree1 = self.tree_index_adjust_(tree1)
        tree_strip(tree1)
        return tree1

    # all positions here are ---------------- local to sql
    def parentheses_(self, select_sql, glo):
        [lefts, rights] = self.lr.get_lefts_rights_(select_sql, '(',')')
        rights = list_add_num_(rights, 1)                            # for parenthensis, end is added 1
        if lefts == []:
            return "No parenthensis"
        paren_tree = self.mp.make_pairs_(lefts, rights, 0)           # local positions b[3], b[4]
        len_ = len(paren_tree)
        for i in range(len_):
            paren_tree[i][0]  =  glo.sqlid
            glo.sqlid   += 1
            paren_tree[i][5]  = "parenthensis"
            paren_tree[i][6]  = "parenthensis"
            paren_tree[i][7]  = select_sql[paren_tree[i][3]:paren_tree[i][4]]
            paren_tree[i][3] += glo.offset + glo.offset_select
            paren_tree[i][4] += glo.offset + glo.offset_select
        return paren_tree                                          # only missing b[1] and b[9]

    #  figure out what'include what exclude, for each block in paren_tree
    def union_separate_ctr_(self, paren_tree, select_sql, level, glo):                                                  # local tree starts here
        u_positions = []
        u_count = select_sql.count("union")
        base = glo.offset + glo.offset_select
        s = select_sql
        for i in range(u_count):
            p = s.find("union")
            u_positions.append(base + p)         # all "union"  local positions
            s     = s[p + 6:]
            base += p + 6
        tree1 = self.union_separate_thru_all_parens_(paren_tree, select_sql, u_positions, glo)
        return tree1

    def union_separate_thru_all_parens_(self, paren_tree, select_sql, u_positions, glo):
        tree1 = []                                                               # p u     !p u     p !u     !p !u
        if paren_tree == "No parenthensis":
            le = glo.offset + glo.offset_select
            ri = le + len(select_sql)
            sqls_union = self.union_separated_sql_(le, ri, select_sql, u_positions, glo)
            tree1.extend(sqls_union)
            return tree1
        else:
            u_processed = []
            # u_positions start from beginning of "select", offset_select = insert to select distance
            le = glo.offset + glo.offset_select
            top_paren = [0, 0, "", le, le + len(select_sql), "query", "may be union", select_sql, False, 0, ""]
            top_excludes   = self.excludes_areas_in_block_(top_paren, paren_tree)
            u_in_top_paren = self.eff_unions_in_block_(top_paren, u_positions, top_excludes)
            if u_in_top_paren != []:
                parenleft  = glo.offset + glo.offset_select
                parenright = parenleft + len(select_sql)
                sqls_unioned_in_top_paren = self.union_separated_sql_(parenleft, parenright, select_sql, u_in_top_paren, glo)
                tree1.extend(sqls_unioned_in_top_paren)
                u_processed.extend(u_in_top_paren)
            u_below_top = self.list_subtract_(u_positions, u_processed)
            for paren in paren_tree:
                excludes   = self.excludes_areas_in_block_(paren, paren_tree)
                u_in_paren = self.eff_unions_in_block_(paren, u_below_top, excludes)  # union in that parenthensis
                parenleft  = glo.offset + glo.offset_select + select_sql.index(paren[7])
                parenright = parenleft + len(paren[7])
                sqls_unioned_in_paren = self.union_separated_sql_(parenleft, parenright, select_sql, u_in_paren, glo)
                tree1.extend(sqls_unioned_in_paren)
                u_processed.extend(u_in_paren)
        tree1.extend(paren_tree)
        return tree1

    def excludes_areas_in_block_(self, pa, pa_tree):
        excludes = []
        for p1 in pa_tree:
            if (pa[3] < p1[3] and p1[4] < pa[4]) == False:
                continue  # make sure p1 is inside pa
            p1_top_subblock = True  # assume p1 is a top sub block ...
            len_ = 0
            pp = 0
            for p2 in pa_tree:  # p2 is sanwiched between p1 and pa,   p1 < p2 < pa
                if (p2[3] < p1[3] and p1[4] < p2[4]) == False:
                    continue
                if (pa[3] <= p2[3] and p2[4] < pa[4]) == False:
                    continue  # make sure p1 < p2 < pa
                p1_top_subblock = False  # verified p1 is not a top sub block of pa
                if p2[4] - p2[3] > len_:
                    len_ = p2[4] - p2[3]  # find the biggest such p2 that p1 < p2 < pa
                    pp = p2
            if p1_top_subblock == False:
                excludes.append([pp[3], pp[4]])  # pp is the top sub block such that p1 < pp < pa
            else:
                excludes.append([p1[3], p1[4]])  # p1 is the top sub block such that p1 < pa
        exblocks_set = set(list(map(tuple, excludes)))
        excludes_distinct = list(map(list, exblocks_set))  # list of distinct top sub blocks of pa
        return excludes_distinct

    def eff_unions_in_block_(self, pa, u_positions, excludes):
        u_this_block = []
        for u in u_positions:  # all comparisons are in global positions
            if (pa[3] < u and u < pa[4]) == False:
                continue
            excl = False  # u is inside pa
            for excb in excludes:
                if (excb[0] < u and u < excb[1]) == True:  # u is inside one of top sub blocks of pa
                    excl = True  # exclude it
                    break
            if excl == False:  # u is not inside any of the top sub blocks of pa
                u_this_block.append(u)  # list of "union"s not inside any of the top sub blocks
        return u_this_block

    # decompose sql_this, using unions
    def union_separated_sql_(self, left, right, select_sql, unions, glo):     # left, right, are distances from the "select" inside select_sql
        sqls_in_block = []
        le            = left                           # should be just 0, if paren_tree = []
        unions.append(right)                           # final u is just the end of this sql block

        if len(unions) > 1:
            uType = True
        else:
            uType = False

        for u in unions:
            ri = u - 1
            sql_ = select_sql[le - glo.offset - glo.offset_select:ri - glo.offset - glo.offset_select].strip()      # coordinates are within select stmt
            pair = [glo.sqlid, 0, "", le, ri, "query", "union", sql_, uType, 0, ""]
            sqls_in_block.append(pair)
            le = u
            glo.sqlid += 1
        return sqls_in_block                          # list of sqls inside this sql_this, separated by "union"

    def nested_paren_(self, tree, level, glo):
        len_ = len(tree)
        for b in tree:
            for i in range(len_):
                tree[i][1] = glo.sqlid_p
                tree[i][9] = level
                length_block_ = 1000000
                for j in range(len_):
                    if ((tree[j][3] <= tree[i][3] and tree[i][4] < tree[j][4])   or  \
                        (tree[j][3] < tree[i][3]  and tree[i][4] <= tree[j][4])) and \
                        length_block_ > tree[j][4] - tree[j][3]:
                        length_block_ = tree[j][4] - tree[j][3]
                        tree[i][1] = tree[j][0]
                        tree[i][9] = tree[j][9] + 1
        return tree

    def tree_next_level_(self, parent, tree):
        children = []
        for b1 in tree:
            if b1[1] == parent[0]:
                b1[9] = parent[9] + 1
                children.append(b1)
                b1go = False
                for b2 in tree:
                    if b2[1] == b1[0] and b1[0] != b1[1]:
                        b1go = True
                if b1go == True:
                    b1list = self.tree_next_level_(b1, tree)
                    children.extend(b1list)
        return children

    def tree_index_adjust_(self, tree):
        if tree[len(tree)-1] == "":
            tree.pop()
        for b in tree:
            if b[7][0] == "(" and b[7][len(b[7]) - 1] != ")":
                b[3] += 1
                b[7] = b[7][1:]
            if b[7][0:5] == "union":
                b[3] += 6
                b[7]  = b[7][6:]
        return tree

    def list_subtract_(self, list_1, list_2):
        list_subtract = []
        for u1 in list_1:
            not_used = True
            for u2 in list_2:
                if u1 == u2:
                    not_used = False
                    break
            if not_used:
                list_subtract.append(u1)
        return list_subtract
