#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NotyCaption Pro - Online-Only AI Caption Generator with Vocal Enhancement
Version: 2026.7.0
Author: NotY215

ONLINE-ONLY MODE:
- All processing done in Google Colab (Transcription + Vocal Enhancement)
- Local app only extracts audio and uploads
- No local Whisper, TensorFlow, Spleeter, or heavy ML libraries
"""

import sys
import os
import platform

# ========================================
# FIRST: Define App Data Directory
# ========================================
if platform.system() == "Windows":
    APP_DATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), "NotyCaptionGenAI")
else:
    APP_DATA_DIR = os.path.join(os.path.expanduser('~'), ".notycaptiongenai")

os.makedirs(APP_DATA_DIR, exist_ok=True)

# Create subdirectories
LOGS_DIR = os.path.join(APP_DATA_DIR, "logs")
CACHE_DIR = os.path.join(APP_DATA_DIR, "cache")
TEMP_DIR = os.path.join(APP_DATA_DIR, "temp")
EXPORTS_DIR = os.path.join(APP_DATA_DIR, "exports")

for dir_path in [LOGS_DIR, CACHE_DIR, TEMP_DIR, EXPORTS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# ========================================
# Setup Logging
# ========================================
import logging
import datetime

def setup_logging():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
    log_file = os.path.join(LOGS_DIR, f"NotyCaption_{timestamp}.log")

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
    logger.info(f"NotyCaption Pro Launch - Version 2026.7.0 (Online-Only Mode)")
    logger.info(f"App data directory: {APP_DATA_DIR}")
    logger.info(f"Log file: {log_file}")
    return logger

logger = setup_logging()

# ========================================
# Continue with remaining imports
# ========================================
import json
import shutil
import subprocess
import traceback
import time
import tempfile
import base64
import threading
import re
import uuid
import gc
import queue
import socket
import webbrowser
import pickle
import zlib
import hashlib
import random
import copy
import functools
import collections
import contextlib
import configparser
import urllib.request
import urllib.parse
import urllib.error
import mimetypes
import glob
import io
import codecs
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Union, List, Dict, Tuple, Callable
from collections import deque
from datetime import timedelta, datetime

# Windows specific
if platform.system() == "Windows":
    import winreg
    import ctypes
    import ctypes.wintypes
    from ctypes import windll
    import win32com.client
    import pythoncom

# Threading
from threading import Thread, Lock, Event
from queue import Queue

# PyQt5
from PyQt5.QtCore import (
    Qt, QObject, QTimer, QThread, QUrl, QRect, QSize,
    pyqtSignal, pyqtSlot, QByteArray, QIODevice, QFile, QDir,
    QPropertyAnimation, QEasingCurve, QProcess, QDateTime,
    QCoreApplication, QEventLoop, QMargins
)

from PyQt5.QtGui import (
    QIcon, QColor, QPixmap, QFont, QFontDatabase, QPalette,
    QPainter, QPen, QLinearGradient, QBrush, QCursor, QClipboard,
    QKeySequence, QImage, QTextCursor, QTextDocument, QTextCharFormat,
    QFontMetrics, QFontInfo, QDesktopServices
)

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QTextEdit, QLineEdit,
    QScrollArea, QProgressBar, QDialog, QGroupBox, QRadioButton,
    QTabWidget, QFrame, QStatusBar, QMenu, QShortcut, QFileDialog,
    QMessageBox, QSlider, QSplitter, QAction, QToolBar,
    QSplashScreen, QGraphicsDropShadowEffect, QStyleFactory, QCheckBox,
    QGridLayout, QListWidgetItem, QMenuBar, QPlainTextEdit, QScrollBar,
    QSizePolicy, QSpacerItem, QStackedWidget, QTableWidget, QTabBar,
    QTextBrowser, QToolButton, QColorDialog
)

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

# Video/Audio Processing
import wave
import soundfile as sf
import pydub
from pydub import AudioSegment
import mutagen
from moviepy.editor import VideoFileClip, AudioFileClip
import imageio

# Subtitles
import pysrt
from pysrt import SubRipFile, SubRipItem, SubRipTime
import pysubs2
from pysubs2 import SSAFile, SSAEvent, SSAStyle

# Google APIs
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
except ImportError:
    pass

# Cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Utilities
import requests
from tqdm import tqdm
import humanize
from humanize import naturalsize

# ========================================
# Package Metadata
# ========================================
APP_NAME = "NotyCaption Pro"
APP_AUTHOR = "NotY215"
APP_VERSION = "2026.7.0"
__version__ = APP_VERSION
__author__ = APP_AUTHOR
APP_BUILD = datetime.now().strftime("%Y%m%d")
APP_COPYRIGHT = f"Copyright © 2026 {APP_AUTHOR}. All rights reserved."

SCOPES = ['https://www.googleapis.com/auth/drive']


# ========================================
# Window Size Constants (3:2 Ratio)
# ========================================
MIN_WINDOW_WIDTH = 900
MIN_WINDOW_HEIGHT = 600
DEFAULT_WINDOW_WIDTH = 1000
DEFAULT_WINDOW_HEIGHT = 667
MAX_WINDOW_WIDTH = 1400
MAX_WINDOW_HEIGHT = 933


# ========================================
# Define remaining directories
# ========================================
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.notcapz")
KEY_FILE = os.path.join(APP_DATA_DIR, "key.notcapz")
TOKEN_FILE = os.path.join(APP_DATA_DIR, "token.json")
CLIENT_JSON = os.path.join(APP_DATA_DIR, "client.json")
CLIENT_ENCRYPTED = os.path.join(APP_DATA_DIR, "client.notycapz")

logger.info(f"App data directory: {APP_DATA_DIR}")
logger.info(f"Logs directory: {LOGS_DIR}")

# ========================================
# Encryption utilities
# ========================================
def generate_key_from_password(password: str, salt: bytes = None) -> tuple:
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def load_or_create_key() -> bytes:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
        key_path = os.path.join(base, "key.notcapz")
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                return f.read()
        else:
            key_path = KEY_FILE
            if os.path.exists(key_path):
                with open(key_path, "rb") as f:
                    return f.read()
            else:
                password = APP_NAME + APP_AUTHOR + APP_VERSION
                key, salt = generate_key_from_password(password)
                with open(KEY_FILE, "wb") as f:
                    f.write(salt + key)
                return key

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            data = f.read()
            return data[16:]
    
    password = APP_NAME + APP_AUTHOR + APP_VERSION
    key, salt = generate_key_from_password(password)
    with open(KEY_FILE, "wb") as f:
        f.write(salt + key)
    return key

try:
    key = load_or_create_key()
    fernet = Fernet(key)
    logger.info("Encryption initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize encryption: {e}")
    key = Fernet.generate_key()
    fernet = Fernet(key)
    logger.warning("Using fallback encryption key")

def encrypt_data(data: Any) -> str:
    try:
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        compressed = zlib.compress(json_str.encode('utf-8'), level=9)
        encrypted = fernet.encrypt(compressed)
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        return base64.b64encode(json.dumps(data).encode()).decode()

def decrypt_data(encrypted_b64: str) -> Optional[Any]:
    try:
        encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
        decrypted = fernet.decrypt(encrypted)
        decompressed = zlib.decompress(decrypted)
        return json.loads(decompressed.decode('utf-8'))
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        try:
            encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
            decrypted = fernet.decrypt(encrypted)
            return json.loads(decrypted.decode('utf-8'))
        except:
            return None

def save_settings(settings_dict: dict) -> bool:
    try:
        encrypted_b64 = encrypt_data(settings_dict)
        with open(SETTINGS_FILE, "w", encoding='utf-8') as f:
            f.write(encrypted_b64)
        return True
    except Exception as e:
        logger.error(f"Failed to save settings: {e}")
        return False

def load_settings() -> dict:
    defaults = {
        "theme": "Dark",
        "temp_dir": tempfile.gettempdir(),
        "last_mode": "online",
        "auto_enhance": True,
        "default_lang": "English",
        "force_cancel_timeout": 30,
        "max_retry_attempts": 5,
        "confirm_cancel": True,
        "words_per_line": 5,
        "output_format": "SRT",
        "last_input_file": "",
        "last_output_folder": "",
        "window_geometry": None,
        "window_state": None,
        "window_width": 1280,
        "window_height": 800,
        "window_maximized": False,
        "font_family": "Segoe UI",
        "font_size": 14,
        "accent_color": "#4a6fa5",
        "recent_files": [],
        "show_tooltips": True,
        "ui_scale": "100%"
    }
    
    if not os.path.exists(SETTINGS_FILE):
        save_settings(defaults)
        return defaults
    
    try:
        with open(SETTINGS_FILE, "r", encoding='utf-8') as f:
            encrypted_b64 = f.read().strip()
        loaded = decrypt_data(encrypted_b64)
        if loaded:
            for key, value in loaded.items():
                if key in defaults:
                    defaults[key] = value
            return defaults
        else:
            save_settings(defaults)
            return defaults
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        save_settings(defaults)
        return defaults

def load_client_secrets() -> Optional[dict]:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
        encrypted_path = os.path.join(base, "client.notycapz")
        if os.path.exists(encrypted_path):
            try:
                with open(encrypted_path, "r", encoding='utf-8') as f:
                    encrypted_b64 = f.read().strip()
                decrypted = decrypt_data(encrypted_b64)
                if decrypted and "installed" in decrypted:
                    return decrypted
            except Exception as e:
                logger.error(f"Decryption failed: {str(e)}")
            
    if os.path.exists(CLIENT_ENCRYPTED):
        try:
            with open(CLIENT_ENCRYPTED, "r", encoding='utf-8') as f:
                encrypted_b64 = f.read().strip()
            decrypted = decrypt_data(encrypted_b64)
            if decrypted and "installed" in decrypted:
                return decrypted
        except Exception as e:
            logger.error(f"Failed to load client secrets: {e}")
            
    if os.path.exists(CLIENT_JSON):
        with open(CLIENT_JSON, "r", encoding='utf-8') as f:
            return json.load(f)

    return None

# ========================================
# Enums
# ========================================
class ProcessingMode(Enum):
    ONLINE = auto()

class Theme(Enum):
    SYSTEM = auto()
    LIGHT = auto()
    DARK = auto()

class SubtitleFormat(Enum):
    SRT = ".srt"
    ASS = ".ass"

# ========================================
# Translations - English Only
# ========================================
TRANSLATIONS = {
    'en': {
        'window_title': 'NotyCaption Pro - AI Caption Generator (Online)',
        'app_name': 'NotyCaption Pro',
        'app_subtitle': 'Online AI-Powered Caption Generator',
        'ready': 'Ready',
        'processing': 'Processing...',
        'canceled': 'Canceled',
        'completed': 'Completed',
        'failed': 'Failed',
        'edit_captions': '✏️ Edit Captions',
        'save_exit_edit': '💾 Save & Exit Edit',
        'settings': '⚙️ Settings',
        'login_google': '🔐 Google Login',
        'import_media': '📁 Import Media',
        'browse_output': '📂 Browse Output',
        'enhance_audio': '🎤 Extract Vocals',
        'enhancing': '🎤 Extracting Vocals in Colab...',
        'enhancement_complete': '🎤 Vocal Extraction Complete',
        'enhancement_success': 'Enhanced vocals saved to:\n{}',
        'play_pause': '▶️ Play / ⏸️ Pause',
        'playing': '⏸️ Playing...',
        'paused': '▶️ Play / ⏸️ Pause',
        'generate': '🚀 Generate Captions',
        'cancel': 'Cancel',
        'force_cancel': '⚠️ Force Cancel',
        'export': '📤 Export',
        'import': '📥 Import',
        'preview': '👁️ Preview',
        'processing_mode': 'Mode:',
        'language': 'Language:',
        'words_per_line': 'Words/Line:',
        'output_format': 'Format:',
        'output_folder': 'Output Folder:',
        'status': 'Status:',
        'colab_link': 'Colab Link:',
        'click_to_open': 'Click to open in browser',
        'online_mode': '☁️ Online (Google Colab)',
        'english_transcribe': '🇺🇸 English',
        'japanese_transcribe': '🇯🇵 Japanese',
        'chinese_transcribe': '🇨🇳 Chinese',
        'french_transcribe': '🇫🇷 French',
        'german_transcribe': '🇩🇪 German',
        'spanish_transcribe': '🇪🇸 Spanish',
        'russian_transcribe': '🇷🇺 Russian',
        'arabic_transcribe': '🇸🇦 Arabic',
        'hindi_transcribe': '🇮🇳 Hindi',
        'korean_transcribe': '🇰🇷 Korean',
        'portuguese_transcribe': '🇵🇹 Portuguese',
        'italian_transcribe': '🇮🇹 Italian',
        'dutch_transcribe': '🇳🇱 Dutch',
        'polish_transcribe': '🇵🇱 Polish',
        'turkish_transcribe': '🇹🇷 Turkish',
        'vietnamese_transcribe': '🇻🇳 Vietnamese',
        'thai_transcribe': '🇹🇭 Thai',
        'srt_format': '📄 SRT',
        'ass_format': '🎨 ASS',
        'import_complete': 'Import Complete',
        'import_success': 'Media imported successfully.',
        'generation_complete': 'Generation Complete',
        'generation_success': 'Captions saved:',
        'cancel_confirm': 'Confirm Cancel',
        'cancel_confirm_msg': 'Cancel current operation?',
        'force_cancel_confirm': '⚠️ Force cancel? This may cause instability.',
        'no_audio': 'No Audio',
        'no_audio_msg': 'No audio file loaded.',
        'no_media': 'No Media',
        'no_media_msg': 'Import media first.',
        'overwrite': 'Overwrite File?',
        'overwrite_msg': 'File exists:\n{}\nOverwrite?',
        'login_required': 'Please login with Google first.',
        'playback_error': 'Playback Error',
        'colab_timeout': 'Colab Timeout',
        'colab_timeout_msg': 'No result file found.',
        'network_error': 'Network Error',
        'settings_title': 'Settings',
        'general_tab': 'General',
        'paths_tab': 'Paths',
        'features_tab': 'Features',
        'visual_theme': 'Theme',
        'system_default': 'System',
        'light_mode': 'Light',
        'dark_mode': 'Dark',
        'ui_scaling': 'UI Scale',
        'scale_factor': 'Scale:',
        'temp_dir': 'Temp Directory',
        'browse_folder': 'Browse',
        'auto_features': 'Auto Features',
        'auto_enhance': 'Auto-Extract Vocals',
        'default_language': 'Default Language:',
        'default_wpl': 'Default Words/Line',
        'words': 'Words:',
        'default_format': 'Default Format',
        'format': 'Format:',
        'cancel_options': 'Cancel Options',
        'confirm_cancel': 'Confirm before cancel',
        'force_cancel_timeout': 'Force cancel after:',
        'seconds': 's',
        'max_retry': 'Max retries:',
        'apply_restart': 'Apply & Restart',
        'accent_color': 'Accent Color',
        'font_family': 'Font Family',
        'font_size': 'Font Size',
        'reset_defaults': 'Reset to Defaults',
        'reset_defaults_confirm': 'Reset all settings to default values?',
        'ui_options': 'UI Options',
        'show_tooltips': 'Show tooltips',
        'voice_enhancement': 'Voice Enhancement',
        'extract_vocals': 'Extract Vocals Only',
        'extract_vocals_desc': 'Remove background music, keep only voice',
    }
}

class Translator:
    def __init__(self, language='en'):
        self.language = language
        self.translations = TRANSLATIONS.get('en', TRANSLATIONS['en'])
        
    def tr(self, key: str) -> str:
        return self.translations.get(key, key)
    
    def set_language(self, language: str):
        self.language = language
        self.translations = TRANSLATIONS.get('en', TRANSLATIONS['en'])

_translator = Translator()

def tr(key: str) -> str:
    return _translator.tr(key)

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, relative_path)
    return full_path

# ========================================
# Windows 11 Style Dark Theme
# ========================================
WIN11_DARK_THEME = {
    'background_dark': '#0c0c0c',
    'background_medium': '#1c1c1c',
    'background_light': '#2a2a2a',
    'background_card': '#252526',
    'accent_primary': '#0078d4',
    'accent_secondary': '#8ab4f8',
    'accent_hover': '#1084d4',
    'text_primary': '#ffffff',
    'text_secondary': '#9ca3af',
    'text_accent': '#0078d4',
    'success': '#0f7b6e',
    'warning': '#d49a2a',
    'error': '#d14a4a',
    'info': '#0078d4',
    'border': '#3c3c3c',
    'border_light': '#404040',
    'hover': '#2d2d2d',
    'overlay': 'rgba(12, 12, 12, 0.95)',
    'card_border': '#2a2a2a',
    'button_bg': '#2c2c2c',
    'button_hover': '#3c3c3c',
    'button_pressed': '#1c1c1c'
}

LIGHT_THEME = {
    'background_dark': '#f3f3f3',
    'background_medium': '#ffffff',
    'background_light': '#e8e8e8',
    'background_card': '#fafafa',
    'accent_primary': '#0078d4',
    'accent_secondary': '#605e5c',
    'accent_hover': '#106ebe',
    'text_primary': '#1a1a1a',  # Dark text for light background
    'text_secondary': '#4a4a4a',  # Darker secondary text
    'text_accent': '#0078d4',
    'success': '#107c10',
    'warning': '#ff8c00',
    'error': '#d13438',
    'info': '#0078d4',
    'border': '#d1d1d1',
    'border_light': '#e0e0e0',
    'hover': '#e5e5e5',
    'overlay': 'rgba(255, 255, 255, 0.95)',
    'card_border': '#e5e5e5',
    'button_bg': '#f3f3f3',
    'button_hover': '#e5e5e5',
    'button_pressed': '#cccccc'
}

def get_stylesheet(theme: str, accent_color: Optional[str] = None, glow_intensity: int = 50) -> str:
    if theme == 'Light':
        colors = LIGHT_THEME
    else:
        colors = WIN11_DARK_THEME.copy()
        if accent_color:
            colors['accent_primary'] = accent_color
            colors['accent_hover'] = accent_color
    
    return f"""
