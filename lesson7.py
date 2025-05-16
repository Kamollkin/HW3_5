import sys, os, sqlite3, socket, shutil

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableView, QPushButton, QLineEdit, QLabel, QStatusBar,
    QFileDialog, QMessageBox, QFormLayout, QSpinBox, QProgressBar, QSplashScreen, QGraphicsOpacityEffect
)

from PyQt6.QtGui import QAction, QMovie
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery


class PortScammer(QThread):
    progress = pyqtSignal(int, bool)
    finished = pyqtSignal()

    def __init__(self, host, ports):
        super().__init__()
        self.host, self.ports = host, ports

    def run(self):
        for p in self.ports:
            s = socket.socket(); s.settimeout(0.3)
            ok = (s.connect_ex((self.host, p)) == 0)
            s.close()
            self.progress.emit(p, ok)
            self.finished.emit()

class DataBaseManager:
    def __init__(self, path = "people.db"):
        self.path = path
    def init(self):
        if not os.exists(self.path):
            conn = sqlite3.connect(self.path)
            conn.execute(*** CREATE TABLE ussers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                
            )***)
            conn.commit(); conn.close()
            

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.path)
        if not self.db.open():
            raise RuntimeError(self.db.lastError().text())
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD + Network Tools ")
        self.resize(900, 600)

        self.dbm = DataBaseManager(); self.dbm.init_db()
        self.model = QSqlTableModel(self, self.dbm.db)
        self.model.setTable("ussers")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.select()
        for i, hdr in enumerate(("ID", "Name", "Age")):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, hdr)
        
        self._build_ui()
        self.animate_table()

    def _build_ui(self):
        m = self.menuBar().addMenu("File")
        for text, method in [("Export CSV", self.export_csv), ("Import CSV", self.import_csv), ("Backup DB", self.backup_db)]:
            act = QAction(text, self, triggered = method)
            m.addAction(act)
            self.addToolBar("T").addAction(act)

        w = QWidget(); self.setCentralWidget(w)
        lay = QVBoxLayout(w)

        h = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText("Поиск по имени...")
        h.addWidget(self.search)
        for txt, fn in [("🔍", self.apply_filter), ("✖️", self.clear_filter)]:
            btn = QPushButton(txt); btn.clicked.connect(fn); h.addWidget(btn)
        lay.addWidget(h)

        self.tv = QTableView()
        self.tv.setModel(self.model)
        self.tv.setSortingEnabled(True)
        self.tv.doubleClicked.connect(self.on_row_double)
        self.tv.horizontalHeader().setStretchLastSection(True)
        self.tv.resizeColumnsToContents()
        lay.addWidget(self.tv)

        frm = QFormLayout()
        self.name = QLineEdit()
        self.age = QSpinBox()
        self.age.setRange(0,200)
        frm.addRow("Name:", self.name)
        frm.addRow("Age:", self.age)
        lay.addWidget(frm)

        h2 = QHBoxLayout()
        for txt, fn in [
            ("Add", self.add_rec),
            ("Update", self.update_rec),
            ("Delete", self.delete_rec)
        ]:
            btn = QPushButton(txt)
            btn.clicked.connect(fn)
            h2.addWidget(btn)
        lay.addLayout(h2)

        lay.addWidget(QLabel("Port Scanner:"))
        nf = QFormLayout()
        self.host = QLineEdit(socket.gethostname())
        self.ports = QLineEdit("22,80-85, 443")
        scan_btn = QPushButton("Scan ports")
        scan_btn.clicked.connect(self.scan_ports)
        nf.addRow("Host:", self.host)
        nf.addRow("Ports:", self.ports)
        nf.addRow(scan_btn)
        lay.addWidget(nf)

        self.spinner_lbl = QLabel()
        self.spinner = QMovie("spinner.gif")
        self.spinner_lbl.setMovie(self.spinner)
        self.spinner_lbl.setVisible(False)
        lay.addWidget(self.spinner_lbl)

        self.pb = QProgressBar()
        self.pb.setVisible(False)
        lay.addWidget(self.pb)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def animate_table(self):
        eff = QGraphicsOpacityEffect(self.tv)
        self.tv.setGraphicsEffect(eff)
        anim = QPropertyAnimation(eff, b"opacity", self)
        anim.setStartValue(0.2)
        anim.setEndValue(1.0)
        anim.setDuration(600)
        anim.start()

        

