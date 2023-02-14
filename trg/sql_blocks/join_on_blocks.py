__author__ = 'Administrator'

from trg.tool.top_blocks  import Top_Blocks
from trg.tool.top_markers import Top_Marker
from trg.tool.splitbylist import SplitByList


class Join_On_Blocks:
    def __init__(self):
        self.top_blocks  = Top_Blocks()
        self.top_markers = Top_Marker()
        self.splitbylist = SplitByList()

    def join_on_blocks_(self, tree, glo):
        join_on_list = []

#        print("join_on_blocks,   111  tree=", tree)
        for b in tree:
            if b[5]=="join":
                top_blocks = self.top_blocks.top_blocks_(b[7],"(",")")
                top_ons    = self.top_markers.top_markers_(b[7], top_blocks, "on ")
                if not top_ons:
                    return "Error: Join without on clause: " + b[7]

                join_units = self.splitbylist.splitbylist_(b[7], top_ons)
                if len(join_units) < 2:
                    return "Error: Join fewer than 2 blocks: " + b[7]

                pair1 = [glo.sqlid, b[0], "", b[3], b[3] + top_ons[0] - 1, \
                         "join table", "clause", join_units[0], False, b[9] + 1, ""]
                glo.sqlid += 1
                join_on_list.append(pair1)
                pair2 = [glo.sqlid, b[0], "", b[3] + top_ons[0], b[3] + len(b[7]), \
                         "join on", "clause", join_units[1], False, b[9] + 1, ""]
                glo.sqlid += 1
                join_on_list.append(pair2)
        tree.extend(join_on_list)
        return tree
