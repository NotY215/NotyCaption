# NotyCaption.py
# App name: NotyCaption
# Developer: NotY215
# All rights reserved by NotY215

import sys
import os
import json
import shutil
import subprocess
import logging
import traceback
import datetime
import socket
from datetime import timedelta
import whisper
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QTextEdit, QFileDialog,
    QMessageBox, QLineEdit, QScrollArea, QSlider, QProgressBar, QDialog,
    QGroupBox, QRadioButton,
)
from PyQt5.QtWidgets import QStyleFactory
from PyQt5.QtGui import QIcon, QColor, QTextCursor, QFont, QPalette
from PyQt5.QtCore import QTimer, Qt, QUrl, QDir, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from moviepy.editor import VideoFileClip, AudioFileClip
import pysrt
import pysubs2
from spleeter.separator import Separator
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import webbrowser


SCOPES = ['https://www.googleapis.com/auth/drive']


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ──────────────────────────────────────────────
# LOGGING SETUP – Fixed to always write next to EXE
# ──────────────────────────────────────────────
def setup_logging():
    # Always log next to the executable (works in both dev and frozen EXE)
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
    log_file = os.path.join(log_dir, f"NotyCaption_{timestamp}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ],
        force=True  # Ensure config is applied even if logging was initialized before
    )
    logging.info("=== NotyCaption started ===")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Working directory: {os.getcwd()}")
    logging.info(f"Log file: {log_file}")
    logging.info(f"PyInstaller frozen: {getattr(sys, 'frozen', False)}")
    logging.info(f"Executable path: {sys.executable if getattr(sys, 'frozen', False) else 'dev mode'}")
    return logging.getLogger("NotyCaption")


logger = setup_logging()


class SingleInstance:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.already_exists = False
        try:
            self.sock.bind(('127.0.0.1', 65432))
            self.sock.listen(1)
        except socket.error:
            self.already_exists = True

    def is_already_running(self):
        return self.already_exists

    def __del__(self):
        if not self.already_exists:
            try:
                self.sock.close()
            except:
                pass


# ──────────────────────────────────────────────
# SETTINGS & ENCRYPTION
# ──────────────────────────────────────────────
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(CURRENT_DIR, "settings.notcapz")
KEY_FILE = os.path.join(CURRENT_DIR, "key.notcapz")

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

fernet = Fernet(load_or_create_key())

def save_settings(settings_dict):
    data = json.dumps(settings_dict, ensure_ascii=False).encode('utf-8')
    encrypted = fernet.encrypt(data)
    with open(SETTINGS_FILE, "wb") as f:
        f.write(encrypted)

def load_settings():
    defaults = {
        "ui_scale": "100%",
        "theme": "Dark",
        "temp_dir": QDir.tempPath(),
        "models_dir": CURRENT_DIR,
    }
    if not os.path.exists(SETTINGS_FILE):
        save_settings(defaults)
        return defaults
    try:
        with open(SETTINGS_FILE, "rb") as f:
            enc = f.read()
        dec = fernet.decrypt(enc).decode('utf-8')
        loaded = json.loads(dec)
        defaults.update(loaded)
        return defaults
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        save_settings(defaults)
        return defaults


# ──────────────────────────────────────────────
# SETTINGS DIALOG
# ──────────────────────────────────────────────
class SettingsDialog(QDialog):
    settingsChanged = pyqtSignal(dict)

    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(540, 500)
        lay = QVBoxLayout()
        self.setLayout(lay)

        th_gb = QGroupBox("Theme")
        th_lay = QVBoxLayout()
        self.rb_win = QRadioButton("System Default")
        self.rb_light = QRadioButton("Light")
        self.rb_dark = QRadioButton("Dark (Modern)")
        th_lay.addWidget(self.rb_win)
        th_lay.addWidget(self.rb_light)
        th_lay.addWidget(self.rb_dark)

        th = current_settings.get("theme", "Dark")
        if th == "Windows Default": self.rb_win.setChecked(True)
        elif th == "Light": self.rb_light.setChecked(True)
        else: self.rb_dark.setChecked(True)

        th_gb.setLayout(th_lay)
        lay.addWidget(th_gb)

        sc_gb = QGroupBox("UI Scale")
        sc_lay = QHBoxLayout()
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["75%", "87%", "100%", "125%", "150%"])
        self.scale_combo.setCurrentText(current_settings.get("ui_scale", "100%"))
        sc_lay.addWidget(QLabel("Scale:"))
        sc_lay.addWidget(self.scale_combo)
        sc_gb.setLayout(sc_lay)
        lay.addWidget(sc_gb)

        tmp_gb = QGroupBox("Temporary Files Folder")
        tmp_lay = QHBoxLayout()
        self.tmp_edit = QLineEdit(current_settings.get("temp_dir", QDir.tempPath()))
        tmp_btn = QPushButton("Browse")
        tmp_btn.clicked.connect(self.browse_temp)
        tmp_lay.addWidget(self.tmp_edit)
        tmp_lay.addWidget(tmp_btn)
        tmp_gb.setLayout(tmp_lay)
        lay.addWidget(tmp_gb)

        mod_gb = QGroupBox("Whisper Models Folder")
        mod_lay = QHBoxLayout()
        self.mod_edit = QLineEdit(current_settings.get("models_dir", CURRENT_DIR))
        mod_btn = QPushButton("Browse")
        mod_btn.clicked.connect(self.browse_models)
        mod_lay.addWidget(self.mod_edit)
        mod_lay.addWidget(mod_btn)
        mod_gb.setLayout(mod_lay)
        lay.addWidget(mod_gb)

        btn_lay = QHBoxLayout()
        apply = QPushButton("Apply")
        apply.setStyleSheet("background:#007aff; color:white; padding:12px;")
        apply.clicked.connect(self.apply_close)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btn_lay.addStretch()
        btn_lay.addWidget(apply)
        btn_lay.addWidget(cancel)
        lay.addLayout(btn_lay)

    def browse_temp(self):
        d = QFileDialog.getExistingDirectory(self, "Select Temp Folder")
        if d: self.tmp_edit.setText(d)

    def browse_models(self):
        d = QFileDialog.getExistingDirectory(self, "Select Models Folder")
        if d: self.mod_edit.setText(d)

    def apply_close(self):
        new = {
            "ui_scale": self.scale_combo.currentText(),
            "theme": "Windows Default" if self.rb_win.isChecked() else
                     "Light" if self.rb_light.isChecked() else "Dark",
            "temp_dir": self.tmp_edit.text(),
            "models_dir": self.mod_edit.text(),
        }
        save_settings(new)
        self.settingsChanged.emit(new)
        self.accept()


