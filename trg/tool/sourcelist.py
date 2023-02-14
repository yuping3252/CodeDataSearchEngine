__author__ = 'YupingYang'
import os

class SourceList:
    def __init__(self, glo):
        self.fname = os.getcwd() + '\\tmp_files\search_root_list.txt'
        f = open(self.fname, 'r')
        self.cds = f.readlines()
        i = 0
        for r in self.cds:
            self.cds[i] = r.strip('\n')
            i += 1
        f.close()

    def read(self):
        return self.cds

    def add_(self, row):
        found_ = False
        if row and self.cds.count(row.strip()) == 0:
            if not self.cds:
                self.cds = []
            self.cds.append(row.strip())
        return self.cds

    def delete_(self, row):
        if self.cds.count(row) > 0:
            self.cds.remove(row)
        elif self.cds.count(row + '\n') > 0:
            self.cds.remove(row + '\n')
        return self.cds

    def write_(self):
        f = open(self.fname, 'w')
        for row in self.cds:
#            print("sourcelist.py,    row=", row)
            f.write(row + '\n')
        f.close()