/* Global Styles */
QMainWindow, QDialog {{
    background: {colors['background_dark']};
}}
QWidget {{
    color: {colors['text_primary']};
    font-family: 'Segoe UI Variable', 'Segoe UI', 'Inter', sans-serif;
    font-size: 13px;
}}

/* Title Bar */
#appTitle {{
    font-size: 28px;
    font-weight: 600;
    color: {colors['text_primary']};
    letter-spacing: -0.5px;
}}
QLabel {{
    color: {colors['text_secondary']};
    background: transparent;
}}

/* Group Box - Windows 11 Style */
QGroupBox {{
    font-weight: 500;
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 8px;
    background: transparent;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    color: {colors['text_secondary']};
}}

/* Push Buttons - Modern Style */
QPushButton {{
    background: {colors['button_bg']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 500;
    font-size: 12px;
    min-height: 28px;
}}
QPushButton:hover {{
    background: {colors['button_hover']};
    border-color: {colors['accent_primary']};
}}
QPushButton:pressed {{
    background: {colors['button_pressed']};
}}
QPushButton:disabled {{
    background: {colors['background_light']};
    color: {colors['text_secondary']};
    border-color: {colors['border']};
}}
QPushButton[type="primary"] {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {colors['accent_primary']}, stop:1 {colors['accent_hover']});
    color: white;
    border: none;
    font-weight: 600;
}}
QPushButton[type="primary"]:hover {{
    background: {colors['accent_hover']};
}}
QPushButton[type="danger"] {{
    background: {colors['error']};
    color: white;
    border: none;
}}
QPushButton[type="danger"]:hover {{
    background: #c42b1c;
}}

/* ComboBox */
QComboBox {{
    background: {colors['button_bg']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 7px 12px;
    min-height: 32px;
}}
QComboBox:hover {{
    border-color: {colors['accent_primary']};
}}
QComboBox:focus {{
    border-color: {colors['accent_primary']};
    outline: none;
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {colors['text_secondary']};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    selection-background-color: {colors['accent_primary']};
    padding: 4px;
}}

/* Line Edit, Text Edit, Spin Box */
QLineEdit, QTextEdit, QSpinBox {{
    background: {colors['button_bg']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 7px 12px;
    min-height: 32px;
}}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {{
    border: 2px solid {colors['accent_primary']};
    padding: 6px 11px;
}}
QTextEdit {{
    padding: 10px;
}}

/* Progress Bar */
QProgressBar {{
    background: {colors['background_light']};
    border: none;
    border-radius: 4px;
    text-align: center;
    color: {colors['text_primary']};
    font-weight: 500;
    height: 6px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors['accent_primary']}, stop:1 {colors['accent_secondary']});
    border-radius: 4px;
}}

/* Tab Widget */
QTabWidget::pane {{
    background: transparent;
    border: none;
    margin-top: 8px;
}}
QTabBar::tab {{
    background: transparent;
    color: {colors['text_secondary']};
    padding: 8px 20px;
    margin-right: 4px;
    border-bottom: 2px solid transparent;
}}
QTabBar::tab:selected {{
    color: {colors['accent_primary']};
    border-bottom: 2px solid {colors['accent_primary']};
    font-weight: 500;
}}
QTabBar::tab:hover {{
    color: {colors['text_primary']};
}}

/* Menu Bar */
QMenuBar {{
    background: {colors['background_dark']};
    color: {colors['text_primary']};
    border-bottom: 1px solid {colors['border']};
    padding: 4px 0;
}}
QMenuBar::item {{
    padding: 6px 12px;
    border-radius: 4px;
}}
QMenuBar::item:selected {{
    background: {colors['hover']};
}}
QMenu {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    padding: 8px;
}}
QMenu::item {{
    padding: 8px 32px 8px 16px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background: {colors['hover']};
}}
QMenu::separator {{
    height: 1px;
    background: {colors['border']};
    margin: 4px 8px;
}}

/* Scroll Bar */
QScrollBar:vertical {{
    background: {colors['background_medium']};
    width: 10px;
    border-radius: 5px;
}}
QScrollBar::handle:vertical {{
    background: {colors['border']};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {colors['accent_primary']};
}}
QScrollBar:horizontal {{
    background: {colors['background_medium']};
    height: 10px;
    border-radius: 5px;
}}
QScrollBar::handle:horizontal {{
    background: {colors['border']};
    border-radius: 5px;
    min-width: 30px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {colors['accent_primary']};
}}

/* Checkbox & Radio Button */
QCheckBox, QRadioButton {{
    color: {colors['text_primary']};
    spacing: 8px;
}}
QCheckBox::indicator, QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    background: {colors['button_bg']};
    border: 1px solid {colors['border']};
}}
QCheckBox::indicator:checked {{
    background: {colors['accent_primary']};
    border-color: {colors['accent_primary']};
}}
QRadioButton::indicator {{
    border-radius: 9px;
}}
QRadioButton::indicator:checked {{
    background: {colors['accent_primary']};
    border: 4px solid {colors['button_bg']};
}}

/* Slider */
QSlider::groove:horizontal {{
    background: {colors['background_light']};
    height: 4px;
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {colors['accent_primary']};
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}}
QSlider::sub-page:horizontal {{
    background: {colors['accent_primary']};
    border-radius: 2px;
}}

/* Tool Tips */
QToolTip {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 6px 12px;
}}

/* Status Bar */
QStatusBar {{
    background: {colors['background_dark']};
    color: {colors['text_secondary']};
    border-top: 1px solid {colors['border']};
    padding: 4px 12px;
}}

/* Glass Card Widget */
GlassCardWidget {{
    background: rgba(37, 37, 38, 0.9);
    border: 1px solid {colors['card_border']};
    border-radius: 12px;
    padding: 16px;
}}
QFrame[frameShape="4"] {{
    background: rgba(37, 37, 38, 0.7);
    border: 1px solid {colors['border']};
    border-radius: 10px;
}}

/* Message Box */
QMessageBox {{
    background: {colors['background_medium']};
}}
QMessageBox QLabel {{
    color: {colors['text_primary']};
}}

