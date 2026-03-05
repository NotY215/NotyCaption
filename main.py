# NotyCaption.py
# App name: NotyCaption
# Developer: NotY215
# All rights reserved by NotY215
# Version: 2.0 - Secure EXE Mode with Inline Resources (2026)
# This application is a advanced caption generator using Whisper AI, with local and online modes.
# Features: Audio/Video import, Spleeter enhancement, Google Colab integration, Subtitle export (SRT/ASS),
#           Real-time playback with sync highlighting, Editable captions, Settings persistence with encryption.
# Dependencies: PyQt5, whisper, moviepy, pysrt, pysubs2, google-api-python-client, cryptography, spleeter.
# Build Notes: Use build.bat to create encrypted resources and EXE bundle.

import sys
import os
import json
import shutil
import subprocess
import logging
import traceback
import datetime
import socket
import time
import tempfile
import base64
from datetime import timedelta
from io import BytesIO
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QTextEdit, QFileDialog,
    QMessageBox, QLineEdit, QScrollArea, QSlider, QProgressBar, QDialog,
    QGroupBox, QRadioButton, QStyleFactory, QTabWidget, QButtonGroup,
)
from PyQt5.QtGui import QIcon, QColor, QTextCharFormat, QTextCursor, QFont, QPalette, QCloseEvent, QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl, QDir, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from moviepy.editor import VideoFileClip, AudioFileClip
import pysrt
import pysubs2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import webbrowser
import whisper
import numpy as np
from spleeter.separator import Separator

# ========================================
# RESOURCE PATH HELPER - For Bundled EXE
# ========================================
def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    In EXE mode, uses sys._MEIPASS for bundled files.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ========================================
# ENCRYPTION UTILS - For Settings & Client
# ========================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(CURRENT_DIR, "settings.notcapz")
KEY_FILE = os.path.join(CURRENT_DIR, "key.notcapz")
CLIENT_JSON = os.path.join(CURRENT_DIR, "client.json")
CLIENT_ENCRYPTED = os.path.join(CURRENT_DIR, "client.notycapz")

def load_or_create_key():
    """
    Load or generate Fernet key for encryption.
    Key is stored in root folder for persistence across runs.
    """
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

fernet = Fernet(load_or_create_key())

def encrypt_data(data):
    """Encrypt JSON data using Fernet."""
    json_str = json.dumps(data, ensure_ascii=False)
    encrypted = fernet.encrypt(json_str.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_data(encrypted_b64):
    """Decrypt base64-encoded encrypted data."""
    try:
        encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
        decrypted = fernet.decrypt(encrypted).decode('utf-8')
        return json.loads(decrypted)
    except Exception:
        return None

def save_settings(settings_dict):
    """Save settings as encrypted JSON."""
    encrypted_b64 = encrypt_data(settings_dict)
    with open(SETTINGS_FILE, "w", encoding='utf-8') as f:
        f.write(encrypted_b64)

def load_settings():
    """Load decrypted settings with defaults."""
    defaults = {
        "ui_scale": "100%",
        "theme": "Dark",
        "temp_dir": QDir.tempPath(),
        "models_dir": CURRENT_DIR,
        "last_mode": "normal",
        "auto_enhance": False,
        "default_lang": "english",
    }
    if not os.path.exists(SETTINGS_FILE):
        save_settings(defaults)
        return defaults
    try:
        with open(SETTINGS_FILE, "r", encoding='utf-8') as f:
            encrypted_b64 = f.read().strip()
        loaded = decrypt_data(encrypted_b64)
        if loaded:
            defaults.update(loaded)
            return defaults
        else:
            save_settings(defaults)
            return defaults
    except Exception as e:
        logging.getLogger("NotyCaption").error(f"Failed to load settings: {e}")
        save_settings(defaults)
        return defaults

def load_client_secrets():
    """Load Google client secrets: Prefer plain JSON in dev, encrypted in EXE."""
    if os.path.exists(CLIENT_JSON):
        # Dev mode: Use plain client.json
        with open(CLIENT_JSON, "r", encoding='utf-8') as f:
            return json.load(f)
    elif os.path.exists(CLIENT_ENCRYPTED):
        # EXE mode: Use decrypted client.notycapz
        try:
            with open(CLIENT_ENCRYPTED, "r", encoding='utf-8') as f:
                encrypted_b64 = f.read().strip()
            decrypted = decrypt_data(encrypted_b64)
            if decrypted and "installed" in decrypted:
                return decrypted
        except Exception as e:
            logging.getLogger("NotyCaption").error(f"Failed to decrypt client: {e}")
    else:
        logging.getLogger("NotyCaption").warning("No client secrets found")
    return None

# ========================================
# LOGGING SETUP - Secure & Persistent
# ========================================
def setup_logging():
    """
    Setup logging to file in root/logs/ and console.
    Logs include timestamps, levels, and full traces for debugging.
    In EXE mode, logs are in EXE dir/logs/.
    """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = CURRENT_DIR

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
        force=True
    )
    logger = logging.getLogger("NotyCaption")
    logger.info("=== NotyCaption Secure Launch 2026 ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Log file: {log_file}")
    logger.info(f"PyInstaller frozen: {getattr(sys, 'frozen', False)}")
    logger.info(f"Executable path: {sys.executable if getattr(sys, 'frozen', False) else 'dev mode'}")
    logger.info(f"Client mode: {'EXE (encrypted)' if os.path.exists(CLIENT_ENCRYPTED) else 'Dev (plain)'}")
    return logger

logger = setup_logging()

