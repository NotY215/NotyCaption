# Installer.py ── NotyCaption modern compact installer (resizable, clean dark theme)

import sys, os, shutil, ctypes, socket, time
from pathlib import Path
import psutil, winreg
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextBrowser, QPushButton, QLineEdit, QCheckBox, QGroupBox,
    QProgressBar, QFileDialog, QMessageBox
)
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import Qt, QThread, Signal
from win32com.client import Dispatch

# ─── Constants ────────────────────────────────────────────────────────────────
APP_NAME      = "NotyCaption"
PUBLISHER     = "NotY215 and Team"
FOLDER_NAME   = "NotyCaption"
DEFAULT_ROOT  = r"C:\Program Files"
MIN_RAM_GB    = 4
MAIN_EXE      = "NotyCaption.exe"
UNINSTALL_EXE = "uninstall.exe"

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def relaunch_as_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable,
            " ".join(f'"{a}"' for a in sys.argv), None, 1)
    except: pass

def has_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), 3.0)
        return True
    except: return False

def res_path(file):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, file)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

def create_shortcut(target, lnk_path, icon=None):
    try:
        shell = Dispatch('WScript.Shell')
        sc = shell.CreateShortCut(lnk_path)
        sc.Targetpath = target
        sc.WorkingDirectory = os.path.dirname(target)
        if icon and os.path.exists(icon): sc.IconLocation = icon
        sc.save()
        return True
    except: return False

def register_uninstall(install_dir):
    try:
        k = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
            rf"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{APP_NAME}")
        winreg.SetValueEx(k, "DisplayName",     0, winreg.REG_SZ, APP_NAME)
        winreg.SetValueEx(k, "Publisher",       0, winreg.REG_SZ, PUBLISHER)
        winreg.SetValueEx(k, "InstallLocation", 0, winreg.REG_SZ, install_dir)
        winreg.SetValueEx(k, "UninstallString", 0, winreg.REG_SZ, os.path.join(install_dir, UNINSTALL_EXE))
        winreg.SetValueEx(k, "DisplayIcon",     0, winreg.REG_SZ, os.path.join(install_dir, MAIN_EXE))
        winreg.SetValueEx(k, "NoModify",        0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(k, "NoRepair",        0, winreg.REG_DWORD, 1)
        winreg.CloseKey(k)
        return True
    except: return False

def add_to_startup(install_dir):
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, APP_NAME, 0, winreg.REG_SZ, os.path.join(install_dir, MAIN_EXE))
        winreg.CloseKey(k)
        return True
    except: return False

# ─── Worker ───────────────────────────────────────────────────────────────────
class InstallThread(QThread):
    progress = Signal(int, str)
    done     = Signal()
    error    = Signal(str)

    def __init__(self, path, desktop, startmenu, startup):
        super().__init__()
        self.path     = Path(path).resolve()
        self.desktop  = desktop
        self.startmenu = startmenu
        self.startup  = startup

    def run(self):
        try:
            self.progress.emit(5, "Checking internet…")
            if not has_internet(): raise Exception("Internet required")

            self.progress.emit(12, "System check…")
            if round(psutil.virtual_memory().total / (1024**3),1) < MIN_RAM_GB:
                raise Exception(f"≥ {MIN_RAM_GB} GB RAM required")

            self.progress.emit(22, "Creating folder…")
            self.path.mkdir(parents=True, exist_ok=True)

            self.progress.emit(38, "Copying files…")
            for f in (MAIN_EXE, UNINSTALL_EXE):
                src = res_path(f)
                if not os.path.isfile(src): raise Exception(f"Missing: {f}")
                shutil.copy2(src, self.path / f)

            ico = res_path("App.ico")

            if self.desktop:
                self.progress.emit(58, "Desktop shortcut…")
                create_shortcut(str(self.path/MAIN_EXE),
                    str(Path.home()/"Desktop"/f"{APP_NAME}.lnk"), ico)

            if self.startmenu:
                self.progress.emit(70, "Start Menu entries…")
                sm = Path(os.environ["ProgramData"])/"Microsoft"/"Windows"/"Start Menu"/"Programs"/APP_NAME
                sm.mkdir(parents=True, exist_ok=True)
                create_shortcut(str(self.path/MAIN_EXE),       str(sm/f"{APP_NAME}.lnk"),       ico)
                create_shortcut(str(self.path/UNINSTALL_EXE), str(sm/f"Uninstall {APP_NAME}.lnk"), ico)

            if self.startup:
                self.progress.emit(84, "Adding to startup…")
                add_to_startup(str(self.path))

            self.progress.emit(94, "Registering uninstall…")
            if not register_uninstall(str(self.path)):
                raise Exception("Registry write failed")

            self.progress.emit(100, "Done!")
            time.sleep(0.6)
            self.done.emit()

        except Exception as e:
            self.error.emit(str(e))

