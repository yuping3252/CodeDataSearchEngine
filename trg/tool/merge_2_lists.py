__author__ = 'Administrator'

class Merge_2_Lists:

    def merge_2_lists_(self, list_1eft_, list_right_):
        listm = []
        list1 = []
        list2 = []
        len1 = len(list_1eft_)
        len2 = len(list_right_)
        for i in range(len1):
            list1.append(list_1eft_[i])
        for i in range(len2):
            list2.append( list_right_[i])
        len_ = len1 + len2
        for k in range(len_):
            one_or_two = 1
            index = -1
            m = 0
            for i in range(len1):
                for j in range(len2):
                    if m < list1[i]:
                        m = list1[i]
                        one_or_two = 1
                        index = i
                    if m < list2[j]:
                        m = list2[j]
                        one_or_two = 2
                        index = j
            listm.append(m)
            if one_or_two == 1:
                list1[index] = 0
            else:
                list2[index] = 0
        listm.reverse()
        return listm
