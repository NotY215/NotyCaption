# Installer.py ── NotyCaption modern compact installer (resizable, clean dark theme)
# INCLUDES: Privacy Policy, Terms & Conditions, Legal Disclaimer

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

# Legal documents filenames
README_FILE   = "Readme.html"
TOC_FILE      = "T&C.html"
PRIVACY_FILE  = "Privacy.html"

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
        winreg.SetValueEx(k, "URLInfoAbout",    0, winreg.REG_SZ, "https://github.com/NotY215/NotyCaption")
        winreg.SetValueEx(k, "URLUpdateInfo",   0, winreg.REG_SZ, "https://github.com/NotY215/NotyCaption/releases")
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
            if not has_internet():
                raise Exception("Internet connection required for first-time setup")

            self.progress.emit(12, "System check…")
            if round(psutil.virtual_memory().total / (1024**3),1) < MIN_RAM_GB:
                raise Exception(f"Minimum {MIN_RAM_GB} GB RAM required")

            self.progress.emit(22, "Creating installation folder…")
            self.path.mkdir(parents=True, exist_ok=True)

            self.progress.emit(38, "Copying application files…")
            for f in (MAIN_EXE, UNINSTALL_EXE):
                src = res_path(f)
                if not os.path.isfile(src):
                    raise Exception(f"Missing file: {f}")
                shutil.copy2(src, self.path / f)

            # Copy legal documents to installation directory
            legal_files = [README_FILE, TOC_FILE, PRIVACY_FILE]
            for legal_file in legal_files:
                src = res_path(legal_file)
                if os.path.isfile(src):
                    shutil.copy2(src, self.path / legal_file)

            ico = res_path("App.ico")

            if self.desktop:
                self.progress.emit(58, "Creating desktop shortcut…")
                create_shortcut(str(self.path/MAIN_EXE),
                    str(Path.home()/"Desktop"/f"{APP_NAME}.lnk"), ico)

            if self.startmenu:
                self.progress.emit(70, "Creating Start Menu entries…")
                sm = Path(os.environ["ProgramData"])/"Microsoft"/"Windows"/"Start Menu"/"Programs"/APP_NAME
                sm.mkdir(parents=True, exist_ok=True)
                create_shortcut(str(self.path/MAIN_EXE),       str(sm/f"{APP_NAME}.lnk"),       ico)
                create_shortcut(str(self.path/UNINSTALL_EXE), str(sm/f"Uninstall {APP_NAME}.lnk"), ico)
                # Add documentation shortcuts
                if (self.path / PRIVACY_FILE).exists():
                    create_shortcut(str(self.path/PRIVACY_FILE), str(sm/f"Privacy Policy.lnk"), ico)
                if (self.path / TOC_FILE).exists():
                    create_shortcut(str(self.path/TOC_FILE), str(sm/f"Terms & Conditions.lnk"), ico)

            if self.startup:
                self.progress.emit(84, "Adding to startup…")
                add_to_startup(str(self.path))

            self.progress.emit(94, "Registering in Windows…")
            if not register_uninstall(str(self.path)):
                raise Exception("Registry registration failed")

            self.progress.emit(100, "Installation complete!")
            time.sleep(0.6)
            self.done.emit()

        except Exception as e:
            self.error.emit(str(e))

