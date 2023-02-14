import traceback
import pymssql
import psycopg2
from   PyQt4.QtCore import *
from   PyQt4.QtGui  import *



class ColumnSlide:
    def __init__(self, t_op, tbl_lst, row_lst, col_lst):
        self.t_op    = t_op
        self.tbl_lst = tbl_lst
        self.row_lst = row_lst
        self.col_lst = col_lst

                                                               # find the table given a column index
    def one_table_columns(self, colpick):                      # find all columns of a table a column index
        c1  = 0
        c2  = 0
        tblidx = 0
        for cols in self.col_lst:
            c1  = c2
            c2 += len(cols)
            if colpick < c2:
                break
            tblidx += 1
        return self.tbl_lst[tblidx], tblidx, c1, c2


    def reload_data(self, tabular, t_op, row1, row2, col):     # vertically shifting contents in all columns of a table
                                                               # containing a given column idx
        tblnm, tblidx, c1, c2 = self.one_table_columns(col)
        #row_cnt = tabular.rowCount()
        #col_cnt = tabular.columnCount()
        row_cnt = tabular.model().rowCount(tabular)
        col_cnt = tabular.model().columnCount(tabular)
        row_lst = t_op.dsply_row_lst[tblidx]

        drow = row2 - row1

        row_min = t_op.dsply_row_min[tblidx]
        row_max = t_op.dsply_row_max[tblidx]
        row_range = row_max - row_min                # range of actual data rows

        if drow > 0:                                 # move downward
            for row in range(row_range - 1, -1, -1): # loop from high to low, thru all data rows, row is row-index, data matrix
                row_idx  = row_lst[row][0]           # source row-index,                      (display)
                row_idx2 = row_idx + drow            # target row-index,                      (display)
                row_lst[row][0] = row_idx2           # source row-index --> target row-index, (display) for the same row data.

                if 0 <= row_idx2 < row_cnt:          # target row-index (display) in displayable row range
                    for col in range(col_cnt):
                        if c1 <= col < c2: 
                            item2 = tabular.item(row_idx2,  col)
                            if  item2 != None:
                                item2.setText(str(row_lst[row][1][col - c1]))
                            else:
                                item2 = QTableWidgetItem(str(row_lst[row][1][col - c1]))
                                tabular.setItem(row_idx2, col, item2)
    
            new_rows = row_min + drow
            if new_rows > 0:
                for row_idx in range(new_rows):
                    for col in range(col_cnt):
                        if c1 <= col < c2: 
                            item2 = tabular.item(row_idx,  col)
                            if  item2 != None:
                                item2.setText("")
                            else:
                                item2 = QTableWidgetItem("")
                                tabular.setItem(row_idx2, col, item2)

        if drow < 0:                                 # move downward
            for row in range(row_range):             # loop from high end and go downward, thru all data rows, row is row-index, data matrix
                row_idx  = row_lst[row][0]           # source row-index,                      (display)
                row_idx2 = row_idx + drow            # target row-index,                      (display)
                row_lst[row][0] = row_idx2           # source row-index --> target row-index, (display) for the same row data.

                if 0 <= row_idx2 < row_cnt:          # target row-index (display) in displayable row range
                    for col in range(col_cnt):
                        if c1 <= col < c2: 
                            item2 = tabular.item(row_idx2,  col)
                            if  item2 != None:
                                item2.setText(str(row_lst[row][1][col - c1]))
                            else:
                                item2 = QTableWidgetItem(str(row_lst[row][1][col - c1]))
                                tabular.setItem(row_idx2, col, item2)
    
            new_top = row_max + drow
            new_rows = row_cnt - new_top
            if new_rows > 0:
                for row_idx in range(new_rows):
                    new_row = new_top + row_idx
                    for col in range(col_cnt):
                        if c1 <= col < c2: 
                            item2 = tabular.item(new_row,  col)
                            if item2 != None: 
                                item2.setText("")
                            else:
                                item2 = QTableWidgetItem("")
                                tabular.setItem(new_row, col, item2)

        t_op.dsply_row_min[tblidx] += drow
        t_op.dsply_row_max[tblidx] += drow

        return tblnm, tblidx, - drow




