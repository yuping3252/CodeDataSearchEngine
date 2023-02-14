import sys

from PyQt4.QtCore    import *
from PyQt4.QtGui     import *
from tables.columnslide     import ColumnSlide
from tables.tablesize       import TableSize
from tables.merge_lst       import MergeList
from tables.row_lst_reorder import RowListReOrder

global_x = 0
global_y = 0


class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        t_op    = []
        tbl_lst = []
        col_lst = ['Col%02d' % i for i in range(1, 21)]
        row_lst = [['cell%02d,%02d' % (i, j) for i in range(1, 21)] for j in range(500, 0, -1)]
        table = TableView(t_op, tbl_lst, row_lst, col_lst, self)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)


class TableView(QTableView):
    def __init__(self, t_op, tbl_lst, row_lst, col_lst, parent=None, *args):
        QTableView.__init__(self, parent, *args)
        self.t_op = t_op
        self.tbl_lst = tbl_lst
        self.row_lst = row_lst
        self.col_lst = col_lst
        self.value_op(t_op, tbl_lst, row_lst, col_lst)
        self.merge_lst = MergeList()

        #self.setMouseTracking(True)
        #self.viewport().installEventFilter(self)

        self._last_index = QPersistentModelIndex()

        self.chart_col_num   = 0
        self.col_range       = []
        self.row_lst_reorder = RowListReOrder()
        self.setMinimumSize(700,500)


    def value_op(self, t_op, tbl_lst, row_lst, col_lst): 
        self.sz = TableSize()
        row_max, col_max, row_max_lst, col_cnt_lst = self.sz.compute_screen_rowcols(row_lst, col_lst)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.columnslide = ColumnSlide(t_op, tbl_lst, row_lst, col_lst)

        self.tm  = TableModel(t_op, tbl_lst, row_lst, col_lst, self)
        self.setModel(self.tm)
        self.setSelectionModel(QAbstractItemView.selectionModel(self))
        self.setEditTriggers(QAbstractItemView.SelectedClicked)

        self.frozenTableWidget = FreezeTableWidget(t_op, tbl_lst, row_lst, col_lst, self)
        self.frozenTableWidget.setMaximumHeight(53)

        self.viewport().stackUnder(self.frozenTableWidget)

        # hide grid
        self.setShowGrid(True)
        self.setStyleSheet('font: 10pt "Courier New"')
        self.setAlternatingRowColors(True)

        hh = self.horizontalHeader()
        hh.setDefaultAlignment(Qt.AlignCenter)
        self.hh = hh

        self.clicked.connect(self.clickedSlot_)
        self.tm.sort(3, Qt.AscendingOrder)

        self.header = self.frozenTableWidget.horizontalHeader()
        self.header.setDefaultSectionSize(hh.defaultSectionSize())
        self.header.sectionClicked.connect(self.columnClickedSlot)

        self.frozenTableWidget.show()
        self.updateFrozenTableGeometry()

        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        # connect the headers and scrollbars of both tableviews together
        self.verticalHeader().  sectionResized.connect(self.updateSectionHeight)
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth )

        self.frozenTableWidget.horizontalScrollBar().valueChanged.connect(self.horizontalScrollBar().setValue)
        self.horizontalScrollBar().valueChanged.connect(self.frozenTableWidget.horizontalScrollBar().setValue)

        self.delegate = Delegate()
        self.delegate.setValue(3,3)
        self.setItemDelegate(self.delegate)
        self.delegate.setValue(2,4)
        self.setItemDelegate(self.delegate)


    def setValue(self, r, c, v):
        i = 1     #   value v set in (r, c) of TableView


    def clickedSlot_(self):
        cindex = self.currentIndex()                        # QTableWidget has a clicked cell, which is a current item
        if cindex is None:
            return
        row   = cindex.row()                               # (row)    of clicked item
        col   = cindex.column()                            # (column) of clicked item
        txt   = cindex.data()

        model = self.model()
        self.setModel(model)
        model.set_cell_background(cindex)
        self._last_index = cindex
        self.repaint()


    # event first go here, then passed to clickSlot()
    def mousePressEvent(self, event):
        return QTableView.mousePressEvent(self, event)


    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if logicalIndex == 0 or logicalIndex == 1:
            self.frozenTableView.setColumnWidth(logicalIndex, newSize)
            self.updateFrozenTableGeometry()


    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)


    def resizeEvent(self, event):
        QTableView.resizeEvent(self, event)
        self.updateFrozenTableGeometry()


    def updateFrozenTableGeometry(self):
        if self.horizontalHeader().isVisible():
            self.frozenTableWidget.setGeometry(self.frameWidth(), self.frameWidth(), 
                                             self.viewport().width()  + 25,
                                             self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozenTableWidget.setGeometry(self.frameWidth(), self.frameWidth(), 
                                             self.viewport().width() + 25,
                                             self.horizontalHeader().height())


    def columnClickedSlot(self, col):
        self.t_op.column_clicked("action", col)


    def contextMenuEvent(self, event):
        self.cell_menu(event)


    def wheelEvent(self, event):                          # wheel rolling
        self.cell_menu(event)


    def cell_menu(self, event):

        self.pivot_index = self.indexAt(event.pos())      # find the cell being acted
        self.model().set_cell_background(self.pivot_index)
        self.menu = QMenu(self)                           # add context menu buttons
        self.addCustomMenu("Back", event)
        self.addCustomMenu("Display Alignment", event)
        self.addCustomMenu("Search  Alignment", event)
        self.addCustomMenu("Recover column data", event)
        self.addCustomMenu("Type in table name", event)
        self.addCustomMenu("Type in column name", event)
        self.addCustomMenu("Data type of result column", event)
        self.addCustomMenu("Use this value to search", event)
        self.addCustomMenu("Restrict result to this table", event)
        self.addCustomMenu("Restrict result to this column", event)
        self.addCustomMenu("Max number of tables", event)
        self.addCustomMenu("Max number of columns", event)
        self.addCustomMenu("Update date range", event)
        self.addCustomMenu("Exit", event)
        self.menu.popup(QCursor.pos())


    def addCustomMenu(self, actionName, event):
        dsply_align_Action = QAction(actionName, self)
        dsply_align_Action.triggered.connect(lambda: self.addCustomActionSlot(actionName, event))
        self.menu.addAction(dsply_align_Action)


    def addCustomActionSlot(self, btntext, event):        # context menu action handles
        if btntext == "Back":
            self.back_action(event)
        if btntext == "Search  Alignment":
            self.search_align_rows_tv(event)
        if btntext == "Recover column data":
            self.recover_column(event)
        if btntext == "Exit":
            exit()


    def back_action(self, event):
        self.t_op.back_action()


    def search_align_rows_tv(self, event):
        r = self.pivot_index.row()
        c = self.pivot_index.column()
        t = self.model().data(self.pivot_index, Qt.DisplayRole)
        self.t_op.search_align_rows_op("action", r, c, t)


    def return_size(self):
        v, h = self.sz.size()
        h2 = h
        if h > 1000:
            h2 = 0.9*h
        if h2 > 3000:
            h2 = 3000
        return v, h2


    def setHeaders(self, tbl_lst, col_lst, col_min_index, original_col_cnt, new_col_max):

        tbls, headers, col_grp_lst = self.merge_lst.merge_lsts(self.tbl_lst, self.col_lst, tbl_lst, col_lst, col_min_index)
        self.frozenTableWidget.setHorizontalHeaderLabels(headers)

        self.tbl_lst = tbls
        self.headers = headers

        return tbls, headers, col_grp_lst


    def set_chart_flg(self, chart_flg):
        if not chart_flg:
            self.chart_flg = False
            self.col_range = []
            self.setRowsBackgroundColor(self.row_lst, 0, [])


    def setColumn(self, tbls, row_lst, headers, col_grp_lst, col_pivot, chart_flg):  # called from table_op.py, column_clicked()
        t_pivot = self.col2tbl_pos(col_pivot)

        updated_t    = []
        updated_rows = []

        # --------------------------------------------- left tables
        t = 0
        c = 0
        for rows in self.row_lst:
            if t == t_pivot:
                break
            updated_t.append(tbls[t])
            updated_rows.append(rows)
            c += len(rows[0][1])
            t += 1

        # --------------------------------------------- split table, possible left
        col_left = c
        partial_rows_cnt1 = 0
        partial_width1    = 0
        partial_rows1 = []
        if col_left < col_pivot:
            partial_rows = self.row_lst[t]
            r = 0
            for row in partial_rows:
                row_ = row[1][:col_pivot - col_left]
                partial_rows1.append(row_)
                r += 1
            partial_rows_cnt1 = len(partial_rows1)
            partial_width1    = len(partial_rows1[0])

        # -------------------------------------------- split table, vertical column
        updated_t.append(tbls[t])
        partial_rows_cnt2 = 0
        partial_width2    = 0
        partial_rows2 = []
        for rows in row_lst:
            r = 0
            for row in rows: 
                row_ = row[1][1:]
                partial_rows2.append(row_)
                r += 1
        partial_rows_cnt2 = len(partial_rows2)
        partial_width2    = len(partial_rows2[0])

        # --------------------------------------------- split table, possible right
        pivot_tbl_len = len(self.row_lst[t][0][1])
        partial_rows_cnt3 = 0 
        partial_width3    = 0
        partial_rows3 = []
        if col_pivot + 1 < col_left + pivot_tbl_len:
            partial_rows = self.row_lst[t]
            r = 0
            for row in partial_rows:
                row_ = row[1][col_pivot - col_left + 1:]
                partial_rows3.append(row_)
                r += 1
            partial_rows_cnt3 = len(partial_rows3)
            partial_width3    = len(partial_rows3[0])

        max_split_rows = partial_rows_cnt1 
        if partial_rows_cnt1 < partial_rows_cnt2:
            max_split_rows = partial_rows_cnt2
        if max_split_rows < partial_rows_cnt3:
            max_split_rows = partial_rows_cnt3

        blank = []
        max_split_width = partial_width1 + partial_width2 + partial_width3
        for cc in range(max_split_width):
            blank.append("")

        merge_rows = []
        for r in range(max_split_rows):
            merge_row = []
            if r < partial_rows_cnt1:
                merge_row.extend(partial_rows1[r])
            else:
                merge_row.extend(blank[:partial_width1])

            if r < partial_rows_cnt2:
                merge_row.extend(partial_rows2[r])
            else:
                merge_row.extend(blank[:partial_width2])

            if r < partial_rows_cnt3:
                merge_row.extend(partial_rows3[r])
            else:
                merge_row.extend(blank[:partial_width3])
            merge_rows.append([r, tuple(merge_row)])
        updated_rows.append(merge_rows)

        # --------------------------------------------- right tables
        t = 0
        for rows in self.row_lst: 
            if t > t_pivot: 
                updated_rows.append(rows)
            t += 1

        # --------------------------------------------- set model

        self.tm.setData_(self.tbl_lst, updated_rows, headers)
        self.setModel(self.tm)

        # --------------------------------------------- load data for charting
        chart_col_data = []
        if chart_flg:
            c1 = 0
            c  = 0
            for rows in updated_rows:
                r = 0
                for row in rows:
                    if r == 0: 
                        c1 = c
                        c += len(row[1])
                    if col_pivot < c: 
                        chart_col_data.append(row[1][col_pivot - c1])
                    r += 1
                if chart_col_data != []:
                    break
        else:
            chart_col_data = []

        if chart_flg: 
            self.col_range.append(col_pivot)
            self.chart_col_num += 1
        else:  
            self.col_range =[col_pivot]
            self.chart_col_num  = 0

        self.setRowsBackgroundColor(updated_rows, 0, self.col_range)

        self.row_lst = updated_rows

        return updated_rows, chart_col_data


    def setRows_a_Block(self, tbls, row_lst, a_rows, headers, tbl_pivot, col_min, col_max):
        t = 0
        merged_rows = []
        for rows in row_lst:
            if t == tbl_pivot:
                merged_rows.append(a_rows)
            else:
                merged_rows.append(row_lst[t])
            t += 1
        self.tm.setData_(tbls, merged_rows, headers)
        self.setModel(self.tm)

        col_range = []
        for c in range(col_max - col_min):
            col_range.append(col_min + c)

        self.setRowsBackgroundColor(row_lst, 0, col_range)


    def setRows(self, tbls, row_lst_, headers, col_grp_lst, row_pivot, col_pivot, col_min, col_max):
        row_lst = self.row_lst_reorder.row_lst_reorder(row_lst_)
        t_pivot = self.col2tbl_pos(col_pivot)       # table index for table containing col_pivot

        print("tableview.py,   setRows(),   col_pivot=", col_pivot, ",   t_pivot=", t_pivot)

        # tbl_len is num of tables, col_len is num of cols
        # col_bndry1 and col_bndry2 are lists, left and right bndry pos of each col grp
        orign_tbl_len, orign_col_len, orign_col_bndry1, orign_col_bndry2 = self.col_group_boundary(self.col_lst)
        align_tbl_len, align_col_len, align_col_bndry1, align_col_bndry2 = self.col_group_boundary(col_grp_lst)

        # self.row_lst are full length display rows, but not row_lst
        # row count includes 0 row at search row, i.e., row_pivot

        # ---------------- rows to the left and including the table containing col_pivot -----------------------
        updated_rows = []
        t = 0
        for rows in self.row_lst:
            updated_rows.append(rows)
            if t == t_pivot:
                break
            t += 1

        # ---------------- rows that are added and aligned to the right of col_pivot -----------------------
        binding_rows = []
        for rows_ in row_lst:
            if rows_ != []:
                row_len = len(rows_[0][1])
                rows1 = []
                rows2 = []
                for row_ in rows_:
                    row1 = [row_[0], tuple(row_[1][:row_len-3])]  # added and to be aligned row, original
                    row2 = [row_[0], row_[1][row_len-3:]]         # pk1_, pk2_
                    rows1.append(row1)
                    rows2.append(row2)
                rows = self.rows_shift(row_pivot, rows1)          # shifted and added to the display
                updated_rows.append(rows)
                binding_rows.append(rows2)

        # ---------------- partially covered original values, use overlap strategy -------------------------------
        col_restart_pos = 0
        for rows in updated_rows:
            col_restart_pos += len(rows[0][1])

        print("tableview.py,   setRows(),   accumulated length in updated_rows=", col_restart_pos)    # 8
        print("tableview.py,   setRows(),   orign_col_bndry2[t_pivot]=", orign_col_bndry2[t_pivot])   # 5

        col_restart_pos += orign_col_bndry2[t_pivot]                          # ???????????????  why add ???
        tbl_restart_pos  = self.col2tbl_pos(col_restart_pos)
        col_restart_base = orign_col_bndry1[tbl_restart_pos]
        print("tableview.py,   setRows(),   col_restart_base=", col_restart_base)


        # ---if col_restart_pos > orign_col_len, then, no restart,  tbl_restart_pos = 0, col_restart_base = 0
        # ---------------- partial rows at the right of the table containing base point ----------------------
        if col_restart_pos < orign_col_len:
            row_lst_at_pos = self.row_lst[tbl_restart_pos]
            rows = []
            for row in row_lst_at_pos:
                c1 = 0
                row_ = []
                for col in row[1]:
                    if col_restart_base + c1 >= col_restart_pos:
                        row_.append(col)
                    c1 += 1
                rows.append([row[0], tuple(row_)])
            updated_rows.append(rows)

        # ---------------- tail rows to the right of the base point ----------------------
        if col_restart_pos < orign_col_len:
            for t in range(tbl_restart_pos + 1, orign_tbl_len):
                updated_rows.append(self.row_lst[t]) 

        col_range = []
        for c in range(col_max - col_min):
            col_range.append(col_min + c)

        self.setRowsBackgroundColor(row_lst, row_pivot, col_range)

        # ---row_lst is only the aligned rows
        # ---updated_rows covers the full screen

        self.tm.setData_(self.tbl_lst, updated_rows, headers)
        self.setModel(self.tm)

        self.col_lst = col_grp_lst
        self.row_lst = updated_rows

        return updated_rows


    def setRowsBackgroundColor(self,   row_lst_bg, row_idx_bg, col_range):
        self.tm.setRowsBackgroundColor(row_lst_bg, row_idx_bg, col_range)


    def rows_shift(self, r, rows_):
        len_ = len(rows_[0][1])
        rows = []
        for rr in range(r-1):
            row_ = []
            for c in range(len_):
                row_.append("")
            rows.append([rr, tuple(row_)]) 

        for row_ in rows_:
            rows.append([row_[0] + r, row_[1]]) 
        return rows


    # if returns t_pos = 0, means no table 
    def col2tbl_pos(self, colpos):
        i     = 0
        t_pos = 0
        b     = 0
        for cols in self.col_lst:
            for col in cols:
                if i == colpos:
                    t_pos = b
                i += 1
            b += 1
        return t_pos


    def col_group_boundary(self, col_lst):
        bndry1 = []
        bndry2 = []

        b    = 0
        tlen = 0
        len_ = 0
        for cols in col_lst: 
            bndry1.append(b)
            b += len(cols)
            bndry2.append(b)
            len_ += len(cols)
            tlen += 1
        return tlen, len_, bndry1, bndry2


    def eventFilter(self, widget, event):
        if widget is self.viewport():                     # event is in the viewport
            index = self._last_index                      # last index   ----> index
            if event.type() == QEvent.MouseMove:
                index = self.indexAt(event.pos())         # mouse move   ----> index
            elif event.type() == QEvent.Leave:
                index = QModelIndex()                     # mouse leave  ----> index
            if index != self._last_index:                 # last index   !=    index
                row   = self._last_index.row()            # mouse moved or left, use last row, column
                col   = self._last_index.column()
                #item  = self.item(row, col)               # item at last location
                #if item is not None:
                #    self.itemExited.emit(item)            # signal at last location (row, col)
                #self.cellExited.emit(row, col)            # signal at last location (row, col)
                self._last_index = QPersistentModelIndex(index)

            self.slidevertical(event)                     # it seems, this is the only useful part of this method
            self.clearFocus()

        return QTableWidget.eventFilter(self, widget, event) # thi



    def slidevertical(self, event):
        if event.type() == QEvent.MouseButtonPress:       # pressed ...... initiate sliding
            self.row1 = self._last_index.row()            # row    of pressed point
            self.col1 = self._last_index.column()         # column of pressed point
            self.pressed = True

        if event.type() == QEvent.MouseButtonRelease and self.pressed: # released ...... end sliding
            row2 = self._last_index.row()                              # row    of released point
            col2 = self._last_index.column()                           # column of released point
            if self.col1 == col2: 
                #tblnm, tblidx, drow = self.columnslide.reload_data(self, self.t_op, self.row1, row2, col2)  

                i = 1

                # pressed and released at the same column
            self.clearSelection()
            self.pressed = False



class FreezeTableWidget(QTableWidget):
    cellExited = pyqtSignal(int, int)
    itemExited = pyqtSignal(QTableWidgetItem)

    def __init__(self, t_op, tbl_lst, row_lst, col_lst, parent=None, *args):
        self.t_op = t_op

        self.sz = TableSize()
        row_max, col_max, row_max_lst, col_cnt_lst = self.sz.compute_screen_rowcols(row_lst, col_lst)
        QTableView.__init__(self, row_max, col_max, parent)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet('''border: none; background-color: #CCC''')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy  (Qt.ScrollBarAlwaysOff)
        self.setMaximumHeight(50)
        self.setEditTriggers(QAbstractItemView.AllEditTriggers)

        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.viewport().installEventFilter(self)
        self.cellClicked.connect(self.clickedSlot)

        self._last_index = QPersistentModelIndex()

        self.sz.compute_screen_pixels(row_max, col_max)
        vpixels, hpixels = self.sz.size()
        self.resize(hpixels, vpixels)

        headerView = self.horizontalHeader()
        headerView.setVisible(True)

        headers = []
        c = 0
        for cols in col_lst:
            for col in cols:
                headers.append(str(col))
                c += 1
        self.setHorizontalHeaderLabels(headers)

        self.show()

        for c in range(len(headers)):
            item = QTableWidgetItem()
            self.setItem(0, c, item)
            item.setTextAlignment(Qt.AlignCenter)

        grey  = QColor(255, 255, 255)
        brush = QBrush(grey)
        for c in range(len(headers)):
            self.item(0, c).setBackground(brush)

        self.verticalHeader().hide()

        self.itemChanged.connect(self.search_col_text_entry)


    def search_col_text_entry(self):
        cindex = self.currentIndex()
        row  = cindex.row()
        col  = cindex.column()
        data = cindex.data()
        if data != "": 
            self.t_op.search_column(col, data)


    def clickedSlot(self):                                # clicked, background color change only, for now
        citem = self.currentItem()                        # QTableWidget has a clicked cell, which is a current item
        if citem is None:
            return
        row   = citem.row()                               # (row)    of clicked item
        col   = citem.column()                            # (column) of clicked item
        txt   = citem.text()
        headtitle = self.horizontalHeaderItem(col).text() # (column) --> header text of clicked item

        grey  = QColor(255, 255, 128)
        brush = QBrush(grey)
        citem.setBackground(brush)
        self.last_item = citem
        self.repaint()



class TableModel(QAbstractTableModel):
    def __init__(self, t_op, tbl_lst, row_lst, col_lst, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)

        self.colLabels  = self.cols_convert(col_lst)
        self.dataCached = self.rows_convert(row_lst)

        self.bgcolor_row = -1
        self.bgcolor_col = -1
        
        self.row_lst_bg = None
        self.row_idx_bg = -1
        self.col_range  = []
        self.col_max_bg = len(self.colLabels)
        self.col_max    = len(self.colLabels)

        self.colors = [QColor(130, 255, 240), QColor(180, 235, 220), QColor(230, 215, 200), QColor(255, 195, 180)]

    # col_lst is one level list
    def setData_(self, tbl_lst, row_lst, col_lst):

        self.col_max     = len(self.colLabels)
        self.colLabels   = col_lst
        self.dataCached  = self.rows_convert(row_lst)

        self.bgcolor_row = -1
        self.bgcolor_col = -1 


    def rowCount(self, parent):
        return len(self.dataCached)


    def columnCount(self, parent):
        return len(self.colLabels)


    def get_value(self, index):
        i = index.row()
        j = index.column()

        if i < len(self.dataCached):
            if j < len(self.dataCached[i]):
                return str(self.dataCached[i][j])
        return


    def setRowsBackgroundColor(self, row_lst_bg, row_idx_bg, col_range):
        self.row_lst_bg = row_lst_bg
        self.row_idx_bg = row_idx_bg
        self.col_range  = col_range


    def resetRowsBackgroundColor(self):
        self.row_lst_bg = None
        self.row_idx_bg = -1
        self.col_range  = []


    def set_cell_background(self, index):
        self.bgcolor_row = index.row()
        self.bgcolor_col = index.column()


    def unset_cell_background(self):
        self.bgcolor_row = -1
        self.bgcolor_col = -1



    def calculate_color(self, index):
        if self.bgcolor_row >= 0:
            if index.row() == self.bgcolor_row and index.column() == self.bgcolor_col:
                return QColor(130, 255, 250)

        if self.row_lst_bg is not None: 
            for rows in self.row_lst_bg: 
                chain = rows[0][1][len(rows[0][1])-1]

                r = 0 
                for row in rows: 
                    if index.row() == self.row_idx_bg + r and  index.column() in self.col_range: 
                        return self.colors[0]  # use chain to make different color, makes no difference, why ???
                    r += 1                     # desire: cells in different chain use different background
        return QColor(230, 255, 255)


    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.get_value(index)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return value
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.BackgroundRole:
            color = self.calculate_color(index)
            return QBrush(color)
        return None


    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col < len(self.colLabels): 
                return self.colLabels[col]
        return None


    def cols_convert(self, col_lst):
        tbl_cols = []
        c = 0
        for cols in col_lst:
            for col in cols:
                tbl_cols.append(col)
                c += 1
        return tbl_cols


    def rows_convert(self, row_lst):
        # --- column numbers for each table, and total columns
        tbl_col_cnt   = []
        col_cnt       = 0
        accum_col_cnt = 0
        for rows in row_lst:
            accum_col_cnt += len(rows[0][1])
            tbl_col_cnt.append(accum_col_cnt)
            col_cnt += len(rows[0][1])

        # --- maximum rows
        row_cnt = 0
        for rows in row_lst:
            if row_cnt < len(rows):
                row_cnt = len(rows)

        # --- reload data
        display_table =[]
        row1 = []
        for c in range(col_cnt):
            row1.append("")
        display_table.append(row1)

        for row in range(row_cnt):
            col_base = 0
            tbl = 0
            row_= []
            for c in range(col_cnt): 
                if c >= tbl_col_cnt[tbl]: 
                    col_base = tbl_col_cnt[tbl]
                    tbl += 1
                tbl_rows = row_lst[tbl]
                if row < len(tbl_rows): 
                    row_.append(tbl_rows[row][1][c - col_base])
                else:
                    row_.append("")
            display_table.append(row_)
        return display_table



class Delegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)
        self.r = -1
        self.c = -1 


    def setValue(self, r, c):
        self.r = r
        self.c = c


    def paint(self, painter, option, index): 
        op = QStyleOptionViewItem(option)

        if index.row() == self.r and index.column() == self.c:
            op.font.setBold(True)
            op.palette.setColor(QPalette.Active, QPalette.Button, QColor(255,0,0,255))  # No effect
            op.palette.setColor(QPalette.Normal, QPalette.Text, QColor(0,0,255,255))
        QStyledItemDelegate.paint(self, painter, op, index)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec())


