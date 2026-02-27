# NotyCaption.py
# App name: NotyCaption
# Developer: NotY215
# All rights reserved by NotY215

import sys
import os
import json
import shutil
from datetime import timedelta
import whisper
import psutil
import torch
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QTextEdit, QFileDialog,
    QMessageBox, QLineEdit, QScrollArea, QSlider, QProgressBar, QDialog, QFormLayout,
    QSizePolicy, QStyleFactory, QDesktopWidget, QGroupBox, QRadioButton,
    QCheckBox, QFrame
)
from PyQt5.QtGui import QIcon, QColor, QTextCursor, QFont, QPalette
from PyQt5.QtCore import QTimer, Qt, QUrl, QDir, pyqtSignal, QRect
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from moviepy.editor import VideoFileClip, AudioFileClip
import pysrt
import pysubs2
from spleeter.separator import Separator
import importlib.resources
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import online  # Import the online mode handler

SCOPES = ['https://www.googleapis.com/auth/drive']

# Force Whisper to find assets in bundled mode
if getattr(sys, 'frozen', False):
    whisper_assets_path = os.path.join(sys._MEIPASS, 'whisper', 'assets')
    if os.path.exists(whisper_assets_path):
        os.environ["WHISPER_ASSETS"] = whisper_assets_path

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
    except:
        save_settings(defaults)
        return defaults

