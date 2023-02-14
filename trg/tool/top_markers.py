__author__ = 'Administrator'


# top_blocks that within a string
class Top_Marker:
    def top_markers_(self, stringsss, top_blocks, marker_passedin):
        len_ = len(marker_passedin)
        sss = "&&&&&&&&&&"
        marker = sss[:len_]
        sss = stringsss.replace(marker_passedin, marker)
        cnt = sss.count(marker)
        base = 0
        markers = []
        for i in range(cnt):
            idx1 = sss.find(marker)
            markers.append(base + idx1)
            sss = sss[idx1 + 1:]
            base += idx1 + 1
        if top_blocks==[]:
            return markers
        top_markers = []
        for c in markers:
            top_marker = True
            for b in top_blocks:
                if b[0] < c < b[1]:
                    top_marker = False
                    break
            if top_marker:
                top_markers.append(c)
        return top_markers





















