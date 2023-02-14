__author__ = 'Administrator'

from trg.tool.lefts_rights import Lefts_Rights
from trg.tool.make_pairs   import Make_Pairs

# top_blocks that within a string
class Top_Blocks:
    def top_blocks_(self, stringsss, le, ri):
        lefts_rights = Lefts_Rights()
        make_pairs   = Make_Pairs()
        [lefts,rights] = lefts_rights.get_lefts_rights_(stringsss, le, ri)
        if len(lefts) == 0:
            return []
        pairlist   = make_pairs.make_pairs_(lefts, rights, 0)
        candidates = []
        for pair in pairlist:
            candidates.append([pair[3],pair[4]])
        sortedlist = sorted(candidates)
        topblocks = [sortedlist[0]]
        i = 0
        for b in sortedlist:
            if topblocks[i][1] < b[0]:
                topblocks.append(b)
                i += 1
        return topblocks




















