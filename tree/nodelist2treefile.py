import os, sys
import types
import json
import logging

class NodeList2TreeFile:
    def __init__(self):
        sys.setrecursionlimit(6000)
        self.nodelist       = []
        self.root_list      = []
        self.root_pair_list = []
        self.nodelistprint  = []
        self.rootcnt        = 0
        self.dots = "                                                                                                                                 "


    # ------------ filtering to obtain all nodes for one root ----------

    def nodelistfilter_(self, nodelist, rootpath_):
        self.nodelist = nodelist
        nodelist_root = []
        for node in nodelist:
            if node[2] == 'root' and type(node[5]) == type([]) and node[5][6] == rootpath_:
                nodelist_root.append(node)
                break
        self.list_one_root = []
        for root in nodelist_root:
            self.recur_one_root(root)
        return self.list_one_root


    def nodelist2treefile_(self, nodelist):
        if nodelist == []:
            self.treefileprint_([])
            return
        self.nodelist = nodelist
        for node in self.nodelist:
            if node[2] == 'root':
                self.root_list.append(node)
        for root in self.root_list:
            root_pair = self.recur_list_(root)
            self.root_pair_list.append(root_pair)
        for root_pair in self.root_pair_list:
            self.treefileprint_(root_pair)


    # -------------------- build a tree structured list -----------------------
    def recur_list_(self, parent):
        childlist = []
        children  = []
        for node in self.nodelist:
            if parent[0] == node[1] and parent[0] != node[0] and (node[3] == 'dir' or node[3] == 'file'):
                childlist.append(node)
        if len(childlist) > 0:
            for child in childlist:
                child_pair = self.recur_list_(child)
                children.append(child_pair)
        return [parent, children]


    # ------------------------ print a tree file ------------------------------
    def treefileprint_(self, root_pair):
        self.treeFile = os.getcwd() + '\\tmp_files\\tree_file.txt'
        if self.rootcnt == 0:
            f = open(self.treeFile, 'w')
        else:
            f = open(self.treeFile, 'a')
        self.recur_print_(f, [], root_pair, 0)
        f.close()
        self.rootcnt += 1


    def recur_print_(self, f, grandparent, parent, level):
        if parent == []:
            f.write("")
            return
        nodeid_str = str(parent[0][0])                      # parent node = parent[0], its nodeid is [0][0]
        nodeid20   = self.dots[:20 - len(nodeid_str)] + nodeid_str
        if level == 0 or len(grandparent) == 0:
            f.write(nodeid20 + self.dots[:level*2] + parent[0][5][6] + "\n")
        else:
            parent1 = parent[0][5][6].replace(grandparent[0][5][6], self.dots[:len(grandparent)])
            f.write(nodeid20 + self.dots[:level * 2] + parent1 + "\n")
        for p in parent[1]:
            self.recur_print_(f, parent, p, level + 1)


    def recur_one_root(self, parent):
        self.list_one_root.append(parent)
        for node in self.nodelist:
            if node[1] == parent[0] and node[2] != 'root':
                self.recur_one_root(node)