/* List Widget */
QListWidget {{
    background: {colors['button_bg']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    padding: 4px;
}}
QListWidget::item {{
    padding: 8px;
    border-radius: 4px;
}}
QListWidget::item:selected {{
    background: {colors['hover']};
}}
"""

# ========================================
# Animated Button and UI Components
# ========================================
class GlowButton(QPushButton):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(8)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.shadow.setOffset(0, 1)
        self.setGraphicsEffect(self.shadow)
        
    def eventFilter(self, obj, event):
        if event.type() == event.Enter:
            self.shadow.setBlurRadius(12)
            self.shadow.setColor(QColor(74, 144, 226, 80))
        elif event.type() == event.Leave:
            self.shadow.setBlurRadius(8)
            self.shadow.setColor(QColor(0, 0, 0, 60))
        return super().eventFilter(obj, event)
        
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

class GlassCardWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(f"""
            GlassCardWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(30, 30, 30, 0.8),
                    stop:1 rgba(20, 20, 20, 0.9));
                border: 1px solid {WIN11_DARK_THEME['border']};
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 50))
        self.shadow.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow)

class PreviewWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(300)
        self.setStyleSheet("""
            PreviewWidget {
                background: #1a1a1a;
                border: 2px solid #333;
                border-radius: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.video_container = QFrame()
        self.video_container.setStyleSheet("""
            QFrame {
                background: #0a0a0a;
                border: 1px solid #333;
                border-radius: 10px;
            }
        """)
        video_layout = QVBoxLayout()
        self.video_container.setLayout(video_layout)
        
        self.video_label = QLabel("No video loaded")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("color: #666; font-size: 16px;")
        video_layout.addWidget(self.video_label)
        
        self.video_widget = QVideoWidget()
        self.video_widget.hide()
        video_layout.addWidget(self.video_widget)
        
        layout.addWidget(self.video_container, stretch=1)
        
        subtitle_frame = QFrame()
        subtitle_frame.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 30, 0.9);
                border: 1px solid #333;
                border-radius: 10px;
                margin-top: 10px;
            }
        """)
        subtitle_layout = QVBoxLayout()
        subtitle_frame.setLayout(subtitle_layout)
        
        subtitle_header = QHBoxLayout()
        subtitle_header.addWidget(QLabel("📝 Subtitle Preview"))
        subtitle_header.addStretch()
        
        self.preview_timer = QLabel("00:00 / 00:00")
        self.preview_timer.setStyleSheet("color: #4a6fa5; font-family: monospace;")
        subtitle_header.addWidget(self.preview_timer)
        
        subtitle_layout.addLayout(subtitle_header)
        
        self.subtitle_display = QTextEdit()
        self.subtitle_display.setReadOnly(True)
        self.subtitle_display.setMaximumHeight(100)
        self.subtitle_display.setStyleSheet("""
            QTextEdit {
                background: #2a2a2a;
                color: #ffffff;
                border: 1px solid #4a6fa5;
                border-radius: 8px;
                font-size: 14px;
                padding: 10px;
            }
        """)
        subtitle_layout.addWidget(self.subtitle_display)
        
        layout.addWidget(subtitle_frame)
        
        control_bar = QFrame()
        control_bar.setStyleSheet("""
            QFrame {
                background: #2a2a2a;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        control_layout = QHBoxLayout()
        control_bar.setLayout(control_layout)
        
        self.play_btn = QPushButton("▶")
        self.play_btn.setFixedSize(40, 30)
        self.play_btn.clicked.connect(self.toggle_playback)
        control_layout.addWidget(self.play_btn)
        
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.sliderMoved.connect(self.seek_position)
        control_layout.addWidget(self.position_slider)
        
        self.time_label = QLabel("00:00/00:00")
        control_layout.addWidget(self.time_label)
        
        self.volume_btn = QPushButton("🔊")
        self.volume_btn.setFixedSize(40, 30)
        self.volume_btn.clicked.connect(self.toggle_mute)
        control_layout.addWidget(self.volume_btn)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.change_volume)
        control_layout.addWidget(self.volume_slider)
        
        layout.addWidget(control_bar)
        
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.stateChanged.connect(self.update_play_state)
        
        self.duration = 0        
        self.muted = False
        self.subtitles = []
        
    def set_media(self, file_path: str):
        if os.path.exists(file_path):
            url = QUrl.fromLocalFile(file_path)
            self.player.setMedia(QMediaContent(url))
            
            if file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                self.video_widget.show()
                self.video_label.hide()
            else:
                self.video_widget.hide()
                self.video_label.show()
                self.video_label.setText(f"Audio: {os.path.basename(file_path)}")
                
            self.player.play()
            
    def set_subtitles(self, subtitles: List[dict]):
        self.subtitles = subtitles
        
    def update_position(self, position: int):
        self.position_slider.setValue(position)
        
        current = self.format_time(position)
        total = self.format_time(self.duration)
        self.time_label.setText(f"{current}/{total}")
        self.preview_timer.setText(f"{current} / {total}")
        
        if self.subtitles:
            sec = position / 1000.0
            for sub in self.subtitles:
                start = sub["start"].total_seconds() if isinstance(sub["start"], timedelta) else sub["start"]
                end = sub["end"].total_seconds() if isinstance(sub["end"], timedelta) else sub["end"]
                if start <= sec <= end:
                    self.subtitle_display.setText(sub["text"])
                    break
                    
    def update_duration(self, duration: int):
        self.duration = duration
        self.position_slider.setRange(0, duration)
        
    def update_play_state(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_btn.setText("⏸")
        else:
            self.play_btn.setText("▶")
            
    def toggle_playback(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
            
    def seek_position(self, position: int):
        self.player.setPosition(position)
        
    def toggle_mute(self):
        self.muted = not self.muted
        self.player.setMuted(self.muted)
        self.volume_btn.setText("🔇" if self.muted else "🔊")
        
    def change_volume(self, value: int):
        self.player.setVolume(value)
        if value == 0:
            self.volume_btn.setText("🔇")
        elif value < 30:
            self.volume_btn.setText("🔈")
        elif value < 70:
            self.volume_btn.setText("🔉")
        else:
            self.volume_btn.setText("🔊")
            
    def format_time(self, ms: int) -> str:
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
# ========================================
# Settings Dialog
# ========================================
class SettingsDialog(QDialog):
    settingsChanged = pyqtSignal(dict)

    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr('settings_title'))
        self.resize(650, 750)
        self.setMinimumSize(550, 650)
        self.current_settings = current_settings
        
        self.setStyleSheet(get_stylesheet(
            current_settings.get('theme', 'Dark'),
            current_settings.get('accent_color', DARK_THEME['accent_primary'])
        ))
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # General Tab
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        general_tab.setLayout(general_layout)

        th_gb = QGroupBox(tr('visual_theme'))
        th_lay = QVBoxLayout()
        self.rb_win = QRadioButton(tr('system_default'))
        self.rb_light = QRadioButton(tr('light_mode'))
        self.rb_dark = QRadioButton(tr('dark_mode'))
        
        th_lay.addWidget(self.rb_win)
        th_lay.addWidget(self.rb_light)
        th_lay.addWidget(self.rb_dark)

        th = current_settings.get("theme", "Dark")
        if th == "Windows Default": 
            self.rb_win.setChecked(True)
        elif th == "Light": 
            self.rb_light.setChecked(True)
        else: 
            self.rb_dark.setChecked(True)

        th_gb.setLayout(th_lay)
        general_layout.addWidget(th_gb)

        sc_gb = QGroupBox(tr('ui_scaling'))
        sc_lay = QHBoxLayout()
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["75%", "87%", "100%", "125%", "150%", "175%", "200%"])
        self.scale_combo.setCurrentText(current_settings.get("ui_scale", "100%"))
        sc_lay.addWidget(QLabel(tr('scale_factor')))
        sc_lay.addWidget(self.scale_combo)
        sc_lay.addStretch()
        sc_gb.setLayout(sc_lay)
        general_layout.addWidget(sc_gb)
        
        general_layout.addStretch()
        tabs.addTab(general_tab, tr('general_tab'))

        # Features Tab
        features_tab = QWidget()
        features_layout = QVBoxLayout()
        features_tab.setLayout(features_layout)

        auto_gb = QGroupBox(tr('auto_features'))
        auto_lay = QVBoxLayout()
        self.cb_auto_enhance = QCheckBox(tr('auto_enhance'))
        self.cb_auto_enhance.setChecked(current_settings.get("auto_enhance", True))
        auto_lay.addWidget(self.cb_auto_enhance)
        auto_gb.setLayout(auto_lay)
        features_layout.addWidget(auto_gb)

        wpl_gb = QGroupBox(tr('default_wpl'))
        wpl_lay = QHBoxLayout()
        self.wpl_spin = QSpinBox()
        self.wpl_spin.setRange(1, 20)
        self.wpl_spin.setValue(current_settings.get("words_per_line", 5))
        wpl_lay.addWidget(QLabel(tr('words')))
        wpl_lay.addWidget(self.wpl_spin)
        wpl_lay.addStretch()
        wpl_gb.setLayout(wpl_lay)
        features_layout.addWidget(wpl_gb)

        fmt_gb = QGroupBox(tr('default_format'))
        fmt_lay = QHBoxLayout()
        self.fmt_combo = QComboBox()
        self.fmt_combo.addItems([tr('srt_format'), tr('ass_format')])
        self.fmt_combo.setCurrentText(current_settings.get("output_format", tr('srt_format')))
        fmt_lay.addWidget(QLabel(tr('format')))
        fmt_lay.addWidget(self.fmt_combo)
        fmt_lay.addStretch()
        fmt_gb.setLayout(fmt_lay)
        features_layout.addWidget(fmt_gb)

        lang_gb = QGroupBox(tr('default_language'))
        lang_lay = QVBoxLayout()
        self.lang_combo_settings = QComboBox()
        languages = [
            tr('english_transcribe'), tr('japanese_transcribe'), tr('chinese_transcribe'),
            tr('french_transcribe'), tr('german_transcribe'), tr('spanish_transcribe'),
            tr('russian_transcribe'), tr('arabic_transcribe'), tr('hindi_transcribe'),
            tr('korean_transcribe'), tr('portuguese_transcribe'), tr('italian_transcribe'),
            tr('dutch_transcribe'), tr('polish_transcribe'), tr('turkish_transcribe'),
            tr('vietnamese_transcribe'), tr('thai_transcribe')
        ]
        self.lang_combo_settings.addItems(languages)
        default_lang = current_settings.get("default_lang", tr('english_transcribe'))
        if default_lang in languages:
            self.lang_combo_settings.setCurrentText(default_lang)
        lang_lay.addWidget(self.lang_combo_settings)
        lang_gb.setLayout(lang_lay)
        features_layout.addWidget(lang_gb)
        
        features_layout.addStretch()
        tabs.addTab(features_tab, tr('features_tab'))

        # UI Options Tab
        ui_tab = QWidget()
        ui_layout = QVBoxLayout()
        ui_tab.setLayout(ui_layout)

        ui_gb = QGroupBox(tr('ui_options'))
        ui_inner_layout = QVBoxLayout()
        
        self.cb_show_tooltips = QCheckBox(tr('show_tooltips'))
        self.cb_show_tooltips.setChecked(current_settings.get("show_tooltips", True))
        ui_inner_layout.addWidget(self.cb_show_tooltips)
        
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel(tr('font_family')))
        self.font_combo = QComboBox()
        self.font_combo.addItems(['Segoe UI', 'Arial', 'Helvetica', 'Verdana', 'Tahoma'])
        self.font_combo.setCurrentText(current_settings.get('font_family', 'Segoe UI'))
        font_layout.addWidget(self.font_combo)
        ui_inner_layout.addLayout(font_layout)
        
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel(tr('font_size')))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 20)
        self.font_size_spin.setValue(current_settings.get('font_size', 14))
        font_size_layout.addWidget(self.font_size_spin)
        ui_inner_layout.addLayout(font_size_layout)
        
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel(tr('accent_color')))
        self.accent_color_btn = QPushButton()
        self.accent_color_btn.setFixedSize(50, 25)
        self.accent_color_btn.clicked.connect(self.choose_accent_color)
        self.current_color = QColor(current_settings.get('accent_color', DARK_THEME['accent_primary']))
        self.update_color_button()
        color_layout.addWidget(self.accent_color_btn)
        color_layout.addStretch()
        ui_inner_layout.addLayout(color_layout)
        
        ui_gb.setLayout(ui_inner_layout)
        ui_layout.addWidget(ui_gb)
        
        reset_btn = QPushButton(tr('reset_defaults'))
        reset_btn.clicked.connect(self.reset_defaults)
        ui_layout.addWidget(reset_btn)
        
        ui_layout.addStretch()
        tabs.addTab(ui_tab, tr('ui_options'))

        # Cancel Options Tab
        cancel_tab = QWidget()
        cancel_layout = QVBoxLayout()
        cancel_tab.setLayout(cancel_layout)

        cancel_gb = QGroupBox(tr('cancel_options'))
        cancel_inner_layout = QVBoxLayout()
        
        self.cb_confirm_cancel = QCheckBox(tr('confirm_cancel'))
        self.cb_confirm_cancel.setChecked(current_settings.get("confirm_cancel", True))
        cancel_inner_layout.addWidget(self.cb_confirm_cancel)
        
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel(tr('force_cancel_timeout')))
        self.force_timeout_spin = QSpinBox()
        self.force_timeout_spin.setRange(10, 120)
        self.force_timeout_spin.setSuffix(tr('seconds'))
        self.force_timeout_spin.setValue(current_settings.get("force_cancel_timeout", 30))
        timeout_layout.addWidget(self.force_timeout_spin)
        timeout_layout.addStretch()
        cancel_inner_layout.addLayout(timeout_layout)
        
        retry_layout = QHBoxLayout()
        retry_layout.addWidget(QLabel(tr('max_retry')))
        self.retry_spin = QSpinBox()
        self.retry_spin.setRange(1, 20)
        self.retry_spin.setValue(current_settings.get("max_retry_attempts", 5))
        retry_layout.addWidget(self.retry_spin)
        retry_layout.addStretch()
        cancel_inner_layout.addLayout(retry_layout)
        
        cancel_gb.setLayout(cancel_inner_layout)
        cancel_layout.addWidget(cancel_gb)
        cancel_layout.addStretch()
        tabs.addTab(cancel_tab, tr('cancel_options'))

        # Buttons
        btn_layout = QHBoxLayout()
        apply_btn = QPushButton(tr('apply_restart'))
        apply_btn.clicked.connect(self.apply_close)
        cancel_btn = QPushButton(tr('cancel'))
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(cancel_btn)
        main_layout.addLayout(btn_layout)

    def update_color_button(self):
        self.accent_color_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.current_color.name()};
                border: 1px solid white;
                border-radius: 3px;
            }}
        """)

    def choose_accent_color(self):
        color = QColorDialog.getColor(self.current_color, self, tr('accent_color'))
        if color.isValid():
            self.current_color = color
            self.update_color_button()

    def reset_defaults(self):
        reply = QMessageBox.question(self, tr('reset_defaults'), tr('reset_defaults_confirm'),
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.rb_dark.setChecked(True)
            self.scale_combo.setCurrentText("100%")
            self.cb_auto_enhance.setChecked(True)
            self.wpl_spin.setValue(5)
            self.fmt_combo.setCurrentText(tr('srt_format'))
            self.lang_combo_settings.setCurrentText(tr('english_transcribe'))
            self.cb_confirm_cancel.setChecked(True)
            self.force_timeout_spin.setValue(30)
            self.retry_spin.setValue(5)
            self.cb_show_tooltips.setChecked(True)
            self.font_combo.setCurrentText("Segoe UI")
            self.font_size_spin.setValue(14)
            self.current_color = QColor(DARK_THEME['accent_primary'])
            self.update_color_button()

    def apply_close(self):
        new_settings = {
            "ui_scale": self.scale_combo.currentText(),
            "theme": "Windows Default" if self.rb_win.isChecked() else
                    "Light" if self.rb_light.isChecked() else "Dark",
            "auto_enhance": self.cb_auto_enhance.isChecked(),
            "default_lang": self.lang_combo_settings.currentText(),
            "force_cancel_timeout": self.force_timeout_spin.value(),
            "max_retry_attempts": self.retry_spin.value(),
            "confirm_cancel": self.cb_confirm_cancel.isChecked(),
            "show_tooltips": self.cb_show_tooltips.isChecked(),
            "words_per_line": self.wpl_spin.value(),
            "output_format": self.fmt_combo.currentText(),
            "last_input_file": self.current_settings.get("last_input_file", ""),
            "last_output_folder": self.current_settings.get("last_output_folder", ""),
            "window_geometry": self.current_settings.get("window_geometry"),
            "window_state": self.current_settings.get("window_state"),
            "window_width": self.current_settings.get("window_width", DEFAULT_WINDOW_WIDTH),
            "window_height": self.current_settings.get("window_height", DEFAULT_WINDOW_HEIGHT),
            "window_maximized": self.current_settings.get("window_maximized", False),
            "accent_color": self.current_color.name(),
            "font_family": self.font_combo.currentText(),
            "font_size": self.font_size_spin.value(),
            "recent_files": self.current_settings.get("recent_files", [])
        }
        save_settings(new_settings)
        _translator.set_language('en')
        
        # Apply settings without restart
        self.settingsChanged.emit(new_settings)
        
        # Apply theme immediately
        if self.parent_window:
            self.parent_window.apply_theme()
            self.parent_window.setup_tooltips()
            self.parent_window.lang_combo.setCurrentText(new_settings.get("default_lang", tr('english_transcribe')))
            self.parent_window.words_spin.setValue(new_settings.get("words_per_line", 5))
            self.parent_window.format_combo.setCurrentText(new_settings.get("output_format", tr('srt_format')))
            if hasattr(self.parent_window, 'online_handler'):
                self.parent_window.online_handler.max_retry_attempts = new_settings.get("max_retry_attempts", 5)
        
        self.accept()

# ========================================
# Single Instance Check
# ========================================
class SingleInstance:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.already_exists = False
        try:
            self.sock.bind(('127.0.0.1', 65432))
            self.sock.listen(1)
            logger.info("Single instance lock acquired successfully")
        except socket.error:
            self.already_exists = True
            logger.warning("Another instance may be running")

    def is_already_running(self):
        return self.already_exists

    def __del__(self):
        if not self.already_exists:
            try:
                self.sock.close()
            except:
                pass


# ========================================
# Audio Extractor Thread
# ========================================
class AudioExtractorThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str, bool)
    error = pyqtSignal(str)
    
    def __init__(self, file_path, temp_dir, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.temp_dir = temp_dir
        self._is_canceled = False
        self._stop_event = threading.Event()
        
    def cancel(self):
        self._is_canceled = True
        self._stop_event.set()
        
    def is_canceled(self):
        return self._is_canceled or self._stop_event.is_set()
    
    def run(self):
        try:
            self.progress.emit(10, "Extracting audio...")
            
            if self.is_canceled():
                self.error.emit("Operation canceled")
                return
            
            temp_name = os.path.splitext(os.path.basename(self.file_path))[0] + ".wav"
            output_path = os.path.join(self.temp_dir, temp_name)
            
            if self.file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv')):
                clip = VideoFileClip(self.file_path)
                if clip.audio is not None:
                    clip.audio.write_audiofile(output_path, codec='pcm_s16le', logger=None, verbose=False)
                    clip.close()
                else:
                    raise Exception("No audio track found in video")
            else:
                audio_clip = AudioFileClip(self.file_path)
                audio_clip.write_audiofile(output_path, codec='pcm_s16le', logger=None, verbose=False)
                audio_clip.close()
            
            if self.is_canceled():
                if os.path.exists(output_path):
                    os.remove(output_path)
                self.error.emit("Operation canceled")
                return
            
            self.progress.emit(100, "Audio extraction complete")
            self.finished.emit(output_path, True)
            
        except Exception as e:
            self.error.emit(str(e))


# ========================================
# Online Handler - Handles Google Drive and Colab (Both Enhancement and Transcription)
# ========================================
class OnlineHandler:
    def __init__(self, parent_window):
        self.parent = parent_window
        self.service = None
        self.poll_timer = QTimer(parent_window)
        self.cleanup_timer = QTimer(parent_window)
        self.retry_timer = QTimer(parent_window)
        self.poll_audio_id = None
        self.poll_notebook_id = None
        self.poll_output_name = None
        self.poll_local_out = None
        self.poll_attempts = 0
        self.max_poll_attempts = 180
        self.retry_attempts = 0
        self.max_retry_attempts = parent_window.settings.get("max_retry_attempts", 5)
        self._canceled = False
        self._cancel_requested = False
        self._stop_event = threading.Event()
        self._current_colab_url = None
        self._online_status = "idle"
        self._download_start_time = None
        self._downloaded_bytes = 0
        self._current_operation = None  # 'enhance' or 'transcribe'
        
        self.cleanup_timer.timeout.connect(self.cleanup_old_drive_files)
        self.cleanup_timer.start(3600000)
        self.retry_timer.timeout.connect(self.retry_polling)
        self.retry_timer.setSingleShot(True)

    def cancel_operation(self):
        self._cancel_requested = True
        self._canceled = True
        self._stop_event.set()
        if self.poll_timer.isActive():
            self.poll_timer.stop()
        if self.retry_timer.isActive():
            self.retry_timer.stop()
        self.cleanup_current_operation()
        self.parent.statusBar().showMessage(tr('canceled'), 5000)

    def force_cancel_operation(self):
        self._cancel_requested = True
        self._canceled = True
        self._stop_event.set()
        if self.poll_timer.isActive():
            self.poll_timer.stop()
        if self.retry_timer.isActive():
            self.retry_timer.stop()
        self.cleanup_current_operation()
        self.parent.update_notebook_url_display(None)
        self.parent.statusBar().showMessage(tr('force_canceled'), 5000)

    def cleanup_current_operation(self):
        if not self.service:
            return
        try:
            if self.poll_audio_id:
                self.service.files().delete(fileId=self.poll_audio_id).execute()
                self.poll_audio_id = None
            if self.poll_notebook_id:
                self.service.files().delete(fileId=self.poll_notebook_id).execute()
                self.poll_notebook_id = None
        except Exception as e:
            logger.warning(f"Cleanup error: {e}")

    def cleanup_old_drive_files(self):
        if not self.service:
            return
        try:
            uploads_id = self.get_or_create_folder("uploads")
            one_day_ago = (datetime.now() - timedelta(days=1)).isoformat() + 'Z'
            query = f"'{uploads_id}' in parents and createdTime < '{one_day_ago}' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            for file in results.get("files", []):
                self.service.files().delete(fileId=file["id"]).execute()
        except Exception as e:
            logger.warning(f"Cleanup error: {e}")

    def retry_polling(self):
        if self._canceled or self._cancel_requested:
            return
        self.retry_attempts += 1
        if self.retry_attempts <= self.max_retry_attempts:
            self.poll_for_output()
        else:
            self.parent.show_force_cancel_option(True)

    def handle_enhancement(self, audio_path, base, out_path):
        """Handle vocal enhancement via Colab"""
        self._current_operation = 'enhance'
        return self._handle_online_operation(audio_path, base, out_path, is_enhancement=True)

    def handle_transcription(self, audio_path, lang_code, task, wpl, fmt, base, out_path):
        """Handle caption generation via Colab"""
        self._current_operation = 'transcribe'
        return self._handle_online_operation(audio_path, base, out_path, is_enhancement=False,
                                              lang_code=lang_code, task=task, wpl=wpl, fmt=fmt)

    def _handle_online_operation(self, audio_path, base, out_path, is_enhancement=False,
                                  lang_code='en', task='transcribe', wpl=5, fmt='.srt'):
        self._canceled = False
        self._cancel_requested = False
        self._stop_event.clear()
        self.retry_attempts = 0
        
        if not self.service:
            QMessageBox.warning(self.parent, tr('error'), tr('login_required'))
            return False

        try:
            if is_enhancement:
                self.poll_output_name = f"{base}_vocals.wav"
            else:
                self.poll_output_name = f"{base}_captions{fmt}"
            
            # Check for existing file
            query = f"name='{self.poll_output_name}' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()

            # Delete old notebook
            query = "name='NotyCaption_Generator.ipynb' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()

            # Upload audio
            uploads_id = self.get_or_create_folder("uploads")
            audio_filename = os.path.basename(audio_path)
            audio_id = self.upload_file(audio_path, audio_filename, uploads_id)
            self.poll_audio_id = audio_id

            # Generate and upload notebook based on operation type
            notebook_content = self.generate_notebook_content(
                audio_filename, wpl, fmt if not is_enhancement else '.srt',
                self.poll_output_name, lang_code if not is_enhancement else 'en',
                task if not is_enhancement else 'transcribe',
                is_enhancement=is_enhancement
            )
            temp_ipynb = os.path.join(tempfile.gettempdir(), "NotyCaption_Generator.ipynb")
            with open(temp_ipynb, "w", encoding="utf-8") as f:
                json.dump(notebook_content, f, indent=2)
            notebook_id = self.upload_file(temp_ipynb, "NotyCaption_Generator.ipynb")
            os.remove(temp_ipynb)
            self.poll_notebook_id = notebook_id

            # Open Colab
            colab_url = f"https://colab.research.google.com/drive/{notebook_id}"
            self._current_colab_url = colab_url
            webbrowser.open(colab_url)
            self.parent.update_notebook_url_display(colab_url)
            
            self.poll_local_out = out_path
            
            # Start polling
            self.poll_timer.stop()
            try:
                self.poll_timer.timeout.disconnect()
            except TypeError:
                pass
            self.poll_timer.timeout.connect(self.poll_for_output)
            self.poll_timer.start(8000)
            return True

        except Exception as e:
            logger.error(f"Online operation failed: {e}")
            self.cleanup_current_operation()
            QMessageBox.critical(self.parent, tr('failed'), str(e))
            return False

    def get_or_create_folder(self, name):
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])
        if files:
            return files[0]["id"]
        metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        folder = self.service.files().create(body=metadata, fields="id").execute()
        return folder.get("id")

    def upload_file(self, filepath, filename, parent_id=None):
        metadata = {"name": filename}
        if parent_id:
            metadata["parents"] = [parent_id]
        media = MediaFileUpload(filepath, resumable=True)
        file = self.service.files().create(body=metadata, media_body=media, fields="id").execute()
        return file.get("id")

    def generate_notebook_content(self, audio_filename, words_per_line, fmt, output_name, 
                                   lang_code='en', task='transcribe', is_enhancement=False):
        def code_cell(lines):
            return {
                "cell_type": "code", "metadata": {}, "execution_count": None,
                "outputs": [], "source": lines
            }

        if is_enhancement:
            # Notebook for vocal enhancement only
            notebook = {
                "nbformat": 4, "nbformat_minor": 0,
                "metadata": {
                    "kernelspec": {"name": "python3", "display_name": "Python 3"},
                    "language_info": {"name": "python"}, "accelerator": "GPU"
                },
                "cells": [
                    code_cell([
                        "%%capture\n!apt update -qq\n!apt install -y ffmpeg -qq\n"
                        "!pip install -q spleeter pydub librosa soundfile\n"
                        "import os, shutil, librosa, soundfile as sf\n"
                        "from pydub import AudioSegment\n"
                        "print('Dependencies installed')"
                    ]),
                    code_cell([
                        "from google.colab import drive\n"
                        "drive.mount('/content/drive', force_remount=True)\n"
                        "print('Drive mounted')"
                    ]),
                    code_cell([
                        f"audio_path = '/content/drive/My Drive/uploads/{audio_filename}'\n"
                        "if not os.path.exists(audio_path):\n"
                        f"    raise FileNotFoundError(f'Audio not found at {{audio_path}}')\n"
                        "print('Audio verified')"
                    ]),
                    code_cell([
                        "from spleeter.separator import Separator\n"
                        "print('Loading Spleeter model...')\n"
                        "separator = Separator('spleeter:2stems')\n"
                        "print('Model loaded')"
                    ]),
                    code_cell([
                        f"output_dir = '/content/vocals_output'\n"
                        "os.makedirs(output_dir, exist_ok=True)\n"
                        "separator.separate_to_file(audio_path, output_dir)\n"
                        "print('Vocal separation complete')"
                    ]),
                    code_cell([
                        f"vocals_path = os.path.join(output_dir, os.path.basename(audio_path).replace('.wav', '_vocals.wav'))\n"
                        f"output_path = '/content/drive/My Drive/{output_name}'\n"
                        "if os.path.exists(vocals_path):\n"
                        "    shutil.copy(vocals_path, output_path)\n"
                        "    print(f'Vocals saved to: {output_path}')\n"
                        "else:\n"
                        "    print('Error: Vocals file not found')\n"
                        "    raise Exception('Vocal separation failed')"
                    ]),
                    code_cell([
                        "try:\n"
                        "    if os.path.exists(audio_path): os.remove(audio_path)\n"
                        "    if os.path.exists(output_dir): shutil.rmtree(output_dir)\n"
                        "    notebook_path = '/content/drive/My Drive/NotyCaption_Generator.ipynb'\n"
                        "    if os.path.exists(notebook_path): os.remove(notebook_path)\n"
                        "    print('Cleanup complete')\n"
                        "except: pass"
                    ])
                ]
            }
        else:
            # Notebook for transcription with optional enhancement
            notebook = {
                "nbformat": 4, "nbformat_minor": 0,
                "metadata": {
                    "kernelspec": {"name": "python3", "display_name": "Python 3"},
                    "language_info": {"name": "python"}, "accelerator": "GPU"
                },
                "cells": [
                    code_cell([
                        "%%capture\n!apt update -qq\n!apt install -y ffmpeg -qq\n"
                        "!pip install -q openai-whisper pysrt pysubs2\n"
                        "import os, shutil, whisper, pysrt, pysubs2\n"
                        "from datetime import timedelta\nprint('Dependencies installed')"
                    ]),
                    code_cell([
                        "from google.colab import drive\n"
                        "drive.mount('/content/drive', force_remount=True)\n"
                        "print('Drive mounted')"
                    ]),
                    code_cell([
                        f"audio_path = '/content/drive/My Drive/uploads/{audio_filename}'\n"
                        "if not os.path.exists(audio_path):\n"
                        f"    raise FileNotFoundError(f'Audio not found at {{audio_path}}')\n"
                        "print('Audio verified')"
                    ]),
                    code_cell([
                        "model_name = 'large-v3-turbo'\n"
                        "model = whisper.load_model('large-v3-turbo')\n"
                        "print('Model loaded')"
                    ]),
                    code_cell([
                        f"result = model.transcribe(audio_path, language='{lang_code}', "
                        f"task='{task}', word_timestamps=True)\n"
                        "print('Transcription complete')"
                    ]),
                    code_cell([
                        f"subtitles = []\nidx = 1\nwpl = {words_per_line}\n"
                        "for seg in result['segments']:\n"
                        "    words = seg.get('words', [])\n"
                        "    if not words: continue\n"
                        f"    for i in range(0, len(words), wpl):\n"
                        "        chunk = words[i:i+wpl]\n"
                        "        if not chunk: continue\n"
                        "        text = ' '.join([w['word'].strip() for w in chunk])\n"
                        "        start = chunk[0]['start']\n"
                        "        end = chunk[-1]['end']\n"
                        "        subtitles.append((idx, start, end, text))\n"
                        "        idx += 1\n"
                        "print(f'Generated {len(subtitles)} lines')"
                    ]),
                    code_cell([
                        f"fmt = '{fmt}'\noutput_path = '/content/drive/My Drive/{output_name}'\n"
                        "if fmt == '.srt':\n"
                        "    srt = pysrt.SubRipFile()\n"
                        "    for idx, start, end, text in subtitles:\n"
                        "        item = pysrt.SubRipItem(index=idx,\n"
                        "            start=pysrt.SubRipTime(milliseconds=int(start*1000)),\n"
                        "            end=pysrt.SubRipTime(milliseconds=int(end*1000)),\n"
                        "            text=text)\n"
                        "        srt.append(item)\n"
                        "    srt.save(output_path)\n"
                        "else:\n"
                        "    ass = pysubs2.SSAFile()\n"
                        "    ass.styles['Default'] = pysubs2.SSAStyle()\n"
                        "    for idx, start, end, text in subtitles:\n"
                        "        ass.events.append(pysubs2.SSAEvent(\n"
                        "            start=int(start*1000), end=int(end*1000), text=text))\n"
                        "    ass.save(output_path)\n"
                        "print('Processing complete')"
                    ]),
                    code_cell([
                        "try:\n    if os.path.exists(audio_path): os.remove(audio_path)\n"
                        "    notebook_path = '/content/drive/My Drive/NotyCaption_Generator.ipynb'\n"
                        "    if os.path.exists(notebook_path): os.remove(notebook_path)\n"
                        "    print('Cleanup complete')\nexcept: pass"
                    ])
                ]
            }
        return notebook

    def poll_for_output(self):
        if not self.poll_output_name or self._canceled or self._cancel_requested:
            self.poll_timer.stop()
            return

        self.poll_attempts += 1
        if self.poll_attempts > self.max_poll_attempts:
            self.poll_timer.stop()
            self.parent.is_processing = False
            self.parent.freeze_ui(False)
            self.parent.reset_progress_bars()
            self.cleanup_current_operation()
            QMessageBox.warning(self.parent, tr('colab_timeout'), tr('colab_timeout_msg'))
            return

        query = f"name='{self.poll_output_name}' and trashed=false"
        try:
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            files = results.get("files", [])
            if files:
                file_id = files[0]["id"]
                
                with open(self.poll_local_out, "wb") as f:
                    request = self.service.files().get_media(fileId=file_id)
                    downloader = MediaIoBaseDownload(f, request)
                    done = False
                    while not done:
                        if self._canceled or self._cancel_requested:
                            return
                        status, done = downloader.next_chunk()
                        if status:
                            progress_pct = int(status.progress() * 100)
                            self.parent.progress_update(progress_pct)
                
                if self._current_operation == 'enhance':
                    self.parent.on_enhancement_downloaded(self.poll_local_out)
                else:
                    self.parent.load_downloaded_subtitles(self.poll_local_out)
                
                self.service.files().delete(fileId=file_id).execute()
                self.poll_timer.stop()
                self.parent.is_processing = False
                self.parent.freeze_ui(False)
                self.parent.reset_progress_bars()
                self.parent.update_notebook_url_display(None)
                
                if self._current_operation == 'enhance':
                    QMessageBox.information(self.parent, tr('enhancement_complete'), 
                                           tr('enhancement_success').format(self.poll_local_out))
                else:
                    QMessageBox.information(self.parent, "Success", 
                                           f"Captions saved to:\n{self.poll_local_out}")
                
                self.poll_attempts = 0
                self._current_operation = None
        except Exception as e:
            logger.warning(f"Poll error: {e}")
            if not self.retry_timer.isActive() and not self._stop_event.is_set():
                self.retry_timer.start(5000)

    def cleanup_drive(self):
        if not self.service:
            return
        try:
            uploads_id = self.get_or_create_folder("uploads")
            query = f"'{uploads_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()
            query = "name='NotyCaption_Generator.ipynb' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()
        except Exception as e:
            logger.warning(f"Drive cleanup error: {e}")