# ─── Main Window ──────────────────────────────────────────────────────────────
class InstallerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} Setup")
        self.resize(860, 640)
        self.setMinimumSize(820, 580)

        ico_path = res_path("App.ico")
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0 y1:0, x2:1 y2:1,
                    stop:0 #0f0f1a, stop:1 #1a1a2e);
            }
            QWidget { color: #e0e0ff; font-family: Segoe UI, sans-serif; }
            QLabel { color: #cdd6f5; }
            QGroupBox {
                font-weight: 600; color: #89b4fa;
                border: 1px solid #45475a; border-radius: 9px;
                margin-top: 14px; padding-top: 10px;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }
            QLineEdit {
                background: #1e1e2e; border: 1px solid #45475a;
                border-radius: 6px; padding: 7px 10px; color: #e0e0ff;
            }
            QLineEdit:focus { border: 1px solid #89b4fa; }
            QPushButton {
                background: #3b4261; color: #e0e0ff; border: none;
                border-radius: 7px; padding: 9px 18px; font-weight: 600;
            }
            QPushButton:hover { background: #525a7a; }
            QPushButton#InstallBtn {
                background: #a6e3a1; color: #1e1e2e; font-size: 14px; font-weight: bold;
            }
            QPushButton#InstallBtn:hover { background: #c0ffbb; }
            QProgressBar {
                border: 2px solid #45475a; border-radius: 7px; background: #1e1e2e;
                text-align: center; color: #e0e0ff; height: 24px; font-weight: 600;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0 y1:0, x2:1 y2:0,
                    stop:0 #89b4fa, stop:1 #b4befe); border-radius: 5px;
            }
            QTextBrowser {
                background: #181824; border: 1px solid #45475a;
                border-radius: 7px; padding: 12px; color: #d0d8ff;
            }
            QCheckBox { spacing: 9px; font-size: 13px; }
            QCheckBox::indicator {
                width: 16px; height: 16px; border: 2px solid #585b70;
                border-radius: 3px; background: #1e1e2e;
            }
            QCheckBox::indicator:checked {
                background: #89b4fa; border-color: #89b4fa;
            }
        """)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.path_edit = self.cb_desktop = self.cb_sm = self.cb_startup = None
        self.prog = self.status = None

        self.create_pages()

    def create_pages(self):
        # ── Welcome ───────────────────────────────────────────────────────
        p1 = QWidget()
        l1 = QVBoxLayout(p1)
        l1.setContentsMargins(36,32,36,32)
        l1.setSpacing(20)

        title = QLabel(f"Welcome to {APP_NAME}")
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: #89b4fa;")
        title.setAlignment(Qt.AlignCenter)
        l1.addWidget(title)

        br = QTextBrowser()
        br.setOpenExternalLinks(True)
        br.setHtml(self.load_doc("Readme.html", "Welcome"))
        l1.addWidget(br, 1)

        next_btn = QPushButton("Next →")
        next_btn.setFixedHeight(46)
        next_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        l1.addWidget(next_btn, alignment=Qt.AlignRight)
        self.stack.addWidget(p1)

        # ── License ───────────────────────────────────────────────────────
        p2 = QWidget()
        l2 = QVBoxLayout(p2)
        l2.setContentsMargins(36,32,36,32)
        l2.setSpacing(20)

        title2 = QLabel("License Agreement")
        title2.setStyleSheet("font-size: 26px; font-weight: 700; color: #f38ba8;")
        title2.setAlignment(Qt.AlignCenter)
        l2.addWidget(title2)

        br2 = QTextBrowser()
        br2.setOpenExternalLinks(True)
        br2.setHtml(self.load_doc("T&C.html", "Terms & Conditions"))
        l2.addWidget(br2, 1)

        self.cb_accept = QCheckBox("I accept the terms and conditions")
        self.cb_accept.setStyleSheet("font-size: 14px; padding: 10px 0;")
        l2.addWidget(self.cb_accept)

        hb = QHBoxLayout()
        hb.addStretch()
        back = QPushButton("← Back")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        cont = QPushButton("Continue →")
        cont.clicked.connect(self.to_options)
        hb.addWidget(back)
        hb.addSpacing(16)
        hb.addWidget(cont)
        l2.addLayout(hb)
        self.stack.addWidget(p2)

        # ── Options + Progress ────────────────────────────────────────────
        p3 = QWidget()
        l3 = QVBoxLayout(p3)
        l3.setContentsMargins(36,28,36,28)
        l3.setSpacing(18)

        title3 = QLabel("Install Settings")
        title3.setStyleSheet("font-size: 26px; font-weight: 700; color: #89b4fa;")
        title3.setAlignment(Qt.AlignCenter)
        l3.addWidget(title3)

        gb_path = QGroupBox("Destination")
        lp = QVBoxLayout(gb_path)
        lp.addWidget(QLabel("Install to:"))

        h = QHBoxLayout()
        self.path_edit = QLineEdit(str(Path(DEFAULT_ROOT)/FOLDER_NAME))
        h.addWidget(self.path_edit, 1)
        brw = QPushButton("Browse…")
        brw.setFixedWidth(100)
        brw.clicked.connect(self.browse)
        h.addWidget(brw)
        lp.addLayout(h)
        l3.addWidget(gb_path)

        gb_opt = QGroupBox("Options")
        lo = QVBoxLayout(gb_opt)
        self.cb_desktop  = QCheckBox("Desktop shortcut")
        self.cb_sm       = QCheckBox("Start Menu shortcuts")
        self.cb_startup  = QCheckBox("Run at startup")
        self.cb_startup.setStyleSheet("color: #a6e3a1;")
        for cb in (self.cb_desktop, self.cb_sm, self.cb_startup):
            cb.setChecked(True if cb is not self.cb_startup else False)
            lo.addWidget(cb)
        l3.addWidget(gb_opt)

        self.prog = QProgressBar()
        self.prog.setVisible(False)
        self.prog.setRange(0,100)
        l3.addWidget(self.prog)

        self.status = QLabel("Ready")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("font-size: 14px; color: #a6e3a1; min-height: 24px;")
        l3.addWidget(self.status)

        l3.addStretch()

        hb3 = QHBoxLayout()
        hb3.addStretch()
        back3 = QPushButton("← Back")
        back3.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        inst = QPushButton("Install Now")
        inst.setObjectName("InstallBtn")
        inst.setFixedHeight(50)
        inst.clicked.connect(self.install)
        hb3.addWidget(back3)
        hb3.addSpacing(20)
        hb3.addWidget(inst)
        l3.addLayout(hb3)

        self.stack.addWidget(p3)

    def load_doc(self, fname, fallback):
        p = res_path(fname)
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as f:
                    txt = f.read()
                return f"""
                <html><head><style>
                    body {{ font-family:Segoe UI,sans-serif; color:#d0d8ff; background:#181824; line-height:1.58; }}
                    h1,h2,h3 {{ color:#89b4fa; }} a {{ color:#b4befe; }}
                    pre {{ background:#242436; padding:10px; border-radius:6px; }}
                </style></head><body>{txt}</body></html>"""
            except: pass
        return f"<h2>{fallback}</h2><p>File <code>{fname}</code> not found.</p>"

    def browse(self):
        d = QFileDialog.getExistingDirectory(self, "Select folder", DEFAULT_ROOT)
        if d: self.path_edit.setText(str(Path(d)/FOLDER_NAME))

    def to_options(self):
        if not self.cb_accept.isChecked():
            QMessageBox.warning(self, "Required", "You must accept the license.")
            return
        self.stack.setCurrentIndex(2)

    def install(self):
        p = self.path_edit.text().strip()
        if not p:
            QMessageBox.warning(self, "Path required", "Select install location.")
            return

        path = Path(p)
        if path.exists() and any(path.iterdir()):
            r = QMessageBox.question(self, "Folder not empty",
                "Folder contains files.\nContinue anyway?",
                QMessageBox.Yes | QMessageBox.No)
            if r != QMessageBox.Yes: return

        if not is_admin():
            QMessageBox.information(self, "Admin needed",
                "Setup requires administrator rights.\nRestarting elevated…")
            relaunch_as_admin()
            QApplication.quit()
            return

        self.prog.setVisible(True)
        self.prog.setValue(0)
        self.status.setText("Preparing…")

        self.thread = InstallThread(
            p,
            self.cb_desktop.isChecked(),
            self.cb_sm.isChecked(),
            self.cb_startup.isChecked()
        )
        self.thread.progress.connect(self.on_prog)
        self.thread.done.connect(self.on_done)
        self.thread.error.connect(self.on_err)
        self.thread.start()

        for w in (self.cb_desktop, self.cb_sm, self.cb_startup, self.path_edit):
            w.setEnabled(False)

    def on_prog(self, v, txt):
        self.prog.setValue(v)
        self.status.setText(txt)

    def on_err(self, msg):
        self.prog.setVisible(False)
        self.status.setText("")
        QMessageBox.critical(self, "Error", msg)
        self._enable_controls()

    def on_done(self):
        QMessageBox.information(self, "Success",
            f"{APP_NAME} installed successfully!")
        QApplication.quit()

    def _enable_controls(self):
        for w in (self.cb_desktop, self.cb_sm, self.cb_startup, self.path_edit):
            w.setEnabled(True)

    def closeEvent(self, event):
        if hasattr(self, 'thread') and self.thread.isRunning():
            r = QMessageBox.question(self, "In progress",
                "Installation running.\nCancel & exit?",
                QMessageBox.Yes | QMessageBox.No)
            if r == QMessageBox.Yes:
                self.thread.terminate()
                self.thread.wait(1500)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    if not is_admin():
        r = QMessageBox.question(None, "Elevation required",
            f"{APP_NAME} Setup needs admin rights.\nRun as administrator?",
            QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            relaunch_as_admin()
        sys.exit(0)

    w = InstallerUI()
    w.show()
    sys.exit(app.exec())