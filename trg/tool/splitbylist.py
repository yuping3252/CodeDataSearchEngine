__author__ = 'Administrator'


# top_blocks that within a string
class SplitByList:
    def __init__(self):
        i = 0

    def splitbylist_(self, sss, markerlist):
        segments = []
        if len(markerlist) >= 1:
            last_c = 0
            for c in markerlist:
                segments.append(sss[last_c:c].strip())
                last_c = c
            segments.append(sss[last_c:len(sss)].strip())
        else:
            segments = [sss]
        return segments





















