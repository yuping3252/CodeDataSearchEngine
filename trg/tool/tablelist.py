__author__ = 'Administrator'

from trg.tool.top_blocks   import Top_Blocks
from trg.tool.top_markers  import Top_Marker
from trg.tool.splitbylist  import SplitByList


# top_blocks that within a string
class TableList:
    def __init__(self):
        self.top_blocks  = Top_Blocks()
        self.top_markers = Top_Marker()
        self.splitbylist = SplitByList()


    def tablelist_(self, table_units):
        tablelist = []
        for tu in table_units:
            tu = tu.strip()
            if tu[:4]=="from":
                tu = tu[5:]
            if tu[:4]=="join":
                tu = tu[5:]
            if tu[0]==",":
                tu = tu[1:]
                tu = tu.strip()
            top_blocks = self.top_blocks.top_blocks_(tu, "(", ")")
            top_spaces = self.top_markers.top_markers_(tu, top_blocks, " ")
            tu_decomp  = self.splitbylist.splitbylist_(tu, top_spaces)
            tablelist.append(tu_decomp)
        return tablelist
