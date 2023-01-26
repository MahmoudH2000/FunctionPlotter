from PySide6 import QtWidgets 
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class GraphPlotter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graph Plotter")

        # Layout
        self.Function    = QtWidgets.QLabel("F(x)")
        self.equation    = QtWidgets.QLineEdit()
        self.xmin_label  = QtWidgets.QLabel("Xmin")
        self.xmin_edit   = QtWidgets.QLineEdit()
        self.xmax_label  = QtWidgets.QLabel("Xmax")
        self.xmax_edit   = QtWidgets.QLineEdit()
        self.plot_button = QtWidgets.QPushButton("Plot")

        My_Layout = QtWidgets.QGridLayout()
        My_Layout.addWidget(self.Function, 0, 0)
        My_Layout.addWidget(self.equation, 0, 1, 2, -1)
        My_Layout.addWidget(self.xmin_label, 2, 0)
        My_Layout.addWidget(self.xmin_edit, 2, 1)
        My_Layout.addWidget(self.xmax_label, 2, 2)
        My_Layout.addWidget(self.xmax_edit, 2, 3)

        plot_layout = QtWidgets.QGridLayout()
        plot_layout.addWidget(self.plot_button, 0, 1)

        self.plot_button.clicked.connect(self.plot_function)

        # Create the matplotlib figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Create the main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(My_Layout)
        main_layout.addLayout(plot_layout)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

    def plot_function(self):
        try:

            function_str = self.equation.text()
            if(function_str == ''):
                self.show_error_message("Error, No Function given")
                return

            changed_s_in = self.resolve_function(function_str)
            

            Final = self.get_axis(changed_s_in)
            if Final is None:
                return
            else:
                x_axis, y_axis = Final

            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x_axis, y_axis)
            ax.set_xlabel('x')
            ax.set_ylabel('F(x)')
            ax.grid(True)
            ax.axhline(y=0, color='k')
            ax.axvline(x=0, color='k')
            self.canvas.draw()

        except:
            self.show_error_message("Invalid function or range (the function has to be a of x)")

    def resolve_function(self, f):
        
        Reserved_F = f

        # resolve power
        Reserved_F = Reserved_F.replace("^", "**")

        # resolve natural log
        Reserved_F = Reserved_F.replace("ln", "log")

        # resolve natural log
        Reserved_F = Reserved_F.replace("ln", "log")

        # resolve Eular's number
        Reserved_F = Reserved_F.replace("e", "2.718281828459045")

        return Reserved_F

    def get_axis(self, f):

        x = Symbol('x')

        x_min = float(self.xmin_edit.text())
        x_max = float(self.xmax_edit.text())

        f = parse_expr(f)

        # chack if the range is correct
        if(x_min >= x_max):
            self.show_error_message("Invalid range, Xmax has to be bigger than Xmin")
            return
        
        # get th X axis
        x_axis = [i for i in np.arange(x_min, x_max+0.1, 0.1)]

        # get th Y axis & check for errors
        try:
            y_axis = [float(f.subs(x,i)) for i in x_axis]
            return [x_axis, y_axis]
        except:
            y_axis = []
            self.show_error_message("Invalid range for F(x)")
            return

    def show_error_message(self, message):
        error = QtWidgets.QErrorMessage(self)
        error.showMessage(message)

