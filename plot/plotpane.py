import os
import sys
from PyQt4.QtCore      import *
from PyQt4.QtGui       import *
from plot.simple_curve import SimpleCurve
from plot.barchart_cnt import BarChartCount
from plot.barchart_amt import BarChartAmount
from plot.line_with_blocks    import LineWithBlocks
from plot.piechart            import PieChart
from plot.fill_between_curves import FillBetweenCurves
from plot.scatter_dots        import ScatterDots


# plotting: 
# plotpane.py, simple_curve.py, barchar_cnt.py, barchart_amt.py, curve_with_blocks.py
# gui\centralareaop.py, gui\toolbar.py, tables\table_op.py, tables\tableview.py

# adding new plot, involving only:
# plotpane.py, table_op.py, the new plot.py




class PlotPane(QDialog):                               # instantiated in toolbar.py
    def __init__(self, parent=None):
        super(PlotPane, self).__init__(parent)
        self.setWindowTitle("Plot Setup")
        self.mw = parent
        self.t_op = ""

        _menubar  = QMenuBar()
        self._plotmenu = _menubar.addMenu('Plot Types')
        _plot_simple_curve = self._plotmenu.addAction('Plot Simple Curve')
        _plot_barchart_cnt = self._plotmenu.addAction('Plot Bar Chart Distinct Count')
        _plot_barchart_amt = self._plotmenu.addAction('Plot Bar Chart Accumulated Amt')
        _plot_line_w_blcks = self._plotmenu.addAction('Plot Line With Blocks')
        _plot_pie_chart    = self._plotmenu.addAction('Plot Pie Chart')
        _plot_pie_explode  = self._plotmenu.addAction('Plot Pie Explode')
        _plot_fill_between = self._plotmenu.addAction('Plot Fill Between 2 Curves')
        _plot_scatter_dots = self._plotmenu.addAction('Plot Scatter Dots')
        _plot_line_curve   = self._plotmenu.addAction('Plot Line Curve')
        _plot_histogram    = self._plotmenu.addAction('Plot Histogram')
        _plot_scatter_disc = self._plotmenu.addAction('Plot Scatter Disc')

        self.connect(_plot_simple_curve, SIGNAL('triggered()'), self.plot_simple_curve)
        self.connect(_plot_barchart_cnt, SIGNAL('triggered()'), self.plot_barchart_cnt)
        self.connect(_plot_barchart_amt, SIGNAL('triggered()'), self.plot_barchart_amt)
        self.connect(_plot_line_w_blcks, SIGNAL('triggered()'), self.plot_line_with_blocks)
        self.connect(_plot_pie_chart,    SIGNAL('triggered()'), self.plot_pie_chart)
        self.connect(_plot_pie_explode,  SIGNAL('triggered()'), self.plot_pie_explode)
        self.connect(_plot_fill_between, SIGNAL('triggered()'), self.plot_fill_between)
        self.connect(_plot_scatter_dots, SIGNAL('triggered()'), self.plot_scatter_dots)
        self.connect(_plot_line_curve,   SIGNAL('triggered()'), self.plot_line_curve)
        self.connect(_plot_histogram,    SIGNAL('triggered()'), self.plot_histogram)
        self.connect(_plot_scatter_disc, SIGNAL('triggered()'), self.plot_scatter_disc)

        layout1 = QVBoxLayout()
        layout1.addWidget(_menubar)

        self.layout2 = QVBoxLayout()

        self.buttonYes  = QPushButton('Plot', self)
        self.buttonYes.clicked.connect(self.handlePlot)
        self.buttonNo   = QPushButton('Cancel', self)
        self.buttonNo.clicked.connect(self.handleCancel)

        layout3 = QHBoxLayout()
        layout3.addWidget(self.buttonYes)
        layout3.addWidget(self.buttonNo)

        layout  = QVBoxLayout(self)
        layout.addLayout(layout1)
        layout.addLayout(self.layout2)
        layout.addLayout(layout3)

        self.x = ""
        self.y = ""
        self.z = ""

        self.num_widgets = 0
        self.widget_x = ""
        self.widget_y = ""
        self.widget_z = ""

        self.setWindowModality(Qt.NonModal)



    def t_op_(self):
        index = self.mw.tabs.currentIndex()

        sqlwindow = self.mw.central.sqlwindows[index]
        tableCombo = sqlwindow[3][1]

        if tableCombo: 
            if tableCombo.t_op: 
                self.t_op = tableCombo.t_op
        return self.t_op



    def plot_simple_curve(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Simple Curve")
        self.t_op.chart_type = "simple_curve"
        self.plot_2_columns_choices()

    def plot_barchart_cnt(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Bar Chart Distinct Count")
        self.t_op.chart_type = "barchart_cnt"
        self.plot_1_column_choice()

    def plot_barchart_amt(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Bar Chart Accumulated Amount")
        self.t_op.chart_type = "barchart_amt"
        self.plot_2_columns_choices()

    def plot_line_with_blocks(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Line With Blocks")
        self.t_op.chart_type = "line_with_blocks"
        self.plot_2_columns_choices()

    def plot_pie_chart(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Pie Chart")
        self.t_op.chart_type = "piechart"
        self.plot_2_columns_choices()

    def plot_pie_explode(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Pie Explode")
        self.t_op.chart_type = "pie_explode"
        self.plot_2_columns_choices()

    def plot_fill_between(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Fill Between 2 Curves")
        self.t_op.chart_type = "fill_between"
        self.plot_3_columns_choices()

    def plot_scatter_dots(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Scatter Dots")
        self.t_op.chart_type = "scatter_dots"
        self.plot_2_columns_choices()

    def plot_line_curve(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Line Curve")
        self.t_op.chart_type = "line_curve"
        self.plot_2_columns_choices()

    def plot_histogram(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Histogram")
        self.t_op.chart_type = "histogram"
        self.plot_2_columns_choices()

    def plot_scatter_disc(self):
        self.t_op = self.t_op_()
        self._plotmenu.setTitle("Plot Scatter Disc")
        self.t_op.chart_type = "scatter_disc"
        self.plot_3_columns_choices()



    def plot_1_column_choice(self):
        self.remove_widgets()

        label_x  = QLabel("X")
        self.x   = QLineEdit()
        self.x.setToolTip("click on column head  to pick a column of data as x values")

        layout_x = QHBoxLayout()
        layout_x.addWidget(label_x)
        layout_x.addWidget(self.x)
        self.widget_x = QWidget()
        self.widget_x.setLayout(layout_x)

        self.layout2.addWidget(self.widget_x)

        self.num_widgets = 1



    def plot_2_columns_choices(self):
        self.remove_widgets()
        self.plot_1_column_choice()

        label_y  = QLabel("Y")
        self.y   = QLineEdit()
        self.y.setToolTip("click on column head  to pick a column of data as y values")

        layout_y = QHBoxLayout()
        layout_y.addWidget(label_y)
        layout_y.addWidget(self.y)
        self.widget_y = QWidget()
        self.widget_y.setLayout(layout_y)

        self.layout2.addWidget(self.widget_y)
        self.num_widgets = 2



    def plot_3_columns_choices(self):
        self.remove_widgets()
        self.plot_2_columns_choices()

        label_z  = QLabel("Z")
        self.z   = QLineEdit()
        self.z.setToolTip("click on column head  to pick a column of data as z values")

        layout_z = QHBoxLayout()
        layout_z.addWidget(label_z)
        layout_z.addWidget(self.z)
        self.widget_z = QWidget()
        self.widget_z.setLayout(layout_z)

        self.layout2.addWidget(self.widget_z)
        self.num_widgets = 3



    def remove_widgets(self):
        if   self.num_widgets == 1: 
            self.remove_1_widget()
        elif self.num_widgets == 2: 
            self.remove_2_widget()
        elif self.num_widgets == 3: 
            self.remove_3_widget()
        self.num_widgets = 0



    def remove_1_widget(self):
        if self.widget_x != "": 
            self.layout2.removeWidget(self.widget_x)
            self.widget_x.deleteLater()
            del self.widget_x
            self.widget_x = ""
            self.x = ""



    def remove_2_widget(self):
        self.remove_1_widget()

        if self.widget_y != "": 
            self.layout2.removeWidget(self.widget_y)
            self.widget_y.deleteLater()
            del self.widget_y
            self.widget_y = ""
            self.y = ""



    def remove_3_widget(self):
        self.remove_2_widget()

        if self.widget_z != "": 
            self.layout2.removeWidget(self.widget_z)
            self.widget_z.deleteLater()
            del self.widget_z
            self.widget_z = ""
            self.z = ""



    def handlePlot(self):

        if   self.t_op.chart_type == "simple_curve": 
            plot_simple_curve = SimpleCurve()
            plot_simple_curve.plot_simple_curve(self.x.text(), self.x_col_data, self.y.text(), self.y_col_data)
            plot_simple_curve.show()

        elif self.t_op.chart_type == "barchart_cnt": 
            plot_barchart_cnt = BarChartCount()
            plot_barchart_cnt.plot_barchart_cnt(self.x.text(), self.x_col_data)

        elif self.t_op.chart_type == "barchart_amt": 
            plot_barchart_amt = BarChartAmount()
            plot_barchart_amt.plot_barchart_amt(self.x.text(), self.x_col_data, self.y.text(), self.y_col_data)

        elif self.t_op.chart_type == "line_with_blocks": 
            plot_line_with_blocks = LineWithBlocks()
            plot_line_with_blocks.plot_line_with_blocks(self.x.text(), self.x_col_data, self.y.text(), self.y_col_data)

        elif self.t_op.chart_type == "piechart": 
            plot_piechart = PieChart()
            plot_piechart.plot_piechart(self.x_col_data, self.y_col_data)

        elif self.t_op.chart_type == "fill_between": 
            plot_fill_between = FillBetweenCurves()
            plot_fill_between.plot_fill_between_curves("Fill Between", self.x_col_data, self.y_col_data, self.z_col_data)

        elif self.t_op.chart_type == "scatter_dots": 
            plot_scatter_dots = ScatterDots()
            plot_scatter_dots.plot_scatter_dots(self.x_col_data, self.y_col_data)

        self.mw.toolbar.unset_chart_flg()
        self.remove_widgets()

        self.accept()



    def handleCancel(self): 
        self.mw.toolbar.unset_chart_flg()
        self.remove_widgets()

        self.reject()



    def display_colnm(self, colaxis, colnm, col_data):
        if self.num_widgets == 1:
            if colaxis == 'x':
                if self.widget_x != "":
                    self.x.setText(colnm)
                    self.x_col_data = col_data

        if self.num_widgets == 2:
            if colaxis == 'x':
                if self.widget_x != "":
                    self.x.setText(colnm)
                    self.x_col_data = col_data
            if colaxis == 'y':
                if self.widget_y != "":
                    self.y.setText(colnm)
                    self.y_col_data = col_data

        if self.num_widgets == 3:
            if colaxis == 'x':
                if self.widget_x != "":
                    self.x.setText(colnm)
                    self.x_col_data = col_data
            if colaxis == 'y':
                if self.widget_y != "":
                    self.y.setText(colnm)
                    self.y_col_data = col_data
            if colaxis == 'z':
                print("plotpane.py,    display_colnm(),   .................... colaxis=", colaxis)

                if self.widget_z != "":
                    self.z.setText(colnm)
                    self.z_col_data = col_data



if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    login = PlotPane()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())