# ──────────────────────────────────────────────
# SETTINGS DIALOG (unchanged)
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
        self.rb_dark = QRadioButton("Dark (Topaz)")
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

        tmp_gb = QGroupBox("Temp Files Folder")
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
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'App.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.settings = load_settings()
        self.apply_ui_scale()
        self.apply_theme()

        self.resize(840, 760)
        self.center()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        # Left - Editor
        self.left_panel = QWidget()
        self.left_panel.setMaximumWidth(580)
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        self.top_layout.addWidget(self.left_panel)

        title = QLabel("Caption Editor")
        title.setFont(QFont("Segoe UI", 17, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(title)

        self.caption_edit = QTextEdit()
        self.caption_edit.setReadOnly(True)
        self.caption_edit.setFont(QFont("Consolas", 13))
        self.caption_edit.setStyleSheet("background:#1e2225; color:#e0f0ff; border:1px solid #3f4a52;")
        self.left_layout.addWidget(self.caption_edit, 1)

        btn_row = QHBoxLayout()
        self.edit_btn = QPushButton("Edit Captions")
        self.edit_btn.setMinimumHeight(62)
        self.edit_btn.setStyleSheet("background:#0a84ff; color:white; border-radius:10px; font-weight:bold;")
        self.edit_btn.clicked.connect(self.toggle_edit)
        self.edit_btn.setEnabled(False)
        btn_row.addWidget(self.edit_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.setMinimumHeight(62)
        settings_btn.setStyleSheet("background:#5e5ce6; color:white; border-radius:10px; font-weight:bold;")
        settings_btn.clicked.connect(self.open_settings)
        btn_row.addWidget(settings_btn)

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

        # Login button
        self.login_button = QPushButton("Login with Google")
        self.login_button.setMinimumHeight(54)
        self.login_button.setStyleSheet("background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #4285f4,stop:1 #357ae8); color:white; border-radius:12px; font-size:16px;")
        self.login_button.clicked.connect(self.google_login)
        self.right_layout.addWidget(self.login_button, r, 0, 1, 2)
        r += 1

        # Mode combo
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Normal", "Online"])
        self.mode_combo.setMinimumHeight(54)
        self.mode_combo.currentTextChanged.connect(self.set_mode)
        self.mode_combo.setVisible(False)
        self.right_layout.addWidget(self.mode_combo, r, 0, 1, 2)
        r += 1

        l = QLabel("Language:")
        l.setFont(QFont("Segoe UI", 12))
        self.right_layout.addWidget(l, r, 0)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["english", "japlish"])
        self.lang_combo.setMinimumHeight(54)
        self.right_layout.addWidget(self.lang_combo, r, 1)
        r += 1

        l = QLabel("Words per Line:")
        l.setFont(QFont("Segoe UI", 12))
        self.right_layout.addWidget(l, r, 0)
        self.words_spin = QSpinBox()
        self.words_spin.setRange(1, 14)
        self.words_spin.setValue(5)
        self.words_spin.setMinimumHeight(54)
        self.right_layout.addWidget(self.words_spin, r, 1)
        r += 1

        self.import_btn = QPushButton("Import Video / Audio")
        self.import_btn.setMinimumHeight(80)
        self.import_btn.setStyleSheet("background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #007aff,stop:1 #0051c7); color:white; border-radius:12px; font-size:16px;")
        self.import_btn.clicked.connect(self.import_file)
        self.right_layout.addWidget(self.import_btn, r, 0, 1, 2)
        r += 1

        l = QLabel("Format:")
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
        browse_btn.setMinimumHeight(60)
        browse_btn.setStyleSheet("background:#3a3a3c; color:white; border-radius:10px;")
        browse_btn.clicked.connect(self.browse_output)
        self.right_layout.addWidget(browse_btn, r, 0, 1, 2)
        r += 1

        self.enhance_btn = QPushButton("Enhance Audio → Vocals Only")
        self.enhance_btn.setMinimumHeight(80)
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

        # Progress bars
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
        self.prog_frame.setFormat("Frames: %v")
        self.prog_frame.setStyleSheet("""
            QProgressBar { background:#22252a; border:1px solid #3a3f44; border-radius:8px; text-align:center; color:white; }
            QProgressBar::chunk { background:#ff9500; border-radius:8px; }
        """)
        self.prog_frame.setMinimumHeight(28)
        prog_v.addWidget(self.prog_frame)

        footer = QLabel("All rights reserved by NotY215")
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

        # Load token if exists
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            self.service = build("drive", "v3", credentials=creds)
            self.login_button.setVisible(False)
            self.mode_combo.setVisible(True)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
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
        self.resize(int(840 * scale), int(760 * scale))

    def apply_theme(self):
        theme = self.settings.get("theme", "Dark")
        if theme == "Light":
            pal = QPalette()
            pal.setColor(QPalette.Window, QColor(250,250,250))
            pal.setColor(QPalette.WindowText, QColor(30,30,30))
            pal.setColor(QPalette.Base, Qt.white)
            pal.setColor(QPalette.Text, QColor(30,30,30))
            pal.setColor(QPalette.Button, QColor(240,240,240))
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

    def open_settings(self):
        dlg = SettingsDialog(self.settings, self)
        dlg.settingsChanged.connect(self.update_settings)
        dlg.exec_()

    def update_settings(self, new_settings):
        self.settings = new_settings
        self.apply_ui_scale()
        self.apply_theme()

    def closeEvent(self, event: QCloseEvent):
        if self.audio_file and self.audio_file.endswith(".temp.wav") and os.path.exists(self.audio_file):
            try:
                os.remove(self.audio_file)
            except:
                pass
        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
            except:
                pass
        super().closeEvent(event)

    def google_login(self):
        if os.path.exists("client.json"):
            flow = InstalledAppFlow.from_client_secrets_file("client.json", SCOPES)
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            self.service = build("drive", "v3", credentials=creds)
            self.login_button.setVisible(False)
            self.mode_combo.setVisible(True)

        else:
            QMessageBox.warning(self, "Error", "client.json not found.")

    def set_mode(self, text):
        self.mode = "online" if "Online" in text else "normal"

    def load_whisper_model(self):
        model_name = "large-v3"
        model_filename = f"{model_name}.pt"
        user_dir = self.settings.get("models_dir", CURRENT_DIR)
        user_model_file = os.path.join(user_dir, model_filename)

        if os.path.exists(user_model_file):
            return whisper.load_model(user_model_file)

        default_cache_dir = os.path.expanduser("~/.cache/whisper")
        default_model_file = os.path.join(default_cache_dir, model_filename)
        if os.path.exists(default_model_file):
            os.makedirs(user_dir, exist_ok=True)
            shutil.copy2(default_model_file, user_model_file)
            return whisper.load_model(user_model_file)

        os.makedirs(user_dir, exist_ok=True)
        return whisper.load_model(model_name, download_root=user_dir)

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
        QMessageBox.warning(self, "Player Error", self.player.errorString() or "Unknown playback error")

    def update_timeline(self):
        if self.duration_ms > 0:
            self.timeline.setValue(self.player.position())

    def toggle_play(self):
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "No Audio", "Import media first.")
            return

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText("Play")
        else:
            try:
                if self.loaded_media != self.audio_file:
                    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
                    self.loaded_media = self.audio_file
                self.player.play()
                self.play_btn.setText("Pause")
            except Exception as e:
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
                cursor.movePosition(QTextCursor.NextBlock, n=i)
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                fmt = cursor.charFormat()
                fmt.setBackground(QColor(255, 215, 0, 160))
                cursor.setCharFormat(fmt)
                self.caption_edit.setTextCursor(cursor)
                self.caption_edit.ensureCursorVisible()
                break

        cursor.endEditBlock()

    def import_file(self):
        filter_str = (
            "All Supported Media (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv "
            "*.mp3 *.wav *.m4a *.aac *.flac *.ogg *.wma *.amr *.opus);;"
            "Video Files (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv);;"
            "Audio Files (*.mp3 *.wav *.m4a *.aac *.flac *.ogg *.wma *.amr *.opus)"
        )

        path, _ = QFileDialog.getOpenFileName(self, "Select Video or Audio", "", filter_str)
        if not path:
            return

        self.input_file = path
        self.output_folder = os.path.dirname(path)
        self.out_folder_edit.setText(self.output_folder)

        temp_dir = self.settings.get("temp_dir", QDir.tempPath())
        temp_name = os.path.basename(path) + ".temp.wav"
        new_temp = os.path.join(temp_dir, temp_name)

        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
            except:
                pass

        success = False
        if path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv')):
            try:
                clip = VideoFileClip(path)
                if clip.audio is not None:
                    clip.audio.write_audiofile(new_temp, codec='pcm_s16le', logger=None)
                    self.audio_file = new_temp
                    success = True
                clip.close()
            except Exception as e:
                pass

        if not success:
            try:
                audio_clip = AudioFileClip(path)
                audio_clip.write_audiofile(new_temp, codec='pcm_s16le', logger=None)
                self.audio_file = new_temp
                audio_clip.close()
                success = True
            except Exception as e:
                self.audio_file = path
                QMessageBox.warning(self, "Conversion Warning",
                                    "Could not convert to WAV.\nUsing original file.")

        self.last_temp_wav = new_temp if success else None

        QMessageBox.information(self, "Success", "Media imported successfully.")
        self.loaded_media = None

    def browse_output(self):
        d = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if d:
            self.output_folder = d
            self.out_folder_edit.setText(d)

    def enhance_audio_only(self):
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "Error", "No audio loaded.")
            return

        temp_dir = self.settings.get("temp_dir", QDir.tempPath())
        output_dir = temp_dir

        spleeter_models_dir = os.path.join(os.path.dirname(__file__), "pretrained_models", "2stems")
        if not os.path.exists(spleeter_models_dir):
            QMessageBox.warning(self, "Spleeter Models Missing",
                                "Spleeter pretrained models not found.\nCannot enhance audio. Install them manually.")
            return

        try:
            separator = Separator('spleeter:2stems')
            separator.separate_to_file(self.audio_file, temp_dir)
            vocals_path = os.path.join(temp_dir, os.path.basename(self.audio_file).replace('.wav', ''), 'vocals.wav')

            if os.path.exists(vocals_path):
                base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
                out_path = os.path.join(self.output_folder, f"{base}_enhanced_vocals.wav")
                shutil.move(vocals_path, out_path)
                QMessageBox.information(self, "Success", f"Enhanced vocals saved to {out_path}")
            else:
                raise FileNotFoundError("vocals.wav not found")
        except Exception as e:
            QMessageBox.warning(self, "Enhance Failed",
                                f"Audio enhancement failed:\n{str(e)}\n"
                                "Using original audio for captioning.")

        # Cleanup
        try:
            acc_path = os.path.join(temp_dir, os.path.basename(self.audio_file).replace('.wav', ''), 'accompaniment.wav')
            if os.path.exists(acc_path):
                os.remove(acc_path)
            spleeter_out = os.path.join(temp_dir, os.path.basename(self.audio_file).replace('.wav', ''))
            if os.path.exists(spleeter_out):
                shutil.rmtree(spleeter_out, ignore_errors=True)
        except:
            pass

    def generate(self):
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "Error", "No audio loaded.")
            return

        temp_dir = self.settings.get("temp_dir", QDir.tempPath())
        enhanced_audio = os.path.join(temp_dir, "enhanced_vocals.wav")
        use_enhanced = False

        spleeter_models_dir = os.path.join(os.path.dirname(__file__), "pretrained_models", "2stems")
        if os.path.exists(spleeter_models_dir):
            try:
                separator = Separator('spleeter:2stems')
                separator.separate_to_file(self.audio_file, temp_dir)
                vocals_path = os.path.join(temp_dir, os.path.basename(self.audio_file).replace('.wav', ''), 'vocals.wav')
                if os.path.exists(vocals_path):
                    shutil.move(vocals_path, enhanced_audio)
                    use_enhanced = True
                else:
                    enhanced_audio = self.audio_file
            except Exception as e:
                enhanced_audio = self.audio_file
                QMessageBox.information(self, "Spleeter Info",
                                        "Could not separate vocals (missing config or error).\n"
                                        "Using original audio for transcription.")
        else:
            enhanced_audio = self.audio_file
            QMessageBox.information(self, "Spleeter Info",
                                    "Spleeter pretrained models not found.\n"
                                    "Using original audio for transcription.")

        lang = self.lang_combo.currentText()
        lang_code = "ja" if lang == "japlish" else "en"
        task = "translate" if lang == "japlish" else "transcribe"

        wpl = self.words_spin.value()

        self.prog_main.setValue(0)
        self.prog_frame.setValue(0)
        self.prog_frame.setMaximum(100)

        fmt = self.format_combo.currentText()
        base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
        out_path = os.path.join(self.output_folder, f"{base}_captions{fmt}")

        if self.mode == "online":
            online.handle_online(self, enhanced_audio if use_enhanced else self.audio_file, lang_code, task, wpl, fmt, base, out_path)
        else:
            # Local mode
            try:
                model = self.load_whisper_model()
                self.prog_main.setValue(15)

                result = model.transcribe(enhanced_audio if use_enhanced else self.audio_file, language=lang_code, task=task, verbose=True, word_timestamps=True)
                self.prog_main.setValue(70)
                self.prog_frame.setValue(100)
                self.prog_frame.setFormat("Frames done")

                self.subtitles = []
                self.display_lines = []
                idx = 1
                for seg in result["segments"]:
                    text = seg["text"].strip()
                    words = text.split()
                    start = seg["start"]
                    end = seg["end"]
                    duration = end - start

                    for i in range(0, len(words), wpl):
                        line_words = words[i:i + wpl]
                        line_text = " ".join(line_words)
                        line_start = start + (i / len(words)) * duration
                        line_end = start + ((i + len(line_words)) / len(words)) * duration

                        self.subtitles.append({
                            "index": idx,
                            "start": timedelta(seconds=line_start),
                            "end": timedelta(seconds=line_end),
                            "text": line_text
                        })
                        self.display_lines.append(line_text)
                        idx += 1

                self.prog_main.setValue(92)

                preview_text = "\n".join(self.display_lines)
                self.caption_edit.setText(preview_text)

                if fmt == ".srt":
                    srt_subs = pysrt.SubRipFile()
                    for sub in self.subtitles:
                        item = pysrt.SubRipItem(
                            index=sub["index"],
                            start=sub["start"],
                            end=sub["end"],
                            text=sub["text"]
                        )
                        srt_subs.append(item)
                    srt_subs.save(out_path, encoding="utf-8")
                elif fmt == ".ass":
                    ass_subs = pysubs2.SSAFile()
                    for sub in self.subtitles:
                        event = pysubs2.SSAEvent(
                            start=pysubs2.make_time(s=sub["start"].total_seconds()),
                            end=pysubs2.make_time(s=sub["end"].total_seconds()),
                            text=sub["text"]
                        )
                        ass_subs.events.append(event)
                    ass_subs.save(out_path)

                self.prog_main.setValue(100)
                QMessageBox.information(self, "Success", f"Captions generated and saved to {out_path}.")

                self.generated = True
                self.edit_btn.setEnabled(True)

            except Exception as e:
                self.prog_frame.setFormat("Error")
                QMessageBox.critical(self, "Generation Failed", f"Failed to generate captions:\n{str(e)}")

        # Cleanup
        try:
            if use_enhanced and os.path.exists(enhanced_audio):
                os.remove(enhanced_audio)
            spleeter_out = os.path.join(temp_dir, os.path.basename(self.audio_file).replace('.wav', ''))
            if os.path.exists(spleeter_out):
                shutil.rmtree(spleeter_out, ignore_errors=True)
        except:
            pass

    def toggle_edit(self):
        if not self.generated:
            return
        self.edit_active = not self.edit_active
        self.caption_edit.setReadOnly(not self.edit_active)
        self.edit_btn.setText("Save Edits" if self.edit_active else "Edit Captions")
        if not self.edit_active:
            self.apply_edit_changes()

    def apply_edit_changes(self):
        text = self.caption_edit.toPlainText().strip()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if len(lines) != len(self.subtitles):
            QMessageBox.warning(self, "Error", "Invalid number of lines. Edits not saved.")
            return
        for i, new_text in enumerate(lines):
            self.subtitles[i]["text"] = new_text
        QMessageBox.information(self, "Success", "Edits saved.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('App.ico'))
    window = NotyCaptionWindow()
    window.show()
    sys.exit(app.exec_())