# ========================================
# SINGLE INSTANCE CHECK - Socket Based
# ========================================
class SingleInstance:
    """
    Prevent multiple instances using TCP socket on localhost.
    Binds to port 65432; if fails, another instance is running.
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.already_exists = False
        try:
            self.sock.bind(('127.0.0.1', 65432))
            self.sock.listen(1)
            logger.info("Single instance lock acquired")
        except socket.error as e:
            self.already_exists = True
            logger.warning(f"Single instance check failed: {e}")

    def is_already_running(self):
        return self.already_exists

    def __del__(self):
        if not self.already_exists:
            try:
                self.sock.close()
                logger.info("Single instance lock released")
            except:
                pass

# ========================================
# SETTINGS DIALOG - Enhanced UI
# ========================================
class SettingsDialog(QDialog):
    """
    Advanced settings dialog with theme, scale, paths, and auto-features.
    Emits signal on changes for live updates.
    """
    settingsChanged = pyqtSignal(dict)

    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("NotyCaption Settings - Secure Edition")
        self.setFixedSize(580, 620)
        self.current_settings = current_settings
        lay = QVBoxLayout()
        self.setLayout(lay)

        # Theme Group
        th_gb = QGroupBox("Visual Theme")
        th_lay = QVBoxLayout()
        self.rb_win = QRadioButton("System Default (Windows)")
        self.rb_light = QRadioButton("Light Mode")
        self.rb_dark = QRadioButton("Dark Mode (Modern)")
        th_lay.addWidget(self.rb_win)
        th_lay.addWidget(self.rb_light)
        th_lay.addWidget(self.rb_dark)

        th = current_settings.get("theme", "Dark")
        if th == "Windows Default": self.rb_win.setChecked(True)
        elif th == "Light": self.rb_light.setChecked(True)
        else: self.rb_dark.setChecked(True)

        th_gb.setLayout(th_lay)
        lay.addWidget(th_gb)

        # Scale Group
        sc_gb = QGroupBox("UI Scaling")
        sc_lay = QHBoxLayout()
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["75%", "87%", "100%", "125%", "150%", "175%"])
        self.scale_combo.setCurrentText(current_settings.get("ui_scale", "100%"))
        sc_lay.addWidget(QLabel("Scale Factor: "))
        sc_lay.addWidget(self.scale_combo)
        sc_lay.addStretch()
        sc_gb.setLayout(sc_lay)
        lay.addWidget(sc_gb)

        # Temp Dir Group
        tmp_gb = QGroupBox("Temporary Files Directory")
        tmp_lay = QHBoxLayout()
        self.tmp_edit = QLineEdit(current_settings.get("temp_dir", QDir.tempPath()))
        self.tmp_edit.setPlaceholderText("Default: System Temp")
        tmp_btn = QPushButton("Browse Folder")
        tmp_btn.clicked.connect(self.browse_temp)
        tmp_lay.addWidget(self.tmp_edit)
        tmp_lay.addWidget(tmp_btn)
        tmp_gb.setLayout(tmp_lay)
        lay.addWidget(tmp_gb)

        # Models Dir Group
        mod_gb = QGroupBox("Whisper Models Directory")
        mod_lay = QHBoxLayout()
        self.mod_edit = QLineEdit(current_settings.get("models_dir", CURRENT_DIR))
        self.mod_edit.setPlaceholderText("Default: App Root")
        mod_btn = QPushButton("Browse Folder")
        mod_btn.clicked.connect(self.browse_models)
        mod_lay.addWidget(self.mod_edit)
        mod_lay.addWidget(mod_btn)
        mod_gb.setLayout(mod_lay)
        lay.addWidget(mod_gb)

        # Auto Features Group
        auto_gb = QGroupBox("Auto Features")
        auto_lay = QVBoxLayout()
        self.cb_auto_enhance = QRadioButton("Auto-Enhance Audio (Vocals Only)")
        self.cb_auto_enhance.setChecked(current_settings.get("auto_enhance", False))
        self.cb_default_lang = QComboBox()
        self.cb_default_lang.addItems(["english", "japanese → english (translate)"])
        self.cb_default_lang.setCurrentText(current_settings.get("default_lang", "english"))
        auto_lay.addWidget(self.cb_auto_enhance)
        auto_lay.addWidget(QLabel("Default Language:"))
        auto_lay.addWidget(self.cb_default_lang)
        auto_gb.setLayout(auto_lay)
        lay.addWidget(auto_gb)

        # Buttons
        btn_lay = QHBoxLayout()
        apply_btn = QPushButton("Apply & Restart UI")
        apply_btn.setStyleSheet("background:#007aff; color:white; padding:12px; border-radius:8px; font-weight:bold;")
        apply_btn.clicked.connect(self.apply_close)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("background:#8e8e93; color:white; padding:12px; border-radius:8px;")
        cancel_btn.clicked.connect(self.reject)
        btn_lay.addStretch()
        btn_lay.addWidget(apply_btn)
        btn_lay.addWidget(cancel_btn)
        lay.addLayout(btn_lay)

        logger.info("Settings dialog initialized")

    def browse_temp(self):
        """Browse for temp directory."""
        d = QFileDialog.getExistingDirectory(self, "Select Temporary Files Folder")
        if d:
            self.tmp_edit.setText(d)
            logger.info(f"Temp dir changed to: {d}")

    def browse_models(self):
        """Browse for models directory."""
        d = QFileDialog.getExistingDirectory(self, "Select Whisper Models Folder")
        if d:
            self.mod_edit.setText(d)
            logger.info(f"Models dir changed to: {d}")

    def apply_close(self):
        """Apply changes and emit signal."""
        new_settings = {
            "ui_scale": self.scale_combo.currentText(),
            "theme": "Windows Default" if self.rb_win.isChecked() else
                     "Light" if self.rb_light.isChecked() else "Dark",
            "temp_dir": self.tmp_edit.text(),
            "models_dir": self.mod_edit.text(),
            "auto_enhance": self.cb_auto_enhance.isChecked(),
            "default_lang": self.cb_default_lang.currentText(),
            "last_mode": self.current_settings.get("last_mode", "normal"),
        }
        save_settings(new_settings)
        self.settingsChanged.emit(new_settings)
        self.accept()
        logger.info("Settings applied")

# ========================================
# ONLINE MODE HANDLER - Inlined for Security
# ========================================
SCOPES = ['https://www.googleapis.com/auth/drive']

class OnlineHandler:
    """
    Inline handler for Google Drive/Colab integration.
    No separate file extraction; all logic bundled.
    Handles upload, notebook generation, polling.
    """
    def __init__(self, parent_window):
        self.parent = parent_window
        self.service = None
        self.poll_timer = QTimer(parent_window)
        self.poll_audio_id = None
        self.poll_notebook_id = None
        self.poll_output_name = None
        self.poll_local_out = None

    def handle_online(self, audio_to_use, lang_code, task, wpl, fmt, base, out_path):
        """
        Main online workflow: Upload audio, generate Colab notebook, open browser, poll for output.
        """
        if not self.service:
            QMessageBox.warning(self.parent, "Error", "Please login with Google first.")
            return False

        logger.info("Starting online mode workflow")
        try:
            # Check/Overwrite existing output
            self.poll_output_name = f"{base}_captions{fmt}"
            query = f"name='{self.poll_output_name}' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            files = results.get("files", [])
            if files:
                reply = QMessageBox.question(self.parent, "File Exists", f"{self.poll_output_name} already exists in Drive.\nOverwrite?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return False
                for f in files:
                    self.service.files().delete(fileId=f["id"]).execute()

            # Cleanup old notebooks
            query = "name='NotyCaption_Generator.ipynb' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()

            # Upload audio to Drive
            uploads_id = self.get_or_create_folder(self.service, "uploads")
            audio_filename = os.path.basename(audio_to_use)
            audio_id = self.upload_file(self.service, audio_to_use, audio_filename, uploads_id)

            # Verify upload
            query = f"name='{audio_filename}' and '{uploads_id}' in parents and trashed=false"
            results = self.service.files().list(q=query).execute()
            if not results.get("files", []):
                raise Exception("Audio upload failed - file not found in Drive.")

            # Generate and upload notebook
            notebook_content = self.generate_notebook_content(
                audio_filename, wpl, fmt, self.poll_output_name, lang_code, task
            )

            temp_ipynb = resource_path("temp_Notycaption_Generator.ipynb")
            with open(temp_ipynb, "w", encoding="utf-8") as f:
                json.dump(notebook_content, f, indent=2)

            notebook_id = self.upload_file(self.service, temp_ipynb, "NotyCaption_Generator.ipynb")
            os.remove(temp_ipynb)

            # Open Colab
            colab_url = f"https://colab.research.google.com/drive/{notebook_id}"
            webbrowser.open(colab_url)

            QMessageBox.information(
                self.parent,
                "Colab Launched",
                "Notebook opened in browser.\n\n"
                "Wait 60 seconds → then Runtime → Run All.\n"
                "App will auto-download results after completion."
            )

            self.poll_audio_id = audio_id
            self.poll_notebook_id = notebook_id
            self.poll_local_out = out_path

            self.poll_timer.stop()
            try:
                self.poll_timer.timeout.disconnect()
            except TypeError:
                pass
            self.poll_timer.timeout.connect(lambda: self.poll_for_output())
            self.poll_timer.start(8000)  # Poll every 8 seconds

            logger.info("Online workflow initiated successfully")
            return True

        except Exception as e:
            logger.error(f"Online mode failed: {traceback.format_exc()}")
            QMessageBox.critical(self.parent, "Online Mode Failed", str(e))
            return False

    def get_or_create_folder(self, service, name):
        """Get or create Drive folder."""
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])
        if files:
            return files[0]["id"]

        metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        folder = service.files().create(body=metadata, fields="id").execute()
        return folder.get("id")

    def upload_file(self, service, filepath, filename, parent_id=None):
        """Upload file to Drive."""
        metadata = {"name": filename}
        if parent_id:
            metadata["parents"] = [parent_id]

        media = MediaFileUpload(filepath, resumable=True)
        file = service.files().create(body=metadata, media_body=media, fields="id").execute()
        return file.get("id")

    def generate_notebook_content(self, audio_filename, words_per_line, fmt, output_name, lang_code='en', task='transcribe'):
        """
        Generate JSON for Colab notebook with Whisper transcription.
        Inline all cell code for security.
        """
        def code_cell(lines):
            return {
                "cell_type": "code",
                "metadata": {},
                "execution_count": None,
                "outputs": [],
                "source": lines
            }

        notebook = {
            "nbformat": 4,
            "nbformat_minor": 0,
            "metadata": {
                "kernelspec": {"name": "python3", "display_name": "Python 3"},
                "language_info": {"name": "python"}
            },
            "cells": [

                # Install dependencies
                code_cell([
                    "%%capture\n",
                    "!apt update -qq\n",
                    "!apt install -y ffmpeg -qq\n",
                    "!pip install -q openai-whisper\n",
                    "!pip install -q pysrt pysubs2\n",
                    "print('Dependencies installed successfully')"
                ]),

                # Mount Drive
                code_cell([
                    "from google.colab import drive\n",
                    "drive.mount('/content/drive', force_remount=True)\n",
                    "print('Drive mounted')"
                ]),

                # Imports
                code_cell([
                    "import whisper\n",
                    "import pysrt\n",
                    "import pysubs2\n",
                    "from datetime import timedelta\n",
                    "import os\n",
                    "print('Libraries imported')"
                ]),

                # Load Model
                code_cell([
                    "model_name = 'medium'  # Balanced for Colab resources\n",
                    "print('Loading Whisper model...')\n",
                    "model = whisper.load_model(model_name)\n",
                    "print('Model loaded successfully')"
                ]),

                # Verify Audio
                code_cell([
                    f"audio_path = '/content/drive/My Drive/uploads/{audio_filename}'\n",
                    "if not os.path.exists(audio_path):\n",
                    f"    raise FileNotFoundError(f'Audio file not found at {{audio_path}}. Ensure upload succeeded.')\n",
                    "print(f'Audio file verified: {{audio_path}}')"
                ]),

                # Transcribe
                code_cell([
                    f"result = model.transcribe(\n",
                    f"    audio_path,\n",
                    f"    language='{lang_code}',\n",
                    f"    task='{task}',\n",
                    "    word_timestamps=True\n",
                    ")\n",
                    "print('Transcription completed')"
                ]),

                # Process Subtitles
                code_cell([
                    "subtitles = []\n",
                    "idx = 1\n",
                    "for seg in result['segments']:\n",
                    "    words = seg.get('words', [])\n",
                    "    if not words: continue\n",
                    f"    for i in range(0, len(words), {words_per_line}):\n",
                    f"        chunk = words[i:i+{words_per_line}]\n",
                    "        if not chunk: continue\n",
                    "        text = ' '.join([w['word'].strip().replace(' ', '') for w in chunk])  # Clean text\n",
                    "        start = chunk[0]['start']\n",
                    "        end = chunk[-1]['end']\n",
                    "        subtitles.append((idx, start, end, text))\n",
                    "        idx += 1\n",
                    "print(f'Generated {len(subtitles)} subtitle lines')"
                ]),

                # Save Subtitles
                code_cell([
                    f"fmt = '{fmt}'\n",
                    f"output_path = '/content/drive/My Drive/{output_name}'\n",
                    "if fmt == '.srt':\n",
                    "    srt = pysrt.SubRipFile()\n",
                    "    for idx, start, end, text in subtitles:\n",
                    "        item = pysrt.SubRipItem(\n",
                    "            index=idx,\n",
                    "            start=pysrt.SubRipTime(milliseconds=int(start*1000)),\n",
                    "            end=pysrt.SubRipTime(milliseconds=int(end*1000)),\n",
                    "            text=text\n",
                    "        )\n",
                    "        srt.append(item)\n",
                    "    srt.save(output_path, encoding='utf-8')\n",
                    "    print(f'SRT saved: {output_path}')\n",
                    "else:\n",
                    "    ass = pysubs2.SSAFile()\n",
                    "    style = pysubs2.SSAStyle()\n",
                    "    ass.styles['Default'] = style\n",
                    "    for idx, start, end, text in subtitles:\n",
                    "        event = pysubs2.SSAEvent(\n",
                    "            start=int(start*1000),\n",
                    "            end=int(end*1000),\n",
                    "            text=text\n",
                    "        )\n",
                    "        ass.events.append(event)\n",
                    "    ass.save(output_path)\n",
                    "    print(f'ASS saved: {output_path}')\n",
                    "print('Processing complete - Download ready')"
                ])
            ]
        }
        return notebook

    def poll_for_output(self):
        """
        Poll Drive for generated subtitle file and download.
        Stops timer on success, loads preview, cleans up.
        """
        if not self.poll_output_name:
            return

        query = f"name='{self.poll_output_name}' and trashed=false"
        try:
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
        except Exception as e:
            logger.warning(f"Poll query failed: {e}")
            return

        files = results.get("files", [])
        if not files:
            logger.info("Output not ready yet - continue polling")
            return

        file_id = files[0]["id"]
        try:
            with open(self.poll_local_out, "wb") as f:
                request = self.service.files().get_media(fileId=file_id)
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        logger.info(f"Download progress: {int(status.progress() * 100)}%")
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return

        # Load preview
        self.parent.load_downloaded_subtitles(self.poll_local_out)

        # Cleanup Drive
        try:
            self.service.files().delete(fileId=self.poll_audio_id).execute()
            self.service.files().delete(fileId=self.poll_notebook_id).execute()
            self.service.files().delete(fileId=file_id).execute()
            logger.info("Drive cleanup completed")
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")

        self.poll_timer.stop()
        self.parent.is_generating = False
        self.parent.gen_btn.setEnabled(True)

        QMessageBox.information(
            self.parent,
            "Download Complete",
            f"Subtitles downloaded and preview loaded:\n{self.poll_local_out}"
        )
        logger.info("Online polling completed successfully")

    def cleanup_drive(self):
        """Empty uploads and delete temp notebooks on close."""
        if not self.service:
            return
        try:
            uploads_id = self.get_or_create_folder(self.service, "uploads")
            query = f"'{uploads_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()

            query = "name='NotyCaption_Generator.ipynb' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()

            logger.info("Drive cleanup executed")
        except Exception as e:
            logger.warning(f"Drive cleanup error: {e}")

# ========================================
# AUDIO ENHANCER THREAD - Non-Blocking
# ========================================
class AudioEnhancerThread(QThread):
    """
    Background thread for Spleeter vocal separation to avoid UI freeze.
    Emits progress and completion signals.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, bool)  # path, success
    error = pyqtSignal(str)

    def __init__(self, audio_file, temp_dir, parent=None):
        super().__init__(parent)
        self.audio_file = audio_file
        self.temp_dir = temp_dir

    @pyqtSlot()
    def run(self):
        """
        Run Spleeter separation in thread.
        Inline Spleeter logic for no external script.
        """
        try:
            self.progress.emit(10)
            separator = Separator('spleeter:2stems')
            base_name = os.path.splitext(os.path.basename(self.audio_file))[0]
            output_dir = os.path.join(self.temp_dir, base_name)

            separator.separate_to_file(
                self.audio_file,
                output_dir,
                synchronous=True
            )
            self.progress.emit(80)

            vocals_path = os.path.join(output_dir, 'vocals.wav')
            if not os.path.exists(vocals_path):
                raise FileNotFoundError("Vocals file not generated")

            self.progress.emit(95)
            logger.info("Spleeter separation completed in thread")
            self.finished.emit(vocals_path, True)
        except Exception as e:
            logger.error(f"Spleeter thread error: {traceback.format_exc()}")
            self.error.emit(str(e))
        finally:
            self.progress.emit(100)

