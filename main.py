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
    QFrame, QGraphicsOpacityEffect, QStackedWidget, QStatusBar
)
from PyQt5.QtGui import QIcon, QColor, QTextCharFormat, QTextCursor, QFont, QPalette, QCloseEvent, QPixmap, QBrush, QLinearGradient
from PyQt5.QtCore import QTimer, Qt, QUrl, QDir, pyqtSignal, QThread, pyqtSlot, QPropertyAnimation, QEasingCurve, QProcess
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
import warnings
import platform

# Try to import optional browser tracking modules with fallback
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger = logging.getLogger("NotyCaption")
    logger.warning("psutil not installed - browser tab tracking disabled")

# Windows-specific imports
IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    try:
        import win32gui
        import win32process
        import win32con
        WIN32_AVAILABLE = True
    except ImportError:
        WIN32_AVAILABLE = False
        logger = logging.getLogger("NotyCaption")
        logger.warning("pywin32 not installed - browser tab tracking disabled")
else:
    WIN32_AVAILABLE = False
    logger.info(f"Running on {platform.system()} - browser tab tracking will use psutil only")

# Force charset_normalizer to pure Python (no mypyc crash in frozen exe)
os.environ["CHARSET_NORMALIZER_USE_MYPYC"] = "0"

# Disable tqdm in frozen EXE to prevent crashes
if getattr(sys, 'frozen', False):
    tqdm.disable = True

# Suppress googleapiclient file_cache warning
os.environ["GOOGLEAPI_DISABLE_FILE_CACHE"] = "1"
warnings.filterwarnings("ignore", category=DeprecationWarning, module="googleapiclient.discovery_cache")

# Suppress TensorFlow CUDA warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# ========================================
# LOGGING SETUP
# ========================================
def setup_logging():
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
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
    logger.info(f"Client mode: {'EXE (encrypted)' if os.path.exists(os.path.join(CURRENT_DIR, 'client.notycapz')) else 'Dev (plain)'}")
    logger.info(f"CUDA available: {tf.test.is_built_with_cuda()} (Auto-fallback to CPU if no GPU)")
    logger.info(f"Browser tracking available: psutil={PSUTIL_AVAILABLE}, win32={WIN32_AVAILABLE}, OS={platform.system()}")
    return logger

logger = setup_logging()

# ========================================
# RESOURCE PATH HELPER
# ========================================
def resource_path(relative_path):
    try:
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
# ENCRYPTION UTILS
# ========================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(CURRENT_DIR, "settings.notcapz")
KEY_FILE = os.path.join(CURRENT_DIR, "key.notcapz")
CLIENT_JSON = os.path.join(CURRENT_DIR, "client.json")
CLIENT_ENCRYPTED = os.path.join(CURRENT_DIR, "client.notycapz")

def load_or_create_key():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
        key_path = os.path.join(base, "key.notcapz")
        logger.info(f"EXE mode: loading bundled key from {key_path}")
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                key_data = f.read()
            logger.info("Bundled key loaded successfully")
            return key_data
        else:
            logger.error(f"Bundled key key.notcapz not found in EXE")
            raise FileNotFoundError(f"Encryption key missing in bundle: key.notcapz")

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key_data = f.read()
        logger.info("Local dev key loaded")
        return key_data

    logger.info("No key found - generating new one (dev mode only)")
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

fernet = Fernet(load_or_create_key())