# ========================================
# Simple Animation Controller
# ========================================
class SimpleAnimationController:
    def __init__(self):
        self.enabled = True
        self.speed = 1.0
    def set_enabled(self, enabled):
        self.enabled = enabled
    def set_speed(self, speed_name):
        speed_map = {'slow': 2.0, 'normal': 1.0, 'fast': 0.5}
        self.speed = speed_map.get(speed_name, 1.0)

animation_controller = SimpleAnimationController()
# ========================================
# Main Window
# ========================================
class NotyCaptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = load_settings()
        _translator.set_language('en')
        animation_controller.set_enabled(True)

        self.setObjectName("NotyCaptionWindow")

        self.setWindowTitle(tr('window_title'))
        
        # Set minimum size with 3:2 ratio
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Set default size
        saved_width = self.settings.get("window_width", DEFAULT_WINDOW_WIDTH)
        saved_height = self.settings.get("window_height", DEFAULT_WINDOW_HEIGHT)
        self.resize(saved_width, saved_height)

        if self.settings.get("window_maximized", False):
            self.showMaximized()

        # Set size policy for responsive layout
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)

        self.apply_theme()
        self.center_window()

        if self.settings.get("window_geometry"):
            self.restoreGeometry(QByteArray.fromHex(self.settings["window_geometry"].encode()))
        if self.settings.get("window_state"):
            self.restoreState(QByteArray.fromHex(self.settings["window_state"].encode()))

        icon_path = resource_path('App.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.statusBar().showMessage(tr('ready'))

        # Initialize variables
        self.timeline = None
        self.workspace_btn = None
        self.main_progress = None
        self.gen_btn = None
        self.is_processing = False
        self._current_theme = self.settings.get("theme", "Dark")
        
        # Initialize audio variables
        self.input_file = None
        self.audio_file = None
        self.output_folder = self.settings.get("last_output_folder", None)
        self.subtitles = []
        self.display_lines = []
        self.generated = False
        self.edit_active = False
        self.loaded_media = None
        self.last_temp_wav = None
        self._closing = False

        # CREATE UI FIRST
        self.create_menu_bar()
        self.create_tool_bar()
        self.create_main_splitter()

        # Initialize player
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.positionChanged.connect(self.on_position_changed)
        self.player.durationChanged.connect(self.on_duration_changed)
        self.player.error.connect(self.on_player_error)
        self.duration_ms = 0

        # Set button states
        self.play_btn.setEnabled(bool(self.audio_file))
        self.enhance_btn.setEnabled(bool(self.audio_file))
        
        if self.output_folder and os.path.exists(self.output_folder):
            self.out_folder_edit.setText(self.output_folder)

        self.online_handler = OnlineHandler(self)
        self.audio_extractor = None

        self.player_timer = QTimer(self)
        self.player_timer.timeout.connect(self.update_timeline)
        self.player_timer.start(50)

        self._cancel_lock = threading.Lock()
        self._operation_in_progress = False
        self._current_notebook_url = None
        self._cancel_processed = False

        self._force_cancel_timer = QTimer(self)
        self._force_cancel_timer.setSingleShot(True)
        self._force_cancel_timer.timeout.connect(self.show_force_cancel_option)

        self.load_existing_credentials()
        self.setup_shortcuts()
        self.setup_tooltips()
        self.create_overlays()

        logger.info("Main window fully initialized")

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('&File')
        import_action = QAction('📁 &Import Media...', self)
        import_action.setShortcut('Ctrl+O')
        import_action.triggered.connect(self.import_media_file)
        file_menu.addAction(import_action)
        
        export_action = QAction('📤 &Export Subtitles...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_subtitles)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        exit_action = QAction('🚪 E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('&Edit')
        cut_action = QAction('✂️ Cu&t', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction('📋 &Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('📌 &Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        select_all_action = QAction('🔍 Select &All', self)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.triggered.connect(self.select_all)
        edit_menu.addAction(select_all_action)

        tools_menu = menubar.addMenu('🛠️ &Tools')
        settings_action = QAction('⚙️ &Settings', self)
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.open_settings_dialog)
        tools_menu.addAction(settings_action)
        
        google_login_action = QAction('🔐 &Google Login', self)
        google_login_action.setShortcut('Ctrl+G')
        google_login_action.triggered.connect(self.initiate_google_login)
        tools_menu.addAction(google_login_action)

        help_menu = menubar.addMenu('❓ &Help')
        documentation_action = QAction('📚 &Documentation', self)
        documentation_action.triggered.connect(self.open_documentation)
        help_menu.addAction(documentation_action)
        
        about_action = QAction('ℹ️ &About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def create_tool_bar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        toolbar.setObjectName("Main Toolbar")  # Add this to fix saveState warning
        self.addToolBar(toolbar)

        import_action = QAction('📁 Import', self)
        import_action.triggered.connect(self.import_media_file)
        toolbar.addAction(import_action)

        generate_action = QAction('🚀 Generate', self)
        generate_action.triggered.connect(self.start_caption_generation)
        toolbar.addAction(generate_action)

        # Enhance button (Vocal Extraction)
        self.enhance_btn = GlowButton(tr('enhance_audio'))
        self.enhance_btn.setMinimumHeight(28)
        self.enhance_btn.setMaximumHeight(28)
        self.enhance_btn.clicked.connect(self.enhance_audio_vocals)
        toolbar.addWidget(self.enhance_btn)

        toolbar.addSeparator()

        # Play button
        self.play_btn = GlowButton(tr('play_pause'))
        self.play_btn.setMinimumHeight(28)
        self.play_btn.setMaximumHeight(28)
        self.play_btn.clicked.connect(self.toggle_media_playback)
        toolbar.addWidget(self.play_btn)

        stop_action = QAction('⏹️ Stop', self)
        stop_action.triggered.connect(self.stop_playback)
        toolbar.addAction(stop_action)

        toolbar.addSeparator()

        settings_action = QAction('⚙️ Settings', self)
        settings_action.triggered.connect(self.open_settings_dialog)
        toolbar.addAction(settings_action)

    def create_main_splitter(self):
        """Create main splitter layout with responsive sizing"""
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setHandleWidth(2)
        self.main_splitter.setStyleSheet("""
            QSplitter::handle {
                background: #2a2a2a;
                width: 2px;
            }
            QSplitter::handle:hover {
                background: #0078d4;
            }
        """)
        self.main_layout.addWidget(self.main_splitter)

        # Left Panel - Caption Editor (takes 60% of space)
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_layout.setSpacing(8)
        self.left_panel.setLayout(self.left_layout)
        self.main_splitter.addWidget(self.left_panel)

        # Title Container - Smaller
        title_container = QFrame()
        title_container.setStyleSheet("background: transparent; border: none;")
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)
        
        app_title = QLabel(tr('app_name'))
        app_title.setObjectName("appTitle")
        app_title.setAlignment(Qt.AlignCenter)
        app_title.setStyleSheet("font-size: 20px; font-weight: 600;")
        title_layout.addWidget(app_title)
        
        app_subtitle = QLabel(tr('app_subtitle'))
        app_subtitle.setAlignment(Qt.AlignCenter)
        app_subtitle.setStyleSheet("font-size: 10px; margin-bottom: 4px; opacity: 0.7;")
        title_layout.addWidget(app_subtitle)
        
        self.left_layout.addWidget(title_container)

        # Caption Edit - With ScrollBars
        self.caption_edit = QTextEdit()
        self.caption_edit.setReadOnly(True)
        self.caption_edit.setFont(QFont('Consolas', 11))
        self.caption_edit.setStyleSheet("""
            QTextEdit {
                background: #1a1a1a;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                padding: 8px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border: 1px solid #0078d4;
            }
        """)
        self.caption_edit.setPlaceholderText("Captions will appear here after generation...")
        self.caption_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.caption_edit.setWordWrapMode(True)
        self.left_layout.addWidget(self.caption_edit, stretch=1)
        self.caption_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.caption_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.caption_edit.setLineWrapMode(QTextEdit.NoWrap)  # Allows horizontal scroll


        # Button Row - Smaller buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        
        self.edit_btn = GlowButton(tr('edit_captions'))
        self.edit_btn.setMinimumHeight(30)
        self.edit_btn.setMaximumHeight(30)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.edit_btn.setEnabled(False)
        btn_row.addWidget(self.edit_btn)
        
        self.settings_btn = GlowButton(tr('settings'))
        self.settings_btn.setMinimumHeight(30)
        self.settings_btn.setMaximumHeight(30)
        self.settings_btn.clicked.connect(self.open_settings_dialog)
        btn_row.addWidget(self.settings_btn)

        self.left_layout.addLayout(btn_row)

        # Right Panel - Controls (takes 40% of space)
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(8, 10, 10, 10)
        self.right_layout.setSpacing(8)
        self.right_panel.setLayout(self.right_layout)
        self.right_panel.setMinimumWidth(240)
        self.right_panel.setMaximumWidth(320)
        self.main_splitter.addWidget(self.right_panel)

        # Login Button
        self.login_button = GlowButton(tr('login_google'))
        self.login_button.setMinimumHeight(34)
        self.login_button.setProperty('type', 'primary')
        self.login_button.clicked.connect(self.initiate_google_login)
        self.right_layout.addWidget(self.login_button)

        # Language Selection Card
        lang_card = GlassCardWidget()
        lang_layout = QVBoxLayout(lang_card)
        lang_layout.setSpacing(4)
        lang_label = QLabel(tr('language'))
        lang_label.setStyleSheet("font-size: 11px; font-weight: 500; opacity: 0.7;")
        lang_layout.addWidget(lang_label)
        self.lang_combo = QComboBox()
        languages = [
            tr('english_transcribe'), tr('japanese_transcribe'), tr('chinese_transcribe'),
            tr('french_transcribe'), tr('german_transcribe'), tr('spanish_transcribe'),
            tr('russian_transcribe'), tr('arabic_transcribe'), tr('hindi_transcribe'),
            tr('korean_transcribe'), tr('portuguese_transcribe'), tr('italian_transcribe'),
            tr('dutch_transcribe'), tr('polish_transcribe'), tr('turkish_transcribe'),
            tr('vietnamese_transcribe'), tr('thai_transcribe')
        ]
        self.lang_combo.addItems(languages)
        self.lang_combo.setCurrentText(self.settings.get("default_lang", tr('english_transcribe')))
        self.lang_combo.setMinimumHeight(28)
        lang_layout.addWidget(self.lang_combo)
        self.right_layout.addWidget(lang_card)

        # Words per line Card
        wpl_card = GlassCardWidget()
        wpl_layout = QVBoxLayout(wpl_card)
        wpl_layout.setSpacing(4)
        wpl_label = QLabel(tr('words_per_line'))
        wpl_label.setStyleSheet("font-size: 11px; font-weight: 500; opacity: 0.7;")
        wpl_layout.addWidget(wpl_label)
        self.words_spin = QSpinBox()
        self.words_spin.setRange(1, 20)
        self.words_spin.setValue(self.settings.get("words_per_line", 5))
        self.words_spin.setMinimumHeight(28)
        wpl_layout.addWidget(self.words_spin)
        self.right_layout.addWidget(wpl_card)

        # Import Button
        self.import_btn = GlowButton(tr('import_media'))
        self.import_btn.setMinimumHeight(34)
        self.import_btn.clicked.connect(self.import_media_file)
        self.right_layout.addWidget(self.import_btn)

        # Format Card
        fmt_card = GlassCardWidget()
        fmt_layout = QVBoxLayout(fmt_card)
        fmt_layout.setSpacing(4)
        fmt_label = QLabel(tr('output_format'))
        fmt_label.setStyleSheet("font-size: 11px; font-weight: 500; opacity: 0.7;")
        fmt_layout.addWidget(fmt_label)
        self.format_combo = QComboBox()
        self.format_combo.addItems([tr('srt_format'), tr('ass_format')])
        self.format_combo.setCurrentText(self.settings.get("output_format", tr('srt_format')))
        self.format_combo.setMinimumHeight(28)
        fmt_layout.addWidget(self.format_combo)
        self.right_layout.addWidget(fmt_card)

        # Output Folder Card
        folder_card = GlassCardWidget()
        folder_layout = QVBoxLayout(folder_card)
        folder_layout.setSpacing(4)
        out_label = QLabel(tr('output_folder'))
        out_label.setStyleSheet("font-size: 11px; font-weight: 500; opacity: 0.7;")
        folder_layout.addWidget(out_label)
        self.out_folder_edit = QLineEdit()
        self.out_folder_edit.setReadOnly(True)
        self.out_folder_edit.setPlaceholderText("Default: Source Folder")
        self.out_folder_edit.setText(self.settings.get("last_output_folder", ""))
        self.out_folder_edit.setMinimumHeight(28)
        folder_layout.addWidget(self.out_folder_edit)
        browse_btn = GlowButton(tr('browse_output'))
        browse_btn.setMinimumHeight(28)
        browse_btn.clicked.connect(self.browse_output_folder)
        folder_layout.addWidget(browse_btn)
        self.right_layout.addWidget(folder_card)

        # Status Card
        status_card = GlassCardWidget()
        status_layout = QVBoxLayout(status_card)
        status_layout.setSpacing(4)
        status_row = QHBoxLayout()
        status_label = QLabel(tr('status'))
        status_label.setStyleSheet("font-size: 11px; font-weight: 500; opacity: 0.7;")
        status_row.addWidget(status_label)
        status_row.addStretch()
        self.status_value = QLabel(tr('ready'))
        self.status_value.setStyleSheet("color: #0f7b6e; font-size: 11px; font-weight: 500;")
        status_row.addWidget(self.status_value)
        status_layout.addLayout(status_row)
        self.right_layout.addWidget(status_card)
        
        self.right_layout.addStretch()

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+O"), self, self.import_media_file)
        QShortcut(QKeySequence("Ctrl+G"), self, self.start_caption_generation)
        QShortcut(QKeySequence("Ctrl+E"), self, self.enhance_audio_vocals)
        QShortcut(QKeySequence("Ctrl+S"), self, self.toggle_edit_mode)
        QShortcut(QKeySequence("Space"), self, self.toggle_media_playback)
        QShortcut(QKeySequence("Ctrl+,"), self, self.open_settings_dialog)
        QShortcut(QKeySequence("Esc"), self, lambda: self.cancel_current_operation(True))
        QShortcut(QKeySequence("Ctrl+L"), self, self.initiate_google_login)

    def setup_tooltips(self):
        if not self.settings.get("show_tooltips", True):
            return
        self.import_btn.setToolTip(tr('import_media') + " (Ctrl+O)")
        self.enhance_btn.setToolTip(tr('enhance_audio') + " - Extract vocals only (Ctrl+E)")
        self.play_btn.setToolTip(tr('play_pause') + " (Space)")
        self.edit_btn.setToolTip(tr('edit_captions') + " (Ctrl+S)")
        self.login_button.setToolTip(tr('login_google') + " (Ctrl+L)")
        self.lang_combo.setToolTip(tr('language'))
        self.words_spin.setToolTip(tr('words_per_line'))
        self.format_combo.setToolTip(tr('output_format'))
        self.out_folder_edit.setToolTip(tr('output_folder'))

    def create_overlays(self):
        self.overlay = QFrame(self.central_widget)
        self.overlay.setStyleSheet("background: rgba(10, 10, 10, 0.95); border: none;")
        self.overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.overlay.hide()

        self.overlay_layout = QVBoxLayout(self.overlay)
        self.overlay_layout.setAlignment(Qt.AlignCenter)

        self.progress_container = QFrame()
        self.progress_container.setStyleSheet(f"""
            QFrame {{ background: {WIN11_DARK_THEME['background_medium']};
            border: 2px solid {self.settings.get('accent_color', WIN11_DARK_THEME['accent_primary'])};
            border-radius: 15px; padding: 30px; max-width: 500px; }}
        """)
        prog_lay = QVBoxLayout(self.progress_container)

        self.prog_title = QLabel(tr('processing'))
        self.prog_title.setAlignment(Qt.AlignCenter)
        prog_lay.addWidget(self.prog_title)

        self.prog_info = QLabel(tr('starting'))
        self.prog_info.setAlignment(Qt.AlignCenter)
        prog_lay.addWidget(self.prog_info)

        self.operation_progress = QProgressBar()
        self.operation_progress.setRange(0, 100)
        prog_lay.addWidget(self.operation_progress)

        self.colab_link_container = QFrame()
        colab_link_layout = QHBoxLayout(self.colab_link_container)
        colab_label = QLabel(tr('colab_link'))
        colab_link_layout.addWidget(colab_label)
        self.colab_link = QLabel()
        self.colab_link.setOpenExternalLinks(True)
        self.colab_link.setWordWrap(True)
        colab_link_layout.addWidget(self.colab_link, 1)
        prog_lay.addWidget(self.colab_link_container)
        self.colab_link_container.hide()

        self.overlay_cancel_btn = GlowButton(tr('cancel'))
        self.overlay_cancel_btn.clicked.connect(lambda: self.cancel_current_operation(self.settings.get("confirm_cancel", True)))
        prog_lay.addWidget(self.overlay_cancel_btn)

        self.overlay_force_cancel_btn = GlowButton(tr('force_cancel'))
        self.overlay_force_cancel_btn.clicked.connect(self.force_cancel_operation)
        self.overlay_force_cancel_btn.hide()
        prog_lay.addWidget(self.overlay_force_cancel_btn)

        self.overlay_layout.addWidget(self.progress_container)


    def resizeEvent(self, event):
        """Handle window resize while maintaining aspect ratio"""
        super().resizeEvent(event)
        # Save size for next session
        if not self.isMaximized():
            self.settings["window_width"] = self.width()
            self.settings["window_height"] = self.height()
            save_settings(self.settings)

    def closeEvent(self, event):
        if not self.isMaximized():
            self.settings["window_width"] = self.width()
            self.settings["window_height"] = self.height()
        self.settings["window_maximized"] = self.isMaximized()
        self.settings["window_geometry"] = self.saveGeometry().toHex().data().decode()
        self.settings["window_state"] = self.saveState().toHex().data().decode()
        save_settings(self.settings)

        if self._operation_in_progress or self.is_processing:
            reply = QMessageBox.question(self, "Operation in Progress",
                "An operation is currently in progress.\n\nAre you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply != QMessageBox.Yes:
                event.ignore()
                return

        self._closing = True
        if self.audio_extractor and self.audio_extractor.isRunning():
            self.audio_extractor.cancel()
        if hasattr(self, 'online_handler'):
            self.online_handler.cancel_operation()
        event.accept()

    def initialize_state(self):
        """Initialize application state (called when resetting)"""
        self.subtitles = []
        self.display_lines = []
        self.generated = False
        self.edit_active = False
        self.is_processing = False
        self._current_notebook_url = None
        
        if hasattr(self, 'play_btn'):
            self.play_btn.setEnabled(bool(self.audio_file))
        if hasattr(self, 'enhance_btn'):
            self.enhance_btn.setEnabled(bool(self.audio_file))
        
        if self.output_folder and os.path.exists(self.output_folder):
            self.out_folder_edit.setText(self.output_folder)
        
        logger.info("App state initialized")

    def center_window(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def apply_ui_scale(self):
        scale_str = self.settings.get("ui_scale", "100%")
        try:
            scale = float(scale_str.rstrip("%")) / 100.0
            font = QApplication.font()
            font.setPointSizeF(font.pointSizeF() * scale)
            QApplication.setFont(font)
        except:
            pass

    def apply_theme(self):
        """Apply theme without restart"""
        theme = self.settings.get("theme", "Dark")
        accent_color = self.settings.get("accent_color", WIN11_DARK_THEME['accent_primary'])
        
        if theme == "Light":
            stylesheet = get_stylesheet('Light', accent_color)
        elif theme == "System":
            stylesheet = ""
            QApplication.setStyle(QStyleFactory.create('windows'))
        else:
            stylesheet = get_stylesheet('Dark', accent_color)
        
        self.setStyleSheet(stylesheet)
        logger.info(f"Theme applied: {theme}")

    def freeze_ui(self, freeze=True, message=tr('processing')):
        """Freeze/unfreeze UI during operations"""
        widgets = [self.import_btn, self.play_btn, self.edit_btn, self.login_button,
                   self.lang_combo, self.words_spin, self.format_combo, 
                   self.out_folder_edit, self.settings_btn, self.enhance_btn]
        for w in widgets:
            if hasattr(w, 'setEnabled'):
                w.setEnabled(not freeze)

        if freeze:
            self._operation_in_progress = True
            self.overlay.show()
            self.overlay.raise_()
            self.overlay_cancel_btn.setEnabled(True)
            self.overlay_force_cancel_btn.hide()
            self.prog_title.setText(message)
            self.prog_info.setText(tr('processing'))
            self.operation_progress.setValue(0)
            self.statusBar().showMessage(message, 0)
            if self._current_notebook_url:
                self.colab_link.setText(f"<a href='{self._current_notebook_url}'>{tr('click_to_open')}</a>")
                self.colab_link_container.show()
            timeout = self.settings.get("force_cancel_timeout", 30)
            self._force_cancel_timer.start(timeout * 1000)
        else:
            self._operation_in_progress = False
            self.is_processing = False
            self.overlay.hide()
            self.overlay_force_cancel_btn.hide()
            self.colab_link_container.hide()
            self._force_cancel_timer.stop()
            self.statusBar().clearMessage()

    def show_force_cancel_option(self):
        if self._operation_in_progress and self.overlay.isVisible():
            self.overlay_force_cancel_btn.show()
            self.overlay_force_cancel_btn.setEnabled(True)

    def reset_progress_bars(self):
        self.operation_progress.setValue(0)
        self.prog_info.setText(tr('ready'))

    def progress_update(self, value):
        self.operation_progress.setValue(value)

    def update_notebook_url_display(self, url):
        self._current_notebook_url = url

    def open_settings_dialog(self):
        dlg = SettingsDialog(self.settings, self)
        dlg.settingsChanged.connect(self.update_from_settings)
        dlg.exec_()

    def update_from_settings(self, new_settings):
        self.settings = new_settings
        self.apply_ui_scale()
        self.apply_theme()
        self.lang_combo.setCurrentText(new_settings.get("default_lang", tr('english_transcribe')))
        self.words_spin.setValue(new_settings.get("words_per_line", 5))
        self.format_combo.setCurrentText(new_settings.get("output_format", tr('srt_format')))
        self.setup_tooltips()
        if hasattr(self, 'online_handler'):
            self.online_handler.max_retry_attempts = new_settings.get("max_retry_attempts", 5)

    def initiate_google_login(self):
        client_secrets = load_client_secrets()
        if not client_secrets:
            QMessageBox.warning(self, "Missing Credentials", "Google client secrets not found.")
            return

        client_path = tempfile.mktemp(suffix='.json')
        try:
            with open(client_path, 'w') as f:
                json.dump(client_secrets, f)
            flow = InstalledAppFlow.from_client_secrets_file(client_path, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
            self.online_handler.service = build("drive", "v3", credentials=creds)
            self.login_button.setVisible(False)
            QMessageBox.information(self, "Login Success", "Google Drive connected.")
        except Exception as e:
            QMessageBox.critical(self, "Login Error", f"Authentication failed:\n{str(e)}")
        finally:
            if os.path.exists(client_path):
                os.remove(client_path)

    def load_existing_credentials(self):
        if os.path.exists(TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                self.online_handler.service = build("drive", "v3", credentials=creds)
                self.login_button.setVisible(False)
                logger.info("Existing credentials loaded")
            except Exception as e:
                logger.error(f"Credential load failed: {e}")
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.play_btn.setEnabled(True)

    def on_position_changed(self, position):
        self.update_caption_highlight(position)

    def on_duration_changed(self, duration):
        self.duration_ms = duration

    def on_player_error(self, error):
        err_str = self.player.errorString() or "Unknown error"
        QMessageBox.warning(self, "Playback Error", f"Audio playback failed:\n{err_str}")

    def update_timeline(self):
        pass

    def toggle_media_playback(self):
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, tr('no_audio'), tr('no_audio_msg'))
            return

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText(tr('play_pause'))
            return

        try:
            url = QUrl.fromLocalFile(self.audio_file)
            self.player.setMedia(QMediaContent(url))
            self.player.play()
            self.play_btn.setText(tr('playing'))
        except Exception as e:
            QMessageBox.critical(self, "Playback Error", str(e))

    def stop_playback(self):
        self.player.stop()
        self.play_btn.setText(tr('play_pause'))

    def update_caption_highlight(self, ms):
        if not self.subtitles or not self.generated:
            return
        sec = ms / 1000.0
        for i, sub in enumerate(self.subtitles):
            start_sec = sub["start"].total_seconds() if isinstance(sub["start"], timedelta) else sub["start"]
            end_sec = sub["end"].total_seconds() if isinstance(sub["end"], timedelta) else sub["end"]
            if start_sec <= sec < end_sec:
                cursor = self.caption_edit.textCursor()
                cursor.movePosition(QTextCursor.Start)
                cursor.movePosition(QTextCursor.NextBlock, QTextCursor.MoveAnchor, i)
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                self.caption_edit.setTextCursor(cursor)
                self.caption_edit.ensureCursorVisible()
                break

    def import_media_file(self, file_path=None):
        if not file_path:
            filter_str = "Media Files (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv *.mp3 *.wav *.m4a *.aac *.flac *.ogg)"
            file_path, _ = QFileDialog.getOpenFileName(self, tr('import_media'), 
                self.settings.get("last_input_file", ""), filter_str)
            
        if not file_path:
            return

        self.input_file = file_path
        self.output_folder = self.output_folder or os.path.dirname(file_path)
        self.out_folder_edit.setText(self.output_folder)
        
        self.settings["last_input_file"] = file_path
        self.settings["last_output_folder"] = self.output_folder
        save_settings(self.settings)

        # Extract audio
        self.freeze_ui(True, "Extracting audio...")
        self.audio_extractor = AudioExtractorThread(file_path, TEMP_DIR, self)
        self.audio_extractor.progress.connect(self.on_extract_progress)
        self.audio_extractor.finished.connect(self.on_extract_finished)
        self.audio_extractor.error.connect(self.on_extract_error)
        self.audio_extractor.start()

    def on_extract_progress(self, value, message):
        self.progress_update(value)
        self.prog_info.setText(message)

    def on_extract_finished(self, audio_path, success):
        """Handle audio extraction completion"""
        self.freeze_ui(False)
        if success:
            self.audio_file = audio_path
            self.last_temp_wav = audio_path
            self.play_btn.setEnabled(True)
            self.enhance_btn.setEnabled(True)
            self.preview_widget.set_media(audio_path)
            QMessageBox.information(self, tr('import_complete'), tr('import_success'))
        self.audio_extractor = None

    def on_extract_error(self, error_msg):
        self.freeze_ui(False)
        QMessageBox.critical(self, "Import Error", error_msg)
        self.audio_extractor = None

    def browse_output_folder(self):
        d = QFileDialog.getExistingDirectory(self, tr('browse_output'), self.output_folder or "")
        if d:
            self.output_folder = d
            self.out_folder_edit.setText(d)
            self.settings["last_output_folder"] = d
            save_settings(self.settings)

    def enhance_audio_vocals(self):
        """Extract vocals using Spleeter via Google Colab"""
        if self.is_processing:
            QMessageBox.warning(self, "In Progress", "Another operation is already in progress.")
            return

        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, tr('no_audio'), "No audio file loaded. Please import media first.")
            return

        if not self.online_handler.service:
            QMessageBox.warning(self, "Login Required", "Please login with Google first.")
            return

        self.is_processing = True
        self.freeze_ui(True, tr('enhancing'))
        self.reset_progress_bars()

        base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
        out_path = os.path.join(self.output_folder or APP_DATA_DIR, f"{base}_vocals.wav")

        if os.path.exists(out_path):
            reply = QMessageBox.question(self, tr('overwrite'), tr('overwrite_msg').format(out_path),
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                self.is_processing = False
                self.freeze_ui(False)
                return

        success = self.online_handler.handle_enhancement(self.audio_file, base, out_path)
        if not success:
            self.is_processing = False
            self.freeze_ui(False)

    def on_enhancement_downloaded(self, file_path):
        """Handle downloaded enhanced audio file"""
        self.audio_file = file_path
        self.last_temp_wav = file_path
        self.play_btn.setEnabled(True)
        self.enhance_btn.setEnabled(True)
        self.preview_widget.set_media(file_path)
        logger.info(f"Enhanced audio saved to: {file_path}")

    def start_caption_generation(self):
        if self.is_processing:
            QMessageBox.warning(self, "In Progress", "Another operation is already in progress.")
            return

        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, tr('no_media'), tr('import_first'))
            return

        if not self.online_handler.service:
            QMessageBox.warning(self, "Login Required", "Please login with Google first.")
            return

        self.is_processing = True
        self.freeze_ui(True, tr('generating'))
        self.reset_progress_bars()

        lang_text = self.lang_combo.currentText()
        lang_map = {
            tr('english_transcribe'): 'en', tr('japanese_transcribe'): 'ja',
            tr('chinese_transcribe'): 'zh', tr('french_transcribe'): 'fr',
            tr('german_transcribe'): 'de', tr('spanish_transcribe'): 'es',
            tr('russian_transcribe'): 'ru', tr('arabic_transcribe'): 'ar',
            tr('hindi_transcribe'): 'hi', tr('korean_transcribe'): 'ko',
            tr('portuguese_transcribe'): 'pt', tr('italian_transcribe'): 'it',
            tr('dutch_transcribe'): 'nl', tr('polish_transcribe'): 'pl',
            tr('turkish_transcribe'): 'tr', tr('vietnamese_transcribe'): 'vi',
            tr('thai_transcribe'): 'th'
        }
        lang_code = lang_map.get(lang_text, 'en')
        task = "transcribe"
        wpl = self.words_spin.value()
        
        fmt_map = {tr('srt_format'): ".srt", tr('ass_format'): ".ass"}
        fmt = fmt_map.get(self.format_combo.currentText(), ".srt")
        base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
        out_path = os.path.join(self.output_folder or APP_DATA_DIR, f"{base}_captions{fmt}")

        if os.path.exists(out_path):
            reply = QMessageBox.question(self, tr('overwrite'), tr('overwrite_msg').format(out_path),
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                self.is_processing = False
                self.freeze_ui(False)
                return

        success = self.online_handler.handle_transcription(
            self.audio_file, lang_code, task, wpl, fmt, base, out_path
        )
        if not success:
            self.is_processing = False
            self.freeze_ui(False)

    def load_downloaded_subtitles(self, file_path):
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
            self.preview_widget.set_subtitles(self.subtitles)
        except Exception as e:
            logger.error(f"Load subtitles error: {e}")

    def toggle_edit_mode(self):
        if not self.generated:
            return
        self.edit_active = not self.edit_active
        self.caption_edit.setReadOnly(not self.edit_active)
        self.edit_btn.setText(tr('save_exit_edit') if self.edit_active else tr('edit_captions'))
        if not self.edit_active:
            self.apply_edited_captions()

    def apply_edited_captions(self):
        text_content = self.caption_edit.toPlainText().strip()
        edited_lines = [line.strip() for line in text_content.split('\n\n') if line.strip()]

        if len(edited_lines) != len(self.subtitles):
            QMessageBox.warning(self, "Mismatch", "Line count changed. Edits not applied.")
            self.refresh_caption_preview()
            return

        for i, new_text in enumerate(edited_lines):
            self.subtitles[i]["text"] = new_text
            self.display_lines[i] = new_text
        self.refresh_caption_preview()
        self.preview_widget.set_subtitles(self.subtitles)
        QMessageBox.information(self, "Saved", "Edits applied to subtitles.")

    def refresh_caption_preview(self):
        preview = "\n\n".join(self.display_lines)
        self.caption_edit.setText(preview)

    def cancel_current_operation(self, with_confirmation=False):
        if with_confirmation and self.settings.get("confirm_cancel", True):
            reply = QMessageBox.question(self, tr('cancel_confirm'), tr('cancel_confirm_msg'),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply != QMessageBox.Yes:
                return

        if self.audio_extractor and self.audio_extractor.isRunning():
            self.audio_extractor.cancel()
        if hasattr(self, 'online_handler'):
            self.online_handler.cancel_operation()
        
        self.is_processing = False
        self.freeze_ui(False)
        self.reset_progress_bars()
        self.statusBar().showMessage(tr('canceled'), 5000)

    def force_cancel_operation(self):
        reply = QMessageBox.warning(self, tr('force_cancel'), tr('force_cancel_confirm'),
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        if self.audio_extractor and self.audio_extractor.isRunning():
            self.audio_extractor.cancel()
        if hasattr(self, 'online_handler'):
            self.online_handler.force_cancel_operation()
        
        self.is_processing = False
        self.freeze_ui(False)
        self.reset_progress_bars()
        self.statusBar().showMessage(tr('force_canceled'), 5000)

    def export_subtitles(self):
        if not self.generated or not self.subtitles:
            QMessageBox.warning(self, "No Subtitles", "No subtitles to export.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(self, "Export Subtitles",
            os.path.join(EXPORTS_DIR, f"subtitles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.srt"),
            "Subtitle Files (*.srt *.ass *.ssa *.vtt)")
        if filename:
            fmt = os.path.splitext(filename)[1]
            self.save_subtitles_to_file(self.subtitles, fmt, filename)
            QMessageBox.information(self, "Export Complete", f"Subtitles exported to:\n{filename}")

    def save_subtitles_to_file(self, subtitles, fmt, out_path):
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
            else:
                ass_file = pysubs2.SSAFile()
                ass_file.styles["Default"] = pysubs2.SSAStyle()
                for sub in subtitles:
                    ass_file.events.append(pysubs2.SSAEvent(
                        start=int(sub["start"].total_seconds() * 1000),
                        end=int(sub["end"].total_seconds() * 1000),
                        text=sub["text"]
                    ))
                ass_file.save(out_path)
            logger.info(f"Subtitles saved to {out_path}")
        except Exception as e:
            logger.error(f"Save failed: {e}")
            raise

    def cut(self):
        self.caption_edit.cut()

    def copy(self):
        self.caption_edit.copy()

    def paste(self):
        self.caption_edit.paste()

    def select_all(self):
        self.caption_edit.selectAll()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def open_documentation(self):
        QDesktopServices.openUrl(QUrl("https://github.com/NotY215/NotyCaption-Official"))

    def show_about_dialog(self):
        about_text = f"""
        <h1>{APP_NAME}</h1>
        <h3>Version {APP_VERSION}</h3>
        <p>Online AI-Powered Caption Generator with Vocal Enhancement</p>
        <p>Build: {APP_BUILD}</p>
        <hr>
        <p><b>Features:</b></p>
        <ul>
            <li>🎤 Vocal Extraction using Spleeter (via Google Colab)</li>
            <li>🎯 AI Transcription using OpenAI Whisper (via Google Colab)</li>
            <li>☁️ Google Drive integration for cloud processing</li>
            <li>🌍 Multiple language support (17+ languages)</li>
            <li>📄 SRT/ASS subtitle export</li>
            <li>💻 No local AI models required</li>
        </ul>
        <hr>
        <p><b>Author:</b> NotY215</p>
        <p><b>GitHub:</b> <a href="https://github.com/NotY215">NotY215</a></p>
        <p><b>Repository:</b> <a href="https://github.com/NotY215/NotyCaption-Official">NotyCaption-Official</a></p>
        """
        QMessageBox.about(self, "About NotyCaption Pro", about_text)


# ========================================
# Main Entry Point
# ========================================
if __name__ == "__main__":
    instance = SingleInstance()
    if instance.is_already_running():
        QMessageBox.warning(None, "Already Running", "NotyCaption is already open in another window.")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_AUTHOR)
    app.setStyle('Fusion')

    icon_path = resource_path('App.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    splash_pixmap = QPixmap(800, 600)
    splash_pixmap.fill(QColor(26, 26, 26))
    painter = QPainter(splash_pixmap)
    painter.setPen(QColor(74, 111, 165))
    painter.setFont(QFont("Segoe UI", 24, QFont.Bold))
    painter.drawText(splash_pixmap.rect(), Qt.AlignCenter, APP_NAME)
    painter.end()
        
    splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    window = NotyCaptionWindow()
    splash.finish(window)
    window.show()
    
    sys.exit(app.exec_())