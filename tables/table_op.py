import traceback
import pymssql
import psycopg2

from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from tables.tabledata   import TableData
from tables.tablerelate import TableRelate
from tables.tableview   import TableView
from tables.cmdstack    import CommandStack
from tables.cmdstack    import CommandInfo


# plotting: 
# gui\centralareaop.py, gui\toolbar.py, tables\table_op.py, tables\tableview.py
# plot\plotpane.py, plot\barchar_cnt.py, plot\barchart_amt.py, gui/toolbar.py


class Table_OP:
    def __init__(self, db, sz, tdata, trelate, mw, parent=None):
        self.db       = db
        self.sz       = sz
        self.tdata    = TableData(  db, sz)
        self.trelate  = TableRelate(db, sz)
        self.mw       = mw
        self.parent   = parent
        self.cmdstack = CommandStack()
        self.action   = "action"

        # -------------------------------------------basic info
        self.tv                 = ""
        self.dbtype             = ""
        self.dbnm               = ""
        self.dsply_tbl_lst      = []
        self.dsply_row_lst      = []
        self.dsply_col_lst      = []
        self.dsply_headers      = []
        self.dsply_col_cnt_orig = 0
        self.dsply_col_cnt      = 0

        self.searched           = []
        self.dsply_col_max      = []
        self.dsply_col_min      = []

        self.dsply_row_min      = []
        self.dsply_row_cnt      = []
        self.dsply_row_cnt_partial = []

        # -------------------------------------------aligned
        #self.dsply_aligned_col_min = 0
        #self.dsply_aligned_col_max = 0
        self.chart_flg   = False
        self.chart_axis  = "x"
        self.chart_type  = ""                       # its value is assigned inside plotpane.py

        self.chart_x_col_name = ""
        self.chart_y_col_name = ""
        self.chart_z_col_name = ""

        self.chart_x_col_data = []
        self.chart_y_col_data = []
        self.chart_z_col_data = []

        self.mw.toolbar.unset_chart_flg()


    def tbl_col_rows(self, action, dbtype, dbnm, tbl_lst, col_lst, parent=None):

        self.action = action
        self.parent = parent
        r    = 0
        c    = 0
        row_lst = []

        if len(tbl_lst) >= 1 and len(tbl_lst) == len(col_lst):
            row_max, col_max, tbl_lst, row_lst, col_lst = self.tdata.get_tbls_rows(dbtype, dbnm, tbl_lst, col_lst)

        elif   len(tbl_lst) == 1 and col_lst == []:
            tblnm = tbl_lst[0]
            row_max, col_max, tbl_lst, row_lst, col_lst = self.tdata.get_one_tbl_all_col_rows(dbnm, tblnm)

        elif len(tbl_lst)  > 1 and col_lst == []:
            row_max, col_max, tbl_lst, row_lst, col_lst = self.tdata.get_multi_tbls_all_col_rows(dbnm, tbl_lst)

        elif tbl_lst == [] and col_lst == []: 
            row_max, col_max, tbl_lst, row_lst, col_lst = self.tdata.get_one_db_all_tbls_rows(dbnm, 200)

        elif len(tbl_lst) == 1 and type(col_lst) == type(""):
            tblnm = tbl_lst[0]
            row_max, col_max, tbl_lst, row_lst, col_lst = self.tdata.get_one_tbl_select_cols_rows(dbnm, tblnm, col_lst)

        # --------------------------------------------------------
        if self.action == "populategrid":
            self.tv = TableView(self, tbl_lst, row_lst, col_lst, parent)
        elif self.action == "repopulategrid": 
            self.tv.tm.setData_(tbl_lst, row_lst, col_lst)

        self.print_table_grid(tbl_lst, row_lst, col_lst)

        # ------------------- get num of rows and cols of the table display
        for rows in row_lst:
            rr = len(rows)
            if r <rr:
                r =rr 
            cc = len(rows[0][1])
            c += cc 

        self.dbtype        = dbtype
        self.dbnm          = dbnm
        self.dsply_basic_lsts(tbl_lst, row_lst, col_lst)

        self.commandPush("tbl_col_rows", "populategrid")
        return self.tv, r, c


    def print_table_grid(self, tbl_lst, row_lst, col_lst):
        for tbl in tbl_lst:
            print("table_op, tbl=", tbl)
        print("")
        for rows in row_lst:
            for row in rows:
                print("table_op, row=", row)
            print("")
        print("")
        for col in col_lst:
            print("table_op, col=", col)
        print("")


    def dsply_basic_lsts(self, tbl_lst, row_lst, col_lst):
        self.dsply_tbl_lst = tbl_lst
        self.dsply_row_lst = row_lst
        self.dsply_col_lst = col_lst

        for rows in row_lst:
            row_num = len(rows)
            self.dsply_row_min.append(0) 
            self.dsply_row_cnt.append(row_num)
        colcnt     = 0
        accum      = 0
        for cols in col_lst:
            self.dsply_col_min.append(accum)
            colcnt = len(cols)
            accum += colcnt
            self.dsply_col_max.append(accum)
        self.dsply_col_cnt_orig = accum
        self.dsply_col_cnt      = accum

    
    def nested_lsts(self, tbl_lst, row_lst, col_lst):
        tbl_col_lst = []
        tblidx = 0
        for cols in col_lst:
            tbl = tbl_lst[tblidx]
            tbl_box = [tbl, cols]
            tbl_col_lst.append(tbl_box)
            tblidx += 1
        tbl_row_lst = []
        tblidx = 0
        for rows in row_lst:
            tbl = tbl_lst[tblidx]
            tbl_box = [tbl, rows]
            tbl_row_lst.append(tbl_box)
            tblidx += 1
        return tbl_col_lst, tbl_row_lst


    def commandPush(self, module, cmd, params=None):
        cmdInfo        = CommandInfo()
        cmdInfo.module = module
        cmdInfo.cmd    = cmd
        cmdInfo.params = params
        self.cmdstack.push(cmdInfo)


    def search_align_rows_op(self, action, row_pivot, col_pivot, txt):

        tblnm, tblidx = self.col2nested_tblnm(col_pivot)
        colnm, colidx = self.col2nested_colnm(col_pivot)

        print("table_op.py,    search_align_rows_op(),    dbnm=", self.dbnm, "    tblnm=", tblnm, "    colnm=", colnm, "    txt=", txt)

        params        = tuple([self.dbnm, tblnm, 0, colnm, "'" + txt + "'"])
        row_max, col_max, tbl_lst, row_lst, col_lst = self.trelate.get_relat_tbl_relat_vals(params)


        #for rows in row_lst:
        #    for row in rows:
        #        print("table_op.py,   search_align_rows_op(),   row_lst,   row=", row)
        #    print("")
        #print("")


        if row_lst == [[]]: 
            return 

        # col_max is the number of columns aligned

        row_data_idx = row_pivot - self.dsply_row_min[tblidx]     
        # when rows of this tblidx shift down or upwards, row_data_idx may be different tha r, not working for now

        col_min_index = self.dsply_col_max[tblidx]            # column index for leftmost aligned column

        col_idx = col_min_index
        for cols in col_lst:
            for col in cols:
                col_idx += 1
        col_max_index = col_idx                               # column index for rightmost aligned column

        # --------------------------------------------------- widen table, if necessary
        original_col_cnt = self.dsply_col_cnt
        if col_max_index > original_col_cnt:
            self.dsply_col_cnt = col_max_index
            self.tv.columnCountChanged(original_col_cnt, col_max_index)
            self.tv.frozenTableWidget.setColumnCount(    col_max_index)

        # --------------------------------------------------- new columns, new data rows to be displayed on screen
        self.tv.tm.beginResetModel()
        tbls, headers, col_grp_lst = self.tv.setHeaders(tbl_lst, col_lst, col_min_index,   original_col_cnt, col_max_index)
        row_lst = self.tv.setRows(tbls, row_lst, headers,  col_grp_lst, row_pivot, col_pivot, col_min_index, col_max_index)
        self.tv.tm.resetInternalData()
        self.tv.tm.endResetModel()

        # --------------------------------------------------- save global variables
        self.action           = action
        self.dsply_tbl_lst    = tbls
        self.dsply_col_lst    = col_grp_lst
        self.dsply_headers    = headers
        self.dsply_row_lst    = row_lst

        self.dsply_col_min = []
        self.dsply_col_max = []
        colcnt     = 0
        accum      = 0
        for cols in col_grp_lst:
            self.dsply_col_min.append(accum)
            colcnt = len(cols)
            accum += colcnt
            self.dsply_col_max.append(accum)
        
        self.dsply_row_min = []
        self.dsply_row_cnt = []
        for rows in row_lst:
            row_num = len(rows)
            self.dsply_row_min.append(0) 
            self.dsply_row_cnt.append(row_num)

        # --------------------------------------------------- save variables to command stack
        rows  = self.dsply_row_lst[tblidx]

        row   = rows[row_pivot - 1]
        cols  = self.dsply_col_lst[tblidx]
        c_min = self.dsply_col_min[tblidx]
        c_max = self.dsply_col_max[tblidx]
        c_cnt = c_max - c_min

        if self.action == "action":
            params = []
            params.append(row_pivot)
            params.append(col_min_index)
            params.append(col_max_index)
            params.append(txt)
            params.append(tblnm)
            params.append(tblidx)
            params.append(colnm)
            params.append(colidx)

            self.commandPush("search_align_rows", "searchalignrows", params)


    def col2nested_tblnm(self, col_pivot):
        i = 0
        last_i = 0

        for colpos in self.dsply_col_min:
            if colpos > col_pivot:
                break
            last_i = i
            i     += 1
        tblnm  = self.dsply_tbl_lst[last_i]
        tblidx = last_i
        return tblnm, tblidx


    def col2nested_colnm(self, col_pivot):
        last_colpos = 0
        i = 0
        for colpos in self.dsply_col_min:
            if colpos > col_pivot:
                break
            last_colpos = colpos
            last_i = i
            i += 1
        colidx = col_pivot - last_colpos
        cols   = self.dsply_col_lst[last_i]
        colnm  = cols[colidx]
        return colnm, colidx
        

    def col_2_heading(self, col):

        tbl_idx     = -1
        last_colmin = 0
        for colmin in self.dsply_col_min:
            if colmin > col:
                break
            last_colmin =colmin 
            tbl_idx += 1

        tblnm = self.dsply_tbl_lst[tbl_idx]
        cols  = self.dsply_col_lst[tbl_idx]

        col_idx_in_tbl = col - last_colmin
        colnm  = cols[col_idx_in_tbl]

        return tblnm, colnm


    def back_action(self):
        info_1 = self.cmdstack.pop()
        if self.action == "action": 
            info_2 = self.cmdstack.pop()
        else:
            info_2 = info_1
        self.action = "back"

        if info_2 is not None:

            if info_2.cmd == "populategrid":
                col_lst = []
                for cols in self.dsply_col_lst:
                    cols = cols[1:]
                    col_lst.append(cols)
                self.tbl_col_rows("repopulategrid", self.dbtype, self.dbnm, self.dsply_tbl_lst, col_lst, self.parent)
                self.tv.tm.resetRowsBackgroundColor()
            elif info_2.cmd == "searchalignrows":
                colidx  = info_2.params.pop()
                colnm   = info_2.params.pop()
                tblidx  = info_2.params.pop()
                tblnm   = info_2.params.pop()
                txt     = info_2.params.pop()
                col_max = info_2.params.pop()
                col_min = info_2.params.pop()
                row_pivot = info_2.params.pop()
                self.search_align_rows_op("back", row_pivot, col_min, txt)
            elif info_2.cmd == "columnclick":
                colidx  = info_2.params.pop()

                self.column_clicked("back", colidx)
        else:
            print("empty command stack 00000000000000000")



    def set_chart_flg(self, chart_flg):
        self.chart_flg  = chart_flg
        self.chart_axis = "x"



    def column_clicked(self, action, colidx):

        self.action = action
        tbl  = ""
        col  = ""
        cols_idx = 0

        # -------------------------------- get tbl
        cc      = 0
        tbl_nbr = 0
        col_at_colidx = None
        for cols in self.dsply_col_lst:
            tbl = self.dsply_tbl_lst[tbl_nbr]
            for col in cols:
                if cc == colidx: 
                    col_at_colidx = col
                cc += 1
            if col_at_colidx is not None:
                break
            tbl_nbr += 1 

        # -------------------------------- setColumn()
        tbl_lst = [tbl]
        col_lst = [[col_at_colidx]]
        row_max, col_max, tbl_lst, a_col_rows, col_lst = self.tdata.get_tbls_rows(self.dbtype, self.dbnm, tbl_lst, col_lst)

        self.tv.tm.beginResetModel()
        tbls, headers, col_grp_lst = self.tv.merge_lst.merge_lsts(self.dsply_tbl_lst, self.dsply_col_lst, [], [], colidx)
        row_lst, chart_col_data = self.tv.setColumn(self.dsply_tbl_lst, a_col_rows, 
                                    headers, 
                                    self.dsply_col_lst, colidx, self.chart_flg)
        self.tv.tm.resetInternalData()
        self.tv.tm.endResetModel()

        if self.chart_flg == True:

            if self.chart_type == "barchart_cnt": 
                if self.chart_axis == "x":
                    self.chart_x_col_name = col_at_colidx
                    self.chart_x_col_data = chart_col_data
                    self.mw.toolbar.plotpane.display_colnm('x', col_at_colidx, chart_col_data)  # display column name on PlotPane as x column
                    self.chart_axis = "x" 

            elif (self.chart_type == "simple_curve")     or (self.chart_type == "barchart_amt") or \
                 (self.chart_type == "line_with_blocks") or (self.chart_type == "piechart") or (self.chart_type == "scatter_dots"):
                if self.chart_axis == "x":
                    self.chart_x_col_name = col_at_colidx
                    self.chart_x_col_data = chart_col_data
                    self.mw.toolbar.plotpane.display_colnm('x', col_at_colidx, chart_col_data)  # display column name on PlotPane as x column
                    self.chart_axis = "y" 
                elif self.chart_axis == "y":
                    self.chart_y_col_name = col_at_colidx
                    self.chart_y_col_data = chart_col_data
                    self.mw.toolbar.plotpane.display_colnm('y', col_at_colidx, chart_col_data)  # display column name on PlotPane as y column
                    self.chart_axis = "x" 

            elif self.chart_type == "fill_between":
                if self.chart_axis == "x":
                    self.chart_x_col_name = col_at_colidx
                    self.chart_x_col_data = chart_col_data
                    self.mw.toolbar.plotpane.display_colnm('x', col_at_colidx, chart_col_data)  # display column name on PlotPane as x column
                    self.chart_axis = "y" 
                elif self.chart_axis == "y":
                    self.chart_y_col_name = col_at_colidx
                    self.chart_y_col_data = chart_col_data
                    self.mw.toolbar.plotpane.display_colnm('y', col_at_colidx, chart_col_data)  # display column name on PlotPane as y column
                    self.chart_axis = "z" 
                elif self.chart_axis == "z":
                    self.chart_z_col_name = col_at_colidx
                    self.chart_z_col_data = chart_col_data
                    self.mw.toolbar.plotpane.display_colnm('z', col_at_colidx, chart_col_data)  # display column name on PlotPane as y column
                    self.chart_axis = "x" 

        self.dsply_row_lst    = row_lst

        if self.action == "action":
            self.commandPush("column_clicked", "columnclick", [colidx])


    # ------------------------------------------- add color change for search result
    def search_column(self, colidx, text):
        rows_tobe_searched = []
        tbl_left  = 0
        tbl_right = 0
        tbl_pivot   = 0
        for rows in self.dsply_row_lst:
            tbl_right += len(rows[0][1])
            if tbl_right > colidx:
                rows_tobe_searched = rows
                break
            tbl_left = tbl_right
            tbl_pivot += 1
        c_diff = colidx - tbl_left
        # ------------------- get rows_tobe_searched, c_diff

        rows_search_result = []
        r = 0
        for row in rows_tobe_searched:
            col_tobe_searched = str(row[1][c_diff])
            search_result = col_tobe_searched.find(text)
            if search_result != -1:
                row[0] = r
                rows_search_result.append(row)
                r += 1
        # ------------------ get rows_search_result

        tbls, headers, col_grp_lst = self.tv.merge_lst.merge_lsts(self.dsply_tbl_lst, self.dsply_col_lst, [], [], colidx)
        # ------------------ get headers

        if rows_search_result == []:
            return

        self.tv.tm.beginResetModel()
        row_lst = self.tv.setRows_a_Block(self.dsply_tbl_lst, 
                self.dsply_row_lst, rows_search_result, headers, tbl_pivot, tbl_left, tbl_right)
        self.tv.tm.resetInternalData()
        self.tv.tm.endResetModel()


    def recover_column_data(self, action, colidx):
        self.action = action
        if colidx >= self.dsply_col_cnt_orig:
            return
        cols_idx = 0
        col_idx  = 0
        c = 0
        break_flg = False
        for cols in self.dsply_col_lst:
            col_idx = 0
            for col in cols:
                if c == colidx: 
                    break_flg = True
                    break
                col_idx += 1
                c       += 1
            if break_flg == True:
                break
            cols_idx += 1

        headItem = self.tv.horizontalHeaderItem(colidx)


        headItem.setBackground(self.tv.brushButton)
        headItem.setText(self.dsply_col_lst[cols_idx][col_idx])
        
        rows = self.dsply_row_lst[cols_idx]
        r = 0
        for row in rows: 
            #repopulated_item = QTableWidgetItem(str(row[1][col_idx]))
            #self.tv.setItem(r, c, repopulated_item)
            r += 1
        if self.action == "action": 
            self.commandPush("recover_column_data", "recovercolumndata", [colidx])

