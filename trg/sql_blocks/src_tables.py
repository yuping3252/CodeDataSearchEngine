__author__ = 'Administrator'

from trg.tool.lefts_rights import Lefts_Rights
from trg.tool.make_pairs   import Make_Pairs
from trg.tool.top_blocks   import Top_Blocks
from trg.tool.top_markers  import Top_Marker
from trg.tool.splitbylist  import SplitByList
from trg.tool.tablelist    import TableList

try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

class Src_Tables:
    def __init__(self):
        self.seq = 0
        self.lefts_rights = Lefts_Rights()
        self.make_pairs   = Make_Pairs()
        self.top_blocks   = Top_Blocks()
        self.top_markers  = Top_Marker()
        self.splitbylist  = SplitByList()
        self.tablelist    = TableList()

    def sourcetbls_(self, tree, from_or_join, glo):
        paren_list = []
        for b in tree:
            if b[5] == "parenthensis":
                paren_list.append(b)
        table_list = []
        for b in tree:
            if b[5] == from_or_join:
                top_blocks  = self.top_blocks.top_blocks_(b[7], "(", ")")
                top_commas  = self.top_markers.top_markers_(b[7], top_blocks, ",")
                table_units = self.splitbylist.splitbylist_(b[7], top_commas)
                tbllist     = self.tablelist.tablelist_(table_units)
                table_list.append([b, tbllist])
        new_list = []
        for t in table_list:                     # [[b, [ [t,a], [t], [t], [t, a] ...] ], [b, [[t,a],[t]...]]... ]
            b = t[0]
            tbllist = t[1]                        # tbllist  = [ [t,a], [t], [t], [t, a] ... ]
            base = b[3] + 5
            new_list1 = []
            seq = 0
            for tbl_unit in tbllist:             # tbl_unit = [t, a]   or [t]
                tbl = tbl_unit[0].strip()         # tbl      =  t
                len_tblnm = len(tbl)
                if tbl[0] == "(" and tbl[-1] == ")":
                    for p in paren_list:
                        if p[7] == tbl:
                            p[1] = b[1]
                            p[6] = "table"
                            tbl = p
                            break
                if len(tbl_unit) == 1:           # table no alias
                    if b[5] == "from":
                        typ_ = "from table only"
                    else:
                        typ_ = "join table only"
                    if not isinstance(tbl, basestring):
                        tbl[1] = b[0]
                        tbl[5] = typ_
                    else:
                        pair1 = [glo.sqlid,b[0],str(seq),base,base+len(tbl),typ_,"table",tbl,False,b[9]+1,""]
                        glo.sqlid += 1
                        new_list1.append(pair1)
                    base += len_tblnm + 2
                else:                           # table has alias
                    base1 = base + len(tbl)
                    if b[5] == "from":
                        typ_ = "from table alias"
                    else:
                        typ_ = "join table alias"
                    if not isinstance(tbl, basestring):
                        tbl[1] = b[0]
                        tbl[2] = str(seq)
                        tbl[5] = typ_
                    else:
                        pair1 = [glo.sqlid, b[0], str(seq), base, base1, typ_, "table", tbl, False, b[9]+1, ""]
                        glo.sqlid += 1
                        new_list1.append(pair1)
                    base += len_tblnm + 1
                    base2 = base + len(tbl_unit[1].strip())
                    pair2 = [glo.sqlid, b[0], str(seq), base, base2, typ_, "alias", tbl_unit[1], False, b[9]+1, ""]
                    glo.sqlid += 1
                    new_list1.append(pair2)
                    base += len(tbl_unit[1].strip()) + 2
                seq += 1
            new_list.extend(new_list1)
        tree.extend(new_list)
        return tree