# ──────────────────────────────────────────────
# MAIN WINDOW
# ──────────────────────────────────────────────
class NotyCaptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NotyCaption by NotY215")

        icon_path = resource_path('App.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        logger.info("Initializing main window...")

        self.settings = load_settings()
        self.apply_ui_scale()
        self.apply_theme()

        self.resize(920, 780)
        self.center()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        # Left - Editor
        self.left_panel = QWidget()
        self.left_panel.setMaximumWidth(620)
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        self.top_layout.addWidget(self.left_panel)

        title = QLabel("Caption Editor")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(title)

        self.caption_edit = QTextEdit()
        self.caption_edit.setReadOnly(True)
        self.caption_edit.setFont(QFont("Consolas", 13))
        self.caption_edit.setStyleSheet("background:#1e2225; color:#e0f0ff; border:1px solid #3f4a52;")
        self.left_layout.addWidget(self.caption_edit, 1)

        btn_row = QHBoxLayout()

        self.edit_btn = QPushButton("Edit Captions")
        self.edit_btn.setMinimumHeight(64)
        self.edit_btn.setStyleSheet("background:#0a84ff; color:white; border-radius:10px; font-weight:bold;")
        self.edit_btn.clicked.connect(self.toggle_edit)
        self.edit_btn.setEnabled(False)
        btn_row.addWidget(self.edit_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.setMinimumHeight(64)
        settings_btn.setStyleSheet("background:#5e5ce6; color:white; border-radius:10px; font-weight:bold;")
        settings_btn.clicked.connect(self.open_settings)
        btn_row.addWidget(settings_btn)

        self.download_btn = QPushButton("Download Model")
        self.download_btn.setMinimumHeight(64)
        self.download_btn.setStyleSheet("background:#ff9500; color:white; border-radius:10px; font-weight:bold;")
        self.download_btn.clicked.connect(self.download_model)
        btn_row.addWidget(self.download_btn)

        self.left_layout.addLayout(btn_row)

        # Right - Controls
        self.right_scroll = QScrollArea()
        self.right_scroll.setWidgetResizable(True)
        self.top_layout.addWidget(self.right_scroll)

        self.right_panel = QWidget()
        self.right_layout = QGridLayout()
        self.right_panel.setLayout(self.right_layout)
        self.right_scroll.setWidget(self.right_panel)

        r = 0

        self.login_button = QPushButton("Login with Google (Online mode)")
        self.login_button.setMinimumHeight(54)
        self.login_button.setStyleSheet("background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #4285f4,stop:1 #357ae8); color:white; border-radius:12px;")
        self.login_button.clicked.connect(self.google_login)
        self.right_layout.addWidget(self.login_button, r, 0, 1, 2)
        r += 1

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Normal (Local)", "Online (Colab + Drive)"])
        self.mode_combo.setMinimumHeight(54)
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        self.right_layout.addWidget(self.mode_combo, r, 0, 1, 2)
        r += 1

        l = QLabel("Language:")
        l.setFont(QFont("Segoe UI", 12))
        self.right_layout.addWidget(l, r, 0)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["english", "japanese → english (translate)"])
        self.lang_combo.setMinimumHeight(54)
        self.right_layout.addWidget(self.lang_combo, r, 1)
        r += 1

        l = QLabel("Words per Line:")
        l.setFont(QFont("Segoe UI", 12))
        self.right_layout.addWidget(l, r, 0)
        self.words_spin = QSpinBox()
        self.words_spin.setRange(1, 16)
        self.words_spin.setValue(5)
        self.words_spin.setMinimumHeight(54)
        self.right_layout.addWidget(self.words_spin, r, 1)
        r += 1

        self.import_btn = QPushButton("Import Video / Audio")
        self.import_btn.setMinimumHeight(84)
        self.import_btn.setStyleSheet("background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #007aff,stop:1 #0051c7); color:white; border-radius:12px; font-size:16px;")
        self.import_btn.clicked.connect(self.import_file)
        self.right_layout.addWidget(self.import_btn, r, 0, 1, 2)
        r += 1

        l = QLabel("Output Format:")
        l.setFont(QFont("Segoe UI", 12))
        self.right_layout.addWidget(l, r, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems([".srt", ".ass"])
        self.format_combo.setMinimumHeight(54)
        self.right_layout.addWidget(self.format_combo, r, 1)
        r += 1

        l = QLabel("Output Folder:")
        l.setFont(QFont("Segoe UI", 12))
        self.right_layout.addWidget(l, r, 0)
        self.out_folder_edit = QLineEdit()
        self.out_folder_edit.setReadOnly(True)
        self.out_folder_edit.setMinimumHeight(54)
        self.right_layout.addWidget(self.out_folder_edit, r, 1)
        r += 1

        browse_btn = QPushButton("Browse")
        browse_btn.setMinimumHeight(64)
        browse_btn.setStyleSheet("background:#3a3a3c; color:white; border-radius:10px;")
        browse_btn.clicked.connect(self.browse_output)
        self.right_layout.addWidget(browse_btn, r, 0, 1, 2)
        r += 1

        self.enhance_btn = QPushButton("Enhance Audio → Vocals Only (Spleeter)")
        self.enhance_btn.setMinimumHeight(84)
        self.enhance_btn.setStyleSheet("background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ffcc00,stop:1 #cc9900); color:white; border-radius:12px; font-size:16px;")
        self.enhance_btn.clicked.connect(self.enhance_audio_only)
        self.right_layout.addWidget(self.enhance_btn, r, 0, 1, 2)
        r += 1

        # Bottom controls
        bottom = QHBoxLayout()
        self.main_layout.addLayout(bottom)

        self.play_btn = QPushButton("Play / Pause")
        self.play_btn.setMinimumHeight(74)
        self.play_btn.setStyleSheet("background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #34c759,stop:1 #2ea44e); color:white; border-radius:12px; font-size:16px;")
        self.play_btn.clicked.connect(self.toggle_play)
        bottom.addWidget(self.play_btn)

        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setStyleSheet("""
            QSlider::groove:horizontal { background:#2a2e34; height:12px; border-radius:6px; }
            QSlider::handle:horizontal { background:#0a84ff; width:28px; border-radius:14px; margin:-8px 0; }
        """)
        self.timeline.sliderMoved.connect(self.seek)
        bottom.addWidget(self.timeline, 1)

        self.gen_btn = QPushButton("Generate Captions")
        self.gen_btn.setMinimumHeight(74)
        self.gen_btn.setStyleSheet("background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff3b30,stop:1 #d32f2f); color:white; border-radius:12px; font-size:16px;")
        self.gen_btn.clicked.connect(self.generate)
        bottom.addWidget(self.gen_btn)

        prog_v = QVBoxLayout()
        bottom.addLayout(prog_v)

        self.prog_main = QProgressBar()
        self.prog_main.setStyleSheet("""
            QProgressBar { background:#22252a; border:1px solid #3a3f44; border-radius:8px; text-align:center; color:white; }
            QProgressBar::chunk { background:#0a84ff; border-radius:8px; }
        """)
        self.prog_main.setMinimumHeight(28)
        prog_v.addWidget(self.prog_main)

        self.prog_frame = QProgressBar()
        self.prog_frame.setFormat("Progress: %v%")
        self.prog_frame.setStyleSheet("""
            QProgressBar { background:#22252a; border:1px solid #3a3f44; border-radius:8px; text-align:center; color:white; }
            QProgressBar::chunk { background:#ff9500; border-radius:8px; }
        """)
        self.prog_frame.setMinimumHeight(28)
        prog_v.addWidget(self.prog_frame)

        footer = QLabel("NotyCaption • All rights reserved by NotY215")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color:#6c757d; font-size:11px; margin:12px 0;")
        self.main_layout.addWidget(footer)

        # State variables
        self.input_file = None
        self.audio_file = None
        self.output_folder = None
        self.subtitles = []
        self.display_lines = []
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.media_status)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.error.connect(self.player_error)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timeline)
        self.timer.start(40)
        self.edit_active = False
        self.duration_ms = 0
        self.generated = False
        self.loaded_media = None
        self.last_temp_wav = None
        self.service = None
        self.mode = "normal"
        self.poll_timer = QTimer(self)
        self.poll_audio_id = None
        self.poll_notebook_id = None
        self.poll_output_name = None
        self.poll_local_out = None
        self.is_generating = False
        self.spleeter_instance = None  # Lazy load Spleeter once

        if os.path.exists("token.json"):
            try:
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                self.service = build("drive", "v3", credentials=creds)
                self.login_button.setVisible(False)
                self.mode_combo.setCurrentText("Online (Colab + Drive)")
                self.mode = "online"
                logger.info("Loaded existing Google token → Online mode activated")
            except Exception as e:
                logger.error(f"Failed to load Google credentials: {e}")

        self.update_download_button_visibility()

        logger.info("Main window UI fully initialized")

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().screenGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def apply_ui_scale(self):
        scale_str = self.settings.get("ui_scale", "100%")
        try:
            scale = float(scale_str.rstrip("%")) / 100.0
        except:
            scale = 1.0
        font = QApplication.font()
        font.setPointSizeF(font.pointSizeF() * scale)
        QApplication.setFont(font)
        self.resize(int(920 * scale), int(780 * scale))
        logger.info(f"UI scale applied: {scale*100}%")

    def apply_theme(self):
        theme = self.settings.get("theme", "Dark")
        if theme == "Light":
            pal = QPalette()
            pal.setColor(QPalette.Window, QColor(245,245,245))
            pal.setColor(QPalette.WindowText, QColor(30,30,30))
            pal.setColor(QPalette.Base, Qt.white)
            pal.setColor(QPalette.Text, QColor(30,30,30))
            pal.setColor(QPalette.Button, QColor(230,230,230))
            pal.setColor(QPalette.ButtonText, QColor(30,30,30))
            pal.setColor(QPalette.Highlight, QColor(0,122,255))
            self.setPalette(pal)
        elif theme == "Windows Default":
            QApplication.setStyle(QStyleFactory.create('windowsvista'))
        else:
            pal = QPalette()
            pal.setColor(QPalette.Window, QColor(28,28,30))
            pal.setColor(QPalette.WindowText, Qt.white)
            pal.setColor(QPalette.Base, QColor(36,36,38))
            pal.setColor(QPalette.Text, Qt.white)
            pal.setColor(QPalette.Button, QColor(44,44,48))
            pal.setColor(QPalette.ButtonText, Qt.white)
            pal.setColor(QPalette.Highlight, QColor(10,132,255))
            self.setPalette(pal)
            QApplication.setStyle(QStyleFactory.create('Fusion'))
        logger.info(f"Theme applied: {theme}")

    def open_settings(self):
        logger.info("Settings dialog opened")
        dlg = SettingsDialog(self.settings, self)
        dlg.settingsChanged.connect(self.update_settings)
        dlg.exec_()

    def update_settings(self, new_settings):
        self.settings = new_settings
        self.apply_ui_scale()
        self.apply_theme()
        self.update_download_button_visibility()
        logger.info("Settings updated")

    def update_download_button_visibility(self):
        if self.mode == "online":
            self.download_btn.setVisible(False)
            logger.info("Download button hidden (Online mode)")
            return

        model_path = os.path.join(self.settings["models_dir"], "large-v3.pt")
        exists = os.path.isfile(model_path)
        self.download_btn.setVisible(not exists)
        logger.info(f"Model exists at {model_path}: {exists} → Download button visible: {not exists}")

    def closeEvent(self, event: QCloseEvent):
        logger.info("Application closing...")
        if self.audio_file and self.audio_file.endswith(".temp.wav") and os.path.exists(self.audio_file):
            try:
                os.remove(self.audio_file)
                logger.info(f"Removed temp audio: {self.audio_file}")
            except Exception as e:
                logger.warning(f"Failed to remove temp audio: {e}")
        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
                logger.info(f"Removed last temp wav: {self.last_temp_wav}")
            except Exception as e:
                logger.warning(f"Failed to remove last temp wav: {e}")

        self.poll_timer.stop()

        if self.service:
            try:
                from online import empty_uploads, delete_temp_notebooks
                empty_uploads(self.service)
                delete_temp_notebooks(self.service)
                logger.info("Cleaned up Google Drive temporary files")
            except Exception as e:
                logger.warning(f"Failed to clean Drive: {e}")

        logger.info("=== NotyCaption closed ===")
        super().closeEvent(event)

    def google_login(self):
        client_path = resource_path("client.json")
        logger.info(f"Google login requested. client.json path: {client_path}")

        if os.path.exists(client_path):
            try:
                flow = InstalledAppFlow.from_client_secrets_file(client_path, SCOPES)
                creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
                self.service = build("drive", "v3", credentials=creds)
                self.login_button.setVisible(False)
                self.mode_combo.setCurrentText("Online (Colab + Drive)")
                self.mode = "online"
                self.update_download_button_visibility()
                logger.info("Google Drive authentication successful")
                QMessageBox.information(self, "Success", "Google Drive connected.")
            except Exception as e:
                logger.error(f"Google login failed: {traceback.format_exc()}")
                QMessageBox.critical(self, "Login Failed", str(e))
        else:
            logger.warning("client.json not found")
            QMessageBox.warning(self, "Missing client.json",
                                f"client.json not found.\n\nExpected location: {client_path}")

    def on_mode_changed(self, text):
        self.mode = "online" if "Online" in text else "normal"
        self.update_download_button_visibility()
        logger.info(f"Mode changed to: {self.mode}")

    def load_whisper_model(self):
        try:
            logger.info(f"Loading Whisper large-v3 model from: {self.settings['models_dir']}")
            model = whisper.load_model("large-v3", download_root=self.settings["models_dir"])
            logger.info("Whisper model loaded successfully")
            return model
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {traceback.format_exc()}")
            raise

    def get_spleeter(self):
        if self.spleeter_instance is None:
            try:
                logger.info("Initializing Spleeter separator (lazy load)...")
                self.spleeter_instance = Separator('spleeter:2stems')
                logger.info("Spleeter initialized successfully")
            except Exception as e:
                logger.error(f"Spleeter initialization failed: {traceback.format_exc()}")
                raise
        return self.spleeter_instance

    def media_status(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.play_btn.setEnabled(True)
        elif status in (QMediaPlayer.NoMedia, QMediaPlayer.InvalidMedia):
            self.play_btn.setEnabled(False)

    def position_changed(self, pos):
        self.update_highlight(pos)

    def duration_changed(self, dur):
        self.duration_ms = dur
        self.timeline.setRange(0, dur)

    def player_error(self):
        err = self.player.errorString() or "Unknown playback error"
        logger.warning(f"Media player error: {err}")
        QMessageBox.warning(self, "Player Error", err)

    def update_timeline(self):
        if self.duration_ms > 0:
            self.timeline.setValue(self.player.position())

    def toggle_play(self):
        if not self.audio_file or not os.path.exists(self.audio_file):
            logger.warning("Play requested but no audio loaded")
            QMessageBox.warning(self, "No Audio", "Import media first.")
            return

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText("Play")
            logger.info("Audio paused")
        else:
            try:
                if self.loaded_media != self.audio_file:
                    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
                    self.loaded_media = self.audio_file
                    logger.info(f"Loaded media for playback: {self.audio_file}")
                self.player.play()
                self.play_btn.setText("Pause")
                logger.info("Audio playing")
            except Exception as e:
                logger.error(f"Playback failed: {e}")
                QMessageBox.warning(self, "Playback Error", str(e))

    def seek(self, pos):
        self.player.setPosition(pos)

    def update_highlight(self, ms):
        if not self.subtitles or not self.generated:
            return
        sec = ms / 1000.0
        doc = self.caption_edit.document()
        cursor = QTextCursor(doc)
        cursor.beginEditBlock()
        clear_fmt = cursor.charFormat()
        clear_fmt.setBackground(QColor(30,30,34))
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(clear_fmt)
        cursor.clearSelection()
        for i, sub in enumerate(self.subtitles):
            if sub["start"].total_seconds() <= sec < sub["end"].total_seconds():
                cursor = QTextCursor(doc)
                cursor.movePosition(QTextCursor.Start)
                cursor.movePosition(QTextCursor.NextBlock, QTextCursor.MoveAnchor, i)
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                fmt = cursor.charFormat()
                fmt.setBackground(QColor(255, 215, 0, 180))
                cursor.setCharFormat(fmt)
                self.caption_edit.setTextCursor(cursor)
                self.caption_edit.ensureCursorVisible()
                break
        cursor.endEditBlock()

    def import_file(self):
        logger.info("Import file dialog opened")
        filter_str = (
            "Media Files (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv "
            "*.mp3 *.wav *.m4a *.aac *.flac *.ogg *.wma *.amr *.opus)"
        )
        path, _ = QFileDialog.getOpenFileName(self, "Select Video or Audio", "", filter_str)
        if not path:
            logger.info("Import cancelled by user")
            return

        logger.info(f"Selected file: {path}")
        self.input_file = path
        self.output_folder = os.path.dirname(path)
        self.out_folder_edit.setText(self.output_folder)

        temp_dir = self.settings.get("temp_dir", QDir.tempPath())
        temp_name = os.path.basename(path) + ".temp.wav"
        new_temp = os.path.join(temp_dir, temp_name)

        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
                logger.info(f"Removed previous temp file: {self.last_temp_wav}")
            except Exception as e:
                logger.warning(f"Could not remove previous temp: {e}")

        success = False
        if path.lower().endswith(('.mp4','.mkv','.avi','.mov','.webm','.flv','.wmv')):
            try:
                logger.info("Extracting audio from video...")
                clip = VideoFileClip(path)
                if clip.audio:
                    clip.audio.write_audiofile(new_temp, codec='pcm_s16le', logger=None)
                    self.audio_file = new_temp
                    success = True
                clip.close()
            except Exception as e:
                logger.error(f"Video audio extraction failed: {traceback.format_exc()}")

        if not success:
            try:
                logger.info("Converting audio file...")
                audio_clip = AudioFileClip(path)
                audio_clip.write_audiofile(new_temp, codec='pcm_s16le', logger=None)
                self.audio_file = new_temp
                audio_clip.close()
                success = True
            except Exception as e:
                logger.warning(f"Audio conversion failed: {e}")
                self.audio_file = path
                QMessageBox.warning(self, "Conversion Warning", "Could not convert to WAV. Using original file.")

        self.last_temp_wav = new_temp if success else None
        logger.info(f"Audio ready: {self.audio_file}")
        QMessageBox.information(self, "Success", "Media imported successfully.")
        self.loaded_media = None

    def browse_output(self):
        logger.info("Output folder browse dialog opened")
        d = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if d:
            self.output_folder = d
            self.out_folder_edit.setText(d)
            logger.info(f"Output folder set to: {d}")

    def enhance_audio_only(self):
        if not self.audio_file or not os.path.exists(self.audio_file):
            logger.warning("Enhance requested but no audio loaded")
            QMessageBox.warning(self, "Error", "No audio loaded.")
            return

        logger.info("Starting audio enhancement (Spleeter)...")
        temp_dir = self.settings.get("temp_dir", QDir.tempPath())
        spleeter_models_dir = os.path.join(os.path.dirname(__file__), "pretrained_models", "2stems")

        if not os.path.exists(spleeter_models_dir):
            logger.warning("Spleeter pretrained models not found")
            QMessageBox.warning(self, "Spleeter Models Missing", "Spleeter pretrained models not found.")
            return

        try:
            self.prog_main.setValue(10)
            separator = self.get_spleeter()
            separator.separate_to_file(self.audio_file, temp_dir, synchronous=True)
            self.prog_main.setValue(60)

            base_name = os.path.splitext(os.path.basename(self.audio_file))[0]
            vocals_path = os.path.join(temp_dir, base_name, 'vocals.wav')

            if not os.path.exists(vocals_path):
                raise FileNotFoundError("vocals.wav not found after separation")

            base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
            final_name = f"{base}_vocals_only.wav"
            final_path = os.path.join(self.output_folder, final_name)

            shutil.move(vocals_path, final_path)
            self.prog_main.setValue(100)
            logger.info(f"Vocals-only file created: {final_path}")
            QMessageBox.information(self, "Audio Enhanced", f"Vocals-only file created:\n{final_path}")

        except Exception as e:
            self.prog_main.setValue(0)
            logger.error(f"Audio enhancement failed: {traceback.format_exc()}")
            QMessageBox.warning(self, "Enhance Failed", f"Audio enhancement failed:\n{str(e)}")

        finally:
            try:
                spleeter_out = os.path.join(temp_dir, base_name)
                if os.path.exists(spleeter_out):
                    shutil.rmtree(spleeter_out, ignore_errors=True)
                    logger.info("Cleaned spleeter temporary output")
            except Exception as e:
                logger.warning(f"Failed to clean spleeter temp: {e}")

    def download_model(self):
        logger.info("Download model dialog opened")
        dlg = QDialog(self)
        dlg.setWindowTitle("Download Model Options")
        lay = QVBoxLayout()
        rb_already = QRadioButton("Already exist (select model file)")
        rb_custom = QRadioButton("Custom location (select folder to download)")
        rb_default = QRadioButton("Default (app root folder)")
        rb_default.setChecked(True)
        lay.addWidget(rb_already)
        lay.addWidget(rb_custom)
        lay.addWidget(rb_default)
        btns = QHBoxLayout()
        ok = QPushButton("OK")
        ok.clicked.connect(dlg.accept)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(dlg.reject)
        btns.addWidget(ok)
        btns.addWidget(cancel)
        lay.addLayout(btns)
        dlg.setLayout(lay)
        if dlg.exec_() != QDialog.Accepted:
            logger.info("Model download cancelled")
            return

        if rb_already.isChecked():
            file, _ = QFileDialog.getOpenFileName(self, "Select large-v3.pt", "", "PyTorch Model (*.pt)")
            if not file:
                logger.info("Model linking cancelled")
                return
            if os.path.basename(file) != "large-v3.pt":
                logger.warning("User selected wrong file for linking")
                QMessageBox.warning(self, "Invalid File", "Please select the file named large-v3.pt")
                return
            new_dir = os.path.dirname(file)
            self.settings["models_dir"] = new_dir
            save_settings(self.settings)
            self.update_download_button_visibility()
            logger.info(f"Model linked from: {new_dir}")
            QMessageBox.information(self, "Success", "Model location linked successfully.")
            return

        # Download case
        if rb_custom.isChecked():
            path = QFileDialog.getExistingDirectory(self, "Select Folder to Download Model")
            if not path:
                logger.info("Custom download path selection cancelled")
                return
        else:
            path = self.settings["models_dir"]

        self.settings["models_dir"] = path
        save_settings(self.settings)
        self.update_download_button_visibility()
        logger.info(f"Model will be downloaded to: {path}")

        cmd = [
            'cmd', '/c',
            'python', '-c',
            f"import whisper; whisper.load_model('large-v3', download_root=r'{path}')",
            '&&', 'echo.', '&&', 'echo Download finished successfully.', '&&', 'pause'
        ]
        logger.info("Starting model download in new console...")
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def generate(self):
        if self.is_generating:
            logger.warning("Generate button clicked while already generating")
            QMessageBox.warning(self, "Busy", "Generation is already in progress. Please wait.")
            return

        self.is_generating = True
        self.gen_btn.setEnabled(False)
        logger.info("=== Caption generation started ===")

        if not self.audio_file or not os.path.exists(self.audio_file):
            logger.error("No audio file loaded for generation")
            QMessageBox.warning(self, "Error", "No audio loaded.")
            self.is_generating = False
            self.gen_btn.setEnabled(True)
            return

        temp_dir = self.settings.get("temp_dir", QDir.tempPath())
        enhanced_audio = os.path.join(temp_dir, "enhanced_vocals.wav")
        use_enhanced = False

        try:
            logger.info("Attempting vocal separation with Spleeter...")
            self.prog_main.setValue(5)
            separator = self.get_spleeter()
            separator.separate_to_file(self.audio_file, temp_dir, synchronous=True)
            self.prog_main.setValue(40)

            base_name = os.path.splitext(os.path.basename(self.audio_file))[0]
            vocals_path = os.path.join(temp_dir, base_name, 'vocals.wav')
            if os.path.exists(vocals_path):
                shutil.move(vocals_path, enhanced_audio)
                use_enhanced = True
                self.prog_main.setValue(60)
                logger.info("Using enhanced vocals for transcription")
            else:
                logger.warning("Spleeter did not produce vocals.wav → using original")
        except Exception as e:
            logger.warning(f"Spleeter failed or skipped: {e} → falling back to original audio")
            enhanced_audio = self.audio_file
            self.prog_main.setValue(40)

        lang = self.lang_combo.currentText()
        lang_code = "ja" if "japanese" in lang.lower() else "en"
        task = "translate" if "translate" in lang.lower() else "transcribe"

        wpl = self.words_spin.value()
        fmt = self.format_combo.currentText()
        base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
        out_path = os.path.join(self.output_folder, f"{base}_captions{fmt}")

        logger.info(f"Generation parameters → lang:{lang_code}, task:{task}, wpl:{wpl}, format:{fmt}, output:{out_path}")

        if os.path.exists(out_path):
            reply = QMessageBox.question(self, "Overwrite?", f"{out_path} already exists.\nOverwrite?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                logger.info("User chose not to overwrite existing captions file")
                self.is_generating = False
                self.gen_btn.setEnabled(True)
                return

        self.prog_main.setValue(65)
        self.prog_frame.setValue(0)

        if self.mode == "online":
            logger.info("Starting ONLINE (Colab) generation mode")
            try:
                self.poll_timer.stop()
                try:
                    self.poll_timer.timeout.disconnect()
                except TypeError:
                    pass

                from online import handle_online
                success = handle_online(self, enhanced_audio if use_enhanced else self.audio_file,
                                        lang_code, task, wpl, fmt, base, out_path)
                if not success:
                    logger.warning("Online generation did not complete successfully")
            except Exception as e:
                logger.error(f"Online mode failed: {traceback.format_exc()}")
                QMessageBox.critical(self, "Online Mode Failed", str(e))
            finally:
                self.is_generating = False
                self.gen_btn.setEnabled(True)
        else:
            logger.info("Starting LOCAL Whisper generation")
            try:
                self.prog_main.setValue(70)
                model = self.load_whisper_model()
                self.prog_main.setValue(75)

                logger.info("Starting transcription...")
                result = model.transcribe(
                    enhanced_audio if use_enhanced else self.audio_file,
                    language=lang_code,
                    task=task,
                    word_timestamps=True
                )
                self.prog_main.setValue(90)
                logger.info("Transcription finished")

                self.subtitles = []
                self.display_lines = []
                idx = 1

                for seg in result.get("segments", []):
                    txt = seg.get("text", "").strip()
                    if not txt: continue

                    s = seg.get("start", 0)
                    e = seg.get("end", s + 1)

                    words = seg.get("words", [])
                    if words:
                        w_txt = [w["word"].strip() for w in words]
                        w_s = [w.get("start", s) for w in words]
                        w_e = [w.get("end", e) for w in words]
                    else:
                        w_txt = txt.split()
                        dur = e - s
                        w_s = [s + i * dur / max(1, len(w_txt)) for i in range(len(w_txt))]
                        w_e = w_s[1:] + [e]

                    for i in range(0, len(w_txt), wpl):
                        chunk = w_txt[i:i + wpl]
                        line = " ".join(chunk).strip()
                        if not line: continue
                        st = w_s[i]
                        en = w_e[min(i + wpl - 1, len(w_e) - 1)]

                        self.subtitles.append({
                            "index": idx,
                            "start": timedelta(seconds=st),
                            "end": timedelta(seconds=en),
                            "text": line
                        })
                        self.display_lines.append(line)
                        idx += 1

                self.prog_main.setValue(95)

                preview = "\n".join(self.display_lines)
                self.caption_edit.setText(preview.strip())

                logger.info(f"Saving captions to {out_path}")
                if fmt == ".srt":
                    srt = pysrt.SubRipFile()
                    for s in self.subtitles:
                        item = pysrt.SubRipItem(
                            index=s["index"],
                            start=pysrt.SubRipTime.from_ordinal(s["start"].total_seconds()*1000),
                            end=pysrt.SubRipTime.from_ordinal(s["end"].total_seconds()*1000),
                            text=s["text"]
                        )
                        srt.append(item)
                    srt.save(out_path, encoding='utf-8')
                else:
                    ass = pysubs2.SSAFile()
                    for s in self.subtitles:
                        ev = pysubs2.SSAEvent(
                            start=int(s["start"].total_seconds()*1000),
                            end=int(s["end"].total_seconds()*1000),
                            text=s["text"]
                        )
                        ass.events.append(ev)
                    ass.save(out_path)

                self.prog_main.setValue(100)
                logger.info(f"Captions successfully saved: {out_path}")
                QMessageBox.information(self, "Success", f"Captions saved:\n{out_path}")

                self.generated = True
                self.edit_btn.setEnabled(True)

            except Exception as e:
                logger.error(f"Local generation failed: {traceback.format_exc()}")
                QMessageBox.critical(self, "Generation Failed", f"Error:\n{str(e)}")

            finally:
                self.is_generating = False
                self.gen_btn.setEnabled(True)

        try:
            if use_enhanced and os.path.exists(enhanced_audio):
                os.remove(enhanced_audio)
                logger.info("Removed temporary enhanced audio")
            spleeter_out = os.path.join(temp_dir, base_name)
            if os.path.exists(spleeter_out):
                shutil.rmtree(spleeter_out, ignore_errors=True)
                logger.info("Cleaned spleeter output folder")
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")

        logger.info("=== Caption generation finished ===")

    def load_downloaded_subtitles(self, file_path):
        logger.info(f"Loading downloaded subtitles: {file_path}")
        try:
            self.subtitles = []
            self.display_lines = []
            if file_path.endswith('.srt'):
                subs = pysrt.open(file_path)
                for sub in subs:
                    self.subtitles.append({
                        "index": sub.index,
                        "start": timedelta(milliseconds=sub.start.ordinal),
                        "end": timedelta(milliseconds=sub.end.ordinal),
                        "text": sub.text
                    })
                    self.display_lines.append(sub.text)
            elif file_path.endswith('.ass'):
                ass = pysubs2.load(file_path)
                for i, event in enumerate(ass.events):
                    self.subtitles.append({
                        "index": i+1,
                        "start": timedelta(milliseconds=event.start),
                        "end": timedelta(milliseconds=event.end),
                        "text": event.text
                    })
                    self.display_lines.append(event.text)
            preview = "\n".join(self.display_lines)
            self.caption_edit.setText(preview.strip())
            self.generated = True
            self.edit_btn.setEnabled(True)
            logger.info("Downloaded subtitles loaded and displayed")
        except Exception as e:
            logger.error(f"Failed to load downloaded subtitles: {traceback.format_exc()}")
            QMessageBox.warning(self, "Load Failed", f"Could not load subtitles for preview:\n{str(e)}")

    def toggle_edit(self):
        if not self.generated:
            return
        self.edit_active = not self.edit_active
        self.caption_edit.setReadOnly(not self.edit_active)
        self.edit_btn.setText("Save Edits" if self.edit_active else "Edit Captions")
        if not self.edit_active:
            self.apply_edit_changes()
        logger.info(f"Edit mode toggled: {'ON' if self.edit_active else 'OFF'}")

    def apply_edit_changes(self):
        logger.info("Applying manual caption edits")
        text = self.caption_edit.toPlainText().strip()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if len(lines) != len(self.subtitles):
            logger.warning("Line count mismatch after edit → changes discarded")
            QMessageBox.warning(self, "Edit Mismatch", "Line count changed. Edits not applied.")
            return
        for i, new_text in enumerate(lines):
            self.subtitles[i]["text"] = new_text
        logger.info("Manual edits applied successfully")
        QMessageBox.information(self, "Edits Saved", "Changes applied.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    instance = SingleInstance()
    if instance.is_already_running():
        logger.warning("Another instance of NotyCaption is already running")
        QMessageBox.warning(None, "Already Running", "NotyCaption is already open.")
        sys.exit(0)

    icon_path = resource_path('App.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    app.setStyle('Fusion')
    logger.info("Launching main window...")
    win = NotyCaptionWindow()
    win.show()
    logger.info("Application main loop started")
    sys.exit(app.exec_())