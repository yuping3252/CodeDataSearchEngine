#!/usr/bin/python

#----------------------------------------------------------------------------------
#               1       3   4--6   9    12  15  `17  19   21
#                      -------------     -----       --------
#                ----------------------------------

#  [[0, 1, '', 4, 6], [1, 3, '', 3, 9], [3, 0, '', 1, 17]],
#  [[2, 3, '', 12, 15], [3, 0, '', 1, 17]],
#  [[4, 0, '', 19, 21]]

def list_sort_(list_pairs):

    list1 = []
    for clause1 in list_pairs:
        list2 = [clause1]
        for clause2 in list_pairs:
            if clause1 != clause2 and clause2[3] < clause1[3] and clause1[4] <= clause2[4]:
                list2.append(clause2)
        list1.append(list2)
    print " list1=", list1
    list2 = list1
    for list_1 in list1:
        for list_2 in list1:
            if list_1 != list_2 and list_2[0][3] < list_1[0][3] and list_1[0][4] < list_2[0][4]:
                list2.remove(list_2)
    print " list2=", list2
    for list_1 in list2:
        len_ = len(list_1)-1
        for i in range(len_):
            list_1[i][1] = list_1[i + 1][0]
    return list2

list_pairs = [[0, 0, "", 4, 6], [1, 0, "", 3, 9], [2, 0, "", 12, 15], [3, 0, "", 1, 17], [4, 0, "", 19, 21]]
list_final = list_sort_(list_pairs)
print " list_final=", list_final