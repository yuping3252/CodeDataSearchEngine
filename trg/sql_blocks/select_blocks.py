__author__ = 'Administrator'

from trg.tool            import tree_strip
from trg.tool.tree_strip import tree_strip

class Select_Blocks:
    def __init__(self):
        self.seq = 0
        self.sf_flg = ""
        self.tree = ""

    def select_blocks_(self, tree, glo):
        self.tree = tree
        s_cols = []
        for b in self.tree:
            if b[5] == "select":
                s_cols.extend(self.select_analysis_(self.tree, b, glo))
        self.tree.extend(s_cols)
        tree_strip(self.tree)
        return self.tree

    def select_analysis_(self, tree, sblock, glo):
        commas_ = []
        le = sblock[3]
        ri = sblock[4]

#        if sblock[7].strip() == "select max( n )":
#            print "........selects_(), sblock=", sblock, ".............................................."

        # get all commas, commas are in global positions
        for p in range(ri - le):
            if sblock[7][p]==',':
                commas_.append(le + p)
        # remove inner commas
        commas = []
        commas_remove = []
        for c in commas_:
            for b in self.tree:
                if b[0] != sblock[0] and \
                   ((sblock[3] <= b[3] and b[4] < sblock[4]) or (sblock[3] < b[3] and b[4] <= sblock[4])):
                    if b[3]<=c and c<b[4]:
                        commas_remove.append(c)
        for c in commas_:
            if commas_remove.count(c) == 0:
                commas.append(c)                     # global
        # remove "select" phrase
        clen = len(commas)
        columns_ = []
        le = sblock[3]                               # global
        # one column only
        if len(commas) == 0:
            col = sblock[7][7:]
            columns_.append([le + 7, sblock[4], col])
        else:
            # multiple columns, except the last column
            p = 0                                    # local
            for i in range(clen):
                if i == 0:
                    left  = le + 7                   # global
                    right = commas[0]                # global
                    col   = sblock[7][7:commas[0] - le]
                    p     = commas[0] - le + 1       # local
                else:
                    # if this column is already a block ?
                    sub_block_exist = False
                    for b in self.tree:
                        if b[7].strip() == sblock[7][p:commas_[i] - le].strip():
                            b[6] = "column"
                            b[1] = sblock[0]
                            sub_block_exist = True
                    # not already a block, make this column a block
                    if sub_block_exist == False:
                        left  = le + p
                        right = commas[i]
                        col   = sblock[7][p:right - le]
                    p = commas[i] - le + 1           # local
                columns_.append([left, right, col])

            # last column, after last comma to the end of sblock[7]
            sub_block_exist = False
            for b in self.tree:
                if b[7].strip() == sblock[7][p:sblock[4] - le].strip():
                    b[6] = "column"
                    b[1] = sblock[0]
                    sub_block_exist = True
            # not already a block, make this column a block
            if sub_block_exist == False:
                left = le + p
                right = sblock[4]
                col = sblock[7][p:right - le]
            columns_.append([left, right, col, str(i)])
        columns = []
        for c in columns_:
            already_a_block = False
            for b in tree:
                if c[0] == b[3] and c[2] == b[7]:
                    already_a_block = True
                    break
            if already_a_block == False:
                pair = [glo.sqlid, sblock[0], "", c[0] , c[1], "expr", "column", c[2], False, sblock[9] + 1, ""]
                columns.append(pair)
                glo.sqlid += 1
        return columns