# ========================================
# MAIN APPLICATION WINDOW
# ========================================
class NotyCaptionWindow(QMainWindow):
    """
    Main application window for NotyCaption.
    Integrates all features: UI, media handling, generation, playback, editing.
    Supports local/online modes, secure resource loading.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NotyCaption Pro - Secure AI Caption Generator by NotY215")
        self.setMinimumSize(1024, 768)

        # Icon Setup
        icon_path = resource_path('App.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        logger.info("Initializing NotyCaption window...")

        # Load Settings
        self.settings = load_settings()
        self.apply_ui_scale()
        self.apply_theme()

        # Center Window
        self.center_window()

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Top Layout: Left Editor | Right Controls
        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        # Left Panel: Caption Editor
        self.setup_left_panel()

        # Right Panel: Controls (Scrollable)
        self.setup_right_panel()

        # Bottom Layout: Playback & Generate
        self.setup_bottom_panel()

        # Footer
        self.setup_footer()

        # State Initialization
        self.initialize_state()

        # Online Handler
        self.online_handler = OnlineHandler(self)

        # Threads & Timers
        self.enhancer_thread = None
        self.player_timer = QTimer(self)
        self.player_timer.timeout.connect(self.update_timeline)
        self.player_timer.start(50)  # 20 FPS update

        # Load Existing Credentials
        self.load_existing_credentials()

        logger.info("Main window fully initialized")

    def setup_left_panel(self):
        """Setup caption editor panel on left."""
        self.left_panel = QWidget()
        self.left_panel.setMaximumWidth(700)
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        self.top_layout.addWidget(self.left_panel)

        # Title
        title = QLabel("AI-Powered Caption Editor")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #ffffff; margin: 10px; padding: 10px;")
        self.left_layout.addWidget(title)

        # Caption Text Edit
        self.caption_edit = QTextEdit()
        self.caption_edit.setReadOnly(True)
        self.caption_edit.setFont(QFont("Consolas", 12))
        self.caption_edit.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1e1e, stop:1 #2d2d30);
                color: #e0e0e0;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 10px;
                selection-background-color: #007acc;
            }
        """)
        self.caption_edit.setPlaceholderText("Captions will appear here after generation...")
        self.left_layout.addWidget(self.caption_edit, stretch=1)

        # Editor Buttons Row
        btn_row = QHBoxLayout()
        self.edit_btn = QPushButton("✏️ Edit Captions")
        self.edit_btn.setMinimumHeight(60)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0a84ff,stop:1 #0066cc);
                color: white;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
            }
            QPushButton:disabled { background: #666; }
        """)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.edit_btn.setEnabled(False)
        btn_row.addWidget(self.edit_btn)

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setMinimumHeight(60)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #5e5ce6,stop:1 #4a4ad8);
                color: white;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
            }
        """)
        settings_btn.clicked.connect(self.open_settings_dialog)
        btn_row.addWidget(settings_btn)

        self.download_btn = QPushButton("📥 Download Model")
        self.download_btn.setMinimumHeight(60)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff9500,stop:1 #e68900);
                color: white;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
            }
            QPushButton:disabled { background: #666; }
        """)
        self.download_btn.clicked.connect(self.download_whisper_model)
        btn_row.addWidget(self.download_btn)

        self.left_layout.addLayout(btn_row)

    def setup_right_panel(self):
        """Setup scrollable controls panel on right."""
        self.right_scroll = QScrollArea()
        self.right_scroll.setWidgetResizable(True)
        self.right_scroll.setStyleSheet("QScrollArea { border: none; }")
        self.top_layout.addWidget(self.right_scroll)

        self.right_panel = QWidget()
        self.right_layout = QGridLayout()
        self.right_panel.setLayout(self.right_layout)
        self.right_scroll.setWidget(self.right_panel)

        row = 0

        # Login Button
        self.login_button = QPushButton("🔐 Login with Google (Enable Online Mode)")
        self.login_button.setMinimumHeight(60)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #4285f4,stop:1 #3367d6);
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
                padding: 15px;
            }
            QPushButton:disabled { background: #ccc; color: #666; }
        """)
        self.login_button.clicked.connect(self.initiate_google_login)
        self.right_layout.addWidget(self.login_button, row, 0, 1, 2)
        row += 1

        # Mode Selection
        mode_label = QLabel("Processing Mode:")
        mode_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(mode_label, row, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["🖥️ Normal (Local Whisper)", "☁️ Online (Colab + Drive)"])
        self.mode_combo.setMinimumHeight(50)
        self.mode_combo.currentTextChanged.connect(self.on_mode_change)
        self.right_layout.addWidget(self.mode_combo, row, 1)
        row += 1

        # Language
        lang_label = QLabel("Language:")
        lang_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(lang_label, row, 0)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["🇺🇸 English (Transcribe)", "🇯🇵 Japanese → English (Translate)"])
        self.lang_combo.setMinimumHeight(50)
        self.lang_combo.setCurrentText(self.settings.get("default_lang", "🇺🇸 English (Transcribe)"))
        self.right_layout.addWidget(self.lang_combo, row, 1)
        row += 1

        # Words Per Line
        wpl_label = QLabel("Words per Line:")
        wpl_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(wpl_label, row, 0)
        self.words_spin = QSpinBox()
        self.words_spin.setRange(1, 20)
        self.words_spin.setValue(5)
        self.words_spin.setMinimumHeight(50)
        self.words_spin.setStyleSheet("QSpinBox { font-size: 14px; padding: 10px; }")
        self.right_layout.addWidget(self.words_spin, row, 1)
        row += 1

        # Import Button
        self.import_btn = QPushButton("📁 Import Video / Audio File")
        self.import_btn.setMinimumHeight(70)
        self.import_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #007aff,stop:1 #0056b3);
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
            }
        """)
        self.import_btn.clicked.connect(self.import_media_file)
        self.right_layout.addWidget(self.import_btn, row, 0, 1, 2)
        row += 1

        # Output Format
        fmt_label = QLabel("Output Format:")
        fmt_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(fmt_label, row, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["📄 .SRT (Standard)", "🎨 .ASS (Advanced)"])
        self.format_combo.setMinimumHeight(50)
        self.right_layout.addWidget(self.format_combo, row, 1)
        row += 1

        # Output Folder
        out_label = QLabel("Output Folder:")
        out_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(out_label, row, 0)
        self.out_folder_edit = QLineEdit()
        self.out_folder_edit.setReadOnly(True)
        self.out_folder_edit.setMinimumHeight(50)
        self.out_folder_edit.setPlaceholderText("Default: Source Folder")
        self.right_layout.addWidget(self.out_folder_edit, row, 1)
        row += 1

        # Browse Output
        browse_btn = QPushButton("📂 Browse Output Folder")
        browse_btn.setMinimumHeight(50)
        browse_btn.setStyleSheet("""
            QPushButton {
                background: #3a3a3c;
                color: white;
                border-radius: 10px;
                font-size: 12px;
                padding: 10px;
            }
        """)
        browse_btn.clicked.connect(self.browse_output_folder)
        self.right_layout.addWidget(browse_btn, row, 0, 1, 2)
        row += 1

        # Enhance Button
        self.enhance_btn = QPushButton("🎤 Enhance Audio (Vocals Only - Spleeter)")
        self.enhance_btn.setMinimumHeight(70)
        self.enhance_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ffcc00,stop:1 #cc9900);
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
            }
            QPushButton:disabled { background: #ccc; }
        """)
        self.enhance_btn.clicked.connect(self.enhance_audio_vocals)
        self.enhance_btn.setEnabled(False)
        self.right_layout.addWidget(self.enhance_btn, row, 0, 1, 2)

    def setup_bottom_panel(self):
        """Setup playback controls and generate button."""
        bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(bottom_layout)

        # Play/Pause
        self.play_btn = QPushButton("▶️ Play / ⏸️ Pause")
        self.play_btn.setMinimumHeight(70)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #34c759,stop:1 #30d158);
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
                min-width: 120px;
            }
            QPushButton:disabled { background: #ccc; }
        """)
        self.play_btn.clicked.connect(self.toggle_media_playback)
        self.play_btn.setEnabled(False)
        bottom_layout.addWidget(self.play_btn)

        # Timeline Slider
        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #2a2e34;
                height: 16px;
                border-radius: 8px;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0a84ff,stop:1 #0066cc);
                width: 24px;
                border-radius: 12px;
                margin: -10px 0;
                border: 2px solid white;
            }
            QSlider::sub-page:horizontal { background: #0a84ff; border-radius: 8px; }
        """)
        self.timeline.sliderMoved.connect(self.seek_media_position)
        bottom_layout.addWidget(self.timeline, stretch=1)

        # Generate Button
        self.gen_btn = QPushButton("🚀 Generate Captions")
        self.gen_btn.setMinimumHeight(70)
        self.gen_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff3b30,stop:1 #d32f2f);
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
                min-width: 180px;
            }
            QPushButton:disabled { background: #ccc; }
        """)
        self.gen_btn.clicked.connect(self.start_caption_generation)
        bottom_layout.addWidget(self.gen_btn)

        # Progress Bars
        prog_container = QVBoxLayout()
        bottom_layout.addLayout(prog_container)

        self.prog_main = QProgressBar()
        self.prog_main.setStyleSheet("""
            QProgressBar {
                background: #22252a;
                border: 2px solid #3a3f44;
                border-radius: 10px;
                text-align: center;
                color: white;
                font-weight: bold;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0a84ff,stop:1 #0066cc);
                border-radius: 8px;
            }
        """)
        self.prog_main.setFormat("Overall: %p%")
        prog_container.addWidget(self.prog_main)

        self.prog_frame = QProgressBar()
        self.prog_frame.setStyleSheet("""
            QProgressBar {
                background: #22252a;
                border: 2px solid #3a3f44;
                border-radius: 10px;
                text-align: center;
                color: white;
                font-weight: bold;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff9500,stop:1 #e68900);
                border-radius: 8px;
            }
        """)
        self.prog_frame.setFormat("Frame: %v / %m")
        prog_container.addWidget(self.prog_frame)

    def setup_footer(self):
        """Setup application footer."""
        footer = QLabel("NotyCaption Pro • Secure Edition 2026 • All rights reserved by NotY215 • Powered by Whisper AI & Spleeter")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #6c757d; font-size: 10px; margin: 15px 0; padding: 10px; border-top: 1px solid #404040;")
        self.main_layout.addWidget(footer)

    def initialize_state(self):
        """Initialize application state variables."""
        self.input_file = None
        self.audio_file = None
        self.output_folder = None
        self.subtitles = []  # List of dicts: {'index', 'start', 'end', 'text'}
        self.display_lines = []
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.positionChanged.connect(self.on_position_changed)
        self.player.durationChanged.connect(self.on_duration_changed)
        self.player.error.connect(self.on_player_error)
        self.duration_ms = 0
        self.generated = False
        self.edit_active = False
        self.loaded_media = None
        self.last_temp_wav = None
        self.mode = self.settings.get("last_mode", "normal")
        self.is_generating = False
        self.service = None  # Google Drive service
        self.mode_combo.setCurrentText("☁️ Online (Colab + Drive)" if self.mode == "online" else "🖥️ Normal (Local Whisper)")

        # Update UI based on state
        self.update_download_button_visibility()
        self.enhance_btn.setEnabled(bool(self.audio_file))

    def center_window(self):
        """Center the window on screen."""
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        logger.info("Window centered")

    def apply_ui_scale(self):
        """Apply UI scaling from settings."""
        scale_str = self.settings.get("ui_scale", "100%")
        try:
            scale = float(scale_str.rstrip("%")) / 100.0
            font = QApplication.font()
            font.setPointSizeF(font.pointSizeF() * scale)
            QApplication.setFont(font)
            self.resize(int(1024 * scale), int(768 * scale))
            logger.info(f"UI scaled to {scale*100}%")
        except Exception as e:
            logger.warning(f"Scale apply failed: {e}")

    def apply_theme(self):
        """Apply theme from settings."""
        theme = self.settings.get("theme", "Dark")
        if theme == "Light":
            pal = QPalette()
            pal.setColor(QPalette.Window, QColor(248, 249, 250))
            pal.setColor(QPalette.WindowText, QColor(33, 37, 41))
            pal.setColor(QPalette.Base, QColor(255, 255, 255))
            pal.setColor(QPalette.Text, QColor(33, 37, 41))
            pal.setColor(QPalette.Button, QColor(248, 249, 250))
            pal.setColor(QPalette.ButtonText, QColor(33, 37, 41))
            pal.setColor(QPalette.Highlight, QColor(0, 123, 255))
            QApplication.setPalette(pal)
        elif theme == "Windows Default":
            QApplication.setStyle(QStyleFactory.create('windows'))
        else:  # Dark
            pal = QPalette()
            pal.setColor(QPalette.Window, QColor(30, 30, 30))
            pal.setColor(QPalette.WindowText, QColor(255, 255, 255))
            pal.setColor(QPalette.Base, QColor(45, 45, 48))
            pal.setColor(QPalette.Text, QColor(255, 255, 255))
            pal.setColor(QPalette.Button, QColor(52, 52, 52))
            pal.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            pal.setColor(QPalette.Highlight, QColor(0, 122, 255))
            QApplication.setPalette(pal)
            QApplication.setStyle(QStyleFactory.create('Fusion'))
        logger.info(f"Theme applied: {theme}")

    def open_settings_dialog(self):
        """Open settings dialog."""
        logger.info("Opening settings dialog")
        dlg = SettingsDialog(self.settings, self)
        dlg.settingsChanged.connect(self.update_from_settings)
        if dlg.exec_() == QDialog.Accepted:
            logger.info("Settings dialog closed")

    def update_from_settings(self, new_settings):
        """Update app from new settings."""
        self.settings = new_settings
        self.apply_ui_scale()
        self.apply_theme()
        self.lang_combo.setCurrentText(new_settings.get("default_lang", "🇺🇸 English (Transcribe)"))
        self.words_spin.setValue(5)  # Reset or load if saved
        self.update_download_button_visibility()
        self.mode_combo.setCurrentText("☁️ Online (Colab + Drive)" if new_settings.get("last_mode", "normal") == "online" else "🖥️ Normal (Local Whisper)")
        logger.info("Settings updated and applied")

    def update_download_button_visibility(self):
        """Show/hide model download button based on mode and existence."""
        if self.mode == "online":
            self.download_btn.setVisible(False)
            logger.info("Download button hidden in online mode")
            return

        model_path = os.path.join(self.settings["models_dir"], "large-v3.pt")
        exists = os.path.exists(model_path)
        self.download_btn.setVisible(not exists)
        logger.info(f"Model at {model_path} exists: {exists} → Button visible: {not exists}")

    def closeEvent(self, event: QCloseEvent):
        """Handle app close: Cleanup temps, Drive, threads."""
        logger.info("App close event triggered")
        self.player.stop()
        self.player_timer.stop()
        self.online_handler.poll_timer.stop()

        # Cleanup temp audio
        if self.audio_file and self.audio_file.endswith(".temp.wav") and os.path.exists(self.audio_file):
            try:
                os.remove(self.audio_file)
                logger.info(f"Temp audio removed: {self.audio_file}")
            except Exception as e:
                logger.warning(f"Temp audio removal failed: {e}")

        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
                logger.info(f"Last temp WAV removed: {self.last_temp_wav}")
            except Exception as e:
                logger.warning(f"Last temp removal failed: {e}")

        # Drive cleanup
        if self.online_handler.service:
            self.online_handler.cleanup_drive()

        # Save last mode
        self.settings["last_mode"] = self.mode
        save_settings(self.settings)

        logger.info("=== NotyCaption Secure Shutdown ===")
        event.accept()

    def initiate_google_login(self):
        """Start Google OAuth flow using loaded client secrets."""
        client_secrets = load_client_secrets()
        if not client_secrets:
            msg = "Google client secrets not found.\nIn dev mode, ensure client.json exists.\nIn EXE mode, rebuild with build.bat to encrypt client.notycapz."
            logger.warning(msg)
            QMessageBox.warning(self, "Missing Credentials", msg)
            return

        client_path = tempfile.mktemp(suffix='.json')
        try:
            with open(client_path, 'w') as f:
                json.dump(client_secrets, f)
            flow = InstalledAppFlow.from_client_secrets_file(client_path, SCOPES)
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            self.online_handler.service = build("drive", "v3", credentials=creds)
            self.login_button.setVisible(False)
            self.mode = "online"
            self.mode_combo.setCurrentText("☁️ Online (Colab + Drive)")
            self.update_download_button_visibility()
            logger.info("Google login successful - Online mode enabled")
            QMessageBox.information(self, "Login Success", "Google Drive connected. Online mode ready.")
        except Exception as e:
            logger.error(f"Google login failed: {traceback.format_exc()}")
            QMessageBox.critical(self, "Login Error", f"Authentication failed:\n{str(e)}")
        finally:
            if os.path.exists(client_path):
                os.remove(client_path)

    def load_existing_credentials(self):
        """Load existing token.json for auto-login."""
        token_path = "token.json"
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                self.online_handler.service = build("drive", "v3", credentials=creds)
                self.login_button.setVisible(False)
                self.mode = "online"
                self.mode_combo.setCurrentText("☁️ Online (Colab + Drive)")
                self.update_download_button_visibility()
                logger.info("Existing credentials loaded - Online mode activated")
            except Exception as e:
                logger.error(f"Credential load failed: {e}")
                if os.path.exists(token_path):
                    os.remove(token_path)

    def on_mode_change(self, text):
        """Handle mode combo change."""
        self.mode = "online" if "Online" in text else "normal"
        self.settings["last_mode"] = self.mode
        save_settings(self.settings)
        self.update_download_button_visibility()
        logger.info(f"Mode switched to: {self.mode}")

    def load_whisper_model(self):
        """Load Whisper large-v3 model from settings dir."""
        try:
            model_dir = self.settings.get("models_dir", CURRENT_DIR)
            logger.info(f"Loading Whisper large-v3 from: {model_dir}")
            model = whisper.load_model("large-v3", download_root=model_dir)
            logger.info("Whisper model loaded successfully")
            return model
        except Exception as e:
            logger.error(f"Whisper load failed: {traceback.format_exc()}")
            raise RuntimeError(f"Model load error: {str(e)}")

    # Media Playback Handlers
    def on_media_status_changed(self, status):
        """Handle media status changes."""
        if status == QMediaPlayer.LoadedMedia:
            self.play_btn.setEnabled(True)
            logger.info("Media loaded for playback")
        elif status in (QMediaPlayer.NoMedia, QMediaPlayer.InvalidMedia):
            self.play_btn.setEnabled(False)
            self.play_btn.setText("▶️ Play / ⏸️ Pause")

    def on_position_changed(self, position):
        """Update highlight on position change."""
        self.update_caption_highlight(position)

    def on_duration_changed(self, duration):
        """Set timeline range on duration change."""
        self.duration_ms = duration
        self.timeline.setRange(0, duration)

    def on_player_error(self, error):
        """Handle player errors."""
        err_str = self.player.errorString() or "Unknown error"
        logger.warning(f"Media player error: {err_str}")
        QMessageBox.warning(self, "Playback Error", f"Audio playback failed:\n{err_str}")

    def update_timeline(self):
        """Update slider position."""
        if self.duration_ms > 0 and self.player.state() == QMediaPlayer.PlayingState:
            self.timeline.setValue(self.player.position())

    def toggle_media_playback(self):
        """Toggle play/pause."""
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "No Media", "Import audio/video first.")
            return

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText("▶️ Play / ⏸️ Pause")
            logger.info("Playback paused")
        else:
            try:
                if self.loaded_media != self.audio_file:
                    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
                    self.loaded_media = self.audio_file
                    logger.info(f"Media set: {self.audio_file}")
                self.player.play()
                self.play_btn.setText("⏸️ Playing...")
                logger.info("Playback started")
            except Exception as e:
                logger.error(f"Playback start failed: {e}")
                QMessageBox.warning(self, "Play Error", str(e))

    def seek_media_position(self, position):
        """Seek to position in media."""
        self.player.setPosition(position)

    def update_caption_highlight(self, ms):
        """Highlight current subtitle line during playback."""
        if not self.subtitles or not self.generated:
            return
        sec = ms / 1000.0
        doc = self.caption_edit.document()
        cursor = QTextCursor(doc)
        cursor.beginEditBlock()

        # Clear previous highlights
        cursor.select(QTextCursor.Document)
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(0, 0, 0, 0))  # Transparent
        cursor.setCharFormat(fmt)

        # Highlight current
        for i, sub in enumerate(self.subtitles):
            if sub["start"].total_seconds() <= sec < sub["end"].total_seconds():
                block = doc.findBlockNumber(cursor.position())
                if block == i:
                    cursor.movePosition(QTextCursor.StartOfBlock)
                    cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                    fmt.setBackground(QColor(255, 255, 0, 150))  # Yellow highlight
                    cursor.setCharFormat(fmt)
                    self.caption_edit.setTextCursor(cursor)
                    self.caption_edit.ensureCursorVisible()
                    break

        cursor.endEditBlock()

    def import_media_file(self):
        """Import video or audio, extract/convert to WAV."""
        logger.info("Media import dialog opened")
        filter_str = (
            "Media Files ("
            "*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv *.mp3 *.wav *.m4a "
            "*.aac *.flac *.ogg *.wma *.amr *.opus);;"
            "Videos (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv);;"
            "Audio (*.mp3 *.wav *.m4a *.aac *.flac *.ogg *.wma *.amr *.opus)"
        )
        path, _ = QFileDialog.getOpenFileName(self, "Import Video or Audio", "", filter_str)
        if not path:
            logger.info("Import cancelled")
            return

        logger.info(f"Importing: {path}")
        self.input_file = path
        self.output_folder = os.path.dirname(path)
        self.out_folder_edit.setText(self.output_folder)
        self.enhance_btn.setEnabled(True)

        # Temp setup
        temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
        temp_name = os.path.splitext(os.path.basename(path))[0] + ".temp.wav"
        new_temp = os.path.join(temp_dir, temp_name)

        # Cleanup previous temp
        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
                logger.info(f"Previous temp removed: {self.last_temp_wav}")
            except Exception as e:
                logger.warning(f"Previous temp removal failed: {e}")

        success = False
        if path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv')):
            try:
                logger.info("Extracting audio from video...")
                clip = VideoFileClip(path)
                if clip.audio is not None:
                    clip.audio.write_audiofile(new_temp, codec='pcm_s16le', logger=None, verbose=False)
                    self.audio_file = new_temp
                    success = True
                clip.close()
            except Exception as e:
                logger.error(f"Video extraction failed: {e}")

        if not success:
            try:
                logger.info("Converting audio file to WAV...")
                audio_clip = AudioFileClip(path)
                audio_clip.write_audiofile(new_temp, codec='pcm_s16le', logger=None, verbose=False)
                self.audio_file = new_temp
                audio_clip.close()
                success = True
            except Exception as e:
                logger.warning(f"Audio conversion failed: {e}")
                self.audio_file = path  # Fallback to original
                QMessageBox.warning(self, "Conversion Warning", "Using original file (may be slower).")

        self.last_temp_wav = new_temp if success else None
        self.loaded_media = None
        logger.info(f"Audio prepared: {self.audio_file}")
        QMessageBox.information(self, "Import Complete", "Media imported and audio ready for processing.")

    def browse_output_folder(self):
        """Browse for output directory."""
        d = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if d:
            self.output_folder = d
            self.out_folder_edit.setText(d)
            logger.info(f"Output folder set: {d}")

    def enhance_audio_vocals(self):
        """Enhance audio to vocals only using Spleeter in thread."""
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "No Audio", "Import media first.")
            return

        logger.info("Starting vocal enhancement...")
        self.enhance_btn.setEnabled(False)
        temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
        self.enhancer_thread = AudioEnhancerThread(self.audio_file, temp_dir, self)
        self.enhancer_thread.progress.connect(self.prog_main.setValue)
        self.enhancer_thread.finished.connect(self.on_enhance_finished)
        self.enhancer_thread.error.connect(self.on_enhance_error)
        self.enhancer_thread.start()

    @pyqtSlot(str, bool)
    def on_enhance_finished(self, vocals_path, success):
        """Handle enhancement completion."""
        if success:
            base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
            final_name = f"{base}_enhanced_vocals.wav"
            final_path = os.path.join(self.output_folder or CURRENT_DIR, final_name)
            try:
                shutil.move(vocals_path, final_path)
                self.audio_file = final_path  # Update to enhanced
                self.last_temp_wav = final_path
                logger.info(f"Enhanced audio saved: {final_path}")
                QMessageBox.information(self, "Enhancement Complete", f"Vocals-only audio created:\n{final_path}")
            except Exception as e:
                logger.error(f"Move enhanced file failed: {e}")
                QMessageBox.warning(self, "Save Error", str(e))
        self.enhance_btn.setEnabled(True)
        self.enhancer_thread = None

    @pyqtSlot(str)
    def on_enhance_error(self, error_msg):
        """Handle enhancement error."""
        logger.error(f"Enhancement error: {error_msg}")
        QMessageBox.critical(self, "Enhancement Failed", error_msg)
        self.enhance_btn.setEnabled(True)
        self.enhancer_thread = None

    def download_whisper_model(self):
        """Dialog for model download or linking."""
        logger.info("Model download dialog opened")
        dlg = QDialog(self)
        dlg.setWindowTitle("Whisper Model Management")
        dlg.setFixedSize(500, 300)
        lay = QVBoxLayout()
        dlg.setLayout(lay)

        options = [
            "🔗 Link Existing Model (select large-v3.pt)",
            "📁 Download to Custom Folder",
            "🏠 Download to Default (App Folder)"
        ]
        rb_group = QButtonGroup()
        rbs = [QRadioButton(opt) for opt in options]
        rbs[2].setChecked(True)  # Default
        for rb in rbs:
            lay.addWidget(rb)
            rb_group.addButton(rb)

        btn_lay = QHBoxLayout()
        ok_btn = QPushButton("Proceed")
        ok_btn.clicked.connect(dlg.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dlg.reject)
        btn_lay.addWidget(ok_btn)
        btn_lay.addWidget(cancel_btn)
        lay.addLayout(btn_lay)

        if dlg.exec_() != QDialog.Accepted:
            return

        selected = next(i for i, rb in enumerate(rbs) if rb.isChecked())

        if selected == 0:  # Link existing
            file_path, _ = QFileDialog.getOpenFileName(self, "Select large-v3.pt", "", "Model Files (*.pt)")
            if file_path and os.path.basename(file_path) == "large-v3.pt":
                model_dir = os.path.dirname(file_path)
                self.settings["models_dir"] = model_dir
                save_settings(self.settings)
                self.update_download_button_visibility()
                QMessageBox.information(self, "Linked", "Model linked successfully.")
                logger.info(f"Model linked: {model_dir}")
                return
            else:
                QMessageBox.warning(self, "Invalid", "Please select 'large-v3.pt'.")
                return

        # Download modes
        if selected == 1:  # Custom
            path = QFileDialog.getExistingDirectory(self, "Select Download Folder")
            if not path:
                return
        else:
            path = self.settings["models_dir"]

        self.settings["models_dir"] = path
        save_settings(self.settings)
        self.update_download_button_visibility()

        # Spawn console for download
        cmd = [
            'cmd', '/c',
            f'echo Downloading Whisper large-v3 to "{path}"... &&',
            sys.executable, '-c',
            f'import whisper; whisper.load_model("large-v3", download_root=r"{path}"); print("Download complete!")',
            '&& pause'
        ]
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        logger.info(f"Model download started to: {path}")

    def start_caption_generation(self):
        """Main generation workflow: Enhance if auto, then local/online transcribe."""
        if self.is_generating:
            QMessageBox.warning(self, "In Progress", "Generation already running.")
            return

        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "No Media", "Import audio/video first.")
            return

        self.is_generating = True
        self.gen_btn.setEnabled(False)
        self.prog_main.setValue(0)
        self.prog_frame.setValue(0)
        logger.info("=== Secure Caption Generation Started ===")

        # Auto-enhance if enabled
        auto_enhance = self.settings.get("auto_enhance", False)
        enhanced_path = None
        if auto_enhance:
            logger.info("Auto-enhancing audio...")
            self.enhance_btn.setEnabled(False)
            temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
            self.enhancer_thread = AudioEnhancerThread(self.audio_file, temp_dir, self)
            self.enhancer_thread.progress.connect(lambda v: self.prog_main.setValue(v // 2))
            self.enhancer_thread.finished.connect(lambda p, s: self.on_auto_enhance_done(p, s))
            self.enhancer_thread.error.connect(lambda e: self.on_auto_enhance_error(e))
            self.enhancer_thread.start()
            return  # Wait for thread

        # Proceed to generation if no auto-enhance
        self.proceed_to_transcription(enhanced_path)

    def on_auto_enhance_done(self, vocals_path, success):
        """Callback for auto-enhance in generation."""
        if success:
            enhanced_path = vocals_path
            base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
            final_name = f"{base}_auto_enhanced.wav"
            final_path = os.path.join(self.output_folder or CURRENT_DIR, final_name)
            shutil.move(vocals_path, final_path)
            self.audio_file = final_path
            logger.info(f"Auto-enhanced: {final_path}")
        else:
            enhanced_path = None
            logger.warning("Auto-enhance failed, using original audio")

        self.enhancer_thread = None
        self.enhance_btn.setEnabled(True)
        self.proceed_to_transcription(enhanced_path)

    def on_auto_enhance_error(self, error):
        """Error callback for auto-enhance."""
        logger.error(f"Auto-enhance error: {error}")
        QMessageBox.warning(self, "Auto-Enhance Failed", error)
        self.enhancer_thread = None
        self.enhance_btn.setEnabled(True)
        self.proceed_to_transcription(None)

    def proceed_to_transcription(self, enhanced_path):
        """Continue to transcription after optional enhance."""
        lang_text = self.lang_combo.currentText()
        lang_code = "ja" if "Japanese" in lang_text else "en"
        task = "translate" if "Translate" in lang_text else "transcribe"

        wpl = self.words_spin.value()
        fmt = self.format_combo.currentText().lower().replace(".srt", ".srt").replace(".ass", ".ass")  # Clean
        base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
        out_path = os.path.join(self.output_folder or CURRENT_DIR, f"{base}_captions{fmt}")

        # Overwrite check
        if os.path.exists(out_path):
            reply = QMessageBox.question(self, "Overwrite File?", f"File exists:\n{out_path}\nOverwrite?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                self.is_generating = False
                self.gen_btn.setEnabled(True)
                return

        logger.info(f"Transcription params: lang={lang_code}, task={task}, wpl={wpl}, fmt={fmt}, out={out_path}")

        self.prog_main.setValue(10)
        audio_to_use = enhanced_path or self.audio_file

        if self.mode == "online":
            success = self.online_handler.handle_online(audio_to_use, lang_code, task, wpl, fmt, base, out_path)
            if not success:
                self.is_generating = False
                self.gen_btn.setEnabled(True)
        else:
            self.perform_local_transcription(audio_to_use, lang_code, task, wpl, fmt, out_path)

    def perform_local_transcription(self, audio_path, lang_code, task, wpl, fmt, out_path):
        """Local Whisper transcription and subtitle generation."""
        try:
            self.prog_main.setValue(20)
            model = self.load_whisper_model()
            self.prog_main.setValue(30)

            logger.info("Starting local transcription...")
            result = model.transcribe(
                audio_path,
                language=lang_code,
                task=task,
                word_timestamps=True,
                verbose=False
            )
            self.prog_main.setValue(80)
            logger.info("Transcription complete")

            # Process into subtitles
            self.subtitles = []
            self.display_lines = []
            idx = 1

            for seg in result.get("segments", []):
                text = seg.get("text", "").strip()
                if not text:
                    continue

                start = seg.get("start", 0)
                end = seg.get("end", start + 1)

                words = seg.get("words", [])
                if words:
                    word_texts = [w["word"].strip() for w in words]
                    word_starts = [w.get("start", start) for w in words]
                    word_ends = [w.get("end", end) for w in words]
                else:
                    word_texts = text.split()
                    seg_dur = end - start
                    word_starts = [start + (i / max(1, len(word_texts))) * seg_dur for i in range(len(word_texts))]
                    word_ends = word_starts[1:] + [end]

                for i in range(0, len(word_texts), wpl):
                    chunk = word_texts[i:i + wpl]
                    line_text = " ".join(chunk).strip()
                    if not line_text:
                        continue
                    chunk_start = word_starts[i]
                    chunk_end = word_ends[min(i + wpl - 1, len(word_ends) - 1)]

                    self.subtitles.append({
                        "index": idx,
                        "start": timedelta(seconds=chunk_start),
                        "end": timedelta(seconds=chunk_end),
                        "text": line_text
                    })
                    self.display_lines.append(line_text)
                    idx += 1

            self.prog_main.setValue(90)

            # Preview
            preview_text = "\n\n".join(self.display_lines)
            self.caption_edit.setText(preview_text)
            self.generated = True
            self.edit_btn.setEnabled(True)

            # Save file
            self.save_subtitles_to_file(self.subtitles, fmt, out_path)
            self.prog_main.setValue(100)

            logger.info(f"Local generation saved: {out_path}")
            QMessageBox.information(self, "Generation Complete", f"Captions generated and saved:\n{out_path}")

        except Exception as e:
            logger.error(f"Local transcription failed: {traceback.format_exc()}")
            QMessageBox.critical(self, "Generation Error", f"Local processing failed:\n{str(e)}")
        finally:
            self.is_generating = False
            self.gen_btn.setEnabled(True)

    def save_subtitles_to_file(self, subtitles, fmt, out_path):
        """Save subtitles to SRT or ASS."""
        try:
            if fmt == ".srt":
                srt_file = pysrt.SubRipFile()
                for sub in subtitles:
                    item = pysrt.SubRipItem(
                        index=sub["index"],
                        start=pysrt.SubRipTime(milliseconds=int(sub["start"].total_seconds() * 1000)),
                        end=pysrt.SubRipTime(milliseconds=int(sub["end"].total_seconds() * 1000)),
                        text=sub["text"]
                    )
                    srt_file.append(item)
                srt_file.save(out_path, encoding='utf-8')
            else:  # .ass
                ass_file = pysubs2.SSAFile()
                default_style = pysubs2.SSAStyle()
                ass_file.styles["Default"] = default_style
                for sub in subtitles:
                    event = pysubs2.SSAEvent(
                        start=int(sub["start"].total_seconds() * 1000),
                        end=int(sub["end"].total_seconds() * 1000),
                        text=sub["text"]
                    )
                    ass_file.events.append(event)
                ass_file.save(out_path, encoding='utf-8')
            logger.info(f"Subtitles saved as {fmt}: {out_path}")
        except Exception as e:
            logger.error(f"Save failed: {e}")
            raise

    def load_downloaded_subtitles(self, file_path):
        """Load and preview downloaded subtitles from online mode."""
        logger.info(f"Loading online subtitles: {file_path}")
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
                        "index": i + 1,
                        "start": timedelta(milliseconds=event.start),
                        "end": timedelta(milliseconds=event.end),
                        "text": event.text
                    })
                    self.display_lines.append(event.text)

            preview = "\n\n".join(self.display_lines)
            self.caption_edit.setText(preview)
            self.generated = True
            self.edit_btn.setEnabled(True)
            logger.info("Online subtitles loaded successfully")
        except Exception as e:
            logger.error(f"Online load failed: {traceback.format_exc()}")
            QMessageBox.warning(self, "Load Error", f"Preview load failed:\n{str(e)}")

    def toggle_edit_mode(self):
        """Toggle editable mode for captions."""
        if not self.generated:
            return
        self.edit_active = not self.edit_active
        self.caption_edit.setReadOnly(not self.edit_active)
        self.edit_btn.setText("💾 Save & Exit Edit" if self.edit_active else "✏️ Edit Captions")
        if self.edit_active:
            self.caption_edit.setFocus()
        else:
            self.apply_edited_captions()
        logger.info(f"Edit mode: {'enabled' if self.edit_active else 'disabled'}")

    def apply_edited_captions(self):
        """Apply text edits to subtitles list."""
        text_content = self.caption_edit.toPlainText().strip()
        edited_lines = [line.strip() for line in text_content.split('\n\n') if line.strip()]

        if len(edited_lines) != len(self.subtitles):
            QMessageBox.warning(self, "Mismatch", "Line count changed. Discarding edits.")
            self.refresh_caption_preview()
            return

        for i, new_text in enumerate(edited_lines):
            self.subtitles[i]["text"] = new_text
            self.display_lines[i] = new_text

        self.refresh_caption_preview()
        logger.info("Edits applied to subtitles")
        QMessageBox.information(self, "Saved", "Edits applied successfully.")

    def refresh_caption_preview(self):
        """Refresh preview from current subtitles."""
        preview = "\n\n".join(self.display_lines)
        self.caption_edit.setText(preview)

if __name__ == "__main__":
    # Single instance check
    instance = SingleInstance()
    if instance.is_already_running():
        logger.warning("Duplicate instance detected")
        QMessageBox.warning(None, "Already Running", "NotyCaption is already open in another window.")
        sys.exit(1)

    # App setup
    app = QApplication(sys.argv)
    app.setApplicationName("NotyCaption Pro")
    app.setOrganizationName("NotY215")

    # Icon for app
    icon_path = resource_path('App.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Default style
    app.setStyle('Fusion')

    # Launch
    logger.info("Launching secure NotyCaption...")
    window = NotyCaptionWindow()
    window.show()
    logger.info("Main loop started")
    sys.exit(app.exec_())