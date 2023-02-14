__author__ = 'Administrator'


def immediate_parent_(self, ss, k, j):
    len_ = len(ss)
    parent = False
    found_in_between = False
    if ss[j][3] < ss[k][3] and ss[k][4] < ss[j][4] and ss[j][1] == 0:
        parent = True
        for i in range(len_):
            if ss[j][3] < ss[i][3] and ss[i][3] < ss[k][3]:
                found_in_between = True
    return parent and not found_in_between