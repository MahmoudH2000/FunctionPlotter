import plotter
from PySide6 import QtWidgets 
import sys

app = QtWidgets.QApplication(sys.argv)
plot_dialog = plotter.GraphPlotter()
plot_dialog.show()
sys.exit(app.exec())