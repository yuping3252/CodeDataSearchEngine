__author__ = 'Administrator'


def parenthesis_process(statement):
    pth_list_left  = []
    pth_list_right = []
    parenthl_cnt = statement.count('(')
    parenthr_cnt = statement.count(')')
    if not parenthl_cnt or parenthl_cnt != parenthr_cnt:
        return
    s = statement
    accumposition = 0
    for i in range(parenthl_cnt):
        idx = s.find('(')
        s   = s[idx+1:]
        pth_list_left.append(idx + accumposition)
        accumposition    = idx + accumposition + 1

    s = statement
    accumposition = 0
    for i in range(parenthr_cnt):
        idx = s.find(')')
        s   = s[idx+1:]
        pth_list_right.append(idx + accumposition)
        accumposition    = idx + accumposition + 1

    return


