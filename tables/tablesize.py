import traceback
import pymssql
import psycopg2
from PyQt4.QtCore import *
from PyQt4.QtGui  import *



class TableSize:
    def __init__(self):
        self.vertical = 0
        self.horizont = 0
        self.row_max  = 0
        self.col_max  = 0


    def dsply_rows_index(self, rows):
        rows_ = []
        r = 0
        for row in rows:
            row_ = [r, row]
            rows_.append(row_)
            r += 1
        return rows_


    def compute_screen_rowcols(self, row_lst, col_lst):
        row_max = 0
        row_max_lst = []
        for rows in row_lst:
            row_cnt = len(rows)
            row_max_lst.append(row_cnt)
            if row_cnt > row_max:
                row_max = row_cnt
        col_max = 0
        col_cnt_lst = []
        for cols in col_lst:
            col_cnt = len(cols)
            col_cnt_lst.append(col_cnt)
            col_max += col_cnt

        self.row_max = row_max
        self.col_max = col_max
        return row_max, col_max, row_max_lst, col_cnt_lst


    def rows(self):
        return self.row_max


    def cols(self):
        return self.col_max


    def compute_screen_pixels(self, rows, cols):
        v = rows * 40
        h = cols * 110

        if  v < 150:
            v = 150
        if  h < 150:
            h = 150

        if  v > 800:
            v = 800
        if  h > 2000:
            h = 2000

        self.vertical = v
        self.horizont = h
        return v, h


    def size(self):
        return self.vertical, self.horizont

