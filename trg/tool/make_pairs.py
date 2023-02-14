__author__ = 'Administrator'

class Make_Pairs:
    def make_pairs_(self, lefts, rights, offset):
        ss = []
        len_ = len(lefts)
        for i in range(len_):
            l_idx = lefts.pop()
            r_match_idx = 0
            cnt         = 0
            for r_idx in rights:
                if l_idx < r_idx:
                    rights[cnt] = 0
                    r_match_idx = r_idx
                    break
                cnt += 1
            pair = [0, 0, "", offset+l_idx, offset+r_match_idx, "", "", "", False, 0, ""]
            ss.append(pair)
        ss.reverse()
        return ss
