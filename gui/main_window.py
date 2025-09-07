import threading
import socket
from PyQt6 import QtWidgets, QtGui, QtCore
import qrcode
from PIL.ImageQt import ImageQt
from app.database import query_visitors, export_visitors_to_excel
from flask import Flask
import sys

# Flask app import
from app import create_app

app = create_app()

server_thread = None
server_running = False

def run_flask_in_thread(host, port):
    app.run(host=host, port=port, threaded=True)

def start_server(host, port):
    global server_thread, server_running
    if server_running:
        return
    server_thread = threading.Thread(target=run_flask_in_thread, args=(host, port), daemon=True)
    server_thread.start()
    server_running = True

def stop_server():
    global server_running
    server_running = False

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.168.1.100", 5000))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

DEFAULT_PORT = 5000

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Police Academy Visitor Manager")
        self.resize(900, 600)

        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Server controls
        top_row = QtWidgets.QHBoxLayout()
        self.ip_label = QtWidgets.QLabel("Host IP:")
        self.ip_value = QtWidgets.QLineEdit(get_local_ip())
        self.port_label = QtWidgets.QLabel("Port:")
        self.port_value = QtWidgets.QLineEdit(str(DEFAULT_PORT))
        self.start_btn = QtWidgets.QPushButton("Start Server")
        self.stop_btn = QtWidgets.QPushButton("Stop Server")
        self.stop_btn.setEnabled(False)

        self.start_btn.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        self.stop_btn.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold;")

        top_row.addWidget(self.ip_label)
        top_row.addWidget(self.ip_value)
        top_row.addWidget(self.port_label)
        top_row.addWidget(self.port_value)
        top_row.addWidget(self.start_btn)
        top_row.addWidget(self.stop_btn)
        layout.addLayout(top_row)

        # QR code
        qr_row = QtWidgets.QHBoxLayout()
        self.qr_label = QtWidgets.QLabel()
        self.qr_label.setFixedSize(200, 200)
        qr_controls = QtWidgets.QVBoxLayout()
        self.generate_qr_btn = QtWidgets.QPushButton("Generate QR for /visit")
        self.qr_url_label = QtWidgets.QLineEdit()
        self.save_qr_btn = QtWidgets.QPushButton("Save QR image")
        qr_controls.addWidget(self.generate_qr_btn)
        qr_controls.addWidget(self.qr_url_label)
        qr_controls.addWidget(self.save_qr_btn)
        qr_row.addWidget(self.qr_label)
        qr_row.addLayout(qr_controls)
        layout.addLayout(qr_row)

        # Search / Export
        search_row = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search by name or national id...")
        self.search_btn = QtWidgets.QPushButton("Search")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.export_btn = QtWidgets.QPushButton("Export Excel")
        search_row.addWidget(self.search_input)
        search_row.addWidget(self.search_btn)
        search_row.addWidget(self.refresh_btn)
        search_row.addWidget(self.export_btn)
        layout.addLayout(search_row)

        # Table
        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "National ID", "Phone", "Reason", "Submitted At"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Connect signals
        self.start_btn.clicked.connect(self.on_start)
        self.stop_btn.clicked.connect(self.on_stop)
        self.generate_qr_btn.clicked.connect(self.on_generate_qr)
        self.save_qr_btn.clicked.connect(self.on_save_qr)
        self.refresh_btn.clicked.connect(self.load_table)
        self.search_btn.clicked.connect(self.on_search)
        self.export_btn.clicked.connect(self.on_export)

        self.current_qr_img = None
        self.load_table()

        self.statusBar().showMessage("جاهز للعمل ✅")

    def on_start(self):
        host = self.ip_value.text().strip() or "0.0.0.0"
        port = int(self.port_value.text().strip() or DEFAULT_PORT)
        start_server(host, port)
        QtWidgets.QMessageBox.information(self, "Server", f" Server started working on http://{host}:{port} ✅")
        self.statusBar().showMessage(f"السيرفر شغال على {host}:{port}")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def on_stop(self):
        stop_server()
        QtWidgets.QMessageBox.warning(self, "Server", "Server stopped⛔")
        self.statusBar().showMessage("Server is turned off❌")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def on_generate_qr(self):
        url = f"http://{self.ip_value.text()}:{self.port_value.text()}/visit"
        self.qr_url_label.setText(url)
        img = qrcode.make(url)
        from PIL import Image
        if not isinstance(img, Image.Image):
            img = img.get_image()
        qim = ImageQt(img).copy()
        pix = QtGui.QPixmap.fromImage(qim).scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.qr_label.setPixmap(pix)
        self.current_qr_img = img

    def on_save_qr(self):
        if self.current_qr_img is None:
            QtWidgets.QMessageBox.warning(self, "QR", "Generate a QR first.")
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save QR", "visitor_qr.png", "PNG Files (*.png)")
        if path:
            self.current_qr_img.save(path)
            QtWidgets.QMessageBox.information(self, "Saved", f"QR saved to {path}")

    def load_table(self, search=None):
        rows = query_visitors(search)
        self.table.setRowCount(0)
        for r in rows:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            for c, val in enumerate(r):
                it = QtWidgets.QTableWidgetItem(str(val) if val is not None else "")
                self.table.setItem(row_idx, c, it)

    def on_search(self):
        term = self.search_input.text().strip()
        self.load_table(search=term)

    def on_export(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Excel", "visitors.xlsx", "Excel Files (*.xlsx)")
        if path:
            export_visitors_to_excel(path)
            QtWidgets.QMessageBox.information(self, "Export", f"Exported visitors to {path}")

