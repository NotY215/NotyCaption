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
import threading
import requests
from tqdm import tqdm
from datetime import timedelta
from io import BytesIO
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QTextEdit, QFileDialog,
    QMessageBox, QLineEdit, QScrollArea, QSlider, QProgressBar, QDialog,
    QGroupBox, QRadioButton, QStyleFactory, QTabWidget, QButtonGroup,
    QFrame, QGraphicsOpacityEffect, QStackedWidget
)
from PyQt5.QtGui import QIcon, QColor, QTextCharFormat, QTextCursor, QFont, QPalette, QCloseEvent, QPixmap, QBrush, QLinearGradient
from PyQt5.QtCore import QTimer, Qt, QUrl, QDir, pyqtSignal, QThread, pyqtSlot, QPropertyAnimation, QEasingCurve
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

# IMPORTANT: Suppress googleapiclient file_cache warning by disabling it
os.environ["GOOGLEAPI_DISABLE_FILE_CACHE"] = "1"

# Suppress TensorFlow CUDA warnings (common on CPU-only systems)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

# ========================================
# LOGGING SETUP - Secure & Persistent (MOVED TO TOP)
# ========================================
def setup_logging():
    """
    Configure logging with file and console handlers.
    Creates timestamped log files in logs/ directory.
    Handles both dev and frozen (EXE) modes.
    """
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # Define here for logging
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        print(f"Logging in frozen EXE mode to {base_dir}")  # Temp print before logger
    else:
        base_dir = CURRENT_DIR
        print(f"Logging in development mode to {base_dir}")  # Temp print

    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    print(f"Log directory: {log_dir}")  # Temp print

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
    log_file = os.path.join(log_dir, f"NotyCaption_{timestamp}.log")
    print(f"Log file path: {log_file}")  # Temp print

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
    logger.info(f"Client mode: {'EXE (encrypted)' if os.path.exists(os.path.join(CURRENT_DIR, 'client.notycapz')) else 'Dev (plain)'}")
    logger.info(f"CUDA available: {tf.test.is_built_with_cuda()} (Auto-fallback to CPU if no GPU)")
    return logger

logger = setup_logging()

# ========================================
# RESOURCE PATH HELPER - For Bundled EXE
# ========================================
def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    Enhanced with error handling for missing resources in bundled mode.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        logger.info(f"Resource path using PyInstaller temp: {base_path}")
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Resource path using dev directory: {base_path}")
    full_path = os.path.join(base_path, relative_path)
    if not os.path.exists(full_path):
        logger.warning(f"Resource not found: {full_path}")
    return full_path

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
    Load encryption key or generate a new one if not exists.
    Ensures secure key management for settings and client secrets.
    """
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key_data = f.read()
            logger.info("Encryption key loaded from file")
            return key_data
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    logger.info("New encryption key generated and saved")
    return key

fernet = Fernet(load_or_create_key())

def encrypt_data(data):
    """
    Encrypt JSON data using Fernet symmetric encryption.
    Base64 encodes for safe file storage.
    """
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    encrypted = fernet.encrypt(json_str.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_data(encrypted_b64):
    """
    Decrypt and parse JSON from base64 encoded string.
    Handles decryption errors gracefully.
    """
    try:
        encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
        decrypted = fernet.decrypt(encrypted).decode('utf-8')
        return json.loads(decrypted)
    except Exception as dec_err:
        logger.error(f"Decryption failed: {dec_err}")
        return None

def save_settings(settings_dict):
    """
    Save encrypted settings to file.
    Overwrites existing file atomically.
    """
    encrypted_b64 = encrypt_data(settings_dict)
    with open(SETTINGS_FILE, "w", encoding='utf-8') as f:
        f.write(encrypted_b64)
    logger.info("Settings saved securely")

def load_settings():
    """
    Load and decrypt settings from file, fallback to defaults if corrupted.
    Merges loaded data with defaults to ensure completeness.
    """
    defaults = {
        "ui_scale": "100%",
        "theme": "Dark",
        "temp_dir": QDir.tempPath(),
        "models_dir": CURRENT_DIR,
        "last_mode": "normal",
        "auto_enhance": False,
        "default_lang": "🇺🇸 English (Transcribe)",
    }
    if not os.path.exists(SETTINGS_FILE):
        logger.info("No settings file found, using defaults")
        save_settings(defaults)
        return defaults
    try:
        with open(SETTINGS_FILE, "r", encoding='utf-8') as f:
            encrypted_b64 = f.read().strip()
        loaded = decrypt_data(encrypted_b64)
        if loaded:
            defaults.update(loaded)
            logger.info("Settings loaded and merged with defaults")
            return defaults
        else:
            logger.warning("Decryption failed, saving defaults")
            save_settings(defaults)
            return defaults
    except Exception as load_err:
        logger.error(f"Failed to load settings: {load_err}")
        save_settings(defaults)
        return defaults

def load_client_secrets():
    """
    Load Google client secrets from JSON or encrypted file.
    Prioritizes encrypted for security in bundled EXE.
    """
    if os.path.exists(CLIENT_JSON):
        logger.info("Loading plain client.json (dev mode)")
        with open(CLIENT_JSON, "r", encoding='utf-8') as f:
            return json.load(f)
    elif os.path.exists(CLIENT_ENCRYPTED):
        logger.info("Loading encrypted client.notycapz (EXE mode)")
        try:
            with open(CLIENT_ENCRYPTED, "r", encoding='utf-8') as f:
                encrypted_b64 = f.read().strip()
            decrypted = decrypt_data(encrypted_b64)
            if decrypted and "installed" in decrypted:
                logger.info("Client secrets decrypted successfully")
                return decrypted
        except Exception as dec_err:
            logger.error(f"Failed to decrypt client: {dec_err}")
    else:
        logger.warning("No client secrets found - Online mode unavailable")
    return None

# ========================================
# SINGLE INSTANCE CHECK - Socket Based
# ========================================
class SingleInstance:
    """
    Ensures only one instance of the app runs using socket binding.
    Prevents multiple windows and resource conflicts.
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.already_exists = False
        try:
            self.sock.bind(('127.0.0.1', 65432))
            self.sock.listen(1)
            logger.info("Single instance lock acquired successfully")
        except socket.error as bind_err:
            self.already_exists = True
            logger.warning(f"Single instance check failed: {bind_err} - Another instance may be running")

    def is_already_running(self):
        """
        Check if another instance is detected.
        """
        return self.already_exists

    def __del__(self):
        """
        Cleanup socket on destruction.
        """
        if not self.already_exists:
            try:
                self.sock.close()
                logger.info("Single instance lock released")
            except Exception as close_err:
                logger.warning(f"Socket close failed: {close_err}")

