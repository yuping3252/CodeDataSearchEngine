import copy


class FindNodeID:
    def __init__(self):
        i = 1

    def nodeid(self, nodelist, path_, searchText):
        node = []
        for n in nodelist:
            if n[5][6] == path_ + '\\' + searchText and n[5][7] == searchText:
                node = n
                return node
        return []
