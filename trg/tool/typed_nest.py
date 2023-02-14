__author__ = 'Administrator'


class TypedNest:
    def __init__(self):
        i = 0

    def typed_nest_(self,typed_block_list, type_, stop_type_, tree):
        typed_lists = []
        for tb in typed_block_list:
            exist = False
            for list1 in typed_lists:
                if list1.count(tb) > 0:
                    exist = True
                    break
            if not exist:
                tb_list = self.tb_list_(tb, type_, stop_type_, tree)
                typed_lists = self.list_merge_(typed_lists, tb_list)
        return typed_lists

    def list_merge_(self, typed_lists, tb_list):
        i = 0
        for list1 in typed_lists:
            if list1.count(tb_list[0]) > 0:
                return typed_lists
            if tb_list.count(list1[0]) > 0:
                typed_lists[i] = tb_list
                return typed_lists
            i += 1
        typed_lists.append(tb_list)
        return typed_lists

    def tb_list_(self, tb, type_, stop_type_, tree):
        len_tree = len(tree)
        tb_list = [tb]
        for i in range(len_tree):
            for j in range(len_tree):
                if tb[1] == tree[j][0]:
                    if tree[j][2] == type_ or tree[j][2] == stop_type_:
                        tb_list.append(tree[j])
                    tb = tree[j]
                    break
            if tb[2] == stop_type_:
                break
        return tb_list


if __name__=='__main__':
    typed_list = [[9,8,"q"], [11,10,"q"], [12,5,"q"]]
    tree = [[0,0,"c"],[1,0,"q"], [2,1,"t"], [3,0,"q"], [4,1,"q"], [5,3,"q"], [7,5,"q"], [8,2,"t"], [9,8,"q"], [10,9,"t"], [11,8,"q"], [11,10,"q"], [12,5,"q"]]
    tynst = TypedNest()

    print (typed_list)
    print ("**************** 111")
    print (tree)
    typed_lists = tynst.typed_nest_(typed_list, "q", "c", tree)
    print ("**************** 222")
    print (typed_lists)