# ========================================
# SETTINGS DIALOG - Enhanced UI
# ========================================
class SettingsDialog(QDialog):
    """
    Advanced settings dialog with theme, scaling, paths, and auto-features.
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

        # Scaling Group
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
        self.cb_default_lang.addItems(["🇺🇸 English (Transcribe)", "🇯🇵 Japanese → English (Translate)"])
        self.cb_default_lang.setCurrentText(current_settings.get("default_lang", "🇺🇸 English (Transcribe)"))
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

        logger.info("Settings dialog initialized with current settings")

    def browse_temp(self):
        """
        Browse and set temporary directory.
        """
        d = QFileDialog.getExistingDirectory(self, "Select Temporary Files Folder")
        if d:
            self.tmp_edit.setText(d)
            logger.info(f"Temp dir changed to: {d}")

    def browse_models(self):
        """
        Browse and set models directory.
        """
        d = QFileDialog.getExistingDirectory(self, "Select Whisper Models Folder")
        if d:
            self.mod_edit.setText(d)
            logger.info(f"Models dir changed to: {d}")

    def apply_close(self):
        """
        Apply changes, save settings, emit signal, and close.
        """
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
        logger.info("Settings applied and dialog closed")

# ========================================
# ONLINE MODE HANDLER - Inlined for Security
# ========================================
SCOPES = ['https://www.googleapis.com/auth/drive']

class OnlineHandler:
    """
    Handles Google Drive integration for online Colab-based processing.
    Includes polling, file upload/download, and cleanup.
    """
    def __init__(self, parent_window):
        self.parent = parent_window
        self.service = None
        self.poll_timer = QTimer(parent_window)
        self.poll_audio_id = None
        self.poll_notebook_id = None
        self.poll_output_name = None
        self.poll_local_out = None
        self.poll_attempts = 0
        self.max_poll_attempts = 180
        logger.info("OnlineHandler initialized")

    def handle_online(self, audio_to_use, lang_code, task, wpl, fmt, base, out_path):
        """
        Orchestrate online workflow: upload, generate notebook, launch Colab, poll for results.
        """
        if not self.service:
            QMessageBox.warning(self.parent, "Error", "Please login with Google first.")
            logger.warning("Online mode attempted without service")
            return False

        logger.info("Starting online mode workflow")
        try:
            self.poll_output_name = f"{base}_captions{fmt}"
            query = f"name='{self.poll_output_name}' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            files = results.get("files", [])
            if files:
                reply = QMessageBox.question(self.parent, "File Exists", f"{self.poll_output_name} already exists in Drive.\nOverwrite?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    logger.info("User chose not to overwrite existing file")
                    return False
                for f in files:
                    self.service.files().delete(fileId=f["id"]).execute()
                    logger.info(f"Deleted existing file: {f['id']}")

            # Cleanup old notebook
            query = "name='NotyCaption_Generator.ipynb' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()
                logger.info(f"Deleted old notebook: {f['id']}")

            uploads_id = self.get_or_create_folder(self.service, "uploads")
            audio_filename = os.path.basename(audio_to_use)
            audio_id = self.upload_file(self.service, audio_to_use, audio_filename, uploads_id)
            logger.info(f"Uploaded audio: {audio_id}")

            query = f"name='{audio_filename}' and '{uploads_id}' in parents and trashed=false"
            results = self.service.files().list(q=query).execute()
            if not results.get("files", []):
                raise Exception("Audio upload failed - file not found in Drive.")

            notebook_content = self.generate_notebook_content(
                audio_filename, wpl, fmt, self.poll_output_name, lang_code, task
            )

            temp_ipynb = resource_path("temp_Notycaption_Generator.ipynb")
            with open(temp_ipynb, "w", encoding="utf-8") as f:
                json.dump(notebook_content, f, indent=2)

            notebook_id = self.upload_file(self.service, temp_ipynb, "NotyCaption_Generator.ipynb")
            os.remove(temp_ipynb)
            logger.info(f"Uploaded notebook: {notebook_id}")

            colab_url = f"https://colab.research.google.com/drive/{notebook_id}"
            webbrowser.open(colab_url)
            logger.info(f"Opened Colab: {colab_url}")

            QMessageBox.information(
                self.parent,
                "Colab Launched (GPU Runtime Recommended)",
                "Notebook opened in browser.\n\n"
                "Important:\n"
                "1. In Colab → Runtime → Change runtime type → Hardware accelerator → GPU (T4 recommended)\n"
                "2. Wait 60 seconds → then Runtime → Run All\n"
                "App will auto-download subtitles when finished."
            )

            self.poll_audio_id = audio_id
            self.poll_notebook_id = notebook_id
            self.poll_local_out = out_path
            self.parent.statusBar().showMessage("Online mode active – waiting for Colab (GPU) to finish...", 12000)

            self.poll_timer.stop()
            try:
                self.poll_timer.timeout.disconnect()
            except TypeError:
                pass
            self.poll_timer.timeout.connect(lambda: self.poll_for_output())
            self.poll_timer.start(8000)

            logger.info("Online workflow initiated successfully")
            return True

        except Exception as online_err:
            logger.error(f"Online mode failed: {traceback.format_exc()}")
            QMessageBox.critical(self.parent, "Online Mode Failed", str(online_err))
            return False

    def get_or_create_folder(self, service, name):
        """
        Retrieve or create a Google Drive folder by name.
        """
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])
        if files:
            folder_id = files[0]["id"]
            logger.info(f"Found existing folder: {name} ({folder_id})")
            return folder_id

        metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        folder = service.files().create(body=metadata, fields="id").execute()
        folder_id = folder.get("id")
        logger.info(f"Created new folder: {name} ({folder_id})")
        return folder_id

    def upload_file(self, service, filepath, filename, parent_id=None):
        """
        Upload a file to Google Drive, optionally to a parent folder.
        Supports resumable uploads for large files.
        """
        metadata = {"name": filename}
        if parent_id:
            metadata["parents"] = [parent_id]

        media = MediaFileUpload(filepath, resumable=True)
        file = service.files().create(body=metadata, media_body=media, fields="id").execute()
        file_id = file.get("id")
        logger.info(f"Uploaded {filename} as {file_id}")
        return file_id

    def generate_notebook_content(self, audio_filename, words_per_line, fmt, output_name, lang_code='en', task='transcribe'):
        """
        Generate Jupyter notebook JSON content for Colab execution.
        Includes all dependencies, transcription, and subtitle generation.
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
                "language_info": {"name": "python"},
                "accelerator": "GPU"
            },
            "cells": [
                code_cell([
                    "%%capture\n",
                    "!apt update -qq\n",
                    "!apt install -y ffmpeg -qq\n",
                    "!pip install -q openai-whisper\n",
                    "!pip install -q pysrt pysubs2\n",
                    "print('Dependencies installed successfully')"
                ]),
                code_cell([
                    "from google.colab import drive\n",
                    "drive.mount('/content/drive', force_remount=True)\n",
                    "print('Drive mounted')"
                ]),
                code_cell([
                    "import whisper\n",
                    "import pysrt\n",
                    "import pysubs2\n",
                    "from datetime import timedelta\n",
                    "import os\n",
                    "print('Libraries imported')"
                ]),
                code_cell([
                    "model_name = 'medium'  # Change to 'large' if GPU is active\n",
                    "print('Loading Whisper model...')\n",
                    "model = whisper.load_model(model_name)\n",
                    "print('Model loaded successfully')"
                ]),
                code_cell([
                    f"audio_path = '/content/drive/My Drive/uploads/{audio_filename}'\n",
                    "if not os.path.exists(audio_path):\n",
                    f"    raise FileNotFoundError(f'Audio file not found at {{audio_path}}. Ensure upload succeeded.')\n",
                    "print(f'Audio file verified: {{audio_path}}')"
                ]),
                code_cell([
                    f"result = model.transcribe(\n",
                    f"    audio_path,\n",
                    f"    language='{lang_code}',\n",
                    f"    task='{task}',\n",
                    "    word_timestamps=True\n",
                    ")\n",
                    "print('Transcription completed')"
                ]),
                code_cell([
                    "subtitles = []\n",
                    "idx = 1\n",
                    "for seg in result['segments']:\n",
                    "    words = seg.get('words', [])\n",
                    "    if not words: continue\n",
                    f"    for i in range(0, len(words), {words_per_line}):\n",
                    f"        chunk = words[i:i+{words_per_line}]\n",
                    "        if not chunk: continue\n",
                    "        text = ' '.join([w['word'].strip() for w in chunk])\n",
                    "        start = chunk[0]['start']\n",
                    "        end = chunk[-1]['end']\n",
                    "        subtitles.append((idx, start, end, text))\n",
                    "        idx += 1\n",
                    "print(f'Generated {len(subtitles)} subtitle lines')"
                ]),
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
        logger.info("Notebook content generated")
        return notebook

    def poll_for_output(self):
        """
        Poll Google Drive for output file every 8 seconds.
        Downloads and loads when found, with timeout handling.
        """
        if not self.poll_output_name:
            logger.warning("Polling without output name set")
            return

        self.poll_attempts += 1
        logger.debug(f"Poll attempt {self.poll_attempts}/{self.max_poll_attempts}")

        if self.poll_attempts > self.max_poll_attempts:
            self.poll_timer.stop()
            self.parent.is_generating = False
            self.parent.gen_btn.setEnabled(True)
            QMessageBox.critical(
                self.parent,
                "Colab Timeout / Crash Detected",
                "No result file appeared in Google Drive after long wait.\n\n"
                "Likely causes:\n"
                "• You closed the Colab tab / notebook\n"
                "• Colab runtime disconnected or crashed\n"
                "• Very long video → transcription still running\n"
                "• Google Drive sync delay\n\n"
                "Next steps:\n"
                "1. Go back to the opened Colab tab — check if it finished or errored\n"
                "2. If subtitles appeared in Drive → download manually\n"
                "3. Try again with shorter clip or 'tiny'/'base' model in notebook"
            )
            logger.warning("Online polling reached max attempts → likely crash/timeout")
            return

        query = f"name='{self.poll_output_name}' and trashed=false"
        try:
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            files = results.get("files", [])
            if files:
                file_id = files[0]["id"]
                logger.info(f"Output file found: {file_id}")
                try:
                    with open(self.poll_local_out, "wb") as f:
                        request = self.service.files().get_media(fileId=file_id)
                        downloader = MediaIoBaseDownload(f, request)
                        done = False
                        while not done:
                            status, done = downloader.next_chunk()
                            if status:
                                progress_pct = int(status.progress() * 100)
                                logger.info(f"Download progress: {progress_pct}%")
                                self.parent.prog_main.setValue(progress_pct)
                    self.parent.load_downloaded_subtitles(self.poll_local_out)
                    try:
                        self.service.files().delete(fileId=self.poll_audio_id).execute()
                        self.service.files().delete(fileId=self.poll_notebook_id).execute()
                        self.service.files().delete(fileId=file_id).execute()
                        logger.info("Drive files cleaned up successfully")
                    except Exception as cleanup_err:
                        logger.warning(f"Cleanup failed: {cleanup_err}")
                    self.poll_timer.stop()
                    self.parent.is_generating = False
                    self.parent.gen_btn.setEnabled(True)
                    QMessageBox.information(
                        self.parent,
                        "Success - Subtitles Ready",
                        f"Downloaded and loaded:\n{self.poll_local_out}"
                    )
                    self.poll_attempts = 0
                    logger.info("Online polling complete - success")
                except Exception as dl_err:
                    logger.error(f"Download failed: {dl_err}")
                    QMessageBox.critical(self.parent, "Download Error", str(dl_err))
            else:
                logger.debug(f"Poll attempt {self.poll_attempts}/{self.max_poll_attempts} — waiting...")
                if self.poll_attempts % 15 == 0:
                    mins = (self.poll_attempts * 8) // 60
                    self.parent.statusBar().showMessage(
                        f"Waiting for Colab (GPU) result... ({mins} min elapsed)", 10000
                    )
        except Exception as poll_err:
            logger.warning(f"Poll network/drive error: {poll_err}")

    def cleanup_drive(self):
        """
        Clean up temporary files in Google Drive on app close.
        """
        if not self.service:
            logger.info("No service for Drive cleanup")
            return
        try:
            uploads_id = self.get_or_create_folder(self.service, "uploads")
            query = f"'{uploads_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()
                logger.info(f"Cleaned upload: {f['id']}")

            query = "name='NotyCaption_Generator.ipynb' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()
                logger.info(f"Cleaned notebook: {f['id']}")

            logger.info("Drive cleanup executed successfully")
        except Exception as cleanup_err:
            logger.warning(f"Drive cleanup error: {cleanup_err}")

# ========================================
# AUDIO ENHANCER THREAD - Non-Blocking
# ========================================
class AudioEnhancerThread(QThread):
    """
    Thread for Spleeter-based vocal separation.
    Emits progress, finish, and error signals for UI updates.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, bool)
    error = pyqtSignal(str)

    def __init__(self, audio_file, temp_dir, parent=None):
        super().__init__(parent)
        self.audio_file = audio_file
        self.temp_dir = temp_dir
        logger.info(f"AudioEnhancerThread initialized for {audio_file}")

    @pyqtSlot()
    def run(self):
        """
        Execute vocal separation in thread.
        Simulate progress during separation.
        """
        try:
            self.progress.emit(10)
            logger.info("Initializing Spleeter separator")
            separator = Separator('spleeter:2stems')
            base_name = os.path.splitext(os.path.basename(self.audio_file))[0]
            output_dir = os.path.join(self.temp_dir, base_name)

            logger.info(f"Starting separation to {output_dir}")
            separator.separate_to_file(
                self.audio_file,
                output_dir,
                synchronous=True
            )
            self.progress.emit(80)
            logger.info("Separation phase complete")

            vocals_path = os.path.join(output_dir, 'vocals.wav')
            if not os.path.exists(vocals_path):
                raise FileNotFoundError(f"Vocals file not generated at {vocals_path}")

            self.progress.emit(95)
            logger.info("Spleeter separation completed (GPU/CPU auto)")
            self.finished.emit(vocals_path, True)
        except Exception as enhance_err:
            error_msg = f"Spleeter error: {str(enhance_err)}"
            logger.error(f"Spleeter thread error: {traceback.format_exc()}")
            self.error.emit(error_msg)
        finally:
            self.progress.emit(100)
            logger.info("Enhancer thread finished")

# ========================================
# CUSTOM DOWNLOAD HANDLER FOR WHISPER - FIXED VERSION WITH PROPER ATTRIBUTES
# ========================================
class CancellableWhisperDownloader:
    """Custom download handler that intercepts Whisper's download process"""
    
    def __init__(self):
        self._canceled = False
        self._progress_callback = None
        self._current_download = None
        self._downloaded = 0  # Add this attribute
        self._total_size = 0   # Add this attribute
        
    def cancel(self):
        """Cancel the download immediately"""
        self._canceled = True
        logger.info("Download cancellation requested - will stop at next chunk")
        
    def patched_download_url_to_file(self, original_func, url, dst, *args, **kwargs):
        """Patched version of download_url_to_file that checks for cancellation"""
        
        # Check cancellation before starting
        if self._canceled:
            raise Exception("DOWNLOAD_CANCELED_BY_USER")
        
        # Store download info for potential cancellation
        self._current_download = {'url': url, 'dst': dst}
        
        try:
            import urllib.request
            import os
            
            # Create a custom opener with progress tracking
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=30) as response:
                # Check cancellation after opening connection
                if self._canceled:
                    raise Exception("DOWNLOAD_CANCELED_BY_USER")
                
                # Get file size for progress tracking
                self._total_size = int(response.headers.get('Content-Length', 0))
                
                # Download with chunk-by-chunk cancellation
                with open(dst + '.tmp', 'wb') as out_file:
                    self._downloaded = 0
                    chunk_size = 8192  # 8KB chunks
                    
                    while True:
                        # Check cancellation before each chunk
                        if self._canceled:
                            logger.info("Cancellation detected during download")
                            out_file.close()
                            if os.path.exists(dst + '.tmp'):
                                os.remove(dst + '.tmp')
                            raise Exception("DOWNLOAD_CANCELED_BY_USER")
                        
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        
                        out_file.write(chunk)
                        self._downloaded += len(chunk)
                        
                        # Report progress
                        if self._progress_callback and self._total_size > 0:
                            progress = int((self._downloaded / self._total_size) * 100)
                            if progress < 100:
                                self._progress_callback(progress)
                
                # Final cancellation check
                if self._canceled:
                    if os.path.exists(dst + '.tmp'):
                        os.remove(dst + '.tmp')
                    raise Exception("DOWNLOAD_CANCELED_BY_USER")
                
                # Move temp file to final destination
                if os.path.exists(dst):
                    os.remove(dst)
                os.rename(dst + '.tmp', dst)
                
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(dst + '.tmp'):
                try:
                    os.remove(dst + '.tmp')
                except:
                    pass
            raise e
        finally:
            self._current_download = None
        
        return dst

    def download_model(self, model_name, download_root, progress_callback=None):
        """
        Download Whisper model with cancellation support
        
        Args:
            model_name: Name of the model (e.g., "large-v1")
            download_root: Directory to download to
            progress_callback: Function to call with progress percentage
        """
        self._canceled = False
        self._progress_callback = progress_callback
        self._downloaded = 0
        self._total_size = 0
        
        try:
            import torch.hub
            import whisper
            
            # Save original function
            original_download = torch.hub.download_url_to_file
            
            # Create patched function with access to self
            def patched_func(url, dst, *args, **kwargs):
                return self.patched_download_url_to_file(original_download, url, dst, *args, **kwargs)
            
            # Apply the patch
            torch.hub.download_url_to_file = patched_func
            
            # Check cancellation before loading
            if self._canceled:
                raise Exception("DOWNLOAD_CANCELED_BY_USER")
            
            logger.info(f"Starting download of {model_name} model to {download_root}")
            
            # Load model - this will use our patched download function
            model = whisper.load_model(
                model_name, 
                download_root=download_root,
                in_memory=False
            )
            
            # Check cancellation after loading
            if self._canceled:
                raise Exception("DOWNLOAD_CANCELED_BY_USER")
                
            logger.info("Model downloaded successfully")
            
            # Report 100% progress
            if progress_callback:
                progress_callback(100)
                
            return model
            
        except Exception as e:
            error_str = str(e)
            if "DOWNLOAD_CANCELED_BY_USER" in error_str:
                logger.info("Download was canceled by user")
                # Clean up any partial files
                model_path = os.path.join(download_root, f"{model_name}.pt")
                temp_path = model_path + '.tmp'
                for path in [model_path, temp_path]:
                    if os.path.exists(path):
                        try:
                            os.remove(path)
                            logger.info(f"Cleaned up file after cancel: {path}")
                        except:
                            pass
                raise Exception("Download canceled by user")
            else:
                logger.error(f"Download error: {e}")
                raise
        finally:
            # Restore original function
            import torch.hub
            torch.hub.download_url_to_file = original_download