def encrypt_data(data):
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    encrypted = fernet.encrypt(json_str.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_data(encrypted_b64):
    try:
        encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
        decrypted = fernet.decrypt(encrypted).decode('utf-8')
        return json.loads(decrypted)
    except Exception as dec_err:
        logger.error(f"Decryption failed: {dec_err}")
        return None

def save_settings(settings_dict):
    encrypted_b64 = encrypt_data(settings_dict)
    with open(SETTINGS_FILE, "w", encoding='utf-8') as f:
        f.write(encrypted_b64)
    logger.info("Settings saved securely")

def load_settings():
    defaults = {
        "ui_scale": "100%",
        "theme": "Dark",
        "temp_dir": tempfile.gettempdir(),
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
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
        encrypted_path = os.path.join(base, "client.notycapz")
        logger.info(f"EXE mode: loading bundled client.notycapz → {encrypted_path}")

        if os.path.exists(encrypted_path):
            try:
                with open(encrypted_path, "r", encoding='utf-8') as f:
                    encrypted_b64 = f.read().strip()
                decrypted = decrypt_data(encrypted_b64)
                if decrypted and "installed" in decrypted:
                    logger.info("Bundled client secrets decrypted OK")
                    return decrypted
                else:
                    logger.warning("Decrypted data invalid or missing 'installed'")
            except Exception as e:
                logger.error(f"Decryption failed for bundled file: {str(e)}")
        else:
            logger.warning("client.notycapz not found in bundle")
    else:
        if os.path.exists(CLIENT_JSON):
            logger.info("Dev mode: loading plain client.json")
            with open(CLIENT_JSON, "r", encoding='utf-8') as f:
                return json.load(f)

    logger.warning("No valid client secrets found")
    return None

# ========================================
# SINGLE INSTANCE CHECK
# ========================================
class SingleInstance:
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
        return self.already_exists

    def __del__(self):
        if not self.already_exists:
            try:
                self.sock.close()
                logger.info("Single instance lock released")
            except Exception as close_err:
                logger.warning(f"Socket close failed: {close_err}")

# ========================================
# SETTINGS DIALOG
# ========================================
class SettingsDialog(QDialog):
    settingsChanged = pyqtSignal(dict)

    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("NotyCaption Settings - Secure Edition")
        self.setFixedSize(580, 620)
        self.current_settings = current_settings
        lay = QVBoxLayout()
        self.setLayout(lay)

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

        tmp_gb = QGroupBox("Temporary Files Directory")
        tmp_lay = QHBoxLayout()
        self.tmp_edit = QLineEdit(current_settings.get("temp_dir", tempfile.gettempdir()))
        self.tmp_edit.setPlaceholderText("Default: System Temp")
        tmp_btn = QPushButton("Browse Folder")
        tmp_btn.clicked.connect(self.browse_temp)
        tmp_lay.addWidget(self.tmp_edit)
        tmp_lay.addWidget(tmp_btn)
        tmp_gb.setLayout(tmp_lay)
        lay.addWidget(tmp_gb)

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
        d = QFileDialog.getExistingDirectory(self, "Select Temporary Files Folder")
        if d:
            self.tmp_edit.setText(d)
            logger.info(f"Temp dir changed to: {d}")

    def browse_models(self):
        d = QFileDialog.getExistingDirectory(self, "Select Whisper Models Folder")
        if d:
            self.mod_edit.setText(d)
            logger.info(f"Models dir changed to: {d}")

    def apply_close(self):
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
# BROWSER TAB TRACKER (with cross-platform support)
# ========================================
class BrowserTabTracker:
    """Tracks browser tabs opened by the application with cross-platform support"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._tabs = {}  # url -> process_info
        self._check_timer = None
        self._available = PSUTIL_AVAILABLE  # psutil is enough for basic tracking
        if not self._available:
            logger.warning("Browser tab tracking disabled - missing psutil. Install with: pip install psutil")
        else:
            logger.info(f"BrowserTabTracker initialized with psutil (OS: {platform.system()})")
        
    def register_tab(self, url, max_attempts=15):
        """Register a browser tab with its process info, retrying multiple times"""
        if not self._available:
            logger.info(f"Tab tracking disabled, skipping registration for {url}")
            return False
            
        with self._lock:
            for attempt in range(max_attempts):
                try:
                    # Find browser process that opened this tab
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            proc_name = proc.info['name'].lower() if proc.info['name'] else ''
                            cmdline = ' '.join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ''
                            
                            # Check if this is a browser process
                            if any(browser in proc_name or browser in cmdline 
                                   for browser in ['chrome', 'firefox', 'edge', 'opera', 'brave', 'safari']):
                                
                                # Check if this process opened our URL
                                if url.lower() in cmdline:
                                    self._tabs[url] = {
                                        'pid': proc.info['pid'],
                                        'name': proc.info['name'],
                                        'cmdline': proc.info['cmdline'],
                                        'timestamp': time.time()
                                    }
                                    logger.info(f"Registered tab for {url} with PID {proc.info['pid']} (attempt {attempt+1})")
                                    return True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    
                    # If not found, wait and retry with increasing delay
                    if attempt < max_attempts - 1:
                        delay = min(1 * (attempt + 1), 3)  # Progressive delay up to 3 seconds
                        time.sleep(delay)
                        
                except Exception as e:
                    logger.error(f"Error registering tab (attempt {attempt+1}): {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                    else:
                        return False
            
            logger.warning(f"Could not find browser process for {url} after {max_attempts} attempts")
            return False
    
    def is_tab_open(self, url):
        """Check if the browser tab is still open"""
        if not self._available:
            # If tracking disabled, assume tab is open
            return True
            
        with self._lock:
            if url not in self._tabs:
                return False
                
            tab_info = self._tabs[url]
            try:
                # Check if process still exists
                proc = psutil.Process(tab_info['pid'])
                
                # Check if process is still running
                if proc.is_running():
                    # On Windows, we can do more detailed checking with win32 if available
                    if IS_WINDOWS and WIN32_AVAILABLE:
                        try:
                            # Try to get window handles for this process
                            def enum_windows_callback(hwnd, windows):
                                if win32process.GetWindowThreadProcessId(hwnd)[1] == tab_info['pid']:
                                    windows.append(hwnd)
                                return True
                            
                            windows = []
                            win32gui.EnumWindows(enum_windows_callback, windows)
                            
                            if windows:
                                # Process has windows, likely still running
                                return True
                            else:
                                # Process has no windows, might be background
                                # Check command line as fallback
                                cmdline = ' '.join(proc.cmdline()).lower()
                                if url.lower() in cmdline:
                                    return True
                        except:
                            # Fall back to cmdline check
                            cmdline = ' '.join(proc.cmdline()).lower()
                            return url.lower() in cmdline
                    else:
                        # On non-Windows, just check if process exists and URL in cmdline
                        cmdline = ' '.join(proc.cmdline()).lower()
                        return url.lower() in cmdline
                else:
                    logger.info(f"Browser process {tab_info['pid']} no longer running")
                    return False
                    
            except psutil.NoSuchProcess:
                logger.info(f"Browser process {tab_info['pid']} not found")
                return False
            except Exception as e:
                logger.error(f"Error checking tab status: {e}")
                return False
    
    def unregister_tab(self, url):
        """Remove tab from tracking"""
        with self._lock:
            if url in self._tabs:
                del self._tabs[url]
                logger.info(f"Unregistered tab for {url}")
    
    def get_open_tabs(self):
        """Get list of currently open tabs"""
        if not self._available:
            return []
            
        with self._lock:
            open_tabs = []
            for url in list(self._tabs.keys()):
                if self.is_tab_open(url):
                    open_tabs.append(url)
                else:
                    # Clean up dead tabs
                    del self._tabs[url]
            return open_tabs

# ========================================
# ONLINE MODE HANDLER
# ========================================
SCOPES = ['https://www.googleapis.com/auth/drive']

class OnlineHandler:
    def __init__(self, parent_window):
        self.parent = parent_window
        self.service = None
        self.poll_timer = QTimer(parent_window)
        self.tab_check_timer = QTimer(parent_window)
        self.cleanup_timer = QTimer(parent_window)  # For periodic cleanup
        self.poll_audio_id = None
        self.poll_notebook_id = None
        self.poll_output_name = None
        self.poll_local_out = None
        self.poll_attempts = 0
        self.max_poll_attempts = 180
        self._canceled = False
        self._lock = threading.Lock()
        self._current_colab_url = None
        self.tab_tracker = BrowserTabTracker()
        self._cancel_lock = threading.Lock()
        logger.info("OnlineHandler initialized")
        
        # Setup tab check timer
        self.tab_check_timer.timeout.connect(self.check_colab_tab_status)
        self.tab_check_timer.start(5000)  # Check every 5 seconds
        
        # Setup cleanup timer to remove old Drive files
        self.cleanup_timer.timeout.connect(self.cleanup_old_drive_files)
        self.cleanup_timer.start(3600000)  # Run every hour

    def cancel_operation(self):
        """Cancel ongoing online operation and clean up Drive files"""
        with self._cancel_lock:
            self._canceled = True
            
        logger.info("Canceling online operation")
        
        # Stop polling timer
        if self.poll_timer.isActive():
            self.poll_timer.stop()
            
        # Clean up Drive files
        self.cleanup_current_operation()
        
        # Unregister tab
        if self._current_colab_url:
            self.tab_tracker.unregister_tab(self._current_colab_url)
            self._current_colab_url = None
            
        self.parent.statusBar().showMessage("Online operation canceled", 5000)

    def cleanup_current_operation(self):
        """Clean up Drive files for current operation"""
        if not self.service:
            return
            
        try:
            # Delete uploaded audio
            if self.poll_audio_id:
                self.service.files().delete(fileId=self.poll_audio_id).execute()
                logger.info(f"Deleted uploaded audio: {self.poll_audio_id}")
                self.poll_audio_id = None
            
            # Delete notebook
            if self.poll_notebook_id:
                self.service.files().delete(fileId=self.poll_notebook_id).execute()
                logger.info(f"Deleted notebook: {self.poll_notebook_id}")
                self.poll_notebook_id = None
                
        except Exception as cleanup_err:
            logger.warning(f"Drive cleanup error during cancel: {cleanup_err}")

    def cleanup_old_drive_files(self):
        """Periodic cleanup of old temporary files in Drive"""
        if not self.service:
            return
            
        try:
            # Find files older than 24 hours in uploads folder
            uploads_id = self.get_or_create_folder(self.service, "uploads")
            one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat() + 'Z'
            
            query = f"'{uploads_id}' in parents and createdTime < '{one_day_ago}' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            
            for file in results.get("files", []):
                self.service.files().delete(fileId=file["id"]).execute()
                logger.info(f"Cleaned up old file: {file['name']} ({file['id']})")
                
            # Clean up old notebooks
            query = f"name='NotyCaption_Generator.ipynb' and createdTime < '{one_day_ago}' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for file in results.get("files", []):
                self.service.files().delete(fileId=file["id"]).execute()
                logger.info(f"Cleaned up old notebook: {file['id']}")
                
        except Exception as e:
            logger.warning(f"Error during Drive cleanup: {e}")

    def check_colab_tab_status(self):
        """Check if Colab tab is still open"""
        if not self._current_colab_url or self._canceled:
            return
            
        try:
            if not self.tab_tracker.is_tab_open(self._current_colab_url):
                logger.info("Colab tab was closed - canceling online operation")
                self.parent.statusBar().showMessage("Colab tab closed - canceling operation...", 5000)
                self.cancel_operation()
                
                # Notify parent
                self.parent.is_generating = False
                self.parent.freeze_ui(False)
                QMessageBox.information(
                    self.parent,
                    "Operation Canceled",
                    "Colab tab was closed. The online operation has been canceled and temporary files have been cleaned up."
                )
        except Exception as e:
            logger.error(f"Error checking tab status: {e}")

    def handle_online(self, audio_to_use, lang_code, task, wpl, fmt, base, out_path):
        with self._lock:
            self._canceled = False
            
        if not self.service:
            QMessageBox.warning(self.parent, "Error", "Please login with Google first.")
            logger.warning("Online mode attempted without service")
            return False

        logger.info("Starting online mode workflow")
        try:
            # Check for cancellation before each major step
            if self._canceled:
                return False
                
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

            if self._canceled:
                return False
                
            query = "name='NotyCaption_Generator.ipynb' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()
                logger.info(f"Deleted old notebook: {f['id']}")

            if self._canceled:
                return False
                
            uploads_id = self.get_or_create_folder(self.service, "uploads")
            audio_filename = os.path.basename(audio_to_use)
            audio_id = self.upload_file(self.service, audio_to_use, audio_filename, uploads_id)
            logger.info(f"Uploaded audio: {audio_id}")
            self.poll_audio_id = audio_id

            if self._canceled:
                self.cleanup_current_operation()
                return False
                
            query = f"name='{audio_filename}' and '{uploads_id}' in parents and trashed=false"
            results = self.service.files().list(q=query).execute()
            if not results.get("files", []):
                raise Exception("Audio upload failed - file not found in Drive.")

            notebook_content = self.generate_notebook_content(
                audio_filename, wpl, fmt, self.poll_output_name, lang_code, task
            )

            if self._canceled:
                self.cleanup_current_operation()
                return False
                
            temp_ipynb = resource_path("temp_Notycaption_Generator.ipynb")
            with open(temp_ipynb, "w", encoding="utf-8") as f:
                json.dump(notebook_content, f, indent=2)

            notebook_id = self.upload_file(self.service, temp_ipynb, "NotyCaption_Generator.ipynb")
            os.remove(temp_ipynb)
            logger.info(f"Uploaded notebook: {notebook_id}")
            self.poll_notebook_id = notebook_id

            if self._canceled:
                self.cleanup_current_operation()
                return False
                
            colab_url = f"https://colab.research.google.com/drive/{notebook_id}"
            self._current_colab_url = colab_url
            
            # Open the URL
            webbrowser.open(colab_url)
            
            # Register the tab with retries
            self.parent.statusBar().showMessage("Registering Colab tab for tracking...", 3000)
            QTimer.singleShot(1000, lambda: self.retry_register_tab(colab_url, 0))
            
            # Show appropriate message based on tracking availability
            track_status = "enabled" if self.tab_tracker._available else "disabled"
            track_msg = f"Tab tracking {track_status}"
            if not self.tab_tracker._available:
                track_msg += " (install psutil for tab tracking: pip install psutil)"
            
            QMessageBox.information(
                self.parent,
                "Colab Launched (GPU Runtime Recommended)",
                f"Notebook opened in browser.\n\n"
                "Important:\n"
                "1. In Colab → Runtime → Change runtime type → Hardware accelerator → GPU (T4 recommended)\n"
                "2. Wait 60 seconds → then Runtime → Run All\n"
                "3. DO NOT close the Colab tab until processing completes\n"
                "App will auto-download subtitles when finished.\n\n"
                f"Status: {track_msg}"
            )

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
            self.cleanup_current_operation()
            QMessageBox.critical(self.parent, "Online Mode Failed", str(online_err))
            return False

    def retry_register_tab(self, url, attempt):
        """Retry tab registration with exponential backoff"""
        if attempt >= 15:  # Max 15 attempts (about 45 seconds total)
            logger.warning(f"Failed to register tab after {attempt} attempts")
            self.parent.statusBar().showMessage("Could not track Colab tab - continuing anyway", 5000)
            return
            
        if self.tab_tracker.register_tab(url):
            logger.info(f"Tab registered successfully on attempt {attempt + 1}")
            self.parent.statusBar().showMessage("Colab tab tracked successfully", 3000)
        else:
            # Try again with increasing delay
            delay = min(1000 * (attempt + 1), 5000)  # Max 5 second delay
            QTimer.singleShot(delay, lambda: self.retry_register_tab(url, attempt + 1))

    def get_or_create_folder(self, service, name):
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
        metadata = {"name": filename}
        if parent_id:
            metadata["parents"] = [parent_id]

        media = MediaFileUpload(filepath, resumable=True)
        file = service.files().create(body=metadata, media_body=media, fields="id").execute()
        file_id = file.get("id")
        logger.info(f"Uploaded {filename} as {file_id}")
        return file_id

    def generate_notebook_content(self, audio_filename, words_per_line, fmt, output_name, lang_code='en', task='transcribe'):
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
        if not self.poll_output_name:
            logger.warning("Polling without output name set")
            return

        # Check if canceled
        if self._canceled:
            self.poll_timer.stop()
            return

        # Check if tab is still open (only if tracking available)
        if self.tab_tracker._available and self._current_colab_url and not self.tab_tracker.is_tab_open(self._current_colab_url):
            logger.info("Colab tab was closed during polling - canceling")
            self.cancel_operation()
            self.parent.is_generating = False
            self.parent.freeze_ui(False)
            QMessageBox.information(
                self.parent,
                "Operation Canceled",
                "Colab tab was closed. The online operation has been canceled."
            )
            return

        self.poll_attempts += 1
        logger.debug(f"Poll attempt {self.poll_attempts}/{self.max_poll_attempts}")

        if self.poll_attempts > self.max_poll_attempts:
            self.poll_timer.stop()
            self.parent.is_generating = False
            self.parent.freeze_ui(False)
            self.cleanup_current_operation()
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
                            if self._canceled:
                                logger.info("Download canceled during chunk download")
                                return
                            status, done = downloader.next_chunk()
                            if status:
                                progress_pct = int(status.progress() * 100)
                                logger.info(f"Download progress: {progress_pct}%")
                                self.parent.progress_update(progress_pct)
                    self.parent.load_downloaded_subtitles(self.poll_local_out)
                    
                    # Clean up Drive files
                    self.cleanup_current_operation()
                    if file_id:
                        self.service.files().delete(fileId=file_id).execute()
                        logger.info(f"Deleted output file: {file_id}")
                        
                    self.poll_timer.stop()
                    self.parent.is_generating = False
                    self.parent.freeze_ui(False)
                    
                    # Ask if user wants to close Colab tab
                    if self._current_colab_url and self.tab_tracker._available:
                        reply = QMessageBox.question(
                            self.parent,
                            "Close Colab Tab?",
                            "Online generation completed successfully!\n\n"
                            "Do you want to close the Colab tab?",
                            QMessageBox.Yes | QMessageBox.No
                        )
                        if reply == QMessageBox.Yes:
                            # Try to close the tab by killing the browser process (gentle approach)
                            self.close_browser_tab(self._current_colab_url)
                    
                    # Unregister tab
                    if self._current_colab_url:
                        self.tab_tracker.unregister_tab(self._current_colab_url)
                        self._current_colab_url = None
                        
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

    def close_browser_tab(self, url):
        """Attempt to close the browser tab"""
        if not self.tab_tracker._available or url not in self.tab_tracker._tabs:
            return
            
        try:
            tab_info = self.tab_tracker._tabs[url]
            proc = psutil.Process(tab_info['pid'])
            
            # On Windows, try to close the window gracefully
            if IS_WINDOWS and WIN32_AVAILABLE:
                def enum_windows_callback(hwnd, windows):
                    if win32process.GetWindowThreadProcessId(hwnd)[1] == tab_info['pid']:
                        windows.append(hwnd)
                    return True
                
                windows = []
                win32gui.EnumWindows(enum_windows_callback, windows)
                
                for hwnd in windows:
                    try:
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                        logger.info(f"Sent close message to window {hwnd}")
                    except:
                        pass
            else:
                # On other platforms, just note that we can't close it
                logger.info("Automatic tab closing not supported on this platform")
                
        except Exception as e:
            logger.error(f"Error closing browser tab: {e}")

    def cleanup_drive(self):
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
# AUDIO ENHANCER THREAD
# ========================================
class AudioEnhancerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, bool)
    error = pyqtSignal(str)

    def __init__(self, audio_file, temp_dir, parent=None):
        super().__init__(parent)
        self.audio_file = audio_file
        self.temp_dir = temp_dir
        self._lock = threading.Lock()
        self._is_canceled = False
        self._output_dir = None
        logger.info(f"AudioEnhancerThread initialized for {audio_file}")

    def cancel(self):
        with self._lock:
            self._is_canceled = True
        logger.info("Audio enhancement cancellation requested")

    def is_canceled(self):
        with self._lock:
            return self._is_canceled

    @pyqtSlot()
    def run(self):
        try:
            self.progress.emit(10)
            logger.info("Initializing Spleeter separator")
            
            if self.is_canceled():
                return
                
            separator = Separator('spleeter:2stems')
            base_name = os.path.splitext(os.path.basename(self.audio_file))[0]
            self._output_dir = os.path.join(self.temp_dir, base_name)

            logger.info(f"Starting separation to {self._output_dir}")
            if self.is_canceled():
                return
                
            separator.separate_to_file(
                self.audio_file,
                self._output_dir,
                synchronous=True
            )
            self.progress.emit(80)
            logger.info("Separation phase complete")
            
            if self.is_canceled():
                # Clean up partial output
                if self._output_dir and os.path.exists(self._output_dir):
                    try:
                        shutil.rmtree(self._output_dir)
                        logger.info(f"Cleaned up partial output: {self._output_dir}")
                    except:
                        pass
                return

            vocals_path = os.path.join(self._output_dir, base_name, 'vocals.wav')
            if not os.path.exists(vocals_path):
                vocals_path = os.path.join(self._output_dir, 'vocals.wav')
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
# MODEL VALIDATION
# ========================================
def validate_model_file(model_path):
    if not os.path.exists(model_path):
        return False
    
    try:
        file_size = os.path.getsize(model_path)
        expected_size_min = 2.5 * 1024 * 1024 * 1024
        expected_size_max = 3.0 * 1024 * 1024 * 1024
        
        if expected_size_min <= file_size <= expected_size_max:
            logger.info(f"Model file validated: {file_size / (1024**3):.2f} GB")
            return True
        return False
    except Exception as e:
        logger.error(f"Error validating model file: {e}")
        return False

def cleanup_corrupt_models(models_dir):
    if not os.path.exists(models_dir):
        return False
    
    removed = False
    model_files = [
        os.path.join(models_dir, "large-v1.pt"),
        os.path.join(models_dir, "large.pt"),
        os.path.join(models_dir, "large-v1.pt.tmp")
    ]
    
    for model_path in model_files:
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    pass
                
                if not validate_model_file(model_path) or model_path.endswith('.tmp'):
                    os.remove(model_path)
                    logger.info(f"Removed corrupt/incomplete model: {model_path}")
                    removed = True
            except (IOError, OSError) as e:
                logger.warning(f"Cannot access model file {model_path}: {e}")
    
    return removed

# ========================================
# CANCELLABLE WHISPER DOWNLOADER
# ========================================
class CancellableWhisperDownloader:
    def __init__(self):
        self._canceled = False
        self._progress_callback = None
        self._current_download = None
        self._downloaded = 0
        self._total_size = 0
        self._download_completed = False
        self._lock = threading.Lock()
        self._response = None
        self._temp_path = None
        
    def cancel(self):
        with self._lock:
            self._canceled = True
            if self._response:
                try:
                    self._response.close()
                except:
                    pass
        logger.info("Download cancellation requested")

    def is_canceled(self):
        with self._lock:
            return self._canceled
        
    def patched_download_url_to_file(self, original_func, url, dst, *args, **kwargs):
        if self.is_canceled():
            raise Exception("DOWNLOAD_CANCELED_BY_USER")
        
        self._current_download = {'url': url, 'dst': dst}
        self._download_completed = False
        self._temp_path = dst + '.tmp'
        
        try:
            import urllib.request
            import os
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            self._response = urllib.request.urlopen(req, timeout=30)
            
            if self.is_canceled():
                self._response.close()
                raise Exception("DOWNLOAD_CANCELED_BY_USER")
            
            self._total_size = int(self._response.headers.get('Content-Length', 0))
            
            with open(self._temp_path, 'wb') as out_file:
                self._downloaded = 0
                chunk_size = 8192
                
                while True:
                    if self.is_canceled():
                        logger.info("Cancellation detected during download")
                        out_file.close()
                        self._response.close()
                        if os.path.exists(self._temp_path):
                            os.remove(self._temp_path)
                        raise Exception("DOWNLOAD_CANCELED_BY_USER")
                    
                    chunk = self._response.read(chunk_size)
                    if not chunk:
                        break
                    
                    out_file.write(chunk)
                    self._downloaded += len(chunk)
                    
                    if self._progress_callback and self._total_size > 0:
                        progress = int((self._downloaded / self._total_size) * 100)
                        if progress < 100:
                            self._progress_callback(progress)
            
            if self.is_canceled():
                if os.path.exists(self._temp_path):
                    os.remove(self._temp_path)
                raise Exception("DOWNLOAD_CANCELED_BY_USER")
            
            if os.path.exists(self._temp_path):
                file_size = os.path.getsize(self._temp_path)
                if file_size < self._total_size * 0.99:
                    logger.warning(f"Downloaded file size mismatch: {file_size} vs {self._total_size}")
                    os.remove(self._temp_path)
                    raise Exception("DOWNLOAD_INCOMPLETE")
            
            if os.path.exists(dst):
                os.remove(dst)
            os.rename(self._temp_path, dst)
            self._download_completed = True
                
        except Exception as e:
            if hasattr(self, '_temp_path') and self._temp_path and os.path.exists(self._temp_path):
                os.remove(self._temp_path)
            raise e
        finally:
            self._current_download = None
            self._response = None
            self._temp_path = None
        
        return dst

    def download_model(self, model_name, download_root, progress_callback=None):
        with self._lock:
            self._canceled = False
        self._progress_callback = progress_callback
        self._downloaded = 0
        self._total_size = 0
        self._download_completed = False
        self._response = None
        self._temp_path = None
        
        original_download = None
        
        try:
            import torch.hub
            import whisper
            
            if getattr(sys, 'frozen', False):
                tqdm.disable = True
                sys.stderr = open(os.devnull, 'w')
            
            original_download = torch.hub.download_url_to_file
            
            def patched_func(url, dst, *args, **kwargs):
                return self.patched_download_url_to_file(original_download, url, dst, *args, **kwargs)
            
            torch.hub.download_url_to_file = patched_func
            
            if self.is_canceled():
                raise Exception("DOWNLOAD_CANCELED_BY_USER")
            
            logger.info(f"Starting download of {model_name} model to {download_root}")
            
            model_path = os.path.join(download_root, f"{model_name}.pt")
            cleanup_corrupt_models(download_root)
            
            model = whisper.load_model(
                model_name, 
                download_root=download_root,
                in_memory=False
            )
            
            if self.is_canceled():
                raise Exception("DOWNLOAD_CANCELED_BY_USER")
            
            if not validate_model_file(model_path):
                logger.warning("Downloaded model validation failed")
                if os.path.exists(model_path):
                    os.remove(model_path)
                raise Exception("Model validation failed")
                
            logger.info("Model downloaded and validated successfully")
            
            if progress_callback:
                progress_callback(100)
                
            return model
            
        except Exception as e:
            error_str = str(e)
            if "DOWNLOAD_CANCELED_BY_USER" in error_str:
                logger.info("Download was canceled by user")
                model_path = os.path.join(download_root, f"{model_name}.pt")
                temp_path = model_path + '.tmp'
                for path in [model_path, temp_path]:
                    if os.path.exists(path):
                        os.remove(path)
                raise Exception("Download canceled by user")
            else:
                logger.error(f"Download error: {e}")
                raise
        finally:
            import torch.hub
            if original_download is not None:
                torch.hub.download_url_to_file = original_download
            self._response = None
            self._temp_path = None

# ========================================
# MODEL DOWNLOAD THREAD
# ========================================
class ModelDownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    canceled = pyqtSignal()

    def __init__(self, model_dir, parent=None):
        super().__init__(parent)
        self.model_dir = model_dir
        self._is_canceled = False
        self._download_started = False
        self._download_completed = False
        self._lock = threading.Lock()
        self._downloader = CancellableWhisperDownloader()
        self.progress_info = {"downloaded": 0, "total": 0}
        logger.info(f"ModelDownloadThread initialized for {model_dir}")

    def cancel(self):
        with self._lock:
            if not self._is_canceled and self._download_started and not self._download_completed:
                self._is_canceled = True
                self._downloader.cancel()
                logger.info("Model download cancellation requested")
                
                if self.isRunning():
                    self.terminate()
                    self.wait(1000)

    def is_downloading(self):
        with self._lock:
            return self._download_started and not self._download_completed and not self._is_canceled

    @pyqtSlot()
    def run(self):
        try:
            cleanup_corrupt_models(self.model_dir)
            
            self.progress.emit(5)
            logger.info("Starting model download process")
            
            model_path_v1 = os.path.join(self.model_dir, "large-v1.pt")
            model_path = os.path.join(self.model_dir, "large.pt")
            
            if validate_model_file(model_path_v1):
                logger.info("Valid large-v1 model already exists, skipping download")
                self.progress.emit(100)
                self.finished.emit(True, "Model already exists and is valid!")
                return
            elif validate_model_file(model_path):
                logger.info("Valid large model already exists, skipping download")
                self.progress.emit(100)
                self.finished.emit(True, "Model already exists and is valid!")
                return
            
            with self._lock:
                self._download_started = True
                self._download_completed = False
            
            # Custom progress callback to capture download info
            def progress_callback(p):
                if hasattr(self._downloader, '_downloaded') and hasattr(self._downloader, '_total_size'):
                    self.progress_info["downloaded"] = self._downloader._downloaded
                    self.progress_info["total"] = self._downloader._total_size
                self.progress.emit(p)
            
            model = self._downloader.download_model(
                "large-v1",
                self.model_dir,
                progress_callback=progress_callback
            )
            
            with self._lock:
                if self._is_canceled:
                    logger.info("Download was canceled after completion check")
                    self.canceled.emit()
                    return
                self._download_completed = True
            
            if validate_model_file(model_path_v1):
                logger.info("Model downloaded and validated successfully")
                self.progress.emit(100)
                self.finished.emit(True, "Model large-v1 downloaded and validated successfully!")
            else:
                raise Exception("Downloaded model validation failed")
                
        except Exception as dl_err:
            error_str = str(dl_err)
            if "canceled" in error_str.lower():
                logger.info("Download was canceled by user")
                with self._lock:
                    self._download_completed = True
                self.canceled.emit()
            elif not self._is_canceled:
                error_msg = f"Download error: {str(dl_err)}"
                logger.error(f"Model thread error: {traceback.format_exc()}")
                self.finished.emit(False, error_msg)
        finally:
            with self._lock:
                self._download_started = False

# ========================================
# MAIN APPLICATION WINDOW
# ========================================
class NotyCaptionWindow(QMainWindow):
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
        
        cleanup_corrupt_models(self.settings.get("models_dir", CURRENT_DIR))
        
        self.apply_ui_scale()
        self.apply_theme()

        self.center_window()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Status bar
        self.statusBar().showMessage("Ready")

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
        self._closing = False
        self._cancel_lock = threading.Lock()
        self._operation_in_progress = False

        self.load_existing_credentials()

        # Enhanced Overlay for full window coverage and blocking
        self.overlay = QFrame(self.central_widget)
        self.overlay.setStyleSheet("""
            QFrame {
                background: rgba(0,0,0,0.85);
                border: none;
            }
        """)
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
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
        self.prog_title = QLabel("Operation in Progress")
        self.prog_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.prog_title.setAlignment(Qt.AlignCenter)
        prog_lay.addWidget(self.prog_title)

        # Progress info with download speed and size (only one progress display)
        self.prog_info = QLabel("Starting...")
        self.prog_info.setStyleSheet("color: #cccccc; font-size: 12px; margin-bottom: 15px;")
        self.prog_info.setAlignment(Qt.AlignCenter)
        prog_lay.addWidget(self.prog_info)

        # Single progress bar for all operations
        self.operation_progress = QProgressBar()
        self.operation_progress.setMinimum(0)
        self.operation_progress.setMaximum(100)
        self.operation_progress.setStyleSheet("""
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
        prog_lay.addWidget(self.operation_progress)

        # Cancel button
        self.overlay_cancel_btn = QPushButton("Cancel Operation")
        self.overlay_cancel_btn.setStyleSheet("""
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
        self.overlay_cancel_btn.clicked.connect(self.cancel_current_operation)
        self.overlay_cancel_btn.setEnabled(False)

        self.overlay_layout.addWidget(self.progress_container)
        self.overlay_layout.addWidget(self.overlay_cancel_btn, alignment=Qt.AlignCenter)
        self.overlay_cancel_btn.setParent(self.overlay)

        # Download overlay for model download (uses same progress bar but different container)
        self.download_overlay = QFrame(self.central_widget)
        self.download_overlay.setStyleSheet("""
            QFrame {
                background: rgba(0,0,0,0.85);
                border: none;
            }
        """)
        self.download_overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.download_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.download_overlay.hide()

        download_overlay_layout = QVBoxLayout(self.download_overlay)
        download_overlay_layout.setAlignment(Qt.AlignCenter)

        download_container = QWidget()
        download_container.setStyleSheet("""
            QWidget {
                background: #2d2d30;
                border-radius: 15px;
                padding: 20px;
                max-width: 500px;
            }
        """)
        download_lay = QVBoxLayout(download_container)

        download_title = QLabel("Downloading Whisper large-v1 Model")
        download_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        download_title.setAlignment(Qt.AlignCenter)
        download_lay.addWidget(download_title)

        self.download_info = QLabel("Starting download...")
        self.download_info.setStyleSheet("color: #cccccc; font-size: 12px; margin-bottom: 15px;")
        self.download_info.setAlignment(Qt.AlignCenter)
        download_lay.addWidget(self.download_info)

        # Download progress bar (separate from main operation progress)
        self.download_progress = QProgressBar()
        self.download_progress.setMinimum(0)
        self.download_progress.setMaximum(100)
        self.download_progress.setStyleSheet("""
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
        download_lay.addWidget(self.download_progress)

        self.download_cancel_btn = QPushButton("Cancel Download")
        self.download_cancel_btn.setStyleSheet("""
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
        """)
        self.download_cancel_btn.clicked.connect(self.cancel_current_operation)
        download_overlay_layout.addWidget(download_container)
        download_overlay_layout.addWidget(self.download_cancel_btn, alignment=Qt.AlignCenter)

        logger.info("Main window fully initialized with enhanced overlay")

    def resizeEvent(self, event):
        """Handle window resize to update overlay geometry."""
        if hasattr(self, 'overlay') and self.overlay.isVisible():
            self.overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
            self.overlay.raise_()
            self.overlay_cancel_btn.raise_()
        if hasattr(self, 'download_overlay') and self.download_overlay.isVisible():
            self.download_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
            self.download_overlay.raise_()
            self.download_cancel_btn.raise_()
        super().resizeEvent(event)

    def closeEvent(self, event: QCloseEvent):
        """Handle app close with confirmation if operations in progress"""
        if self._operation_in_progress or self.is_generating:
            reply = QMessageBox.question(
                self,
                "Operation in Progress",
                "An operation is currently in progress.\n\n"
                "Are you sure you want to exit? Any unsaved progress will be lost.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return

        logger.info("App close event triggered")
        self._closing = True
        
        self.player.stop()
        self.player_timer.stop()
        if hasattr(self, 'online_handler'):
            self.online_handler.poll_timer.stop()
            self.online_handler.tab_check_timer.stop()
            self.online_handler.cleanup_timer.stop()

        if self.model_download_thread and self.model_download_thread.isRunning():
            logger.info("Download thread still running, canceling and waiting...")
            self.model_download_thread.cancel()
            if not self.model_download_thread.wait(3000):
                logger.warning("Download thread did not finish in time, terminating...")
                self.model_download_thread.terminate()
                self.model_download_thread.wait(1000)

        if self.enhancer_thread and self.enhancer_thread.isRunning():
            logger.info("Enhancer thread still running, terminating...")
            self.enhancer_thread.terminate()
            self.enhancer_thread.wait(1000)

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

        if hasattr(self, 'online_handler') and self.online_handler.service:
            self.online_handler.cleanup_drive()

        try:
            cleanup_corrupt_models(self.settings.get("models_dir", CURRENT_DIR))
        except Exception as e:
            logger.warning(f"Failed to clean up models on exit: {e}")

        self.settings["last_mode"] = self.mode
        save_settings(self.settings)

        logger.info("=== NotyCaption Secure Shutdown ===")
        event.accept()

    def setup_left_panel(self):
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

        # Single progress bar for main operations
        self.main_progress = QProgressBar()
        self.main_progress.setStyleSheet("""
            QProgressBar { background: #22252a; border: 2px solid #3a3f44; border-radius: 10px; text-align: center; color: white; font-weight: bold; height: 25px; }
            QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0a84ff,stop:1 #0066cc); border-radius: 8px; }
        """)
        self.main_progress.setFormat("Progress: %p%")
        bottom_layout.addWidget(self.main_progress)

        logger.info("Bottom panel setup complete")

    def setup_footer(self):
        footer = QLabel("NotyCaption Pro • Secure Edition 2026 • All rights reserved by NotY215 • Powered by Whisper AI & Spleeter (GPU/CPU Auto)")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #6c757d; font-size: 10px; margin: 15px 0; padding: 10px; border-top: 1px solid #404040;")
        self.main_layout.addWidget(footer)
        logger.info("Footer setup complete")

    def initialize_state(self):
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
        self._closing = False
        self._cancel_processed = False
        self.mode_combo.setCurrentText("☁️ Online (Colab + Drive)" if self.mode == "online" else "🖥️ Normal (Local Whisper)")

        self.update_download_button_visibility()
        self.enhance_btn.setEnabled(bool(self.audio_file))
        self.play_btn.setEnabled(bool(self.audio_file))
        logger.info("App state initialized")

    def center_window(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        logger.info("Window centered on screen")

    def apply_ui_scale(self):
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

    def freeze_ui(self, freeze=True, message="Processing... Please wait or cancel"):
        """Freeze/unfreeze UI + show custom message - CANCEL BUTTON ALWAYS ENABLED"""
        widgets_to_disable = [
            self.import_btn,
            self.enhance_btn,
            self.gen_btn,
            self.play_btn,
            self.edit_btn,
            self.download_btn,
            self.login_button,
            self.mode_combo,
            self.lang_combo,
            self.words_spin,
            self.format_combo,
            self.out_folder_edit,
            self.timeline
        ]

        # Disable only main widgets - NEVER disable cancel buttons
        for w in widgets_to_disable:
            if hasattr(w, 'setEnabled'):
                w.setEnabled(not freeze)

        if freeze:
            self._operation_in_progress = True
            self.overlay.show()
            self.overlay.raise_()
            self.overlay_cancel_btn.raise_()
            self.overlay_cancel_btn.setEnabled(True)
            self.overlay_cancel_btn.setFocus()
            self.prog_title.setText(message)
            self.prog_info.setText("Processing...")
            self.operation_progress.setValue(0)
            self.statusBar().showMessage(message, 0)
            # Ensure cancel button is the only interactive element
            self.show_cancel_only(True)
        else:
            self._operation_in_progress = False
            self.overlay.hide()
            self.statusBar().clearMessage()
            self.show_cancel_only(False)

    def show_cancel_only(self, show=True):
        """Make sure only cancel button is interactive on overlay"""
        self.overlay_cancel_btn.setEnabled(show)
        if show:
            self.overlay_cancel_btn.raise_()
            self.overlay_cancel_btn.setFocus()

    def progress_update(self, value):
        """Update both progress bars with the same value"""
        self.operation_progress.setValue(value)
        self.main_progress.setValue(value)

    def open_settings_dialog(self):
        logger.info("Opening settings dialog")
        dlg = SettingsDialog(self.settings, self)
        dlg.settingsChanged.connect(self.update_from_settings)
        if dlg.exec_() == QDialog.Accepted:
            logger.info("Settings dialog accepted")
        else:
            logger.info("Settings dialog canceled")

    def update_from_settings(self, new_settings):
        self.settings = new_settings
        self.apply_ui_scale()
        self.apply_theme()
        self.lang_combo.setCurrentText(new_settings.get("default_lang", "🇺🇸 English (Transcribe)"))
        self.words_spin.setValue(5)
        self.update_download_button_visibility()
        self.mode_combo.setCurrentText("☁️ Online (Colab + Drive)" if new_settings.get("last_mode", "normal") == "online" else "🖥️ Normal (Local Whisper)")
        logger.info("Settings updated and applied globally")

    def update_download_button_visibility(self):
        if self.mode == "online":
            self.download_btn.setVisible(False)
            logger.info("Download button hidden in online mode")
            return

        model_dir = self.settings.get("models_dir", CURRENT_DIR)
        model_path_v1 = os.path.join(model_dir, "large-v1.pt")
        model_path = os.path.join(model_dir, "large.pt")
        
        exists = validate_model_file(model_path_v1) or validate_model_file(model_path)
        self.download_btn.setVisible(not exists)
        logger.info(f"Valid model exists: {exists} → Button visible: {not exists}")

    def initiate_google_login(self):
        client_secrets = load_client_secrets()
        if not client_secrets:
            msg = "Google client secrets not found.\nIn dev mode, ensure client.json exists.\nIn EXE mode, rebuild with build.py to encrypt client.notycapz."
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
        self.mode = "online" if "Online" in text else "normal"
        self.settings["last_mode"] = self.mode
        save_settings(self.settings)
        self.update_download_button_visibility()
        logger.info(f"Mode switched to: {self.mode}")

    def load_whisper_model(self):
        try:
            model_dir = self.settings.get("models_dir", CURRENT_DIR)
            logger.info(f"Loading Whisper large-v1 from: {model_dir} (Auto GPU/CPU)")
            
            cleanup_corrupt_models(model_dir)
            
            model = whisper.load_model("large-v1", download_root=model_dir)
            logger.info("Whisper model loaded successfully")
            return model
        except Exception as load_err:
            logger.error(f"Whisper load failed: {traceback.format_exc()}")
            QMessageBox.critical(self, "Model Load Error", f"Failed to load Whisper model:\n{str(load_err)}")
            raise RuntimeError(f"Model load error: {str(load_err)}")

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.play_btn.setEnabled(True)
            logger.info("Media loaded for playback")
        elif status in (QMediaPlayer.NoMedia, QMediaPlayer.InvalidMedia):
            self.play_btn.setEnabled(False)
            self.play_btn.setText("▶️ Play / ⏸️ Pause")
            logger.warning("Media status invalid")

    def on_position_changed(self, position):
        self.update_caption_highlight(position)

    def on_duration_changed(self, duration):
        self.duration_ms = duration
        self.timeline.setRange(0, duration)
        logger.debug(f"Media duration set: {duration} ms")

    def on_player_error(self, error):
        err_str = self.player.errorString() or "Unknown error"
        logger.warning(f"Media player error: {err_str}")
        QMessageBox.warning(self, "Playback Error", f"Audio playback failed:\n{err_str}")

    def update_timeline(self):
        if self.duration_ms > 0 and self.player.state() == QMediaPlayer.PlayingState:
            self.timeline.setValue(self.player.position())

    def toggle_media_playback(self):
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
        self.player.setPosition(position)
        logger.debug(f"Seek to: {position} ms")

    def update_caption_highlight(self, ms):
        if not self.subtitles or not self.generated:
            return
        sec = ms / 1000.0
        doc = self.caption_edit.document()
        cursor = QTextCursor(doc)
        cursor.beginEditBlock()

        cursor.select(QTextCursor.Document)
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(0, 0, 0, 0))
        cursor.setCharFormat(fmt)

        for i, sub in enumerate(self.subtitles):
            start_sec = sub["start"].total_seconds() if isinstance(sub["start"], timedelta) else sub["start"]
            end_sec = sub["end"].total_seconds() if isinstance(sub["end"], timedelta) else sub["end"]
            
            if start_sec <= sec < end_sec:
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
        logger.info("Media import dialog opened")
        filter_str = "Media Files (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv *.mp3 *.wav *.m4a *.aac *.flac *.ogg *.wma *.amr *.opus)"
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
        if not self.audio_file:
            logger.info("No audio file set")
            return
        logger.info(f"Audio file path: {self.audio_file}")
        logger.info(f"Exists: {os.path.exists(self.audio_file)}")
        logger.info(f"Size: {os.path.getsize(self.audio_file) / 1024 / 1024:.2f} MB")

    def browse_output_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if d:
            self.output_folder = d
            self.out_folder_edit.setText(d)
            logger.info(f"Output folder set: {d}")

    def enhance_audio_vocals(self):
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "No Audio", "Import media first.")
            logger.warning("Enhance clicked without audio")
            return

        logger.info("Starting vocal enhancement...")
        self.freeze_ui(True, "Enhancing vocals with Spleeter... (this may take a while)")
        temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
        self.enhancer_thread = AudioEnhancerThread(self.audio_file, temp_dir, self)
        self.enhancer_thread.progress.connect(self.on_enhance_progress)
        self.enhancer_thread.finished.connect(self.on_enhance_finished)
        self.enhancer_thread.error.connect(self.on_enhance_error)
        self.enhancer_thread.start()
        logger.info("Enhancer thread started")

    def on_enhance_progress(self, value):
        self.progress_update(value)

    def on_enhance_finished(self, vocals_path, success):
        self.freeze_ui(False)
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
        self.enhancer_thread = None
        logger.info("Enhancer thread finished")

    def on_enhance_error(self, error_msg):
        self.freeze_ui(False)
        logger.error(f"Enhancement error: {error_msg}")
        QMessageBox.critical(self, "Enhancement Failed", error_msg)
        self.enhancer_thread = None

    def open_model_download_dialog(self):
        if self._closing:
            return
            
        logger.info("Opening model download dialog")
        dlg = QDialog(self)
        dlg.setWindowTitle("Whisper large-v1 Model Download")
        dlg.setFixedSize(520, 340)
        lay = QVBoxLayout()
        dlg.setLayout(lay)

        title = QLabel("Download Whisper large-v1 Model (~2.9 GB)")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        lay.addWidget(title)

        desc = QLabel("large-v1 is the most accurate model.\nRequires ~3 GB disk space.\nDownload may take 5-30 minutes depending on internet speed.\n\nOptional dependencies for tab tracking:\n  pip install psutil pywin32")
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

        if selected == 2:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select large-v1.pt", "", "PyTorch Model (*.pt)")
            if file_path and os.path.basename(file_path) == "large-v1.pt":
                if validate_model_file(file_path):
                    model_dir = os.path.dirname(file_path)
                    self.settings["models_dir"] = model_dir
                    save_settings(self.settings)
                    self.update_download_button_visibility()
                    QMessageBox.information(self, "Success", "Valid model file linked successfully!")
                    logger.info(f"Valid model linked from: {model_dir}")
                else:
                    QMessageBox.warning(self, "Invalid File", "The selected model file appears to be corrupt or incomplete.")
            else:
                QMessageBox.warning(self, "Invalid File", "Please select a file named exactly 'large-v1.pt'")
            return

        if selected == 1:
            path = QFileDialog.getExistingDirectory(self, "Select Folder to Download Model")
            if not path:
                logger.info("Custom folder selection canceled")
                return
        else:
            path = self.settings["models_dir"]

        cleanup_corrupt_models(path)

        self.settings["models_dir"] = path
        save_settings(self.settings)
        self.update_download_button_visibility()

        # Show download overlay
        self.download_overlay.show()
        self.download_overlay.raise_()
        self.download_cancel_btn.raise_()
        self.download_progress.setValue(0)
        self.download_info.setText("Starting download...")
        self.download_cancel_btn.setEnabled(True)

        # Freeze UI with custom message
        self.freeze_ui(True, "Downloading Whisper large-v1 model... (5–30 min)")

        self.model_download_thread = ModelDownloadThread(path, self)
        self.model_download_thread.progress.connect(self.on_download_progress)
        self.model_download_thread.finished.connect(self.on_model_download_finished)
        self.model_download_thread.canceled.connect(self.on_model_download_canceled)
        self.model_download_thread.start()

        logger.info(f"Model download started to: {path}")

    def on_download_progress(self, value):
        if self._closing:
            return
            
        self.download_progress.setValue(value)
        self.progress_update(value)
        
        try:
            if (hasattr(self, 'model_download_thread') and 
                self.model_download_thread and 
                hasattr(self.model_download_thread, 'progress_info')):
                
                info = self.model_download_thread.progress_info
                
                if info["total"] > 0:
                    downloaded_mb = info["downloaded"] / (1024 * 1024)
                    total_mb = info["total"] / (1024 * 1024)
                    self.download_info.setText(f"Downloading... {downloaded_mb:.1f} MB / {total_mb:.1f} MB ({value}%)")
                    self.prog_info.setText(f"Downloading... {downloaded_mb:.1f} MB / {total_mb:.1f} MB")
                else:
                    self.download_info.setText(f"Downloading... ({value}%)")
                    self.prog_info.setText(f"Downloading... ({value}%)")
            else:
                self.download_info.setText(f"Downloading... ({value}%)")
                self.prog_info.setText(f"Downloading... ({value}%)")
        except Exception as e:
            logger.debug(f"Progress display error: {e}")
            self.download_info.setText(f"Downloading... ({value}%)")
            self.prog_info.setText(f"Downloading... ({value}%)")

    def on_model_download_finished(self, success, message):
        self.download_overlay.hide()
        self.freeze_ui(False)
        
        if success:
            self.update_download_button_visibility()
            QMessageBox.information(self, "Success", message)
            logger.info("Model download finished successfully")
        else:
            QMessageBox.critical(self, "Download Failed", message)
            logger.error("Model download failed")
        self.model_download_thread = None
        self._cancel_processed = False

    def on_model_download_canceled(self):
        self.download_overlay.hide()
        self.freeze_ui(False)
        logger.info("UI buttons re-enabled after cancel")
        
        try:
            cleanup_corrupt_models(self.settings.get("models_dir", CURRENT_DIR))
        except Exception as e:
            logger.warning(f"Failed to clean up models after cancel: {e}")
        
        QMessageBox.information(
            self, 
            "Download Canceled", 
            "The model download has been canceled and the partial file has been deleted."
        )
        self.model_download_thread = None
        self._cancel_processed = False

    def start_caption_generation(self):
        if self.is_generating:
            QMessageBox.warning(self, "In Progress", "Generation already running.")
            logger.warning("Generation attempted while in progress")
            return

        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, "No Media", "Import audio/video first.")
            logger.warning("Generation attempted without media")
            return

        self.is_generating = True
        self.freeze_ui(True, "Generating captions... Please wait or cancel")
        self.main_progress.setValue(0)
        self.operation_progress.setValue(0)
        logger.info("=== Secure Caption Generation Started ===")

        auto_enhance = self.settings.get("auto_enhance", False)
        if auto_enhance:
            logger.info("Auto-enhancing audio before generation...")
            temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
            self.enhancer_thread = AudioEnhancerThread(self.audio_file, temp_dir, self)
            self.enhancer_thread.progress.connect(lambda v: self.progress_update(v // 2))
            self.enhancer_thread.finished.connect(lambda p, s: self.on_auto_enhance_done(p, s))
            self.enhancer_thread.error.connect(self.on_auto_enhance_error)
            self.enhancer_thread.start()
            return

        self.proceed_to_transcription(self.audio_file)

    def on_auto_enhance_done(self, vocals_path, success):
        if success:
            enhanced_path = vocals_path
            base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
            final_name = f"{base}_auto_enhanced.wav"
            final_path = os.path.join(self.output_folder or CURRENT_DIR, final_name)
            shutil.move(vocals_path, final_path)
            self.audio_file = final_path
            self.play_btn.setEnabled(True)
            logger.info(f"Auto-enhanced: {final_path}")
            self.proceed_to_transcription(final_path)
        else:
            logger.warning("Auto-enhance failed, using original audio")
            self.proceed_to_transcription(self.audio_file)

        self.enhancer_thread = None

    def on_auto_enhance_error(self, error):
        logger.error(f"Auto-enhance error: {error}")
        QMessageBox.warning(self, "Auto-Enhance Failed", error)
        self.enhancer_thread = None
        self.proceed_to_transcription(self.audio_file)

    def proceed_to_transcription(self, audio_to_use):
        lang_text = self.lang_combo.currentText()
        lang_code = "ja" if "Japanese" in lang_text else "en"
        task = "translate" if "Translate" in lang_text else "transcribe"

        wpl = self.words_spin.value()
        fmt_map = {
            "📄 .SRT (Standard)": ".srt",
            "🎨 .ASS (Advanced)": ".ass",
        }
        fmt = fmt_map.get(self.format_combo.currentText(), ".srt")
        base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
        out_path = os.path.join(self.output_folder or CURRENT_DIR, f"{base}_captions{fmt}")

        if os.path.exists(out_path):
            reply = QMessageBox.question(self, "Overwrite File?", f"File exists:\n{out_path}\nOverwrite?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                self.is_generating = False
                self.freeze_ui(False)
                logger.info("Overwrite canceled")
                return

        logger.info(f"Transcription params: lang={lang_code}, task={task}, wpl={wpl}, fmt={fmt}, out={out_path}")

        self.progress_update(10)

        if self.mode == "online":
            success = self.online_handler.handle_online(audio_to_use, lang_code, task, wpl, fmt, base, out_path)
            if not success:
                self.is_generating = False
                self.freeze_ui(False)
        else:
            self.perform_local_transcription(audio_to_use, lang_code, task, wpl, fmt, out_path)

    def perform_local_transcription(self, audio_path, lang_code, task, wpl, fmt, out_path):
        try:
            self.progress_update(20)
            model = self.load_whisper_model()
            self.progress_update(30)

            logger.info("Starting local transcription...")
            result = model.transcribe(
                audio_path,
                language=lang_code,
                task=task,
                word_timestamps=True,
                verbose=False
            )
            self.progress_update(80)
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

            self.progress_update(90)

            preview_text = "\n\n".join(self.display_lines)
            self.caption_edit.setText(preview_text)
            self.generated = True
            self.edit_btn.setEnabled(True)

            self.save_subtitles_to_file(self.subtitles, fmt, out_path)
            self.progress_update(100)

            logger.info(f"Local generation saved: {out_path}")
            QMessageBox.information(self, "Generation Complete", f"Captions generated and saved:\n{out_path}")

        except Exception as trans_err:
            logger.error(f"Local transcription failed: {traceback.format_exc()}")
            QMessageBox.critical(self, "Generation Error", f"Local processing failed:\n{str(trans_err)}")
        finally:
            self.is_generating = False
            self.freeze_ui(False)

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
        preview = "\n\n".join(self.display_lines)
        self.caption_edit.setText(preview)
        logger.debug("Caption preview refreshed")

    def cancel_current_operation(self):
        logger.info("Cancel button pressed - stopping current operation")
        
        with self._cancel_lock:
            stopped = False

            # Cancel online operation if active
            if hasattr(self, 'online_handler') and self.online_handler.poll_timer.isActive():
                logger.info("Canceling online operation...")
                self.online_handler.cancel_operation()
                self.is_generating = False
                self.freeze_ui(False)
                stopped = True

            # Cancel Spleeter enhancement if running
            if self.enhancer_thread and self.enhancer_thread.isRunning():
                logger.info("Canceling Spleeter enhancement...")
                self.enhancer_thread.cancel()
                self.enhancer_thread.terminate()
                self.enhancer_thread.wait(2000)
                self.enhancer_thread = None
                self.is_generating = False
                self.freeze_ui(False)
                stopped = True

            # Cancel model download if running
            if self.model_download_thread and self.model_download_thread.isRunning():
                logger.info("Canceling model download...")
                self.model_download_thread.cancel()
                self._check_cancel_complete()
                stopped = True

            # Cancel local generation if running
            if self.is_generating and not stopped:
                self.is_generating = False
                self.freeze_ui(False)
                stopped = True

            if stopped:
                self.statusBar().showMessage("Operation canceled by user", 5000)
            else:
                self.statusBar().showMessage("Nothing to cancel", 3000)

    def _check_cancel_complete(self):
        """Check if cancellation is complete with proper error handling"""
        try:
            if self._closing:
                return
                
            if self.model_download_thread and self.model_download_thread.isRunning():
                logger.warning("Download thread still running after cancel - forcing termination")
                self.model_download_thread.terminate()
                self.model_download_thread.wait(1000)
                self.on_model_download_canceled()
            else:
                self.on_model_download_canceled()
        except Exception as e:
            logger.error(f"Error during cancel completion check: {e}")
            self.on_model_download_canceled()

# ========================================
# MAIN ENTRY
# ========================================
if __name__ == "__main__":
    instance = SingleInstance()
    if instance.is_already_running():
        logger.warning("Duplicate instance detected")
        QMessageBox.warning(None, "Already Running", "NotyCaption is already open in another window.")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName("NotyCaption Pro")
    app.setOrganizationName("NotY215")
    app.setStyle('Fusion')

    icon_path = resource_path('App.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        logger.info("Global app icon set")

    logger.info("Launching secure NotyCaption...")
    window = NotyCaptionWindow()
    window.show()
    logger.info("Main loop started")
    sys.exit(app.exec_())