# ─── Main Window ──────────────────────────────────────────────────────────────
class InstallerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} Setup")
        self.resize(900, 700)
        self.setMinimumSize(860, 640)

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
        self.cb_accept_terms = None
        self.cb_accept_privacy = None
        self.cb_accept_disclaimer = None
        self.prog = self.status = None

        self.create_pages()

    def create_pages(self):
        # ── Welcome Page ───────────────────────────────────────────────────────
        p1 = QWidget()
        l1 = QVBoxLayout(p1)
        l1.setContentsMargins(36,32,36,32)
        l1.setSpacing(20)

        title = QLabel(f"Welcome to {APP_NAME} Pro")
        title.setStyleSheet("font-size: 32px; font-weight: 700; color: #89b4fa;")
        title.setAlignment(Qt.AlignCenter)
        l1.addWidget(title)

        subtitle = QLabel("AI-Powered Professional Caption Generator")
        subtitle.setStyleSheet("font-size: 16px; color: #a6e3a1; margin-bottom: 15px;")
        subtitle.setAlignment(Qt.AlignCenter)
        l1.addWidget(subtitle)

        br = QTextBrowser()
        br.setOpenExternalLinks(True)
        br.setHtml(self.load_doc(README_FILE, "Welcome to NotyCaption Pro"))
        l1.addWidget(br, 1)

        next_btn = QPushButton("Next →")
        next_btn.setFixedHeight(46)
        next_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        l1.addWidget(next_btn, alignment=Qt.AlignRight)
        self.stack.addWidget(p1)

        # ── Legal Agreements Page (Terms, Privacy, Disclaimer) ─────────────────
        p2 = QWidget()
        l2 = QVBoxLayout(p2)
        l2.setContentsMargins(36,32,36,32)
        l2.setSpacing(20)

        title2 = QLabel("Legal Agreements")
        title2.setStyleSheet("font-size: 28px; font-weight: 700; color: #f38ba8;")
        title2.setAlignment(Qt.AlignCenter)
        l2.addWidget(title2)

        # Tabs for legal documents
        legal_tabs = QTabWidget()
        legal_tabs.setStyleSheet("""
            QTabWidget::pane { background: #181824; border-radius: 7px; }
            QTabBar::tab { padding: 10px 20px; }
        """)

        # Terms & Conditions Tab
        terms_tab = QWidget()
        terms_layout = QVBoxLayout(terms_tab)
        terms_browser = QTextBrowser()
        terms_browser.setOpenExternalLinks(True)
        terms_browser.setHtml(self.load_doc(TOC_FILE, "Terms & Conditions"))
        terms_layout.addWidget(terms_browser)
        legal_tabs.addTab(terms_tab, "📜 Terms & Conditions")

        # Privacy Policy Tab
        privacy_tab = QWidget()
        privacy_layout = QVBoxLayout(privacy_tab)
        privacy_browser = QTextBrowser()
        privacy_browser.setOpenExternalLinks(True)
        privacy_browser.setHtml(self.load_doc(PRIVACY_FILE, "Privacy Policy"))
        privacy_layout.addWidget(privacy_browser)
        legal_tabs.addTab(privacy_tab, "🔒 Privacy Policy")

        l2.addWidget(legal_tabs, 2)

        # Disclaimer Warning Box
        disclaimer_box = QGroupBox("⚠️ IMPORTANT DISCLAIMER - READ CAREFULLY")
        disclaimer_box.setStyleSheet("QGroupBox { color: #ff4081; border-color: #ff4081; }")
        disclaimer_layout = QVBoxLayout(disclaimer_box)
        disclaimer_text = QLabel(
            "TO THE MAXIMUM EXTENT PERMITTED BY LAW:\n\n"
            "• THIS SOFTWARE IS PROVIDED 'AS IS' AND 'AS AVAILABLE'\n"
            "• YOU USE THIS SOFTWARE AT YOUR OWN RISK\n"
            "• WE ARE NOT RESPONSIBLE FOR ANY DATA LOSS, DAMAGE, OR CORRUPTION\n"
            "• WE ARE NOT RESPONSIBLE FOR ANY UNAUTHORIZED ACCESS TO YOUR GOOGLE ACCOUNT\n"
            "• YOU AGREE THAT YOU CANNOT TAKE ANY LEGAL ACTION AGAINST THE DEVELOPERS\n"
            "• BY INSTALLING, YOU AGREE TO THE GOVERNING LAW OF INDIA (Patna, Bihar)"
        )
        disclaimer_text.setWordWrap(True)
        disclaimer_text.setStyleSheet("color: #ff4081; font-size: 12px; padding: 10px;")
        disclaimer_layout.addWidget(disclaimer_text)
        l2.addWidget(disclaimer_box)

        # Checkboxes for agreements
        self.cb_accept_terms = QCheckBox("I have read and agree to the Terms and Conditions")
        self.cb_accept_terms.setStyleSheet("font-size: 13px; padding: 5px 0;")
        l2.addWidget(self.cb_accept_terms)

        self.cb_accept_privacy = QCheckBox("I have read and agree to the Privacy Policy")
        self.cb_accept_privacy.setStyleSheet("font-size: 13px; padding: 5px 0;")
        l2.addWidget(self.cb_accept_privacy)

        self.cb_accept_disclaimer = QCheckBox("I acknowledge the Disclaimer and agree not to take legal action against NotY215")
        self.cb_accept_disclaimer.setStyleSheet("font-size: 13px; padding: 5px 0; color: #ff4081;")
        l2.addWidget(self.cb_accept_disclaimer)

        # Navigation buttons
        hb = QHBoxLayout()
        hb.addStretch()
        back = QPushButton("← Back")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        cont = QPushButton("Accept & Continue →")
        cont.clicked.connect(self.to_options)
        hb.addWidget(back)
        hb.addSpacing(16)
        hb.addWidget(cont)
        l2.addLayout(hb)
        self.stack.addWidget(p2)

        # ── Options + Progress Page ────────────────────────────────────────────
        p3 = QWidget()
        l3 = QVBoxLayout(p3)
        l3.setContentsMargins(36,28,36,28)
        l3.setSpacing(18)

        title3 = QLabel("Installation Settings")
        title3.setStyleSheet("font-size: 26px; font-weight: 700; color: #89b4fa;")
        title3.setAlignment(Qt.AlignCenter)
        l3.addWidget(title3)

        gb_path = QGroupBox("Destination Folder")
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

        gb_opt = QGroupBox("Optional Shortcuts")
        lo = QVBoxLayout(gb_opt)
        self.cb_desktop  = QCheckBox("Create Desktop shortcut")
        self.cb_sm       = QCheckBox("Create Start Menu shortcuts")
        self.cb_startup  = QCheckBox("Run application at Windows startup")
        self.cb_startup.setStyleSheet("color: #a6e3a1;")
        for cb in (self.cb_desktop, self.cb_sm, self.cb_startup):
            cb.setChecked(True if cb is not self.cb_startup else False)
            lo.addWidget(cb)
        l3.addWidget(gb_opt)

        self.prog = QProgressBar()
        self.prog.setVisible(False)
        self.prog.setRange(0,100)
        l3.addWidget(self.prog)

        self.status = QLabel("Ready to install")
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
                    body {{ font-family: 'Segoe UI', sans-serif; color: #d0d8ff; background: #181824; line-height: 1.58; }}
                    h1, h2, h3 {{ color: #89b4fa; }}
                    a {{ color: #b4befe; }}
                    pre {{ background: #242436; padding: 10px; border-radius: 6px; }}
                    .disclaimer {{ color: #ff4081; font-weight: bold; }}
                </style></head><body>{txt}</body></html>"""
            except: pass
        return f"<h2>{fallback}</h2><p>File <code>{fname}</code> not found.</p>"

    def browse(self):
        d = QFileDialog.getExistingDirectory(self, "Select installation folder", DEFAULT_ROOT)
        if d: self.path_edit.setText(str(Path(d)/FOLDER_NAME))

    def to_options(self):
        # Check all agreements are accepted
        if not self.cb_accept_terms.isChecked():
            QMessageBox.warning(self, "Agreement Required", 
                "You must accept the Terms and Conditions to continue.")
            return
        if not self.cb_accept_privacy.isChecked():
            QMessageBox.warning(self, "Agreement Required", 
                "You must accept the Privacy Policy to continue.")
            return
        if not self.cb_accept_disclaimer.isChecked():
            QMessageBox.warning(self, "Disclaimer Required", 
                "You must acknowledge the Disclaimer to continue.\n\n"
                "By using this software, you agree that you cannot take legal action against the developers.")
            return
        
        self.stack.setCurrentIndex(2)

    def install(self):
        p = self.path_edit.text().strip()
        if not p:
            QMessageBox.warning(self, "Path Required", "Please select an installation location.")
            return

        path = Path(p)
        if path.exists() and any(path.iterdir()):
            r = QMessageBox.question(self, "Folder Not Empty",
                "The selected folder contains files.\nContinue installation anyway?",
                QMessageBox.Yes | QMessageBox.No)
            if r != QMessageBox.Yes: 
                return

        if not is_admin():
            QMessageBox.information(self, "Administrator Rights Required",
                "Setup requires administrator privileges.\nRestarting with elevated rights...")
            relaunch_as_admin()
            QApplication.quit()
            return

        self.prog.setVisible(True)
        self.prog.setValue(0)
        self.status.setText("Preparing installation...")

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
        QMessageBox.critical(self, "Installation Error", msg)
        self._enable_controls()

    def on_done(self):
        QMessageBox.information(self, "Installation Successful",
            f"{APP_NAME} Pro has been installed successfully!\n\n"
            f"⚠️ REMINDER: You are using this software at your own risk.\n"
            f"You have agreed not to take legal action against NotY215.\n\n"
            f"Click OK to launch the application.")
        QApplication.quit()

    def _enable_controls(self):
        for w in (self.cb_desktop, self.cb_sm, self.cb_startup, self.path_edit):
            w.setEnabled(True)

    def closeEvent(self, event):
        if hasattr(self, 'thread') and self.thread.isRunning():
            r = QMessageBox.question(self, "Installation In Progress",
                "Installation is currently running.\nCancel and exit?",
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
        r = QMessageBox.question(None, "Elevation Required",
            f"{APP_NAME} Pro Setup needs administrator rights.\n\n"
            f"⚠️ By continuing, you agree to the Terms & Conditions, Privacy Policy, "
            f"and Disclaimer. You acknowledge that you use this software at your own risk "
            f"and cannot take legal action against NotY215.\n\n"
            f"Run as administrator?",
            QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            relaunch_as_admin()
        sys.exit(0)

    w = InstallerUI()
    w.show()
    sys.exit(app.exec())