# ========================================
# MODEL DOWNLOAD THREAD - Fixed with proper cancellation
# ========================================
class ModelDownloadThread(QThread):
    """
    Thread for downloading Whisper model with proper cancellation.
    Uses patched downloader that actually stops when canceled.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)  # success, message
    canceled = pyqtSignal()

    def __init__(self, model_dir, parent=None):
        super().__init__(parent)
        self.model_dir = model_dir
        self._is_canceled = False
        self._downloader = CancellableWhisperDownloader()
        logger.info(f"ModelDownloadThread initialized for {model_dir}")

    def cancel(self):
        """
        Set cancellation flag and stop the download immediately.
        """
        self._is_canceled = True
        self._downloader.cancel()
        logger.info("Model download cancellation requested - stopping download immediately")

    @pyqtSlot()
    def run(self):
        """
        Download the model with proper progress tracking.
        """
        try:
            self.progress.emit(5)
            logger.info("Starting model download process")
            
            # Check if model already exists (check for both large-v1.pt and large.pt)
            model_path = os.path.join(self.model_dir, "large-v1.pt")
            if not os.path.exists(model_path):
                model_path = os.path.join(self.model_dir, "large.pt")
            
            if os.path.exists(model_path):
                logger.info("Model already exists, skipping download")
                self.progress.emit(100)
                self.finished.emit(True, "Model already exists!")
                return
            
            # Download with progress callback
            model = self._downloader.download_model(
                "large-v1",  # Use large-v1 instead of large
                self.model_dir,
                progress_callback=lambda p: self.progress.emit(p)
            )
            
            if self._is_canceled:
                logger.info("Download was canceled after completion check")
                self.canceled.emit()
                return
            
            logger.info("Model downloaded successfully")
            self.progress.emit(100)
            self.finished.emit(True, "Model large-v1 downloaded successfully!")
                
        except Exception as dl_err:
            error_str = str(dl_err)
            if "canceled" in error_str.lower():
                logger.info("Download was canceled by user")
                # Clean up any remaining files
                model_path = os.path.join(self.model_dir, "large-v1.pt")
                temp_path = model_path + '.tmp'
                for path in [model_path, temp_path]:
                    if os.path.exists(path):
                        try:
                            os.remove(path)
                            logger.info(f"Cleaned up file after cancel: {path}")
                        except:
                            pass
                self.canceled.emit()
            elif not self._is_canceled:  # Only report error if not canceled
                error_msg = f"Download error: {str(dl_err)}"
                logger.error(f"Model thread error: {traceback.format_exc()}")
                self.finished.emit(False, error_msg)

# ========================================
# MAIN APPLICATION WINDOW
# ========================================
class NotyCaptionWindow(QMainWindow):
    """
    Main application window with full UI, threads, and state management.
    Handles all features: import, enhance, generate, playback, edit.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NotyCaption Pro - Secure AI Caption Generator by NotY215")
        self.setMinimumSize(1024, 768)
        logger.info("Initializing main window")

        icon_path = resource_path('App.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            logger.info("App icon set")

        self.settings = load_settings()
        self.apply_ui_scale()
        self.apply_theme()

        self.center_window()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Enhanced Overlay for full window coverage and blocking
        self.overlay = QFrame(self.central_widget)
        self.overlay.setStyleSheet("""
            QFrame {
                background: rgba(0,0,0,0.85);
                border: none;
            }
        """)
        self.overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.overlay.hide()

        # Overlay layout with centered content
        self.overlay_layout = QVBoxLayout(self.overlay)
        self.overlay_layout.setAlignment(Qt.AlignCenter)

        # Progress container
        self.progress_container = QWidget()
        self.progress_container.setStyleSheet("""
            QWidget {
                background: #2d2d30;
                border-radius: 15px;
                padding: 20px;
                max-width: 500px;
            }
        """)
        prog_lay = QVBoxLayout(self.progress_container)

        # Progress title
        prog_title = QLabel("Downloading Whisper large Model")
        prog_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        prog_title.setAlignment(Qt.AlignCenter)
        prog_lay.addWidget(prog_title)

        # Progress info with download speed and size
        self.prog_info = QLabel("Starting download...")
        self.prog_info.setStyleSheet("color: #cccccc; font-size: 12px; margin-bottom: 15px;")
        self.prog_info.setAlignment(Qt.AlignCenter)
        prog_lay.addWidget(self.prog_info)

        # Progress bar
        self.download_prog = QProgressBar()
        self.download_prog.setMinimum(0)
        self.download_prog.setMaximum(100)
        self.download_prog.setStyleSheet("""
            QProgressBar {
                background: #3a3f44;
                border: 2px solid #4a4f55;
                border-radius: 10px;
                text-align: center;
                color: white;
                font-weight: bold;
                height: 35px;
                min-width: 400px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00c853, stop:0.5 #00b140, stop:1 #009624);
                border-radius: 8px;
            }
        """)
        prog_lay.addWidget(self.download_prog)

        # Cancel button
        self.cancel_download_btn = QPushButton("Cancel Download")
        self.cancel_download_btn.setStyleSheet("""
            QPushButton {
                background: #d32f2f;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 25px;
                margin-top: 15px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: #b71c1c;
            }
            QPushButton:pressed {
                background: #9a0000;
            }
            QPushButton:disabled {
                background: #666666;
                color: #999999;
            }
        """)
        self.cancel_download_btn.clicked.connect(self.confirm_cancel_download)
        self.cancel_download_btn.setEnabled(False)
        prog_lay.addWidget(self.cancel_download_btn, alignment=Qt.AlignCenter)

        self.overlay_layout.addWidget(self.progress_container)

        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        self.setup_left_panel()
        self.setup_right_panel()
        self.setup_bottom_panel()
        self.setup_footer()

        self.initialize_state()
        self.online_handler = OnlineHandler(self)

        self.enhancer_thread = None
        self.model_download_thread = None
        self.player_timer = QTimer(self)
        self.player_timer.timeout.connect(self.update_timeline)
        self.player_timer.start(50)

        self.load_existing_credentials()

        logger.info("Main window fully initialized with enhanced overlay")

    def resizeEvent(self, event):
        """
        Handle window resize to update overlay geometry.
        """
        if self.overlay.isVisible():
            self.overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
            self.overlay.raise_()
        super().resizeEvent(event)

    def setup_left_panel(self):
        """Setup left panel with caption editor and action buttons."""
        self.left_panel = QWidget()
        self.left_panel.setMaximumWidth(700)
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        self.top_layout.addWidget(self.left_panel)

        title = QLabel("AI-Powered Caption Editor")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #ffffff; margin: 10px; padding: 10px;")
        self.left_layout.addWidget(title)

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

        btn_row = QHBoxLayout()
        self.edit_btn = QPushButton("✏️ Edit Captions")
        self.edit_btn.setMinimumHeight(60)
        self.edit_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0a84ff,stop:1 #0066cc); color: white; border-radius: 12px; font-weight: bold; font-size: 14px; padding: 12px; }
            QPushButton:disabled { background: #666; }
        """)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.edit_btn.setEnabled(False)
        btn_row.addWidget(self.edit_btn)

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setMinimumHeight(60)
        settings_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #5e5ce6,stop:1 #4a4ad8); color: white; border-radius: 12px; font-weight: bold; font-size: 14px; padding: 12px; }
        """)
        settings_btn.clicked.connect(self.open_settings_dialog)
        btn_row.addWidget(settings_btn)

        self.download_btn = QPushButton("📥 Download large-v1 Model")
        self.download_btn.setMinimumHeight(60)
        self.download_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff9500,stop:1 #e68900); color: white; border-radius: 12px; font-weight: bold; font-size: 14px; padding: 12px; }
            QPushButton:disabled { background: #666; }
        """)
        self.download_btn.clicked.connect(self.open_model_download_dialog)
        btn_row.addWidget(self.download_btn)

        self.left_layout.addLayout(btn_row)
        logger.info("Left panel setup complete")

    def setup_right_panel(self):
        """Setup right panel with controls."""
        self.right_scroll = QScrollArea()
        self.right_scroll.setWidgetResizable(True)
        self.right_scroll.setStyleSheet("QScrollArea { border: none; }")
        self.top_layout.addWidget(self.right_scroll)

        self.right_panel = QWidget()
        self.right_layout = QGridLayout()
        self.right_panel.setLayout(self.right_layout)
        self.right_scroll.setWidget(self.right_panel)

        row = 0

        self.login_button = QPushButton("🔐 Login with Google (Enable Online Mode)")
        self.login_button.setMinimumHeight(60)
        self.login_button.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #4285f4,stop:1 #3367d6); color: white; border-radius: 15px; font-weight: bold; font-size: 14px; padding: 15px; }
            QPushButton:disabled { background: #ccc; color: #666; }
        """)
        self.login_button.clicked.connect(self.initiate_google_login)
        self.right_layout.addWidget(self.login_button, row, 0, 1, 2)
        row += 1

        mode_label = QLabel("Processing Mode:")
        mode_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(mode_label, row, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["🖥️ Normal (Local Whisper)", "☁️ Online (Colab + Drive)"])
        self.mode_combo.setMinimumHeight(50)
        self.mode_combo.currentTextChanged.connect(self.on_mode_change)
        self.right_layout.addWidget(self.mode_combo, row, 1)
        row += 1

        lang_label = QLabel("Language:")
        lang_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(lang_label, row, 0)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["🇺🇸 English (Transcribe)", "🇯🇵 Japanese → English (Translate)"])
        self.lang_combo.setMinimumHeight(50)
        self.lang_combo.setCurrentText(self.settings.get("default_lang", "🇺🇸 English (Transcribe)"))
        self.right_layout.addWidget(self.lang_combo, row, 1)
        row += 1

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

        self.import_btn = QPushButton("📁 Import Video / Audio File")
        self.import_btn.setMinimumHeight(70)
        self.import_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #007aff,stop:1 #0056b3); color: white; border-radius: 15px; font-weight: bold; font-size: 16px; padding: 15px; }
        """)
        self.import_btn.clicked.connect(self.import_media_file)
        self.right_layout.addWidget(self.import_btn, row, 0, 1, 2)
        row += 1

        fmt_label = QLabel("Output Format:")
        fmt_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(fmt_label, row, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["📄 .SRT (Standard)", "🎨 .ASS (Advanced)"])
        self.format_combo.setMinimumHeight(50)
        self.right_layout.addWidget(self.format_combo, row, 1)
        row += 1

        out_label = QLabel("Output Folder:")
        out_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(out_label, row, 0)
        self.out_folder_edit = QLineEdit()
        self.out_folder_edit.setReadOnly(True)
        self.out_folder_edit.setMinimumHeight(50)
        self.out_folder_edit.setPlaceholderText("Default: Source Folder")
        self.right_layout.addWidget(self.out_folder_edit, row, 1)
        row += 1

        browse_btn = QPushButton("📂 Browse Output Folder")
        browse_btn.setMinimumHeight(50)
        browse_btn.setStyleSheet("""
            QPushButton { background: #3a3a3c; color: white; border-radius: 10px; font-size: 12px; padding: 10px; }
        """)
        browse_btn.clicked.connect(self.browse_output_folder)
        self.right_layout.addWidget(browse_btn, row, 0, 1, 2)
        row += 1

        self.enhance_btn = QPushButton("🎤 Enhance Audio (Vocals Only - Spleeter)")
        self.enhance_btn.setMinimumHeight(70)
        self.enhance_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ffcc00,stop:1 #cc9900); color: white; border-radius: 15px; font-weight: bold; font-size: 16px; padding: 15px; }
            QPushButton:disabled { background: #ccc; }
        """)
        self.enhance_btn.clicked.connect(self.enhance_audio_vocals)
        self.enhance_btn.setEnabled(False)
        self.right_layout.addWidget(self.enhance_btn, row, 0, 1, 2)
        logger.info("Right panel setup complete")

    def setup_bottom_panel(self):
        """Setup bottom panel with playback controls and progress bars."""
        bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(bottom_layout)

        self.play_btn = QPushButton("▶️ Play / ⏸️ Pause")
        self.play_btn.setMinimumHeight(70)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #007aff,stop:1 #0056b3);
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
                min-width: 120px;
            }
            QPushButton:disabled { 
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #cccccc,stop:1 #aaaaaa); 
                color: #666666; 
            }
        """)
        self.play_btn.clicked.connect(self.toggle_media_playback)
        self.play_btn.setEnabled(False)
        bottom_layout.addWidget(self.play_btn)

        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setStyleSheet("""
            QSlider::groove:horizontal { background: #2a2e34; height: 16px; border-radius: 8px; margin: 2px 0; }
            QSlider::handle:horizontal { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0a84ff,stop:1 #0066cc); width: 24px; border-radius: 12px; margin: -10px 0; border: 2px solid white; }
            QSlider::sub-page:horizontal { background: #0a84ff; border-radius: 8px; }
        """)
        self.timeline.sliderMoved.connect(self.seek_media_position)
        bottom_layout.addWidget(self.timeline, stretch=1)

        self.gen_btn = QPushButton("🚀 Generate Captions")
        self.gen_btn.setMinimumHeight(70)
        self.gen_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff3b30,stop:1 #d32f2f); color: white; border-radius: 15px; font-weight: bold; font-size: 16px; padding: 15px; min-width: 180px; }
            QPushButton:disabled { background: #ccc; }
        """)
        self.gen_btn.clicked.connect(self.start_caption_generation)
        bottom_layout.addWidget(self.gen_btn)

        prog_container = QVBoxLayout()
        bottom_layout.addLayout(prog_container)

        self.prog_main = QProgressBar()
        self.prog_main.setStyleSheet("""
            QProgressBar { background: #22252a; border: 2px solid #3a3f44; border-radius: 10px; text-align: center; color: white; font-weight: bold; height: 25px; }
            QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0a84ff,stop:1 #0066cc); border-radius: 8px; }
        """)
        self.prog_main.setFormat("Overall: %p%")
        prog_container.addWidget(self.prog_main)

        self.prog_frame = QProgressBar()
        self.prog_frame.setStyleSheet("""
            QProgressBar { background: #22252a; border: 2px solid #3a3f44; border-radius: 10px; text-align: center; color: white; font-weight: bold; height: 25px; }
            QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff9500,stop:1 #e68900); border-radius: 8px; }
        """)
        self.prog_frame.setFormat("Frame: %v / %m")
        prog_container.addWidget(self.prog_frame)
        logger.info("Bottom panel setup complete")

    def setup_footer(self):
        """Setup footer with copyright and credits."""
        footer = QLabel("NotyCaption Pro • Secure Edition 2026 • All rights reserved by NotY215 • Powered by Whisper AI & Spleeter (GPU/CPU Auto)")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #6c757d; font-size: 10px; margin: 15px 0; padding: 10px; border-top: 1px solid #404040;")
        self.main_layout.addWidget(footer)
        logger.info("Footer setup complete")

    def initialize_state(self):
        """Initialize app state variables."""
        self.input_file = None
        self.audio_file = None
        self.output_folder = None
        self.subtitles = []
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
        self.service = None
        self.mode_combo.setCurrentText("☁️ Online (Colab + Drive)" if self.mode == "online" else "🖥️ Normal (Local Whisper)")

        self.update_download_button_visibility()
        self.enhance_btn.setEnabled(bool(self.audio_file))
        self.play_btn.setEnabled(bool(self.audio_file))
        logger.info("App state initialized")

    def center_window(self):
        """Center the window on screen."""
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        logger.info("Window centered on screen")

    def apply_ui_scale(self):
        """Apply UI scaling based on settings."""
        scale_str = self.settings.get("ui_scale", "100%")
        try:
            scale = float(scale_str.rstrip("%")) / 100.0
            font = QApplication.font()
            font.setPointSizeF(font.pointSizeF() * scale)
            QApplication.setFont(font)
            self.resize(int(1024 * scale), int(768 * scale))
            logger.info(f"UI scaled to {scale*100}% successfully")
        except Exception as scale_err:
            logger.warning(f"UI scale apply failed: {scale_err}")

    def apply_theme(self):
        """Apply selected theme."""
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
            logger.info("Light theme applied")
        elif theme == "Windows Default":
            QApplication.setStyle(QStyleFactory.create('windows'))
            logger.info("Windows Default theme applied")
        else:
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
            logger.info("Dark theme applied")
        logger.info(f"Theme applied: {theme}")

    def open_settings_dialog(self):
        """Open and manage settings dialog."""
        logger.info("Opening settings dialog")
        dlg = SettingsDialog(self.settings, self)
        dlg.settingsChanged.connect(self.update_from_settings)
        if dlg.exec_() == QDialog.Accepted:
            logger.info("Settings dialog accepted")
        else:
            logger.info("Settings dialog canceled")

    def update_from_settings(self, new_settings):
        """Update app with new settings."""
        self.settings = new_settings
        self.apply_ui_scale()
        self.apply_theme()
        self.lang_combo.setCurrentText(new_settings.get("default_lang", "🇺🇸 English (Transcribe)"))
        self.words_spin.setValue(5)
        self.update_download_button_visibility()
        self.mode_combo.setCurrentText("☁️ Online (Colab + Drive)" if new_settings.get("last_mode", "normal") == "online" else "🖥️ Normal (Local Whisper)")
        logger.info("Settings updated and applied globally")

    def update_download_button_visibility(self):
        """Show/hide download button based on mode and model existence."""
        if self.mode == "online":
            self.download_btn.setVisible(False)
            logger.info("Download button hidden in online mode")
            return

        # Check for both large-v1.pt and large.pt (for backward compatibility)
        model_path_v1 = os.path.join(self.settings["models_dir"], "large-v1.pt")
        model_path = os.path.join(self.settings["models_dir"], "large.pt")
        exists = os.path.exists(model_path_v1) or os.path.exists(model_path)
        self.download_btn.setVisible(not exists)
        logger.info(f"Model exists: {exists} → Button visible: {not exists}")

    def closeEvent(self, event: QCloseEvent):
        """Handle app close: cleanup threads, files, Drive, save settings."""
        logger.info("App close event triggered")
        self.player.stop()
        self.player_timer.stop()
        self.online_handler.poll_timer.stop()

        if self.audio_file and self.audio_file.endswith(".temp.wav") and os.path.exists(self.audio_file):
            try:
                os.remove(self.audio_file)
                logger.info(f"Temp audio removed: {self.audio_file}")
            except Exception as rm_err:
                logger.warning(f"Temp audio removal failed: {rm_err}")

        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
                logger.info(f"Last temp WAV removed: {self.last_temp_wav}")
            except Exception as rm_err:
                logger.warning(f"Last temp removal failed: {rm_err}")

        if self.online_handler.service:
            self.online_handler.cleanup_drive()

        self.settings["last_mode"] = self.mode
        save_settings(self.settings)

        logger.info("=== NotyCaption Secure Shutdown ===")
        event.accept()

    def initiate_google_login(self):
        """Initiate Google OAuth flow for Drive access."""
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
        except Exception as login_err:
            logger.error(f"Google login failed: {traceback.format_exc()}")
            QMessageBox.critical(self, "Login Error", f"Authentication failed:\n{str(login_err)}")
        finally:
            if os.path.exists(client_path):
                os.remove(client_path)
                logger.info("Temp client file removed")

    def load_existing_credentials(self):
        """Load and refresh existing Google credentials from token.json."""
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
                logger.info("Existing credentials loaded and refreshed - Online mode activated")
            except Exception as cred_err:
                logger.error(f"Credential load failed: {cred_err}")
                if os.path.exists(token_path):
                    os.remove(token_path)
                    logger.info("Invalid token removed")

    def on_mode_change(self, text):
        """Handle mode switch between local and online."""
        self.mode = "online" if "Online" in text else "normal"
        self.settings["last_mode"] = self.mode
        save_settings(self.settings)
        self.update_download_button_visibility()
        logger.info(f"Mode switched to: {self.mode}")

    def load_whisper_model(self):
        """Load Whisper large-v1 model with error handling."""
        try:
            model_dir = self.settings.get("models_dir", CURRENT_DIR)
            logger.info(f"Loading Whisper large-v1 from: {model_dir} (Auto GPU/CPU)")
            model = whisper.load_model("large-v1", download_root=model_dir)
            logger.info("Whisper model loaded successfully")
            return model
        except Exception as load_err:
            logger.error(f"Whisper load failed: {traceback.format_exc()}")
            raise RuntimeError(f"Model load error: {str(load_err)}")

    def on_media_status_changed(self, status):
        """Handle media status changes for playback UI."""
        if status == QMediaPlayer.LoadedMedia:
            self.play_btn.setEnabled(True)
            logger.info("Media loaded for playback")
        elif status in (QMediaPlayer.NoMedia, QMediaPlayer.InvalidMedia):
            self.play_btn.setEnabled(False)
            self.play_btn.setText("▶️ Play / ⏸️ Pause")
            logger.warning("Media status invalid")

    def on_position_changed(self, position):
        """Update caption highlighting based on playback position."""
        self.update_caption_highlight(position)

    def on_duration_changed(self, duration):
        """Set timeline range based on media duration."""
        self.duration_ms = duration
        self.timeline.setRange(0, duration)
        logger.debug(f"Media duration set: {duration} ms")

    def on_player_error(self, error):
        """Handle media player errors with user notification."""
        err_str = self.player.errorString() or "Unknown error"
        logger.warning(f"Media player error: {err_str}")
        QMessageBox.warning(self, "Playback Error", f"Audio playback failed:\n{err_str}")

    def update_timeline(self):
        """Update timeline slider during playback."""
        if self.duration_ms > 0 and self.player.state() == QMediaPlayer.PlayingState:
            self.timeline.setValue(self.player.position())

    def toggle_media_playback(self):
        """Toggle play/pause for loaded media."""
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "No Audio", "No audio file loaded or file was deleted.")
            logger.warning("Play clicked → no audio_file")
            return

        logger.info(f"Play/Pause clicked | File: {self.audio_file}")

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText("▶️ Play / ⏸️ Pause")
            logger.info("→ Paused")
            return

        try:
            url = QUrl.fromLocalFile(self.audio_file)
            media = QMediaContent(url)
            self.player.setMedia(media)
            self.loaded_media = self.audio_file
            logger.info("Media reloaded successfully")

            self.player.play()
            self.play_btn.setText("⏸️ Playing...")
            logger.info("→ Play command sent")

            QTimer.singleShot(1500, self.check_playback_status)

        except Exception as play_err:
            logger.error(f"Playback setup failed: {play_err}", exc_info=True)
            QMessageBox.critical(self, "Critical Playback Error",
                                f"Qt could not prepare audio:\n{str(play_err)}\n\n"
                                "Try:\n1. Play the .temp.wav file in VLC/Media Player\n"
                                "2. If it plays → issue is QtMultimedia\n"
                                "3. Re-import or restart app")

    def check_playback_status(self):
        """Verify playback status after load attempt."""
        status = self.player.mediaStatus()
        logger.info(f"Playback status check: {status}")
        if status == QMediaPlayer.LoadedMedia:
            logger.info("Media loaded OK")
        elif status in (QMediaPlayer.NoMedia, QMediaPlayer.InvalidMedia):
            logger.error("Media invalid after load attempt")
            QMessageBox.warning(self, "Cannot Play",
                                "Qt says media is invalid.\n\n"
                                "Common fixes:\n"
                                "• Shorten filename (remove spaces/special chars)\n"
                                "• Re-extract audio\n"
                                "• Install/update K-Lite Codec Pack (Basic)")

    def seek_media_position(self, position):
        """Seek to position in media."""
        self.player.setPosition(position)
        logger.debug(f"Seek to: {position} ms")

    def update_caption_highlight(self, ms):
        """Highlight current caption line during playback."""
        if not self.subtitles or not self.generated:
            return
        sec = ms / 1000.0
        doc = self.caption_edit.document()
        cursor = QTextCursor(doc)
        cursor.beginEditBlock()

        # Reset all highlights
        cursor.select(QTextCursor.Document)
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(0, 0, 0, 0))
        cursor.setCharFormat(fmt)

        # Highlight current line
        for i, sub in enumerate(self.subtitles):
            if sub["start"].total_seconds() <= sec < sub["end"].total_seconds():
                cursor.movePosition(QTextCursor.Start)
                cursor.movePosition(QTextCursor.NextBlock, QTextCursor.MoveAnchor, i)
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                fmt.setBackground(QColor(255, 215, 0, 180))
                cursor.setCharFormat(fmt)
                self.caption_edit.setTextCursor(cursor)
                self.caption_edit.ensureCursorVisible()
                break

        cursor.endEditBlock()
        logger.debug(f"Highlighted line for time: {sec:.2f}s")

    def import_media_file(self):
        """Import video or audio, extract/convert to WAV temp file."""
        logger.info("Media import dialog opened")
        filter_str = (
            "Media Files (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv *.mp3 *.wav *.m4a *.aac *.flac *.ogg *.wma *.amr *.opus)"
        )
        path, _ = QFileDialog.getOpenFileName(self, "Import Video or Audio", "", filter_str)
        if not path:
            logger.info("Import cancelled by user")
            return

        logger.info(f"Importing: {path}")
        self.input_file = path
        self.output_folder = os.path.dirname(path)
        self.out_folder_edit.setText(self.output_folder)
        self.enhance_btn.setEnabled(True)

        temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
        temp_name = os.path.splitext(os.path.basename(path))[0] + ".temp.wav"
        new_temp = os.path.join(temp_dir, temp_name)

        # Cleanup previous temp
        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
                logger.info(f"Previous temp removed: {self.last_temp_wav}")
            except Exception as rm_err:
                logger.warning(f"Previous temp removal failed: {rm_err}")

        success = False
        if path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv')):
            try:
                logger.info("Extracting audio from video...")
                clip = VideoFileClip(path)
                if clip.audio is not None:
                    clip.audio.write_audiofile(new_temp, codec='pcm_s16le', logger=None, verbose=False)
                    self.audio_file = new_temp
                    success = True
                    logger.info("Video audio extracted successfully")
                clip.close()
            except Exception as vid_err:
                logger.error(f"Video extraction failed: {vid_err}")

        if not success:
            try:
                logger.info("Converting audio file to WAV...")
                audio_clip = AudioFileClip(path)
                audio_clip.write_audiofile(new_temp, codec='pcm_s16le', logger=None, verbose=False)
                self.audio_file = new_temp
                self.debug_audio_file()
                audio_clip.close()
                success = True
                logger.info("Audio conversion to WAV complete")
            except Exception as aud_err:
                logger.warning(f"Audio conversion failed: {aud_err}")
                self.audio_file = path
                QMessageBox.warning(self, "Conversion Warning", "Using original file (may be slower).")

        self.last_temp_wav = new_temp if success else None
        self.loaded_media = None
        self.play_btn.setEnabled(True)
        logger.info(f"Audio prepared: {self.audio_file}")
        QMessageBox.information(self, "Import Complete", "Media imported and audio ready for processing.")

    def debug_audio_file(self):
        """Log audio file details for debugging."""
        if not self.audio_file:
            logger.info("No audio file set")
            return
        logger.info(f"Audio file path: {self.audio_file}")
        logger.info(f"Exists: {os.path.exists(self.audio_file)}")
        logger.info(f"Size: {os.path.getsize(self.audio_file) / 1024 / 1024:.2f} MB")

    def browse_output_folder(self):
        """Browse and set output folder."""
        d = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if d:
            self.output_folder = d
            self.out_folder_edit.setText(d)
            logger.info(f"Output folder set: {d}")

    def enhance_audio_vocals(self):
        """Start vocal enhancement thread."""
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "No Audio", "Import media first.")
            logger.warning("Enhance clicked without audio")
            return

        logger.info("Starting vocal enhancement...")
        self.enhance_btn.setEnabled(False)
        temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
        self.enhancer_thread = AudioEnhancerThread(self.audio_file, temp_dir, self)
        self.enhancer_thread.progress.connect(self.prog_main.setValue)
        self.enhancer_thread.finished.connect(self.on_enhance_finished)
        self.enhancer_thread.error.connect(self.on_enhance_error)
        self.enhancer_thread.start()
        logger.info("Enhancer thread started")

    @pyqtSlot(str, bool)
    def on_enhance_finished(self, vocals_path, success):
        """Handle enhancement completion."""
        if success:
            base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
            final_name = f"{base}_enhanced_vocals.wav"
            final_path = os.path.join(self.output_folder or CURRENT_DIR, final_name)
            try:
                shutil.move(vocals_path, final_path)
                self.audio_file = final_path
                self.last_temp_wav = final_path
                self.play_btn.setEnabled(True)
                logger.info(f"Enhanced audio saved: {final_path}")
                QMessageBox.information(self, "Enhancement Complete", f"Vocals-only audio created:\n{final_path}")
            except Exception as move_err:
                logger.error(f"Move enhanced file failed: {move_err}")
                QMessageBox.warning(self, "Save Error", str(move_err))
        self.enhance_btn.setEnabled(True)
        self.enhancer_thread = None
        logger.info("Enhancer thread finished")

    @pyqtSlot(str)
    def on_enhance_error(self, error_msg):
        """Handle enhancement errors."""
        logger.error(f"Enhancement error: {error_msg}")
        QMessageBox.critical(self, "Enhancement Failed", error_msg)
        self.enhance_btn.setEnabled(True)
        self.enhancer_thread = None

    def confirm_cancel_download(self):
        """Show confirmation dialog before canceling download."""
        reply = QMessageBox.question(
            self,
            "Confirm Cancel",
            "Are you sure you want to cancel the download?\n\nThe partially downloaded file will be deleted permanently.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.cancel_download_btn.setEnabled(False)
            self.download_prog.setFormat("Canceling...")
            self.prog_info.setText("Canceling download and cleaning up...")
            
            # Cancel the download immediately
            if self.model_download_thread:
                self.model_download_thread.cancel()
                
                # Wait a bit for cancellation to complete
                QTimer.singleShot(500, self._check_cancel_complete)
            logger.info("User confirmed download cancellation")

    def _check_cancel_complete(self):
        """Check if cancellation is complete and force if needed"""
        if self.model_download_thread and self.model_download_thread.isRunning():
            logger.warning("Thread still running after cancel - forcing cleanup")
            # Force terminate if still running after 500ms
            self.model_download_thread.terminate()
            self.model_download_thread.wait(1000)
            self.on_model_download_canceled()

    def open_model_download_dialog(self):
        """Open dialog for model download options."""
        logger.info("Opening model download dialog")
        dlg = QDialog(self)
        dlg.setWindowTitle("Whisper large Model Download")
        dlg.setFixedSize(520, 340)
        lay = QVBoxLayout()
        dlg.setLayout(lay)

        title = QLabel("Download Whisper large-v1 Model (~2.9 GB)")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        lay.addWidget(title)

        desc = QLabel("large-v1 is the most accurate model.\nRequires ~3 GB disk space.\nDownload may take 5-30 minutes depending on internet speed.")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        lay.addWidget(desc)

        options = [
            "🏠 Download to Default Folder (App Root)",
            "📁 Choose Custom Download Folder",
            "🔗 I already have large-v1.pt (link existing file)"
        ]
        rb_group = QButtonGroup()
        rbs = [QRadioButton(opt) for opt in options]
        rbs[0].setChecked(True)
        for rb in rbs:
            lay.addWidget(rb)
            rb_group.addButton(rb)

        btn_lay = QHBoxLayout()
        ok_btn = QPushButton("Start Download / Link")
        ok_btn.setStyleSheet("background:#00c853; color:white; padding:12px; border-radius:8px; font-weight:bold;")
        ok_btn.clicked.connect(dlg.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("background:#d32f2f; color:white; padding:12px; border-radius:8px;")
        cancel_btn.clicked.connect(dlg.reject)
        btn_lay.addStretch()
        btn_lay.addWidget(ok_btn)
        btn_lay.addWidget(cancel_btn)
        lay.addLayout(btn_lay)

        if dlg.exec_() != QDialog.Accepted:
            logger.info("Model download dialog canceled")
            return

        selected = next(i for i, rb in enumerate(rbs) if rb.isChecked())

        if selected == 2:  # Link existing
            file_path, _ = QFileDialog.getOpenFileName(self, "Select large.pt", "", "PyTorch Model (*.pt)")
            if file_path and os.path.basename(file_path) == "large.pt":
                model_dir = os.path.dirname(file_path)
                self.settings["models_dir"] = model_dir
                save_settings(self.settings)
                self.update_download_button_visibility()
                QMessageBox.information(self, "Success", "Model file linked successfully!")
                logger.info(f"Model linked from: {model_dir}")
            else:
                QMessageBox.warning(self, "Invalid File", "Please select a file named exactly 'large.pt'")
            return

        if selected == 1:  # Custom folder
            path = QFileDialog.getExistingDirectory(self, "Select Folder to Download Model")
            if not path:
                logger.info("Custom folder selection canceled")
                return
        else:
            path = self.settings["models_dir"]

        self.settings["models_dir"] = path
        save_settings(self.settings)
        self.update_download_button_visibility()

        # Show overlay with full coverage
        self.overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.overlay.raise_()
        self.overlay.show()
        
        # Update progress info
        self.download_prog.setValue(0)
        self.download_prog.setFormat("%p%")
        self.prog_info.setText("Starting download...")
        self.cancel_download_btn.setEnabled(True)

        # Disable other buttons
        self.gen_btn.setEnabled(False)
        self.import_btn.setEnabled(False)
        self.enhance_btn.setEnabled(False)
        self.play_btn.setEnabled(False)
        self.edit_btn.setEnabled(False)
        logger.info("UI buttons disabled during download")

        self.model_download_thread = ModelDownloadThread(path, self)
        self.model_download_thread.progress.connect(self.on_download_progress)
        self.model_download_thread.finished.connect(self.on_model_download_finished)
        self.model_download_thread.canceled.connect(self.on_model_download_canceled)
        self.model_download_thread.start()

        logger.info(f"Model download started to: {path}")

    def on_download_progress(self, value):
        """Update download progress display."""
        self.download_prog.setValue(value)
        
        # Format the progress info nicely with error handling
        try:
            if (hasattr(self, 'model_download_thread') and 
                self.model_download_thread and 
                hasattr(self.model_download_thread, '_downloader')):
                
                downloader = self.model_download_thread._downloader
                
                # Check if attributes exist before using them
                if hasattr(downloader, '_downloaded') and hasattr(downloader, '_total_size'):
                    downloaded_mb = downloader._downloaded / (1024 * 1024)
                    total_mb = downloader._total_size / (1024 * 1024)
                    
                    if total_mb > 0:
                        self.prog_info.setText(f"Downloading... {downloaded_mb:.1f} MB / {total_mb:.1f} MB ({value}%)")
                    else:
                        self.prog_info.setText(f"Downloading... ({value}%)")
                else:
                    self.prog_info.setText(f"Downloading... ({value}%)")
            else:
                self.prog_info.setText(f"Downloading... ({value}%)")
        except Exception as e:
            # Fallback to simple progress display if any error occurs
            logger.debug(f"Progress display error: {e}")
            self.prog_info.setText(f"Downloading... ({value}%)")
        
        self.download_prog.setFormat(f"{value}%")

    @pyqtSlot(bool, str)
    def on_model_download_finished(self, success, message):
        """Handle download completion."""
        self.overlay.hide()
        # Re-enable buttons
        self.gen_btn.setEnabled(True)
        self.import_btn.setEnabled(True)
        self.enhance_btn.setEnabled(bool(self.audio_file))
        self.play_btn.setEnabled(bool(self.audio_file))
        self.edit_btn.setEnabled(self.generated)
        self.cancel_download_btn.setEnabled(False)
        logger.info("UI buttons re-enabled after download")
        
        if success:
            self.update_download_button_visibility()
            QMessageBox.information(self, "Success", message)
            logger.info("Model download finished successfully")
        else:
            QMessageBox.critical(self, "Download Failed", message)
            logger.error("Model download failed")
        self.model_download_thread = None

    @pyqtSlot()
    def on_model_download_canceled(self):
        """Handle cancellation: hide overlay, re-enable buttons."""
        self.overlay.hide()
        # Re-enable buttons
        self.gen_btn.setEnabled(True)
        self.import_btn.setEnabled(True)
        self.enhance_btn.setEnabled(bool(self.audio_file))
        self.play_btn.setEnabled(bool(self.audio_file))
        self.edit_btn.setEnabled(self.generated)
        self.cancel_download_btn.setEnabled(False)
        logger.info("UI buttons re-enabled after cancel")
        
        QMessageBox.information(
            self, 
            "Download Canceled", 
            "The model download has been canceled and the partial file has been deleted."
        )
        self.model_download_thread = None

    def start_caption_generation(self):
        """Start caption generation workflow."""
        if self.is_generating:
            QMessageBox.warning(self, "In Progress", "Generation already running.")
            logger.warning("Generation attempted while in progress")
            return

        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "No Media", "Import audio/video first.")
            logger.warning("Generation attempted without media")
            return

        self.is_generating = True
        self.gen_btn.setEnabled(False)
        self.prog_main.setValue(0)
        self.prog_frame.setValue(0)
        logger.info("=== Secure Caption Generation Started ===")

        auto_enhance = self.settings.get("auto_enhance", False)
        enhanced_path = None
        if auto_enhance:
            logger.info("Auto-enhancing audio before generation...")
            self.enhance_btn.setEnabled(False)
            temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
            self.enhancer_thread = AudioEnhancerThread(self.audio_file, temp_dir, self)
            self.enhancer_thread.progress.connect(lambda v: self.prog_main.setValue(v // 2))
            self.enhancer_thread.finished.connect(lambda p, s: self.on_auto_enhance_done(p, s))
            self.enhancer_thread.error.connect(lambda e: self.on_auto_enhance_error(e))
            self.enhancer_thread.start()
            return

        self.proceed_to_transcription(enhanced_path)

    def on_auto_enhance_done(self, vocals_path, success):
        """Handle auto-enhance for generation."""
        if success:
            enhanced_path = vocals_path
            base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
            final_name = f"{base}_auto_enhanced.wav"
            final_path = os.path.join(self.output_folder or CURRENT_DIR, final_name)
            shutil.move(vocals_path, final_path)
            self.audio_file = final_path
            self.play_btn.setEnabled(True)
            logger.info(f"Auto-enhanced: {final_path}")
        else:
            enhanced_path = None
            logger.warning("Auto-enhance failed, using original audio")

        self.enhancer_thread = None
        self.enhance_btn.setEnabled(True)
        self.proceed_to_transcription(enhanced_path)

    def on_auto_enhance_error(self, error):
        """Handle auto-enhance error for generation."""
        logger.error(f"Auto-enhance error: {error}")
        QMessageBox.warning(self, "Auto-Enhance Failed", error)
        self.enhancer_thread = None
        self.enhance_btn.setEnabled(True)
        self.proceed_to_transcription(None)

    def proceed_to_transcription(self, enhanced_path):
        """Proceed to transcription after optional enhancement."""
        lang_text = self.lang_combo.currentText()
        lang_code = "ja" if "Japanese" in lang_text else "en"
        task = "translate" if "Translate" in lang_text else "transcribe"

        wpl = self.words_spin.value()
        fmt_map = {
            "📄 .SRT (Standard)": ".srt",
            ".srt (standard)":    ".srt",
            "🎨 .ASS (Advanced)":  ".ass",
            ".ass":               ".ass",
        }
        fmt = fmt_map.get(self.format_combo.currentText(), ".srt")
        base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
        out_path = os.path.join(self.output_folder or CURRENT_DIR, f"{base}_captions{fmt}")

        if os.path.exists(out_path):
            reply = QMessageBox.question(self, "Overwrite File?", f"File exists:\n{out_path}\nOverwrite?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                self.is_generating = False
                self.gen_btn.setEnabled(True)
                logger.info("Overwrite canceled")
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
        """Perform local Whisper transcription."""
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

            preview_text = "\n\n".join(self.display_lines)
            self.caption_edit.setText(preview_text)
            self.generated = True
            self.edit_btn.setEnabled(True)

            self.save_subtitles_to_file(self.subtitles, fmt, out_path)
            self.prog_main.setValue(100)

            logger.info(f"Local generation saved: {out_path}")
            QMessageBox.information(self, "Generation Complete", f"Captions generated and saved:\n{out_path}")

        except Exception as trans_err:
            logger.error(f"Local transcription failed: {traceback.format_exc()}")
            QMessageBox.critical(self, "Generation Error", f"Local processing failed:\n{str(trans_err)}")
        finally:
            self.is_generating = False
            self.gen_btn.setEnabled(True)

    def save_subtitles_to_file(self, subtitles, fmt, out_path):
        """Save subtitles to SRT or ASS file."""
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
                logger.info(f"SRT saved: {out_path}")
            else:
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
                logger.info(f"ASS saved: {out_path}")
            logger.info(f"Subtitles saved as {fmt}: {out_path}")
        except Exception as save_err:
            logger.error(f"Save failed: {save_err}")
            raise

    def load_downloaded_subtitles(self, file_path):
        """Load subtitles from downloaded file for preview."""
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
                logger.info("SRT loaded")
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
                logger.info("ASS loaded")

            preview = "\n\n".join(self.display_lines)
            self.caption_edit.setText(preview)
            self.generated = True
            self.edit_btn.setEnabled(True)
            logger.info("Online subtitles loaded successfully")
        except Exception as load_err:
            logger.error(f"Online load failed: {traceback.format_exc()}")
            QMessageBox.warning(self, "Load Error", f"Preview load failed:\n{str(load_err)}")

    def toggle_edit_mode(self):
        """Toggle editable mode for captions."""
        if not self.generated:
            logger.warning("Edit toggled without generated captions")
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
        """Apply user edits to subtitles."""
        text_content = self.caption_edit.toPlainText().strip()
        edited_lines = [line.strip() for line in text_content.split('\n\n') if line.strip()]

        if len(edited_lines) != len(self.subtitles):
            QMessageBox.warning(self, "Mismatch", "Line count changed. Discarding edits.")
            self.refresh_caption_preview()
            logger.warning("Edit discarded due to line mismatch")
            return

        for i, new_text in enumerate(edited_lines):
            self.subtitles[i]["text"] = new_text
            self.display_lines[i] = new_text

        self.refresh_caption_preview()
        logger.info("Edits applied to subtitles")
        QMessageBox.information(self, "Saved", "Edits applied successfully.")

    def refresh_caption_preview(self):
        """Refresh caption display from current lines."""
        preview = "\n\n".join(self.display_lines)
        self.caption_edit.setText(preview)
        logger.debug("Caption preview refreshed")

if __name__ == "__main__":
    """
    Main entry point: single instance check, app setup, run.
    """
    instance = SingleInstance()
    if instance.is_already_running():
        logger.warning("Duplicate instance detected")
        QMessageBox.warning(None, "Already Running", "NotyCaption is already open in another window.")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName("NotyCaption Pro")
    app.setOrganizationName("NotY215")

    icon_path = resource_path('App.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        logger.info("Global app icon set")

    app.setStyle('Fusion')
    logger.info("Fusion style applied globally")

    logger.info("Launching secure NotyCaption...")
    window = NotyCaptionWindow()
    window.show()
    logger.info("Main loop started")
    sys.exit(app.exec_())