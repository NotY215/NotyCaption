# uninstaller.py
# Fixed self-deletion version - batch file should now be found and executed reliably

import sys
import os
import shutil
import winreg
import ctypes
import subprocess
import time
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QMessageBox, QGroupBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QThread, Signal

APP_NAME = "NotyCaption"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restart_elevated():
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable,
            " ".join(f'"{arg}"' for arg in sys.argv),
            None, 1
        )
    except:
        pass


def get_install_path():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\\" + APP_NAME
        )
        val, _ = winreg.QueryValueEx(key, "InstallLocation")
        winreg.CloseKey(key)
        return Path(val).resolve()
    except:
        pass

    # Fallback: uninstaller is inside APP_NAME folder?
    here = Path(sys.executable if getattr(sys, 'frozen', False) else __file__).parent.resolve()
    if here.name == APP_NAME:
        return here

    return None


def remove_startup_entry():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except:
        return False


def delete_shortcuts():
    deleted = []
    paths = [
        Path(os.environ["USERPROFILE"]) / "Desktop" / f"{APP_NAME}.lnk",
        Path(os.environ["ProgramData"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / APP_NAME,
        Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / APP_NAME,
    ]

    for p in paths:
        try:
            if p.is_file():
                p.unlink(missing_ok=True)
                deleted.append(p.name)
            elif p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
                deleted.append(p.name)
        except:
            pass
    return deleted


def clean_registry():
    deleted = []
    keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\\" + APP_NAME,
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\\" + APP_NAME,
    ]
    for k in keys:
        try:
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, k)
            deleted.append(k.split("\\")[-1])
        except:
            pass
    return deleted


class UninstallWorker(QThread):
    update = Signal(int, str)
    done   = Signal(bool, str, list)

    def __init__(self, install_dir: Path, self_exe: Path):
        super().__init__()
        self.install_dir = install_dir
        self.self_exe    = self_exe

    def run(self):
        removed = []

        try:
            self.update.emit(5, "Verifying installation…")
            if not self.install_dir or not self.install_dir.exists():
                self.done.emit(False, "Installation folder not found.", [])
                return

            self.update.emit(18, "Removing startup entry…")
            if remove_startup_entry():
                removed.append("Startup entry removed")

            self.update.emit(32, "Deleting shortcuts…")
            removed.extend(delete_shortcuts())

            self.update.emit(48, "Cleaning registry…")
            removed.extend(clean_registry())

            self.update.emit(65, "Removing program files…")

            self_is_inside = self.install_dir == self.self_exe.parent.resolve()

            if self_is_inside:
                # Delete everything except the running exe
                for child in self.install_dir.iterdir():
                    if child.resolve() == self.self_exe.resolve():
                        continue
                    try:
                        if child.is_file() or child.is_symlink():
                            child.unlink(missing_ok=True)
                        elif child.is_dir():
                            shutil.rmtree(child, ignore_errors=True)
                    except:
                        pass
                removed.append("Application files (except uninstaller)")
            else:
                try:
                    shutil.rmtree(self.install_dir, ignore_errors=False)
                    removed.append("Entire installation folder")
                except Exception as ex:
                    removed.append(f"Partial file removal ({ex})")

            self.update.emit(85, "Preparing final cleanup (self-delete)…")

            # ────────────────────────────────────────────────────────────────
            #   Create self-deleting batch file
            # ────────────────────────────────────────────────────────────────

            bat_commands = [
                "@echo off",
                "setlocal",
                "title Cleaning up NotyCaption - please wait",
                "timeout /t 4 /nobreak >nul 2>&1",
                f'rmdir /s /q "{self.install_dir}" 2>nul',
                'del /f /q "%~f0" 2>nul',
            ]

            if not self_is_inside:
                bat_commands.insert(-2, f'del /f /q "{self.self_exe}" 2>nul')

            bat_text = "\n".join(bat_commands)

            # Try current folder first (most reliable in many cases)
            bat_filename = f"~cleanup_{APP_NAME}_{int(time.time())}.bat"
            bat_path = Path.cwd() / bat_filename

            try:
                bat_path.write_text(bat_text, encoding="ansi")
            except:
                # Fallback to TEMP
                from tempfile import gettempdir
                bat_path = Path(gettempdir()) / bat_filename
                bat_path.write_text(bat_text, encoding="ansi")

            # Launch hidden and detached
            subprocess.Popen(
                f'cmd.exe /c start "" /b "{bat_path}"',
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            )

            removed.append("Self-deletion batch created and launched")
            if self_is_inside:
                removed.append("Uninstaller will delete itself")

            self.update.emit(100, "Uninstallation complete")
            time.sleep(1.1)

            self.done.emit(True, f"{APP_NAME} has been removed from your system.", removed)

        except Exception as e:
            self.done.emit(False, f"Critical error:\n{str(e)}", removed)


class UninstallUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Remove {APP_NAME}")
        self.resize(740, 560)
        self.setMinimumSize(700, 520)

        self.setStyleSheet("""
            QMainWindow {background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #0f0f1a, stop:1 #1a1a2e);}
            QWidget {color:#e0e0ff; font-family:Segoe UI;}
            QLabel {color:#cdd6f5;}
            QGroupBox {font-weight:600; color:#f38ba8; border:1px solid #45475a; border-radius:9px; margin-top:12px; padding-top:10px;}
            QGroupBox::title {left:12px; padding:0 6px;}
            QPushButton {background:#3b4261; color:#e0e0ff; border:none; border-radius:7px; padding:10px 20px; font-weight:600;}
            QPushButton:hover {background:#525a7a;}
            QPushButton#UnBtn {background:#f38ba8; color:#1e1e2e; font-weight:bold;}
            QPushButton#UnBtn:hover {background:#fab387;}
            QProgressBar {border:2px solid #45475a; border-radius:7px; background:#1e1e2e; text-align:center; color:#e0e0ff; height:26px; font-weight:600;}
            QProgressBar::chunk {background:qlineargradient(x1:0 y1:0, x2:1 y2:0, stop:0 #f38ba8, stop:1 #fab387); border-radius:5px;}
        """)

        central = QWidget()
        self.setCentralWidget(central)
        ly = QVBoxLayout(central)
        ly.setContentsMargins(32,24,32,28)
        ly.setSpacing(16)

        title = QLabel(f"Uninstall {APP_NAME}")
        title.setStyleSheet("font-size:26px; font-weight:700; color:#f38ba8;")
        title.setAlignment(Qt.AlignCenter)
        ly.addWidget(title)

        st_gb = QGroupBox("Status")
        st_ly = QVBoxLayout(st_gb)
        self.lbl_status = QLabel("Looking for installation…")
        self.lbl_status.setStyleSheet("font-size:15px; font-weight:600;")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        st_ly.addWidget(self.lbl_status)
        ly.addWidget(st_gb)

        rem_gb = QGroupBox("Will be removed")
        rem_ly = QVBoxLayout(rem_gb)
        for t in [
            "Application files & folder",
            "Shortcuts (Desktop + Start Menu)",
            "Startup entry",
            "Registry entries",
            "Uninstaller + self-deletion batch"
        ]:
            rem_ly.addWidget(QLabel("• " + t))
        ly.addWidget(rem_gb)

        self.bar = QProgressBar()
        self.bar.setVisible(False)
        self.bar.setRange(0,100)
        ly.addWidget(self.bar)

        self.msg = QLabel("")
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.setStyleSheet("font-size:14px; color:#a6e3a1;")
        ly.addWidget(self.msg)

        ly.addStretch()

        btn_ly = QHBoxLayout()
        btn_ly.addStretch()
        cancel = QPushButton("Cancel")
        cancel.setFixedSize(130,46)
        cancel.clicked.connect(self.close)
        btn_ly.addWidget(cancel)

        self.btn_un = QPushButton("Uninstall Now")
        self.btn_un.setObjectName("UnBtn")
        self.btn_un.setFixedSize(170,46)
        self.btn_un.clicked.connect(self.start)
        btn_ly.addWidget(self.btn_un)
        ly.addLayout(btn_ly)

        self.install_path = get_install_path()
        self.self_path = Path(sys.executable if getattr(sys,'frozen',False) else __file__).resolve()

        if self.install_path and self.install_path.exists():
            self.lbl_status.setText("Found installation")
            self.lbl_status.setStyleSheet("color:#a6e3a1;")
            self.btn_un.setEnabled(True)
        else:
            self.lbl_status.setText("Installation not found")
            self.lbl_status.setStyleSheet("color:#fab387;")
            self.btn_un.setEnabled(False)

    def start(self):
        if not is_admin():
            QMessageBox.warning(self, "Admin rights needed",
                "Please run as administrator.")
            restart_elevated()
            QApplication.quit()
            return

        if QMessageBox.question(
            self, "Confirm",
            f"Remove {APP_NAME} completely?\nThis cannot be undone.\n\nThe uninstaller will delete itself.",
            QMessageBox.Yes | QMessageBox.No
        ) != QMessageBox.Yes:
            return

        self.btn_un.setEnabled(False)
        self.bar.setVisible(True)
        self.bar.setValue(0)
        self.msg.setText("Starting…")

        self.worker = UninstallWorker(self.install_path, self.self_path)
        self.worker.update.connect(self.on_update)
        self.worker.done.connect(self.on_done)
        self.worker.start()

    def on_update(self, val, text):
        self.bar.setValue(val)
        self.msg.setText(text)

    def on_done(self, ok, msg, lst):
        self.bar.setVisible(False)
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Information if ok else QMessageBox.Critical)
        box.setWindowTitle("Result")
        box.setText("Uninstall " + ("finished" if ok else "failed"))
        txt = msg
        if lst:
            txt += "\n\nRemoved:\n• " + "\n• ".join(lst)
        box.setInformativeText(txt)
        box.exec()

        if ok:
            time.sleep(1.2)
            QApplication.quit()
        else:
            self.btn_un.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    if not is_admin():
        if QMessageBox.question(None, "Run as administrator?",
            "Uninstaller needs elevated privileges.\nRestart as admin?") == QMessageBox.Yes:
            restart_elevated()
        sys.exit()

    w = UninstallUI()
    w.show()
    sys.exit(app.exec())