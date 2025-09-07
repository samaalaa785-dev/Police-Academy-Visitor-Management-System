import sys
from PyQt6 import QtWidgets
from app.database import init_db
from gui.main_window import MainWindow

def main():
    init_db()
    app_qt = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app_qt.exec())

if __name__ == "__main__":
    main()
