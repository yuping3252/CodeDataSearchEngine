__author__ = 'Administrator'
from trg.tool.lefts_rights import Lefts_Rights
from trg.tool.make_pairs   import Make_Pairs
from trg.tool.top_blocks   import Top_Blocks
from trg.tool.top_markers  import Top_Marker
from trg.tool.splitbylist  import SplitByList
from trg.tool.tablelist    import TableList

class Src_Tables:
    def __init__(self):
        self.seq = 0
        self.lefts_rights = Lefts_Rights()
        self.make_pairs   = Make_Pairs()
        self.top_blocks   = Top_Blocks()
        self.top_markers  = Top_Marker()
        self.splitbylist  = SplitByList()
        self.tablelist    = TableList()

    def sourcetbls_(self, data, from_or_join, glo):
        tablelist = []
        for row in data:
            if row[5] == from_or_join:
                top_blocks  = self.top_blocks.top_blocks_(row[7], "(", ")")
                top_commas  = self.top_markers.top_markers_(row[7], top_blocks, ",")
                table_units = self.splitbylist.splitbylist_(row[7], top_commas)
                tbllist     = self.tablelist.tablelist_(table_units)
                tablelist.extend(tbllist)
        return tablelist
