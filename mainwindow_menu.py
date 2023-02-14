#!/usr/bin/python
import os

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from guidata.find_nodeid       import FindNodeID
from gui.dataloaddialog        import DataLoadDialog
from gui.conn_database         import ConnectDatabase
from gui.datasourcedialog      import DataSourceDialog
from gui.toolbar               import ToolBar
from gui.treeview1             import TreeView1
from travel                    import travel_
from trg.cmd.configinfo        import ConfigInfo
from trg.cmd.global_set        import GlobalSetting
from trg.globaldata            import Tables_TRO
from trg.sql_tool.data_clear   import DataClear
from trg.sql_tool.data_load    import DataLoad
from close                     import Close
from gui.centralareaop         import CentralAreaOp
from gui.rightpane             import RightPane

from trg.sql_client.travel_db  import TravelDatabase
from trg.sql_client.tblcolumns import TableColumns
from trg.sql_client.storedproc import StoredProc
from tree.nodelist2treefile    import NodeList2TreeFile
from tree.dbobject2treefile    import DBObject2TreeFile



class Window(QMainWindow):
    newTask = pyqtSignal(object)

    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Data Tracing")
        self.resize(1200, 600)
        self.treeFile      = os.getcwd() + '\\tmp_files\\tree_file.txt'
        self.treeDBTable   = os.getcwd() + '\\tmp_files\\tree_dbtable.txt'
        self.treeDBProc    = os.getcwd() + '\\tmp_files\\tree_dbproc.txt'
        self.travel_db     = TravelDatabase()
        self.tblcolumns    = TableColumns()
        self.storedproc    = StoredProc()

        self.travelpath    = ""

        self.selectionList = []
        self.selectedPath  = []
        self.pathidx       = -1
        self.find_nodeid   = FindNodeID()

        # ------------------------ Tool Bar -----------------------------
        self.toolbar       = ToolBar("SeeThrough Hub", self)
        self.addToolBar(self.toolbar)

        # ------------------------ Center Area -----------------------------
        menubar          = self.menuBar()
        self.central     = CentralAreaOp(self)

        # ------------------------- data ------------------------------
        self.config      = ConfigInfo()
        self.glo_setting = GlobalSetting(self.config)
        self.glo         = self.glo_setting.get_glo()

        # ------------------------ File Menu -----------------------------
        self.file  = menubar.addMenu('&File')

        _loadFiles = self.file.addAction('Load Selected File Info')
        _loadDBs   = self.file.addAction('Load Selected Database Info')
        _loadFiles.setToolTip("Load previously collected file system data from TR repository")
        _loadDBs.setToolTip("Load previously collected database data from TR repository")
        self.connect(_loadFiles,   SIGNAL('triggered()'), self.loadFiles)
        self.connect(_loadDBs,     SIGNAL('triggered()'), self.loadDBs)

        self.file.addSeparator()
        _travelFiles = self.file.addAction('Collect File System Info')
        _travelDBs   = self.file.addAction('Collect Database Info'   )

        self.connect(_travelFiles, SIGNAL('triggered()'), self.travelFiles)
        self.connect(_travelDBs,   SIGNAL('triggered()'), self.travelDBs)

        _travelFiles.setToolTip('Collect info from file systems, may be slow')
        _travelDBs.  setToolTip('Collect info from databases, may be slow')

        self.file.addSeparator()
        _open  = self.file.addAction('Open File')
        _copy  = self.file.addAction('Copy Case')
        _print = self.file.addAction('Print Center Screen')
        self.connect( _open,  SIGNAL('triggered()'), self.OnOpen)
        self.connect( _copy,  SIGNAL('triggered()'), self.OnCopy)
        self.connect( _print, SIGNAL('triggered()'), self.OnPrint)

        # ------------------------ File close sub Menu -----------------------------
        self.file.addSeparator()
        _cleardisplay = self.file.addAction('Clear Tree Display')
        _clear        = self.file.addAction('Clear Repository')
        _close        = self.file.addAction('Close')
        self.connect(_cleardisplay,  SIGNAL("triggered()"), self.OnClearDisplay)
        self.connect(_clear,         SIGNAL("triggered()"), self.OnClear)
        self.connect(_close,         SIGNAL("triggered()"), self.OnClose)

        # ------------------------ Search Menu -----------------------------
        self.search           = menubar.    addMenu(  '&Search Info')
        self.datalineage_file = self.search.addAction('Data lineage (SQL files)')
        self.datalineage_db   = self.search.addAction('Data lineage (database)')
        self.datalineage_mix  = self.search.addAction('Data lineage (SQL files/database)')
        self.connect(self.datalineage_file, SIGNAL(   'triggered()'), self.datalineage_filesql)
        self.connect(self.datalineage_db,   SIGNAL(   'triggered()'), self.datalineage_dbsql)
        self.connect(self.datalineage_mix,  SIGNAL(   'triggered()'), self.datalineage_mixsql)

        # ------------------------ Connection Menu -----------------------------
        self.connection = menubar.addMenu('&Connect')
        _toDatabase     = self.connection.addAction('to Database')
        self.connect(_toDatabase, SIGNAL('triggered()'), self.OnToDatabase)

        # ------------------------ Setting Menu -----------------------------
        self.setting        = menubar.addMenu('&Setting')
        self.dataloadAction = QAction('Load data on starting', self.setting, checkable=True)
        self.dataloadAction.triggered.connect(self.OnGuiDataLoad)

        if self.config.flag_read():
            self.dataloadAction.setChecked(True)

        self.setting.addAction(self.dataloadAction)
        self._layout = self.setting.addAction('Layout')
        self._users  = self.setting.addAction('Users')

        self.dataloadAction.setToolTip("Load previously collected data from repository on starting")
        self._layout.       setToolTip("Reset GUI Layout")
        self._users.        setToolTip("Editing Users")

        self.connect( self.setting,  SIGNAL("hovered(QAction *)"), self.datainitHovered)
        self.connect( self._layout,  SIGNAL('triggered()'),        self.OnLayout)
        self.connect( self._users,   SIGNAL('triggered()'),        self.OnUser)

        self.conn_db_dialog = ""

        # ------------------------       Top    -----------------------------
        self.toppane = QDockWidget()
        self.toppane.setFeatures(self.toppane.NoDockWidgetFeatures)
        self.addDockWidget(Qt.TopDockWidgetArea, self.toppane)
        #self.toppane.setWidget(widget)

        # ------------ Search Field (immediately below top file menu) ---------------
        """
        dir = os.getcwd() + '/images/'
        search_pixmap    = QPixmap(dir + "search-small.jpg")
        search_label     = QLabel()
        search_label.setPixmap(search_pixmap)
        self.search_text = QLineEdit()
        self.search_text.setFrame(False)

        search_menubar     = QMenuBar()
        search_option_menu = search_menubar.addMenu("&Search Scope Switch")
        self.search_scope_switch(search_option_menu)

        searchArea = QHBoxLayout()
        searchArea.addWidget(search_label)
        searchArea.addWidget(self.search_text)
        searchArea.addWidget(search_menubar)
        searchArea.setStretchFactor(     search_label, 0.5)
        searchArea.setStretchFactor(self.search_text,   25)
        searchArea.setStretchFactor(     search_menubar, 4)

        widget = QWidget()
        widget.setLayout(searchArea)
        self.search_text.textChanged.connect  (self.searchPathSuggest_)
        self.search_text.returnPressed.connect(self.searchFileByName_)
        """

        # ------------------- Left Pane (file trees, etc.) ------------------
        self.leftpane   = QDockWidget()
        self.leftpane.setFeatures(self.leftpane.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftpane)

        self.bottompane = QDockWidget()
        self.bottompane.setFeatures(self.bottompane.NoDockWidgetFeatures)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottompane)

        # -------- pop up tree during starting, multi-threading ---------
        if self.config.flag_read():
            self.loadFiles()
        self.writeSettings()

        self.rightpane = RightPane(self)
        self.close     = Close(self.rightpane)



    def search_entry(self):
        dir = os.getcwd() + '/images/'
        search_pixmap = QPixmap(dir + "search-small.jpg")
        #search_pixmap = QPixmap(dir + "double-arrow.jpg")
        #search_pixmap = QPixmap(dir + "double5.png")
        search_label  = QLabel()
        search_label.setPixmap(search_pixmap)
        search_text   = QLineEdit()
        search_text.setFrame(False)

        searchArea    = QHBoxLayout()
        searchArea.addWidget(search_label)
        searchArea.addWidget(search_text)
        searchArea.setStretchFactor(search_label, 0.5)
        searchArea.setStretchFactor(search_text,   25)

        search_widget = QWidget()
        search_widget.setLayout(searchArea)
        return search_widget, search_text


        # ------------------------     Right   -----------------------------

    def search_scope_switch(self, search_option_menu):

        ag   = QActionGroup(self, exclusive=True)

        msg1 = 'Search files ... in directories'
        ac1  = ag.addAction(QAction(msg1, self, checkable=True))
        search_option_menu.addAction(ac1)
        ac1.triggered.connect(lambda: self.ac_action1(search_option_menu, msg1))

        msg2 = 'Search data item names  ... in databases'
        ac2  = ag.addAction(QAction(msg2, self, checkable=True))
        search_option_menu.addAction(ac2)
        ac2.triggered.connect(lambda: self.ac_action2(search_option_menu, msg2))

        msg3 = 'Search processing logic ... in databases'
        ac3  = ag.addAction(QAction(msg3, self, checkable=True))
        search_option_menu.addAction(ac3)
        ac3.triggered.connect(lambda: self.ac_action3(search_option_menu, msg3))


    def ac_action1(self, menu, msg):
        print("search msg=", msg)
        menu.setTitle(msg)

    def ac_action2(self, menu, msg):
        print("search msg=", msg)
        menu.setTitle(msg)

    def ac_action3(self, menu, msg):
        print("search msg=", msg)
        menu.setTitle(msg)


    def searchPathSuggest_(self):
        print("You can put the suggested path into the search area")
        i = 1


    # ---------------------- Search Bar Action ------------------------
    def searchFileByName_(self, searchText):

        if self.travelpath != "":
            if self.search_text.text():
                searchText = self.search_text.text()

            node = self.find_nodeid.nodeid(self.glo.nodelist, self.travelpath, searchText)
            if node != []:
                if  node[5][5] == 'sql' or  node[5][5] == 'py'  or node[5][5] == 'txt' or \
                    node[5][5] == 'log' or  node[5][5] == 'xml' or node[5][5] == 'conf':
                    self.tree1.file_doubleclicked.clicked(node[0])

    def datainitHovered(self, action):
        tip = action.toolTip()
        QToolTip.showText(QCursor.pos(), tip)

    # ------------------------ File Menu -----------------------------
    def loadFiles(self):
        data_load                = DataLoad(self.glo)
        self.glo.nodelist        = data_load.list_node()
        self.glo.sqltrace        = data_load.list_sqlquerytrace()
        self.glo.sqlinsertsels   = data_load.list_sqlinsertselcls()
        self.glo.sqlqueryselcols = data_load.list_sqlqueryselcols()

        self.dldialog = DataLoadDialog(self, self.glo.nodelist, self.glo)
        self.dldialog.exec_()
        root_ = ""
        if self.dldialog.result() == 0:
            root_ = self.dldialog.OnReturnPressed()
        else:
            root_ = self.dldialog.OnOk()

        if root_:
            self.selectedPath.append(root_)
            self.pathidx = len(self.selectedPath) - 1
            self.loadFiles2(root_)
            self.travelpath = root_

    def backward_load_file(self):
        path_ = ""
        len_ = len(self.selectedPath)
        if len_ > 0:
            if self.pathidx - 1 >= 0:
                self.pathidx -= 1
                path_ = self.selectedPath[self.pathidx]
                self.loadFiles2(path_)
            else:
                path_ = ""
        return path_

    def forward_load_file(self):
        path_ = ""
        len_ = len(self.selectedPath)
        if len_ > 0:
            if self.pathidx < len_ - 1:
                self.pathidx += 1
                path_ = self.selectedPath[self.pathidx]
                self.loadFiles2(path_)
            else:
                path_ = ""
        return path_

    def loadFiles2(self, root_):
        nodeobj = NodeList2TreeFile()

        list_one_root = nodeobj.nodelistfilter_(self.glo.nodelist, root_)

        nodeobj.nodelist2treefile_(list_one_root)
        self.treeDisplay()

    def loadDBs(self):
        i = 1

    def travelFiles(self):
        #self.search_text.setText('travel file system to gather information')
        self.dsd = DataSourceDialog(self, self.selectionList, self.glo)
        self.selectionList = self.dsd.selectionList_()
        self.dsd.exec_()
        if self.dsd.result() == 0:
            path_ = self.dsd.OnReturnPressed()
            self.travelpath = path_
        else:
            path_ = self.dsd.OnOk()
        if path_:                                                                   # a valid path to travel
            self.selectedPath.append(path_)
            self.pathidx = len(self.selectedPath) - 1
            self.travelFiles2(path_)
            self.loadFiles()

    def travelFiles2(self, path_):                                                  # travel to collect info is done in travelFiles2()
        self.selectedPath.append(path_)
        self.travelpath = path_
        travel_type = "file system"
        travel_result = travel_('t', self.travelpath, travel_type, self.glo)        # travel is done in travel_(), which is in  travel_.py
        if travel_result:
            self.selectionList = self.dsd.add_(path_)
            self.treeDisplay()
        else:
            self.selectionList = self.dsd.delete_(path_)
            self.travelpath = ""
        self.dsd.write_()

    def travelDBs(self):
        print("travel databases")


    @pyqtSlot()
    def treeDisplay(self):
        self.treeFile       = os.getcwd() + '\\tmp_files\\tree_file.txt'
        self.treeDBTable    = os.getcwd() + '\\tmp_files\\tree_dbtable.txt'
        self.treeDBProc     = os.getcwd() + '\\tmp_files\\tree_dbproc.txt'

        self.travelTreeFile    = QFile(self.treeFile)
        self.travelTreeDBTable = QFile(self.treeDBTable)
        self.travelTreeDBProc  = QFile(self.treeDBProc)

        self.travelTreeFile.open(   QIODevice.ReadOnly)
        self.travelTreeDBTable.open(QIODevice.ReadOnly)
        self.travelTreeDBProc.open( QIODevice.ReadOnly)

        bytes1 = self.travelTreeFile.   readAll()
        bytes2 = self.travelTreeDBTable.readAll()
        bytes3 = self.travelTreeDBProc. readAll()


        # ----------------------------- tree1 and tree2 search
        self.tree1_search_widget, self.tree1_search_text = self.search_entry() 
        self.tree1_search_text.returnPressed.connect(self.search_file_tree)
        self.tree1_search_row = 0

        self.tree2_search_widget, self.tree2_search_text = self.search_entry()
        self.tree2_search_text.returnPressed.connect(self.search_db_tree)
        self.tree2_search_row = 0

        #------------------------------ cross search button
        self.cross_search_button = QToolButton()
        self.cross_search_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.cross_search_button.setMaximumSize(14,14)
        self.cross_search_button.resize(14,14)
        dir_   = os.getcwd() + '/images/'
        search_pixmap = QPixmap(dir_ + "double-arrow.png")
        icon = QIcon()
        icon.addPixmap(search_pixmap)
        self.cross_search_button.setIcon(icon)
        self.cross_search_button.clicked.connect(self.cross_search)

        dir_   = os.getcwd() + '/images/'

        #------------------------------ left and right arrow pixmaps
        arrow_left_pixmap  = QPixmap(dir_ + "arrow-left-triangle.png")
        self.arrow_left_icon = QIcon()
        self.arrow_left_icon.addPixmap( arrow_left_pixmap)

        arrow_right_pixmap = QPixmap(dir_ + "arrow-right-triangle.png")
        self.arrow_right_icon = QIcon()
        self.arrow_right_icon.addPixmap(arrow_right_pixmap)

        #------------------------------ left and right arrow buttons
        self.tree1_arrow_button = QToolButton()
        self.tree1_arrow_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.tree1_arrow_button.setMaximumSize(12,12)
        self.tree1_arrow_button.resize(12,12)
        self.tree1_arrow_button.setIcon(self.arrow_left_icon)
        self.tree1_arrow_button.clicked.connect(self.tree1_arrow)

        self.tree2_arrow_button = QToolButton()
        self.tree2_arrow_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.tree2_arrow_button.setMaximumSize(12,12)
        self.tree2_arrow_button.resize(12,12)
        self.tree2_arrow_button.setIcon(self.arrow_left_icon)
        self.tree2_arrow_button.clicked.connect(self.tree2_arrow)

        #------------------------------ trees, layouts, and widgets
        self.tree1   = TreeView1(self, self.glo, bytes1)
        self.tree2   = TreeView1(self, self.glo, bytes2)
        self.tree3   = TreeView1(self, self.glo, bytes3)

        self.tree1.setProperty("TreeName", "FileTree" )
        self.tree2.setProperty("TreeName", "DBTableTree"  )
        self.tree3.setProperty("TreeName", "DBProcTree"  )

        search_layout  = QHBoxLayout()

        search_widget  = QWidget()

        #------------------------------ search_layout assembly
        search_layout.addWidget(self.tree1_arrow_button)
        search_layout.addWidget(self.tree1_search_widget)
        search_layout.addWidget(self.cross_search_button)
        search_layout.addWidget(self.tree2_search_widget)
        search_layout.addWidget(self.tree2_arrow_button)
        search_widget.setLayout(search_layout)

        #------------------------------ tree_layout assembly
        tree_vsplitter = QSplitter(Qt.Vertical)
        tree_hsplitter = QSplitter(Qt.Horizontal)
        
        tree_vsplitter.addWidget(self.tree2)
        tree_vsplitter.addWidget(self.tree3)

        tree_hsplitter.addWidget(self.tree1)
        tree_hsplitter.addWidget(tree_vsplitter)

        #------------------------------ leftpane assembly
        self.leftbox        = QVBoxLayout()
        self.leftbox.addWidget(search_widget)
        self.leftbox.addWidget(tree_hsplitter)
        self.leftbox.setStretchFactor(search_widget, 1)
        self.leftbox.setStretchFactor(tree_hsplitter, 20)

        self.leftwidget     = QWidget()
        self.leftwidget.setLayout(self.leftbox)
        self.leftpane.setWidget(self.leftwidget)

        #------------------------------ close, title, repaint
        self.travelTreeFile.close()
        self.tree1.model.setHorizontalHeaderLabels(["File System Path"])
        # self.tree1.expandToDepth(1)
        self.travelTreeDBTable.close()
        self.travelTreeDBProc.close()
        self.tree2.model.setHorizontalHeaderLabels(["Database Tables"])
        self.tree3.model.setHorizontalHeaderLabels(["Database Procs"])
        self.tree1.repaint()
        self.tree2.repaint()


    def tree1_arrow(self):
        if self.tree1.isVisible(): 
            self.tree1_arrow_button.setIcon(self.arrow_right_icon)
            self.tree1.hide()
            self.tree1_search_widget.hide()
            self.cross_search_button.hide()
            if self.tree2.isVisible(): 
                self.leftpane.setMinimumSize(QSize(100, 0))
            else:
                self.leftpane.setMinimumSize(QSize(0, 0))
        else:
            self.tree1_arrow_button.setIcon(self.arrow_left_icon)
            self.tree1.show()
            self.tree1_search_widget.show()
            if self.tree2.isVisible(): 
                self.cross_search_button.show()
                self.leftpane.setMinimumSize(QSize(200, 0))
            else: 
                self.leftpane.setMinimumSize(QSize(100, 0))


    def tree2_arrow(self):
        if self.tree2.isVisible(): 
            self.tree2_arrow_button.setIcon(self.arrow_right_icon)
            self.tree2.hide()
            self.tree3.hide()
            self.tree2_search_widget.hide()
            self.cross_search_button.hide()
            if self.tree1.isVisible(): 
                self.leftpane.setMinimumSize(QSize(100, 0))
            else:
                self.leftpane.setMinimumSize(QSize(0, 0))
        else:
            self.tree2_arrow_button.setIcon(self.arrow_left_icon)
            self.tree2.show()
            self.tree3.show()
            self.tree2_search_widget.show()
            if self.tree1.isVisible(): 
                self.cross_search_button.show()
                self.leftpane.setMinimumSize(QSize(200, 0))
            else: 
                self.leftpane.setMinimumSize(QSize(100, 0))



    def iterItems(self, root):
        if root is not None:
            stack = [root]
            while stack:
                parent = stack.pop(0)
                for row in range(parent.rowCount()):
                    for column in range(parent.columnCount()):
                        child = parent.child(row, column)
                        yield child
                        if child.hasChildren():
                            stack.append(child)

    def search_file_tree(self):
        searchphrase = self.tree1_search_text.text()
        if searchphrase == "":
            self.tree1_search_row = 0
        last_row = self.tree1_search_row
        rootItem = self.tree1.model.invisibleRootItem()
        self.search_file_traverse(rootItem, searchphrase, self.tree1_search_row)
        if last_row == self.tree1_search_row:
            self.tree1_search_row = 0 
            self.search_file_traverse(rootItem, searchphrase, self.tree1_search_row)


    def search_file_traverse(self, root, searchphrase, start_row):
        for item in self.iterItems(root): 
            if searchphrase in item.text() and item.index().row() > start_row: 
                self.tree1.setCurrentIndex(item.index())
                self.tree1_search_row = item.index().row()
                return


    def search_db_tree(self):
        searchphrase = self.tree2_search_text.text()
        if searchphrase == "":
            self.tree2_search_row = 0
        last_row = self.tree2_search_row
        rootItem = self.tree2.model.invisibleRootItem()
        self.search_db_traverse(rootItem, searchphrase, self.tree2_search_row)
        if last_row == self.tree2_search_row:
            self.tree2_search_row = 0
            self.search_db_traverse(rootItem, searchphrase, self.tree2_search_row)


    def search_db_traverse(self, root, searchphrase, start_row):
        for item in self.iterItems(root): 
            if searchphrase in item.text() and item.index().row() > start_row: 
                self.tree2.setCurrentIndex(item.index())
                self.tree2_search_row = item.index().row()
                return


    def cross_search(self):
        text1_buffer = ""
        text2_buffer = ""
        text1 = self.tree1_search_text.text()
        text2 = self.tree2_search_text.text()
        if not text1 == "":
            text1_buffer = text1
        if not text2 == "":
            text2_buffer = text2
        if not text1 == "": 
            self.tree2_search_text.setText(text1_buffer)
        if not text2 == "": 
            self.tree1_search_text.setText(text2_buffer)


    def OnOpen(self):
        print("open ..................")

    def OnCopy(self):
        print("copy ..................")

    def OnPrint(self):
        print("print .................")

    # ------------------------ Search Menu    -----------------------------
    def datalineage_filesql(self):
        print("data lineage search (thru SQL files)")

    def datalineage_dbsql(self):
        print("data lineage search (thru stored procedures)")

    def datalineage_mixsql(self):
        print("data lineage search (SQL files/stored procedures)")

    # ------------------------ Close Sub Menu -----------------------------
    def OnClearDisplay(self):
        nodelist = []
        nodeobj  = NodeList2TreeFile()
        nodeobj.nodelist2treefile_(nodelist)
        self.travelpath = ''
        self.treeDisplay()

    def OnClear(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText("Clear collected data in TR repository")
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox Demo")
        msg.setDetailedText("Data in TR repository will be cleared. These data are " + \
                            "previously collected file system information.")
        msg.addButton("OK",     msg.AcceptRole)
        msg.addButton("Cancel", msg.RejectRole)
        msg.buttonClicked.connect(self.msgbtn)
        self.travelpath = ''
        retval = msg.exec_()

    def msgbtn(self, i):
        if i.text() == "OK":
            data_delete = DataClear()
            data_delete.truncate_all_db_tables_(self.glo)
            dbload   = DataLoad(self.glo)
            nodelist = dbload.list_node()

            nodeobj  = NodeList2TreeFile()
            nodeobj.nodelist2treefile_(nodelist)
            self.travelpath = ''
            self.treeDisplay()
            tro = Tables_TRO()
            tro.reset_count('TR_Node',   self.glo.dbserver_[0])
            tro.reset_count('TR_File',   self.glo.dbserver_[0])
            tro.reset_count('TR_SQL',    self.glo.dbserver_[0])
            tro.reset_count('TR_Server', self.glo.dbserver_[0])

            tro.reset_count('TR_Table',  self.glo.dbserver_[0])
            tro.reset_count('TR_Proc',   self.glo.dbserver_[0])


    def OnClose(self):
        self.close.exec_()

    def contextMenuEvent(self, event):
        self.file.exec_(event.globalPos())

    # ------------------------ Connection Menu -----------------------------
    def OnToDatabase(self):
        conn_db = ConnectDatabase(self, self.glo)
        if conn_db.exec_() == QDialog.Accepted:    # when success, placs itself into list glo.dbconn_
            self.travel_db.travel_db(conn_db, self.glo)
            for table in self.glo.db_tbl_lst_: 
                for tbl in table: 
                    self.tblcolumns.a_query(tbl, conn_db, self.glo)  # each tbl = [ db, table, [.....]  ]

            # for proc in self.glo.db_proc_lst_: 
            #     for prc in proc: 
            #         print("mainwindow_menu.py,   OnToDatabase(),   prc=", prc)

            obj2tree = DBObject2TreeFile()
            obj2tree.table2treefile(self.glo)        # make a tree_dbtable.txt file
            obj2tree.proc2treefile(self.glo)         # make a tree_dbproc.txt  file
        #elif conn_db.exec_() == QDialog.Rejected:
        #    print("mainwindow_menu.py,    OnToDatabase(),   making new connection rejected")


    # ------------------------ Setting Menu -----------------------------
    def OnGuiDataLoad(self):
        if self.config.flag_read() == True:
            self.config.flag_write("False")
            self.dataloadAction.setChecked(False)
        else:
            self.config.flag_write("True")
            self.dataloadAction.setChecked(True)

    def OnLayout(self):
        print("mainwindow_menu.py,  OnLayout()")

    def OnUser(self):
        print("mainwindow_menu.py,  OnUser()")

    def showEvent(self, event):
        i = 1

    def writeSettings(self):
        self.leftpane.setMinimumSize(QSize(100, 0))

