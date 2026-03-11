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
    QFrame, QGraphicsOpacityEffect, QStackedWidget, QStatusBar, QSystemTrayIcon,
    QMenu, QShortcut, QToolTip, QApplication
)
from PyQt5.QtGui import QIcon, QColor, QTextCharFormat, QTextCursor, QFont, QPalette, QCloseEvent, QPixmap, QBrush, QLinearGradient, QDesktopServices, QKeySequence
from PyQt5.QtCore import QTimer, Qt, QUrl, QDir, pyqtSignal, QThread, pyqtSlot, QPropertyAnimation, QEasingCurve, QProcess, QSettings, QTranslator, QLocale
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
import math
import GPUtil
import psutil
import cpuinfo

# Optional Windows-specific imports (don't break if missing)
try:
    import win32gui
    import win32process
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# Force charset_normalizer to pure Python
os.environ["CHARSET_NORMALIZER_USE_MYPYC"] = "0"

# Disable tqdm in frozen EXE
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
# TRANSLATIONS
# ========================================
TRANSLATIONS = {
    'en': {
        # Window Title
        'window_title': 'NotyCaption Pro - Secure AI Caption Generator by NotY215',
        
        # Menu and Status
        'ready': 'Ready',
        'processing': 'Processing...',
        'canceled': 'Canceled',
        'completed': 'Completed',
        'failed': 'Failed',
        
        # Buttons
        'edit_captions': '✏️ Edit Captions',
        'save_exit_edit': '💾 Save & Exit Edit',
        'settings': '⚙️ Settings',
        'download_model': '📥 Download large-v1 Model',
        'login_google': '🔐 Login with Google (Enable Online Mode)',
        'import_media': '📁 Import Video / Audio File',
        'browse_output': '📂 Browse Output Folder',
        'enhance_audio': '🎤 Enhance Audio (Vocals Only - Spleeter)',
        'play_pause': '▶️ Play / ⏸️ Pause',
        'playing': '⏸️ Playing...',
        'paused': '▶️ Play / ⏸️ Pause',
        'generate': '🚀 Generate Captions',
        'cancel': 'Cancel Operation',
        'force_cancel': '⚠️ Force Cancel (Emergency)',
        'reopen_notebook': '🔗 Reopen Notebook',
        'copy_url': '📋 Copy URL',
        
        # Labels
        'ai_caption_editor': 'AI-Powered Caption Editor',
        'processing_mode': 'Processing Mode:',
        'language': 'Language:',
        'words_per_line': 'Words per Line:',
        'output_format': 'Output Format:',
        'output_folder': 'Output Folder:',
        'status': 'Status:',
        'notebook_url': 'Notebook URL:',
        'not_available': 'Not available',
        'idle': 'Idle',
        'speed': 'Speed:',
        'eta': 'ETA:',
        'downloading': 'Downloading...',
        'uploading': 'Uploading...',
        'waiting': 'Waiting...',
        
        # Modes
        'normal_mode': '🖥️ Normal (Local Whisper)',
        'online_mode': '☁️ Online (Colab + Drive)',
        
        # Languages for transcription
        'english_transcribe': '🇺🇸 English (Transcribe)',
        'japanese_translate': '🇯🇵 Japanese → English (Translate)',
        'chinese_transcribe': '🇨🇳 Chinese (Transcribe)',
        'french_transcribe': '🇫🇷 French (Transcribe)',
        'german_transcribe': '🇩🇪 German (Transcribe)',
        'spanish_transcribe': '🇪🇸 Spanish (Transcribe)',
        'russian_transcribe': '🇷🇺 Russian (Transcribe)',
        'arabic_transcribe': '🇸🇦 Arabic (Transcribe)',
        'hindi_transcribe': '🇮🇳 Hindi (Transcribe)',
        'bengali_transcribe': '🇧🇩 Bengali (Transcribe)',
        'urdu_transcribe': '🇵🇰 Urdu (Transcribe)',
        'portuguese_transcribe': '🇵🇹 Portuguese (Transcribe)',
        'italian_transcribe': '🇮🇹 Italian (Transcribe)',
        'dutch_transcribe': '🇳🇱 Dutch (Transcribe)',
        'polish_transcribe': '🇵🇱 Polish (Transcribe)',
        'turkish_transcribe': '🇹🇷 Turkish (Transcribe)',
        'vietnamese_transcribe': '🇻🇳 Vietnamese (Transcribe)',
        'thai_transcribe': '🇹🇭 Thai (Transcribe)',
        'korean_transcribe': '🇰🇷 Korean (Transcribe)',
        
        # Formats
        'srt_format': '📄 .SRT (Standard)',
        'ass_format': '🎨 .ASS (Advanced)',
        
        # Messages
        'import_complete': 'Import Complete',
        'import_success': 'Media imported and audio ready for processing.',
        'enhancement_complete': 'Enhancement Complete',
        'enhancement_success': 'Vocals-only audio created:',
        'generation_complete': 'Generation Complete',
        'generation_success': 'Captions generated and saved:',
        'download_complete': 'Download Complete',
        'download_success': 'Model downloaded successfully!',
        'download_failed': 'Download Failed',
        'cancel_confirm': 'Confirm Cancel',
        'cancel_confirm_msg': 'Are you sure you want to cancel the current operation?\n\nAny progress will be lost.',
        'force_cancel_confirm': '⚠️ FORCE CANCEL ⚠️\n\nThis will immediately terminate the current operation.\nThis may cause corrupted files or unstable behavior.\n\nOnly use this if the operation is completely frozen.\n\nAre you absolutely sure?',
        'no_audio': 'No Audio',
        'no_audio_msg': 'No audio file loaded or file was deleted.',
        'no_media': 'No Media',
        'no_media_msg': 'Import audio/video first.',
        'overwrite': 'Overwrite File?',
        'overwrite_msg': 'File exists:\n{}\nOverwrite?',
        'login_required': 'Please login with Google first.',
        'conversion_warning': 'Conversion Warning',
        'conversion_warning_msg': 'Using original file (may be slower).',
        'playback_error': 'Playback Error',
        'colab_timeout': 'Colab Timeout / Crash Detected',
        'colab_timeout_msg': 'No result file appeared in Google Drive after long wait.',
        'network_error': 'Network Error',
        'model_load_error': 'Model Load Error',
        
        # Settings Dialog
        'settings_title': 'NotyCaption Settings - Secure Edition',
        'general_tab': 'General',
        'paths_tab': 'Paths',
        'features_tab': 'Features',
        'advanced_tab': 'Advanced',
        'language_tab': 'Language',
        'visual_theme': 'Visual Theme',
        'system_default': 'System Default (Windows)',
        'light_mode': 'Light Mode',
        'dark_mode': 'Dark Mode (Modern)',
        'ui_scaling': 'UI Scaling',
        'scale_factor': 'Scale Factor:',
        'temp_dir': 'Temporary Files Directory',
        'temp_dir_placeholder': 'Default: System Temp',
        'browse_folder': 'Browse Folder',
        'models_dir': 'Whisper Models Directory',
        'models_dir_placeholder': 'Default: App Root',
        'auto_features': 'Auto Features',
        'auto_enhance': 'Auto-Enhance Audio (Vocals Only)',
        'default_language': 'Default Language:',
        'default_wpl': 'Default Words per Line',
        'words': 'Words:',
        'default_format': 'Default Output Format',
        'format': 'Format:',
        'cancel_options': 'Cancel Options',
        'confirm_cancel': 'Ask for confirmation before canceling',
        'force_cancel_timeout': 'Show force cancel after:',
        'seconds': ' seconds',
        'max_retry': 'Max retry attempts:',
        'ui_options': 'UI Options',
        'minimize_tray': 'Minimize to system tray',
        'show_tooltips': 'Show tooltips',
        'ui_language': 'UI Language:',
        'apply_restart': 'Apply & Restart UI',
        
        # Hardware Detection
        'hardware_acceleration': 'Hardware Acceleration',
        'cuda_available': 'CUDA Available',
        'cuda_not_available': 'CUDA Not Available',
        'gpu_info': 'GPU: {}',
        'cpu_info': 'CPU: {}',
        'memory_info': 'Memory: {:.1f} GB',
        'using_gpu': 'Using GPU Acceleration',
        'using_cpu': 'Using CPU (Fallback Mode)',
    },
    
    'zh': {
        'window_title': 'NotyCaption Pro - NotY215的安全AI字幕生成器',
        'ready': '就绪',
        'processing': '处理中...',
        'canceled': '已取消',
        'completed': '已完成',
        'failed': '失败',
        'edit_captions': '✏️ 编辑字幕',
        'save_exit_edit': '💾 保存并退出编辑',
        'settings': '⚙️ 设置',
        'download_model': '📥 下载 large-v1 模型',
        'login_google': '🔐 使用Google登录（启用在线模式）',
        'import_media': '📁 导入视频/音频文件',
        'browse_output': '📂 浏览输出文件夹',
        'enhance_audio': '🎤 增强音频（仅人声 - Spleeter）',
        'play_pause': '▶️ 播放 / ⏸️ 暂停',
        'playing': '⏸️ 播放中...',
        'paused': '▶️ 播放 / ⏸️ 暂停',
        'generate': '🚀 生成字幕',
        'cancel': '取消操作',
        'force_cancel': '⚠️ 强制取消（紧急）',
        'reopen_notebook': '🔗 重新打开笔记本',
        'copy_url': '📋 复制网址',
        'ai_caption_editor': 'AI驱动字幕编辑器',
        'processing_mode': '处理模式:',
        'language': '语言:',
        'words_per_line': '每行词数:',
        'output_format': '输出格式:',
        'output_folder': '输出文件夹:',
        'status': '状态:',
        'notebook_url': '笔记本网址:',
        'not_available': '不可用',
        'idle': '空闲',
        'speed': '速度:',
        'eta': '剩余时间:',
        'downloading': '下载中...',
        'uploading': '上传中...',
        'waiting': '等待中...',
        'normal_mode': '🖥️ 普通模式（本地Whisper）',
        'online_mode': '☁️ 在线模式（Colab + 云端硬盘）',
        'english_transcribe': '🇺🇸 英语（转录）',
        'japanese_translate': '🇯🇵 日语 → 英语（翻译）',
        'chinese_transcribe': '🇨🇳 中文（转录）',
        'srt_format': '📄 .SRT（标准）',
        'ass_format': '🎨 .ASS（高级）',
        'import_complete': '导入完成',
        'import_success': '媒体已导入，音频准备就绪。',
        'enhancement_complete': '增强完成',
        'enhancement_success': '已创建纯人声音频:',
        'generation_complete': '生成完成',
        'generation_success': '字幕已生成并保存:',
        'download_complete': '下载完成',
        'download_success': '模型下载成功！',
        'download_failed': '下载失败',
        'cancel_confirm': '确认取消',
        'cancel_confirm_msg': '确定要取消当前操作吗？\n\n任何进度都将丢失。',
        'force_cancel_confirm': '⚠️ 强制取消 ⚠️\n\n这将立即终止当前操作。\n可能导致文件损坏或不稳定行为。\n\n仅在操作完全卡顿时使用。\n\n你确定吗？',
        'no_audio': '无音频',
        'no_audio_msg': '未加载音频文件或文件已被删除。',
        'no_media': '无媒体',
        'no_media_msg': '请先导入音频/视频。',
        'overwrite': '覆盖文件？',
        'overwrite_msg': '文件已存在：\n{}\n要覆盖吗？',
        'login_required': '请先使用Google登录。',
        'conversion_warning': '转换警告',
        'conversion_warning_msg': '使用原始文件（可能较慢）。',
        'playback_error': '播放错误',
        'colab_timeout': 'Colab超时/崩溃检测',
        'colab_timeout_msg': '长时间等待后未在Google云端硬盘中找到结果文件。',
        'network_error': '网络错误',
        'model_load_error': '模型加载错误',
        'settings_title': 'NotyCaption设置 - 安全版',
        'general_tab': '常规',
        'paths_tab': '路径',
        'features_tab': '功能',
        'advanced_tab': '高级',
        'language_tab': '语言',
        'visual_theme': '视觉主题',
        'system_default': '系统默认（Windows）',
        'light_mode': '亮色模式',
        'dark_mode': '暗色模式（现代）',
        'ui_scaling': '界面缩放',
        'scale_factor': '缩放比例:',
        'temp_dir': '临时文件目录',
        'temp_dir_placeholder': '默认：系统临时目录',
        'browse_folder': '浏览文件夹',
        'models_dir': 'Whisper模型目录',
        'models_dir_placeholder': '默认：应用根目录',
        'auto_features': '自动功能',
        'auto_enhance': '自动增强音频（仅人声）',
        'default_language': '默认语言:',
        'default_wpl': '默认每行词数',
        'words': '词数:',
        'default_format': '默认输出格式',
        'format': '格式:',
        'cancel_options': '取消选项',
        'confirm_cancel': '取消前询问确认',
        'force_cancel_timeout': '显示强制取消在:',
        'seconds': '秒后',
        'max_retry': '最大重试次数:',
        'ui_options': '界面选项',
        'minimize_tray': '最小化到系统托盘',
        'show_tooltips': '显示提示',
        'ui_language': '界面语言:',
        'apply_restart': '应用并重启界面',
        'hardware_acceleration': '硬件加速',
        'cuda_available': 'CUDA可用',
        'cuda_not_available': 'CUDA不可用',
        'gpu_info': 'GPU: {}',
        'cpu_info': 'CPU: {}',
        'memory_info': '内存: {:.1f} GB',
        'using_gpu': '使用GPU加速',
        'using_cpu': '使用CPU（回退模式）',
    },
    
    'fr': {
        'window_title': 'NotyCaption Pro - Générateur de Sous-titres IA Sécurisé par NotY215',
        'ready': 'Prêt',
        'processing': 'Traitement...',
        'canceled': 'Annulé',
        'completed': 'Terminé',
        'failed': 'Échoué',
        'edit_captions': '✏️ Modifier les sous-titres',
        'save_exit_edit': '💾 Sauvegarder et quitter',
        'settings': '⚙️ Paramètres',
        'download_model': '📥 Télécharger le modèle large-v1',
        'login_google': '🔐 Connexion Google (Mode en ligne)',
        'import_media': '📁 Importer un fichier vidéo/audio',
        'browse_output': '📂 Parcourir le dossier de sortie',
        'enhance_audio': '🎤 Améliorer l\'audio (Voix seulement)',
        'play_pause': '▶️ Lecture / ⏸️ Pause',
        'playing': '⏸️ Lecture...',
        'paused': '▶️ Lecture / ⏸️ Pause',
        'generate': '🚀 Générer les sous-titres',
        'cancel': 'Annuler l\'opération',
        'force_cancel': '⚠️ Annulation forcée (Urgence)',
        'reopen_notebook': '🔗 Rouvrir le notebook',
        'copy_url': '📋 Copier l\'URL',
        'ai_caption_editor': 'Éditeur de sous-titres IA',
        'processing_mode': 'Mode de traitement:',
        'language': 'Langue:',
        'words_per_line': 'Mots par ligne:',
        'output_format': 'Format de sortie:',
        'output_folder': 'Dossier de sortie:',
        'status': 'Statut:',
        'notebook_url': 'URL du notebook:',
        'not_available': 'Non disponible',
        'idle': 'Inactif',
        'speed': 'Vitesse:',
        'eta': 'ETA:',
        'downloading': 'Téléchargement...',
        'uploading': 'Téléversement...',
        'waiting': 'Attente...',
        'normal_mode': '🖥️ Normal (Whisper local)',
        'online_mode': '☁️ En ligne (Colab + Drive)',
        'english_transcribe': '🇺🇸 Anglais (Transcrire)',
        'japanese_translate': '🇯🇵 Japonais → Anglais (Traduire)',
        'french_transcribe': '🇫🇷 Français (Transcrire)',
        'srt_format': '📄 .SRT (Standard)',
        'ass_format': '🎨 .ASS (Avancé)',
        'import_complete': 'Import terminé',
        'import_success': 'Média importé, audio prêt.',
        'enhancement_complete': 'Amélioration terminée',
        'enhancement_success': 'Audio voix seulement créé:',
        'generation_complete': 'Génération terminée',
        'generation_success': 'Sous-titres générés et sauvegardés:',
        'download_complete': 'Téléchargement terminé',
        'download_success': 'Modèle téléchargé avec succès!',
        'download_failed': 'Échec du téléchargement',
        'cancel_confirm': 'Confirmer l\'annulation',
        'cancel_confirm_msg': 'Êtes-vous sûr de vouloir annuler l\'opération?\n\nToute progression sera perdue.',
        'force_cancel_confirm': '⚠️ ANNULATION FORCÉE ⚠️\n\nCela terminera immédiatement l\'opération.\nCela peut causer des fichiers corrompus.\n\nÀ utiliser seulement si l\'opération est bloquée.\n\nÊtes-vous absolument sûr?',
        'settings_title': 'Paramètres NotyCaption - Édition Sécurisée',
        'general_tab': 'Général',
        'paths_tab': 'Chemins',
        'features_tab': 'Fonctionnalités',
        'advanced_tab': 'Avancé',
        'language_tab': 'Langue',
        'visual_theme': 'Thème visuel',
        'system_default': 'Défaut système (Windows)',
        'light_mode': 'Mode clair',
        'dark_mode': 'Mode sombre (Moderne)',
        'ui_scaling': 'Échelle d\'interface',
        'scale_factor': 'Facteur d\'échelle:',
        'temp_dir': 'Dossier temporaire',
        'browse_folder': 'Parcourir',
        'models_dir': 'Dossier des modèles Whisper',
        'auto_features': 'Fonctions automatiques',
        'auto_enhance': 'Amélioration audio auto (voix seulement)',
        'default_language': 'Langue par défaut:',
        'ui_language': 'Langue d\'interface:',
        'apply_restart': 'Appliquer et redémarrer',
    },
    
    'de': {
        'window_title': 'NotyCaption Pro - Sicherer KI-Untertitelgenerator von NotY215',
        'ready': 'Bereit',
        'processing': 'Verarbeitung...',
        'canceled': 'Abgebrochen',
        'completed': 'Abgeschlossen',
        'failed': 'Fehlgeschlagen',
        'edit_captions': '✏️ Untertitel bearbeiten',
        'save_exit_edit': '💾 Speichern & beenden',
        'settings': '⚙️ Einstellungen',
        'download_model': '📥 large-v1 Modell herunterladen',
        'login_google': '🔐 Google Login (Online-Modus)',
        'import_media': '📁 Video/Audio importieren',
        'browse_output': '📂 Ausgabeordner durchsuchen',
        'enhance_audio': '🎤 Audio verbessern (nur Stimme)',
        'play_pause': '▶️ Abspielen / ⏸️ Pause',
        'playing': '⏸️ Wiedergabe...',
        'paused': '▶️ Abspielen / ⏸️ Pause',
        'generate': '🚀 Untertitel generieren',
        'cancel': 'Vorgang abbrechen',
        'force_cancel': '⚠️ Erzwingen (Notfall)',
        'reopen_notebook': '🔗 Notebook neu öffnen',
        'copy_url': '📋 URL kopieren',
        'ai_caption_editor': 'KI-gestützter Untertitel-Editor',
        'processing_mode': 'Verarbeitungsmodus:',
        'language': 'Sprache:',
        'words_per_line': 'Wörter pro Zeile:',
        'output_format': 'Ausgabeformat:',
        'output_folder': 'Ausgabeordner:',
        'status': 'Status:',
        'notebook_url': 'Notebook-URL:',
        'not_available': 'Nicht verfügbar',
        'idle': 'Leerlauf',
        'speed': 'Geschwindigkeit:',
        'eta': 'Verbleibend:',
        'downloading': 'Herunterladen...',
        'uploading': 'Hochladen...',
        'waiting': 'Warten...',
        'normal_mode': '🖥️ Normal (Lokales Whisper)',
        'online_mode': '☁️ Online (Colab + Drive)',
        'english_transcribe': '🇺🇸 Englisch (Transkribieren)',
        'japanese_translate': '🇯🇵 Japanisch → Englisch (Übersetzen)',
        'german_transcribe': '🇩🇪 Deutsch (Transkribieren)',
        'srt_format': '📄 .SRT (Standard)',
        'ass_format': '🎨 .ASS (Erweitert)',
        'settings_title': 'NotyCaption Einstellungen - Sichere Ausgabe',
        'general_tab': 'Allgemein',
        'paths_tab': 'Pfade',
        'features_tab': 'Funktionen',
        'advanced_tab': 'Erweitert',
        'language_tab': 'Sprache',
        'visual_theme': 'Visuelles Thema',
        'system_default': 'Systemstandard (Windows)',
        'light_mode': 'Heller Modus',
        'dark_mode': 'Dunkler Modus (Modern)',
        'ui_scaling': 'UI-Skalierung',
        'scale_factor': 'Skalierungsfaktor:',
        'temp_dir': 'Temporärer Ordner',
        'browse_folder': 'Durchsuchen',
        'models_dir': 'Whisper-Modelle Ordner',
        'auto_features': 'Auto-Funktionen',
        'auto_enhance': 'Audio automatisch verbessern (nur Stimme)',
        'default_language': 'Standardsprache:',
        'ui_language': 'UI-Sprache:',
        'apply_restart': 'Anwenden & Neustarten',
    },
    
    'hi': {
        'window_title': 'NotyCaption Pro - NotY215 द्वारा सुरक्षित AI कैप्शन जनरेटर',
        'ready': 'तैयार',
        'processing': 'प्रक्रिया चल रही है...',
        'canceled': 'रद्द किया गया',
        'completed': 'पूर्ण हुआ',
        'failed': 'विफल',
        'edit_captions': '✏️ कैप्शन संपादित करें',
        'save_exit_edit': '💾 सहेजें और बाहर निकलें',
        'settings': '⚙️ सेटिंग्स',
        'download_model': '📥 large-v1 मॉडल डाउनलोड करें',
        'login_google': '🔐 Google से लॉगिन करें (ऑनलाइन मोड)',
        'import_media': '📁 वीडियो/ऑडियो फ़ाइल आयात करें',
        'browse_output': '📂 आउटपुट फ़ोल्डर ब्राउज़ करें',
        'enhance_audio': '🎤 ऑडियो बढ़ाएं (केवल स्वर)',
        'play_pause': '▶️ चलाएं / ⏸️ रोकें',
        'playing': '⏸️ चल रहा है...',
        'paused': '▶️ चलाएं / ⏸️ रोकें',
        'generate': '🚀 कैप्शन जनरेट करें',
        'cancel': 'ऑपरेशन रद्द करें',
        'force_cancel': '⚠️ जबरन रद्द करें (आपातकालीन)',
        'reopen_notebook': '🔗 नोटबुक फिर से खोलें',
        'copy_url': '📋 URL कॉपी करें',
        'ai_caption_editor': 'AI-संचालित कैप्शन संपादक',
        'processing_mode': 'प्रसंस्करण मोड:',
        'language': 'भाषा:',
        'words_per_line': 'प्रति पंक्ति शब्द:',
        'output_format': 'आउटपुट फॉर्मेट:',
        'output_folder': 'आउटपुट फ़ोल्डर:',
        'status': 'स्थिति:',
        'notebook_url': 'नोटबुक URL:',
        'not_available': 'उपलब्ध नहीं',
        'idle': 'निष्क्रिय',
        'speed': 'गति:',
        'eta': 'शेष समय:',
        'downloading': 'डाउनलोड हो रहा है...',
        'uploading': 'अपलोड हो रहा है...',
        'waiting': 'प्रतीक्षा कर रहा है...',
        'normal_mode': '🖥️ सामान्य (स्थानीय Whisper)',
        'online_mode': '☁️ ऑनलाइन (Colab + Drive)',
        'english_transcribe': '🇺🇸 अंग्रेज़ी (ट्रांसक्राइब)',
        'hindi_transcribe': '🇮🇳 हिंदी (ट्रांसक्राइब)',
        'settings_title': 'NotyCaption सेटिंग्स - सुरक्षित संस्करण',
        'general_tab': 'सामान्य',
        'paths_tab': 'पथ',
        'features_tab': 'सुविधाएँ',
        'advanced_tab': 'उन्नत',
        'language_tab': 'भाषा',
        'ui_language': 'इंटरफ़ेस भाषा:',
    },
    
    'bn': {
        'window_title': 'NotyCaption Pro - NotY215 দ্বারা সুরক্ষিত AI ক্যাপশন জেনারেটর',
        'ready': 'প্রস্তুত',
        'processing': 'প্রক্রিয়াকরণ চলছে...',
        'canceled': 'বাতিল করা হয়েছে',
        'completed': 'সম্পন্ন হয়েছে',
        'failed': 'ব্যর্থ হয়েছে',
        'edit_captions': '✏️ ক্যাপশন সম্পাদনা করুন',
        'save_exit_edit': '💾 সংরক্ষণ করুন ও প্রস্থান করুন',
        'settings': '⚙️ সেটিংস',
        'download_model': '📥 large-v1 মডেল ডাউনলোড করুন',
        'login_google': '🔐 Google দিয়ে লগইন করুন (অনলাইন মোড)',
        'import_media': '📁 ভিডিও/অডিও ফাইল ইম্পোর্ট করুন',
        'browse_output': '📂 আউটপুট ফোল্ডার ব্রাউজ করুন',
        'enhance_audio': '🎤 অডিও উন্নত করুন (শুধু কণ্ঠ)',
        'play_pause': '▶️ চালান / ⏸️ বিরাম',
        'playing': '⏸️ চলছে...',
        'paused': '▶️ চালান / ⏸️ বিরাম',
        'generate': '🚀 ক্যাপশন জেনারেট করুন',
        'cancel': 'অপারেশন বাতিল করুন',
        'force_cancel': '⚠️ জোর করে বাতিল (জরুরি)',
        'reopen_notebook': '🔗 নোটবুক পুনরায় খুলুন',
        'copy_url': '📋 URL কপি করুন',
        'ai_caption_editor': 'AI-চালিত ক্যাপশন সম্পাদক',
        'processing_mode': 'প্রক্রিয়াকরণ মোড:',
        'language': 'ভাষা:',
        'words_per_line': 'প্রতি লাইনে শব্দ:',
        'output_format': 'আউটপুট ফরম্যাট:',
        'output_folder': 'আউটপুট ফোল্ডার:',
        'status': 'অবস্থা:',
        'notebook_url': 'নোটবুক URL:',
        'not_available': 'উপলব্ধ নয়',
        'idle': 'নিষ্ক্রিয়',
        'speed': 'গতি:',
        'eta': 'অবশিষ্ট সময়:',
        'downloading': 'ডাউনলোড হচ্ছে...',
        'uploading': 'আপলোড হচ্ছে...',
        'waiting': 'অপেক্ষা করছে...',
        'normal_mode': '🖥️ সাধারণ (স্থানীয় Whisper)',
        'online_mode': '☁️ অনলাইন (Colab + Drive)',
        'english_transcribe': '🇺🇸 ইংরেজি (ট্রান্সক্রাইব)',
        'bengali_transcribe': '🇧🇩 বাংলা (ট্রান্সক্রাইব)',
        'settings_title': 'NotyCaption সেটিংস - সুরক্ষিত সংস্করণ',
    },
    
    'ur': {
        'window_title': 'NotyCaption Pro - NotY215 کا محفوظ AI کیپشن جنریٹر',
        'ready': 'تیار',
        'processing': 'پروسیسنگ جاری ہے...',
        'canceled': 'منسوخ کر دیا گیا',
        'completed': 'مکمل ہو گیا',
        'failed': 'ناکام',
        'edit_captions': '✏️ کیپشن میں ترمیم کریں',
        'save_exit_edit': '💾 محفوظ کریں اور باہر جائیں',
        'settings': '⚙️ ترتیبات',
        'download_model': '📥 large-v1 ماڈل ڈاؤن لوڈ کریں',
        'login_google': '🔐 Google سے لاگ ان کریں (آن لائن موڈ)',
        'import_media': '📁 ویڈیو/آڈیو فائل درآمد کریں',
        'browse_output': '📂 آؤٹ پٹ فولڈر براؤز کریں',
        'enhance_audio': '🎤 آڈیو بہتر بنائیں (صرف آواز)',
        'play_pause': '▶️ چلائیں / ⏸️ روکیں',
        'playing': '⏸️ چل رہا ہے...',
        'paused': '▶️ چلائیں / ⏸️ روکیں',
        'generate': '🚀 کیپشن جنریٹ کریں',
        'cancel': 'آپریشن منسوخ کریں',
        'force_cancel': '⚠️ جبری منسوخی (ہنگامی)',
        'reopen_notebook': '🔗 نوٹ بک دوبارہ کھولیں',
        'copy_url': '📋 URL کاپی کریں',
        'ai_caption_editor': 'AI سے چلنے والا کیپشن ایڈیٹر',
        'processing_mode': 'پروسیسنگ موڈ:',
        'language': 'زبان:',
        'words_per_line': 'فی سطر الفاظ:',
        'output_format': 'آؤٹ پٹ فارمیٹ:',
        'output_folder': 'آؤٹ پٹ فولڈر:',
        'status': 'حالت:',
        'notebook_url': 'نوٹ بک URL:',
        'not_available': 'دستیاب نہیں',
        'idle': 'غیر فعال',
        'speed': 'رفتار:',
        'eta': 'متوقع وقت:',
        'downloading': 'ڈاؤن لوڈ ہو رہا ہے...',
        'uploading': 'اپ لوڈ ہو رہا ہے...',
        'waiting': 'انتظار کر رہا ہے...',
        'normal_mode': '🖥️ عام (مقامی Whisper)',
        'online_mode': '☁️ آن لائن (Colab + Drive)',
        'english_transcribe': '🇺🇸 انگریزی (ٹرانسکرائب)',
        'urdu_transcribe': '🇵🇰 اردو (ٹرانسکرائب)',
        'settings_title': 'NotyCaption ترتیبات - محفوظ ورژن',
    },
    
    'ja': {
        'window_title': 'NotyCaption Pro - NotY215による安全なAIキャプションジェネレーター',
        'ready': '準備完了',
        'processing': '処理中...',
        'canceled': 'キャンセルされました',
        'completed': '完了しました',
        'failed': '失敗しました',
        'edit_captions': '✏️ キャプションを編集',
        'save_exit_edit': '💾 保存して終了',
        'settings': '⚙️ 設定',
        'download_model': '📥 large-v1モデルをダウンロード',
        'login_google': '🔐 Googleでログイン（オンラインモード）',
        'import_media': '📁 動画/音声ファイルをインポート',
        'browse_output': '📂 出力フォルダを参照',
        'enhance_audio': '🎤 音声を強化（ボーカルのみ）',
        'play_pause': '▶️ 再生 / ⏸️ 一時停止',
        'playing': '⏸️ 再生中...',
        'paused': '▶️ 再生 / ⏸️ 一時停止',
        'generate': '🚀 キャプションを生成',
        'cancel': '操作をキャンセル',
        'force_cancel': '⚠️ 強制キャンセル（緊急）',
        'reopen_notebook': '🔗 ノートブックを再開',
        'copy_url': '📋 URLをコピー',
        'ai_caption_editor': 'AI搭載キャプションエディタ',
        'processing_mode': '処理モード:',
        'language': '言語:',
        'words_per_line': '1行あたりの単語数:',
        'output_format': '出力形式:',
        'output_folder': '出力フォルダ:',
        'status': 'ステータス:',
        'notebook_url': 'ノートブックURL:',
        'not_available': '利用できません',
        'idle': 'アイドル',
        'speed': '速度:',
        'eta': '残り時間:',
        'downloading': 'ダウンロード中...',
        'uploading': 'アップロード中...',
        'waiting': '待機中...',
        'normal_mode': '🖥️ 通常（ローカルWhisper）',
        'online_mode': '☁️ オンライン（Colab + Drive）',
        'english_transcribe': '🇺🇸 英語（文字起こし）',
        'japanese_translate': '🇯🇵 日本語 → 英語（翻訳）',
        'japanese_transcribe': '🇯🇵 日本語（文字起こし）',
        'settings_title': 'NotyCaption設定 - セキュアエディション',
    }
}

# ========================================
# HARDWARE DETECTION - IMPROVED VERSION
# ========================================
class HardwareDetector:
    """Detect and report hardware capabilities with multiple fallback methods"""
    
    def __init__(self):
        self.cuda_available = False
        self.rocm_available = False
        self.opencl_available = False
        self.gpu_info = []
        self.gpu_memory = []
        self.cpu_info = ""
        self.cpu_cores = 0
        self.cpu_threads = 0
        self.total_ram = 0
        self.available_ram = 0
        self.ram_usage = 0
        self.disk_free = 0
        self.disk_total = 0
        self.tensorflow_gpu = False
        self.pytorch_gpu = False
        self.detect_hardware()
        
    def detect_hardware(self):
        """Detect all hardware components with multiple fallback methods"""
        self.detect_cpu()
        self.detect_ram()
        self.detect_disk()
        self.detect_gpu_tensorflow()
        self.detect_gpu_pytorch()
        self.detect_gpu_gputil()
        self.detect_gpu_nvidia_smi()
        self.detect_gpu_wmi()
        self.detect_opencl()
        
    def detect_cpu(self):
        """Detect CPU information with multiple methods"""
        try:
            # Method 1: cpuinfo (most detailed)
            import cpuinfo
            cpu_info_dict = cpuinfo.get_cpu_info()
            self.cpu_info = cpu_info_dict.get('brand_raw', 'Unknown CPU')
            self.cpu_cores = cpu_info_dict.get('count', 0)
            if 'hz_actual_friendly' in cpu_info_dict:
                self.cpu_info += f" @ {cpu_info_dict['hz_actual_friendly']}"
        except:
            try:
                # Method 2: platform module
                import platform
                self.cpu_info = platform.processor()
                if not self.cpu_info or self.cpu_info == '':
                    self.cpu_info = platform.machine()
                
                # Method 3: multiprocessing for core count
                import multiprocessing
                self.cpu_cores = multiprocessing.cpu_count()
                self.cpu_threads = self.cpu_cores
                
                # Method 4: psutil for more details
                try:
                    import psutil
                    cpu_freq = psutil.cpu_freq()
                    if cpu_freq:
                        self.cpu_info += f" @ {cpu_freq.current:.0f}MHz"
                    self.cpu_cores = psutil.cpu_count(logical=False)
                    self.cpu_threads = psutil.cpu_count(logical=True)
                except:
                    pass
            except:
                self.cpu_info = "Unknown CPU"
                self.cpu_cores = 0
                
        logger.info(f"CPU detected: {self.cpu_info} ({self.cpu_cores} cores)")
        
    def detect_ram(self):
        """Detect RAM information"""
        try:
            import psutil
            mem = psutil.virtual_memory()
            self.total_ram = mem.total / (1024**3)  # GB
            self.available_ram = mem.available / (1024**3)
            self.ram_usage = mem.percent
        except:
            try:
                # Fallback method for RAM detection
                import os
                if os.name == 'nt':  # Windows
                    import ctypes
                    kernel32 = ctypes.windll.kernel32
                    class MEMORYSTATUSEX(ctypes.Structure):
                        _fields_ = [
                            ("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                        ]
                    memoryStatus = MEMORYSTATUSEX()
                    memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                    if kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus)):
                        self.total_ram = memoryStatus.ullTotalPhys / (1024**3)
                        self.available_ram = memoryStatus.ullAvailPhys / (1024**3)
                else:  # Linux/Mac
                    with open('/proc/meminfo', 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            if 'MemTotal' in line:
                                self.total_ram = int(line.split()[1]) / (1024**2)  # Convert KB to GB
                            if 'MemAvailable' in line:
                                self.available_ram = int(line.split()[1]) / (1024**2)
            except:
                self.total_ram = 0
                self.available_ram = 0
                
        logger.info(f"RAM detected: {self.total_ram:.1f}GB total, {self.available_ram:.1f}GB available")
        
    def detect_disk(self):
        """Detect disk space"""
        try:
            import psutil
            disk = psutil.disk_usage('/')
            self.disk_total = disk.total / (1024**3)
            self.disk_free = disk.free / (1024**3)
        except:
            try:
                import shutil
                total, used, free = shutil.disk_usage('/')
                self.disk_total = total / (1024**3)
                self.disk_free = free / (1024**3)
            except:
                self.disk_total = 0
                self.disk_free = 0
                
    def detect_gpu_tensorflow(self):
        """Detect GPU using TensorFlow"""
        try:
            import tensorflow as tf
            gpus = tf.config.list_physical_devices('GPU')
            if gpus:
                self.tensorflow_gpu = True
                self.cuda_available = True
                for i, gpu in enumerate(gpus):
                    try:
                        # Try to get GPU details
                        details = tf.config.experimental.get_device_details(gpu)
                        if details:
                            gpu_name = details.get('device_name', f'GPU {i}')
                            compute_capability = details.get('compute_capability', '')
                            if compute_capability:
                                gpu_name += f" (CC {compute_capability})"
                        else:
                            gpu_name = str(gpu)
                    except:
                        gpu_name = str(gpu)
                    
                    # Get memory info if possible
                    try:
                        memory_info = tf.config.experimental.get_memory_info(f'GPU:{i}')
                        if memory_info and 'current' in memory_info:
                            memory_mb = memory_info['current'] / (1024**2)
                            gpu_name += f" - {memory_mb:.0f}MB used"
                    except:
                        pass
                        
                    self.gpu_info.append(gpu_name)
                    logger.info(f"TensorFlow GPU detected: {gpu_name}")
        except:
            self.tensorflow_gpu = False
            
    def detect_gpu_pytorch(self):
        """Detect GPU using PyTorch"""
        try:
            import torch
            if torch.cuda.is_available():
                self.pytorch_gpu = True
                self.cuda_available = True
                count = torch.cuda.device_count()
                for i in range(count):
                    try:
                        gpu_name = torch.cuda.get_device_name(i)
                        try:
                            memory_allocated = torch.cuda.memory_allocated(i) / (1024**2)
                            memory_reserved = torch.cuda.memory_reserved(i) / (1024**2)
                            gpu_name += f" - {memory_allocated:.0f}MB/{memory_reserved:.0f}MB"
                        except:
                            pass
                        if gpu_name not in self.gpu_info:
                            self.gpu_info.append(gpu_name)
                            logger.info(f"PyTorch GPU detected: {gpu_name}")
                    except:
                        pass
        except:
            self.pytorch_gpu = False
            
    def detect_gpu_gputil(self):
        """Detect GPU using GPUtil (most detailed)"""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                self.cuda_available = True
                for gpu in gpus:
                    gpu_name = f"{gpu.name}"
                    if hasattr(gpu, 'memoryTotal') and gpu.memoryTotal:
                        gpu_name += f" - {gpu.memoryTotal:.0f}MB"
                    if hasattr(gpu, 'temperature') and gpu.temperature:
                        gpu_name += f" - {gpu.temperature:.0f}°C"
                    if hasattr(gpu, 'load') and gpu.load:
                        gpu_name += f" - Load: {gpu.load*100:.0f}%"
                    
                    # Store memory info separately
                    if hasattr(gpu, 'memoryTotal'):
                        self.gpu_memory.append({
                            'name': gpu.name,
                            'total': gpu.memoryTotal,
                            'used': gpu.memoryUsed if hasattr(gpu, 'memoryUsed') else 0,
                            'free': gpu.memoryFree if hasattr(gpu, 'memoryFree') else 0
                        })
                    
                    if gpu_name not in self.gpu_info:
                        self.gpu_info.append(gpu_name)
                        logger.info(f"GPUtil GPU detected: {gpu_name}")
        except:
            pass
            
    def detect_gpu_nvidia_smi(self):
        """Detect GPU using nvidia-smi command line"""
        if self.gpu_info:  # Already have GPU info
            return
            
        try:
            import subprocess
            import shutil
            
            # Check if nvidia-smi is available
            nvidia_smi_path = shutil.which('nvidia-smi')
            if nvidia_smi_path:
                # Get GPU info
                result = subprocess.run(
                    [nvidia_smi_path, '--query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu', '--format=csv,noheader'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            parts = [p.strip() for p in line.split(',')]
                            if len(parts) >= 1:
                                gpu_name = parts[0]
                                if len(parts) >= 2:
                                    gpu_name += f" - {parts[1]}"
                                if len(parts) >= 5:
                                    gpu_name += f" - {parts[4]}°C"
                                self.gpu_info.append(gpu_name)
                                self.cuda_available = True
                                logger.info(f"nvidia-smi GPU detected: {gpu_name}")
        except:
            pass
            
    def detect_gpu_wmi(self):
        """Detect GPU using WMI on Windows"""
        if self.gpu_info or not sys.platform.startswith('win'):
            return
            
        try:
            import wmi
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                gpu_name = gpu.Name
                if gpu.AdapterRAM:
                    ram_gb = int(gpu.AdapterRAM) / (1024**3)
                    gpu_name += f" - {ram_gb:.1f}GB"
                self.gpu_info.append(gpu_name)
                # Could be Intel, AMD, or NVIDIA
                if 'nvidia' in gpu_name.lower() or 'amd' in gpu_name.lower():
                    self.cuda_available = True
                logger.info(f"WMI GPU detected: {gpu_name}")
        except:
            pass
            
    def detect_opencl(self):
        """Detect OpenCL capability"""
        try:
            import pyopencl as cl
            platforms = cl.get_platforms()
            if platforms:
                self.opencl_available = True
                for platform in platforms:
                    devices = platform.get_devices()
                    for device in devices:
                        if device.type == cl.device_type.GPU:
                            gpu_name = f"OpenCL: {device.name}"
                            if gpu_name not in self.gpu_info:
                                self.gpu_info.append(gpu_name)
                                logger.info(f"OpenCL GPU detected: {gpu_name}")
        except:
            self.opencl_available = False
            
    def get_acceleration_status(self):
        """Get human-readable acceleration status with recommendations"""
        if self.cuda_available:
            return "gpu", f"✅ GPU Acceleration Available\n{chr(10).join(self.gpu_info)}"
        elif self.rocm_available:
            return "gpu", f"✅ ROCm Acceleration Available\n{chr(10).join(self.gpu_info)}"
        elif self.opencl_available:
            return "gpu", f"⚠️ OpenCL Available (Limited Acceleration)\n{chr(10).join(self.gpu_info)}"
        else:
            cpu_rec = self.get_cpu_recommendation()
            return "cpu", f"⚠️ CPU Mode Only\nCPU: {self.cpu_info}\n{cpu_rec}"
            
    def get_cpu_recommendation(self):
        """Get CPU-based recommendations"""
        if self.cpu_cores >= 8:
            return "✓ High-performance CPU detected - Good for processing"
        elif self.cpu_cores >= 4:
            return "✓ Medium-performance CPU - Will work but may be slower"
        else:
            return "! Low-performance CPU - Consider using online mode with GPU"
            
    def get_memory_status(self):
        """Get memory status with warnings"""
        status = f"RAM: {self.available_ram:.1f}GB / {self.total_ram:.1f}GB ({self.ram_usage:.0f}% used)"
        if self.available_ram < 2:
            status += "\n⚠️ Low memory! Close other applications"
        elif self.available_ram < 4:
            status += "\n⚠️ Limited memory available"
        return status
        
    def get_disk_status(self):
        """Get disk status"""
        return f"Disk: {self.disk_free:.1f}GB free / {self.disk_total:.1f}GB total"
        
    def get_detailed_info(self):
        """Get detailed hardware info for display"""
        info = []
        info.append("=" * 50)
        info.append("HARDWARE DETECTION REPORT")
        info.append("=" * 50)
        
        # CPU Info
        info.append(f"\n📌 CPU:")
        info.append(f"   Model: {self.cpu_info}")
        info.append(f"   Cores: {self.cpu_cores} physical, {self.cpu_threads} logical")
        
        # RAM Info
        info.append(f"\n📌 Memory:")
        info.append(f"   Total: {self.total_ram:.1f} GB")
        info.append(f"   Available: {self.available_ram:.1f} GB")
        info.append(f"   Usage: {self.ram_usage:.0f}%")
        
        # Disk Info
        info.append(f"\n📌 Storage:")
        info.append(self.get_disk_status())
        
        # GPU Info
        info.append(f"\n📌 Graphics:")
        if self.gpu_info:
            for i, gpu in enumerate(self.gpu_info, 1):
                info.append(f"   GPU {i}: {gpu}")
                
            # Memory details if available
            if self.gpu_memory:
                for mem in self.gpu_memory:
                    info.append(f"   VRAM: {mem['used']:.0f}MB / {mem['total']:.0f}MB used")
        else:
            info.append("   No GPU detected")
            
        # Acceleration Capabilities
        info.append(f"\n📌 Acceleration:")
        info.append(f"   CUDA: {'✅ Available' if self.cuda_available else '❌ Not Available'}")
        info.append(f"   ROCm: {'✅ Available' if self.rocm_available else '❌ Not Available'}")
        info.append(f"   OpenCL: {'✅ Available' if self.opencl_available else '❌ Not Available'}")
        info.append(f"   TensorFlow GPU: {'✅ Yes' if self.tensorflow_gpu else '❌ No'}")
        info.append(f"   PyTorch GPU: {'✅ Yes' if self.pytorch_gpu else '❌ No'}")
        
        # Recommendations
        info.append(f"\n📌 Recommendations:")
        accel_type, accel_msg = self.get_acceleration_status()
        info.append(f"   {accel_msg}")
        
        info.append("=" * 50)
        return info
        
    def get_performance_estimate(self):
        """Get estimated performance for different tasks"""
        if self.cuda_available:
            return {
                'transcription': 'Very Fast (GPU accelerated)',
                'enhancement': 'Fast',
                'model_download': 'Limited by internet speed'
            }
        elif self.cpu_cores >= 8:
            return {
                'transcription': 'Fast (Multi-core CPU)',
                'enhancement': 'Moderate',
                'model_download': 'Limited by internet speed'
            }
        elif self.cpu_cores >= 4:
            return {
                'transcription': 'Moderate',
                'enhancement': 'Slow',
                'model_download': 'Limited by internet speed'
            }
        else:
            return {
                'transcription': 'Slow - Use online mode',
                'enhancement': 'Very Slow - Use online mode',
                'model_download': 'Limited by internet speed'
            }

# Initialize global hardware detector (after logger is defined)
try:
    hardware_detector = HardwareDetector()
    logger.info("Hardware detector initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize hardware detector: {e}")
    # Create a minimal fallback
    class MinimalHardwareDetector:
        def get_acceleration_status(self): return "cpu", "⚠️ Hardware detection failed"
        def get_memory_status(self): return "Memory: Unknown"
        def get_detailed_info(self): return ["Hardware detection failed"]
        def get_performance_estimate(self): return {}
    hardware_detector = MinimalHardwareDetector()

# ========================================
# CONFIGURATION
# ========================================
APP_NAME = "NotyCaption"
APP_AUTHOR = "NotY215"

# Get app data directory for settings
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    if platform.system() == "Windows":
        APP_DATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), f"{APP_NAME}Saves")
    else:
        # Linux/Mac fallback
        APP_DATA_DIR = os.path.join(os.path.expanduser('~'), f".{APP_NAME.lower()}saves")
else:
    # Running in development
    APP_DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Create app data directory if it doesn't exist
os.makedirs(APP_DATA_DIR, exist_ok=True)

SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.notcapz")
KEY_FILE = os.path.join(APP_DATA_DIR, "key.notcapz")
SESSION_FILE = os.path.join(APP_DATA_DIR, "session.json")
TOKEN_FILE = os.path.join(APP_DATA_DIR, "token.json")
CLIENT_JSON = os.path.join(APP_DATA_DIR, "client.json")
CLIENT_ENCRYPTED = os.path.join(APP_DATA_DIR, "client.notycapz")

# ========================================
# LOGGING SETUP
# ========================================
def setup_logging():
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
        force=True
    )
    logger = logging.getLogger("NotyCaption")
    logger.info("=== NotyCaption Secure Launch 2026 ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Log file: {log_file}")
    logger.info(f"App data directory: {APP_DATA_DIR}")
    logger.info(f"PyInstaller frozen: {getattr(sys, 'frozen', False)}")
    logger.info(f"Executable path: {sys.executable if getattr(sys, 'frozen', False) else 'dev mode'}")
    logger.info(f"Client mode: {'EXE (encrypted)' if os.path.exists(CLIENT_ENCRYPTED) else 'Dev (plain)'}")
    
    # Hardware detection (now using the global hardware_detector)
    try:
        accel_type, accel_info = hardware_detector.get_acceleration_status()
        logger.info(f"Hardware acceleration: {accel_type}")
        logger.info(f"Hardware info: {accel_info}")
        logger.info(f"Memory: {hardware_detector.get_memory_status()}")
    except:
        logger.info("Hardware detection not available")
    
    return logger

logger = setup_logging()

# ========================================
# TRANSLATION HELPER
# ========================================
class Translator:
    """Handle UI translations"""
    
    def __init__(self, language='en'):
        self.language = language
        self.translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])
        
    def tr(self, key):
        """Translate a key"""
        return self.translations.get(key, TRANSLATIONS['en'].get(key, key))
        
    def set_language(self, language):
        """Change language"""
        self.language = language
        self.translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])
        
    def get_available_languages(self):
        """Get list of available languages"""
        return list(TRANSLATIONS.keys())

# Global translator instance
_translator = Translator()

def tr(key):
    """Global translate function"""
    return _translator.tr(key)

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
# SESSION MANAGEMENT
# ========================================
class SessionManager:
    """Manages session persistence for crash recovery"""
    
    def __init__(self):
        self.session_file = SESSION_FILE
        self._lock = threading.Lock()
        logger.info(f"Session manager initialized with file: {self.session_file}")
        
    def save_session(self, session_data):
        """Save current session data"""
        with self._lock:
            try:
                # Add timestamp
                session_data['last_saved'] = datetime.datetime.now().isoformat()
                session_data['app_version'] = "2026.1.0"
                
                with open(self.session_file, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2)
                logger.info("Session saved successfully")
                return True
            except Exception as e:
                logger.error(f"Failed to save session: {e}")
                return False
                
    def load_session(self):
        """Load last saved session"""
        with self._lock:
            try:
                if os.path.exists(self.session_file):
                    with open(self.session_file, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                    logger.info("Session loaded successfully")
                    return session_data
                else:
                    logger.info("No session file found")
                    return None
            except Exception as e:
                logger.error(f"Failed to load session: {e}")
                return None
                
    def clear_session(self):
        """Clear current session"""
        with self._lock:
            try:
                if os.path.exists(self.session_file):
                    os.remove(self.session_file)
                    logger.info("Session cleared")
                return True
            except Exception as e:
                logger.error(f"Failed to clear session: {e}")
                return False
                
    def save_operation_state(self, operation_type, data):
        """Save ongoing operation state for recovery"""
        session = self.load_session() or {}
        if 'operations' not in session:
            session['operations'] = []
        
        # Remove old operations of same type
        session['operations'] = [op for op in session['operations'] if op.get('type') != operation_type]
        
        # Add new operation
        operation = {
            'type': operation_type,
            'data': data,
            'timestamp': datetime.datetime.now().isoformat()
        }
        session['operations'].append(operation)
        
        self.save_session(session)
        
    def get_operation_state(self, operation_type):
        """Get saved operation state"""
        session = self.load_session()
        if session and 'operations' in session:
            for op in session['operations']:
                if op.get('type') == operation_type:
                    return op.get('data')
        return None
        
    def clear_operation_state(self, operation_type):
        """Clear operation state"""
        session = self.load_session()
        if session and 'operations' in session:
            session['operations'] = [op for op in session['operations'] if op.get('type') != operation_type]
            self.save_session(session)

# ========================================
# ENCRYPTION UTILS
# ========================================
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
            # Fallback to app data directory
            key_path = KEY_FILE
            if os.path.exists(key_path):
                with open(key_path, "rb") as f:
                    key_data = f.read()
                logger.info("Fallback key loaded from app data")
                return key_data
            else:
                raise FileNotFoundError(f"Encryption key missing")

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key_data = f.read()
        logger.info("Local dev key loaded")
        return key_data

    logger.info("No key found - generating new one")
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
    logger.info(f"Settings saved securely to {SETTINGS_FILE}")

def load_settings():
    defaults = {
        "ui_scale": "100%",
        "theme": "Dark",
        "temp_dir": tempfile.gettempdir(),
        "models_dir": APP_DATA_DIR,
        "last_mode": "normal",
        "auto_enhance": False,
        "default_lang": tr('english_transcribe'),
        "force_cancel_timeout": 30,
        "max_retry_attempts": 5,
        "confirm_cancel": True,
        "minimize_to_tray": False,
        "show_tooltips": True,
        "words_per_line": 5,
        "output_format": tr('srt_format'),
        "last_input_file": "",
        "last_output_folder": "",
        "window_geometry": None,
        "window_state": None,
        "language": "en"
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
            
    # Fallback to app data directory
    if os.path.exists(CLIENT_ENCRYPTED):
        try:
            with open(CLIENT_ENCRYPTED, "r", encoding='utf-8') as f:
                encrypted_b64 = f.read().strip()
            decrypted = decrypt_data(encrypted_b64)
            if decrypted and "installed" in decrypted:
                logger.info("Client secrets loaded from app data")
                return decrypted
        except Exception as e:
            logger.error(f"Failed to load client secrets from app data: {e}")
            
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
# WHISPER TRANSCRIPTION WITH PROGRESS
# ========================================
class ProgressWhisper:
    """Wrapper for Whisper that provides real progress updates"""
    
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self._canceled = False
        self._lock = threading.Lock()
        
    def cancel(self):
        with self._lock:
            self._canceled = True
            
    def is_canceled(self):
        with self._lock:
            return self._canceled
            
    def transcribe_with_progress(self, model, audio_path, **kwargs):
        """Transcribe with progress updates"""
        import tqdm
        import whisper
        import numpy as np
        
        # Load audio and compute Mel spectrogram
        audio = whisper.load_audio(audio_path)
        audio_length = len(audio) / whisper.audio.SAMPLE_RATE
        
        # Get model dimensions
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        content_frames = mel.shape[-1]
        
        # Detect language if not specified
        if kwargs.get('language') is None:
            segment, _ = model.detect_language(mel[:1])
            kwargs['language'] = segment[0][0]
            if self.progress_callback:
                self.progress_callback(5, f"Detected language: {kwargs['language']}")
                
        # Prepare for decoding
        options = whisper.DecodingOptions(
            task=kwargs.get('task', 'transcribe'),
            language=kwargs.get('language'),
            without_timestamps=False,
            fp16=model.device == 'cuda'
        )
        
        # Run transcription with word timestamps
        result = whisper.transcribe(
            model,
            audio,
            task=kwargs.get('task', 'transcribe'),
            language=kwargs.get('language'),
            word_timestamps=kwargs.get('word_timestamps', True),
            verbose=False
        )
        
        # Calculate progress based on segments
        total_segments = len(result['segments'])
        for i, segment in enumerate(result['segments']):
            if self.is_canceled():
                raise Exception("Transcription canceled by user")
                
            if self.progress_callback:
                # Progress from 20% to 80% during segment processing
                progress = 20 + int((i / total_segments) * 60)
                self.progress_callback(progress, f"Processing segment {i+1}/{total_segments}")
                
        return result

# ========================================
# SETTINGS DIALOG
# ========================================
class SettingsDialog(QDialog):
    settingsChanged = pyqtSignal(dict)

    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr('settings_title'))
        self.setFixedSize(700, 800)
        self.current_settings = current_settings
        self.parent_window = parent
        lay = QVBoxLayout()
        self.setLayout(lay)

        # Create tab widget
        tabs = QTabWidget()
        lay.addWidget(tabs)

        # ===== General Tab =====
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
        if th == "Windows Default": self.rb_win.setChecked(True)
        elif th == "Light": self.rb_light.setChecked(True)
        else: self.rb_dark.setChecked(True)

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

        # ===== Paths Tab =====
        paths_tab = QWidget()
        paths_layout = QVBoxLayout()
        paths_tab.setLayout(paths_layout)

        tmp_gb = QGroupBox(tr('temp_dir'))
        tmp_lay = QHBoxLayout()
        self.tmp_edit = QLineEdit(current_settings.get("temp_dir", tempfile.gettempdir()))
        self.tmp_edit.setPlaceholderText(tr('temp_dir_placeholder'))
        tmp_btn = QPushButton(tr('browse_folder'))
        tmp_btn.clicked.connect(self.browse_temp)
        tmp_lay.addWidget(self.tmp_edit)
        tmp_lay.addWidget(tmp_btn)
        tmp_gb.setLayout(tmp_lay)
        paths_layout.addWidget(tmp_gb)

        mod_gb = QGroupBox(tr('models_dir'))
        mod_lay = QHBoxLayout()
        self.mod_edit = QLineEdit(current_settings.get("models_dir", APP_DATA_DIR))
        self.mod_edit.setPlaceholderText(tr('models_dir_placeholder'))
        mod_btn = QPushButton(tr('browse_folder'))
        mod_btn.clicked.connect(self.browse_models)
        mod_lay.addWidget(self.mod_edit)
        mod_lay.addWidget(mod_btn)
        mod_gb.setLayout(mod_lay)
        paths_layout.addWidget(mod_gb)

        paths_layout.addStretch()

        # ===== Features Tab =====
        features_tab = QWidget()
        features_layout = QVBoxLayout()
        features_tab.setLayout(features_layout)

        auto_gb = QGroupBox(tr('auto_features'))
        auto_lay = QVBoxLayout()
        self.cb_auto_enhance = QRadioButton(tr('auto_enhance'))
        self.cb_auto_enhance.setChecked(current_settings.get("auto_enhance", False))
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
        
        features_layout.addStretch()

        # ===== Language Tab =====
        language_tab = QWidget()
        language_layout = QVBoxLayout()
        language_tab.setLayout(language_layout)
        
        lang_gb = QGroupBox(tr('ui_language'))
        lang_lay = QVBoxLayout()
        
        self.lang_combo = QComboBox()
        languages = [
            ('en', 'English'),
            ('zh', '中文'),
            ('fr', 'Français'),
            ('de', 'Deutsch'),
            ('hi', 'हिन्दी'),
            ('bn', 'বাংলা'),
            ('ur', 'اردو'),
            ('ja', '日本語')
        ]
        for code, name in languages:
            self.lang_combo.addItem(f"{name}", code)
        
        # Set current language
        current_lang = current_settings.get("language", "en")
        index = self.lang_combo.findData(current_lang)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
            
        lang_lay.addWidget(QLabel(tr('ui_language')))
        lang_lay.addWidget(self.lang_combo)
        lang_lay.addStretch()
        
        lang_gb.setLayout(lang_lay)
        language_layout.addWidget(lang_gb)
        
        # Default transcription language
        default_lang_gb = QGroupBox(tr('default_language'))
        default_lang_lay = QVBoxLayout()
        
        self.default_lang_combo = QComboBox()
        default_languages = [
            tr('english_transcribe'), tr('japanese_translate'), tr('chinese_transcribe'),
            tr('french_transcribe'), tr('german_transcribe'), tr('spanish_transcribe'),
            tr('russian_transcribe'), tr('arabic_transcribe'), tr('hindi_transcribe'),
            tr('bengali_transcribe'), tr('urdu_transcribe'), tr('portuguese_transcribe'),
            tr('italian_transcribe'), tr('dutch_transcribe'), tr('polish_transcribe'),
            tr('turkish_transcribe'), tr('vietnamese_transcribe'), tr('thai_transcribe'),
            tr('korean_transcribe')
        ]
        self.default_lang_combo.addItems(default_languages)
        self.default_lang_combo.setCurrentText(current_settings.get("default_lang", tr('english_transcribe')))
        
        default_lang_lay.addWidget(self.default_lang_combo)
        default_lang_gb.setLayout(default_lang_lay)
        language_layout.addWidget(default_lang_gb)
        
        language_layout.addStretch()

        # ===== Advanced Tab =====
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout()
        advanced_tab.setLayout(advanced_layout)

        # Hardware info section
        hw_gb = QGroupBox(tr('hardware_acceleration'))
        hw_lay = QVBoxLayout()
        
        accel_type, accel_info = hardware_detector.get_acceleration_status()
        if accel_type == 'gpu':
            hw_lay.addWidget(QLabel(f"✅ {tr('using_gpu')}"))
            hw_lay.addWidget(QLabel(f"   {accel_info}"))
        else:
            hw_lay.addWidget(QLabel(f"⚠️ {tr('using_cpu')}"))
            hw_lay.addWidget(QLabel(f"   {accel_info}"))
            
        hw_lay.addWidget(QLabel(hardware_detector.get_memory_status()))
        
        # Detailed info button
        hw_details_btn = QPushButton("Show Detailed Hardware Info")
        hw_details_btn.clicked.connect(self.show_hardware_details)
        hw_lay.addWidget(hw_details_btn)
        
        hw_gb.setLayout(hw_lay)
        advanced_layout.addWidget(hw_gb)

        cancel_gb = QGroupBox(tr('cancel_options'))
        cancel_lay = QVBoxLayout()
        self.cb_confirm_cancel = QRadioButton(tr('confirm_cancel'))
        self.cb_confirm_cancel.setChecked(current_settings.get("confirm_cancel", True))
        cancel_lay.addWidget(self.cb_confirm_cancel)
        
        timeout_lay = QHBoxLayout()
        timeout_lay.addWidget(QLabel(tr('force_cancel_timeout')))
        self.force_timeout_spin = QSpinBox()
        self.force_timeout_spin.setRange(10, 120)
        self.force_timeout_spin.setSuffix(tr('seconds'))
        self.force_timeout_spin.setValue(current_settings.get("force_cancel_timeout", 30))
        timeout_lay.addWidget(self.force_timeout_spin)
        timeout_lay.addStretch()
        cancel_lay.addLayout(timeout_lay)
        
        retry_lay = QHBoxLayout()
        retry_lay.addWidget(QLabel(tr('max_retry')))
        self.retry_spin = QSpinBox()
        self.retry_spin.setRange(1, 20)
        self.retry_spin.setValue(current_settings.get("max_retry_attempts", 5))
        retry_lay.addWidget(self.retry_spin)
        retry_lay.addStretch()
        cancel_lay.addLayout(retry_lay)
        
        cancel_gb.setLayout(cancel_lay)
        advanced_layout.addWidget(cancel_gb)

        ui_gb = QGroupBox(tr('ui_options'))
        ui_lay = QVBoxLayout()
        self.cb_minimize_tray = QRadioButton(tr('minimize_tray'))
        self.cb_minimize_tray.setChecked(current_settings.get("minimize_to_tray", False))
        ui_lay.addWidget(self.cb_minimize_tray)
        
        self.cb_show_tooltips = QRadioButton(tr('show_tooltips'))
        self.cb_show_tooltips.setChecked(current_settings.get("show_tooltips", True))
        ui_lay.addWidget(self.cb_show_tooltips)
        
        ui_gb.setLayout(ui_lay)
        advanced_layout.addWidget(ui_gb)
        
        advanced_layout.addStretch()

        # Add tabs
        tabs.addTab(general_tab, tr('general_tab'))
        tabs.addTab(paths_tab, tr('paths_tab'))
        tabs.addTab(features_tab, tr('features_tab'))
        tabs.addTab(language_tab, tr('language_tab'))
        tabs.addTab(advanced_tab, tr('advanced_tab'))

        # Buttons
        btn_lay = QHBoxLayout()
        apply_btn = QPushButton(tr('apply_restart'))
        apply_btn.setStyleSheet("background:#007aff; color:white; padding:12px; border-radius:8px; font-weight:bold;")
        apply_btn.clicked.connect(self.apply_close)
        cancel_btn = QPushButton(tr('cancel'))
        cancel_btn.setStyleSheet("background:#8e8e93; color:white; padding:12px; border-radius:8px;")
        cancel_btn.clicked.connect(self.reject)
        btn_lay.addStretch()
        btn_lay.addWidget(apply_btn)
        btn_lay.addWidget(cancel_btn)
        lay.addLayout(btn_lay)

        logger.info("Settings dialog initialized with current settings")

    def show_hardware_details(self):
        """Show detailed hardware information"""
        details = hardware_detector.get_detailed_info()
        msg = "\n".join(details)
        QMessageBox.information(self, tr('hardware_acceleration'), msg)

    def browse_temp(self):
        d = QFileDialog.getExistingDirectory(self, tr('temp_dir'))
        if d:
            self.tmp_edit.setText(d)
            logger.info(f"Temp dir changed to: {d}")

    def browse_models(self):
        d = QFileDialog.getExistingDirectory(self, tr('models_dir'))
        if d:
            self.mod_edit.setText(d)
            logger.info(f"Models dir changed to: {d}")

    def apply_close(self):
        # Get selected language
        lang_code = self.lang_combo.currentData()
        
        new_settings = {
            "ui_scale": self.scale_combo.currentText(),
            "theme": "Windows Default" if self.rb_win.isChecked() else
                     "Light" if self.rb_light.isChecked() else "Dark",
            "temp_dir": self.tmp_edit.text(),
            "models_dir": self.mod_edit.text(),
            "auto_enhance": self.cb_auto_enhance.isChecked(),
            "default_lang": self.default_lang_combo.currentText(),
            "last_mode": self.current_settings.get("last_mode", "normal"),
            "force_cancel_timeout": self.force_timeout_spin.value(),
            "max_retry_attempts": self.retry_spin.value(),
            "confirm_cancel": self.cb_confirm_cancel.isChecked(),
            "minimize_to_tray": self.cb_minimize_tray.isChecked(),
            "show_tooltips": self.cb_show_tooltips.isChecked(),
            "words_per_line": self.wpl_spin.value(),
            "output_format": self.fmt_combo.currentText(),
            "last_input_file": self.current_settings.get("last_input_file", ""),
            "last_output_folder": self.current_settings.get("last_output_folder", ""),
            "window_geometry": self.current_settings.get("window_geometry"),
            "window_state": self.current_settings.get("window_state"),
            "language": lang_code
        }
        save_settings(new_settings)
        
        # Update global translator
        _translator.set_language(lang_code)
        
        self.settingsChanged.emit(new_settings)
        self.accept()
        logger.info("Settings applied and dialog closed")

# ========================================
# ONLINE MODE HANDLER
# ========================================
SCOPES = ['https://www.googleapis.com/auth/drive']

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
        self._lock = threading.Lock()
        self._current_colab_url = None
        self._cancel_lock = threading.Lock()
        self._cancel_requested = False
        self._stop_event = threading.Event()
        self._polling_active = False
        self._online_status = "idle"
        self._download_start_time = None
        self._downloaded_bytes = 0
        self._last_progress_update = 0
        logger.info("OnlineHandler initialized")
        
        # Setup cleanup timer
        self.cleanup_timer.timeout.connect(self.cleanup_old_drive_files)
        self.cleanup_timer.start(3600000)  # Run every hour
        
        # Setup retry timer
        self.retry_timer.timeout.connect(self.retry_polling)
        self.retry_timer.setSingleShot(True)

    def cancel_operation(self):
        """Cancel ongoing online operation and clean up Drive files"""
        with self._cancel_lock:
            self._cancel_requested = True
            self._canceled = True
            self._stop_event.set()
            
        logger.info("Canceling online operation")
        
        # Update status
        self.update_status("canceled")
        
        # Reset progress bars
        self.parent.reset_progress_bars()
        
        # Stop polling timer
        if self.poll_timer.isActive():
            self.poll_timer.stop()
            self._polling_active = False
            
        # Stop retry timer
        if self.retry_timer.isActive():
            self.retry_timer.stop()
            
        # Clean up Drive files
        self.cleanup_current_operation()
            
        self.parent.statusBar().showMessage(tr('canceled'), 5000)

    def force_cancel_operation(self):
        """Force cancel operation without waiting for graceful shutdown"""
        with self._cancel_lock:
            self._cancel_requested = True
            self._canceled = True
            self._stop_event.set()
            
        logger.info("Force canceling online operation")
        
        # Update status
        self.update_status("force_canceled")
        
        # Reset progress bars
        self.parent.reset_progress_bars()
        
        # Stop polling timer immediately
        if self.poll_timer.isActive():
            self.poll_timer.stop()
            self._polling_active = False
            
        # Stop retry timer
        if self.retry_timer.isActive():
            self.retry_timer.stop()
            
        # Clean up Drive files
        self.cleanup_current_operation()
        
        # Clear notebook URL
        self.parent.update_notebook_url_display(None)
            
        self.parent.statusBar().showMessage(tr('force_canceled'), 5000)

    def update_status(self, status):
        """Update online mode status"""
        self._online_status = status
        self.parent.update_online_status_display(status)

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
        """Periodic cleanup of old temporary files in Drive (older than 24 hours)"""
        if not self.service:
            return
            
        try:
            uploads_id = self.get_or_create_folder(self.service, "uploads")
            one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat() + 'Z'
            
            # Clean old uploads
            query = f"'{uploads_id}' in parents and createdTime < '{one_day_ago}' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            for file in results.get("files", []):
                self.service.files().delete(fileId=file["id"]).execute()
                logger.info(f"Cleaned up old file: {file['name']} ({file['id']})")
                
            # Clean old notebooks
            query = f"name='NotyCaption_Generator.ipynb' and createdTime < '{one_day_ago}' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for file in results.get("files", []):
                self.service.files().delete(fileId=file["id"]).execute()
                logger.info(f"Cleaned up old notebook: {file['id']}")
                
        except Exception as e:
            logger.warning(f"Error during Drive cleanup: {e}")

    def get_notebook_url(self):
        """Get the current Colab notebook URL"""
        return self._current_colab_url

    def retry_polling(self):
        """Retry polling after network failure"""
        if self._canceled or self._cancel_requested or self._stop_event.is_set():
            return
            
        self.retry_attempts += 1
        if self.retry_attempts <= self.max_retry_attempts:
            logger.info(f"Retrying polling (attempt {self.retry_attempts}/{self.max_retry_attempts})")
            self.parent.statusBar().showMessage(f"Network issue - retrying... ({self.retry_attempts}/{self.max_retry_attempts})", 5000)
            self.poll_for_output()
        else:
            logger.warning("Max retry attempts reached")
            self.update_status("failed")
            self.parent.statusBar().showMessage(tr('failed'), 5000)
            self.parent.show_force_cancel_option(True)

    def handle_online(self, audio_to_use, lang_code, task, wpl, fmt, base, out_path):
        with self._lock:
            self._canceled = False
            self._cancel_requested = False
            self._stop_event.clear()
            self.retry_attempts = 0
            self.max_retry_attempts = self.parent.settings.get("max_retry_attempts", 5)
            
        if not self.service:
            QMessageBox.warning(self.parent, tr('error'), tr('login_required'))
            logger.warning("Online mode attempted without service")
            return False

        logger.info("Starting online mode workflow")
        self.update_status("uploading")
        
        try:
            if self._stop_event.is_set():
                return False
                
            self.poll_output_name = f"{base}_captions{fmt}"
            
            # Check for existing output file
            query = f"name='{self.poll_output_name}' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            files = results.get("files", [])
            if files:
                reply = QMessageBox.question(self.parent, tr('overwrite'), tr('overwrite_msg').format(self.poll_output_name), QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    logger.info("User chose not to overwrite existing file")
                    return False
                for f in files:
                    self.service.files().delete(fileId=f["id"]).execute()
                    logger.info(f"Deleted existing file: {f['id']}")

            if self._stop_event.is_set():
                return False
                
            # Clean up any old notebook
            query = "name='NotyCaption_Generator.ipynb' and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()
                logger.info(f"Deleted old notebook: {f['id']}")

            if self._stop_event.is_set():
                return False
                
            # Upload audio
            uploads_id = self.get_or_create_folder(self.service, "uploads")
            audio_filename = os.path.basename(audio_to_use)
            audio_id = self.upload_file(self.service, audio_to_use, audio_filename, uploads_id)
            logger.info(f"Uploaded audio: {audio_id}")
            self.poll_audio_id = audio_id

            if self._stop_event.is_set():
                self.cleanup_current_operation()
                return False
                
            # Verify upload
            query = f"name='{audio_filename}' and '{uploads_id}' in parents and trashed=false"
            results = self.service.files().list(q=query).execute()
            if not results.get("files", []):
                raise Exception("Audio upload failed - file not found in Drive.")

            # Generate notebook
            notebook_content = self.generate_notebook_content(
                audio_filename, wpl, fmt, self.poll_output_name, lang_code, task
            )

            if self._stop_event.is_set():
                self.cleanup_current_operation()
                return False
                
            # Create notebook file
            temp_ipynb = os.path.join(tempfile.gettempdir(), "NotyCaption_Generator.ipynb")
            with open(temp_ipynb, "w", encoding="utf-8") as f:
                json.dump(notebook_content, f, indent=2)

            # Upload notebook
            notebook_id = self.upload_file(self.service, temp_ipynb, "NotyCaption_Generator.ipynb")
            logger.info(f"Uploaded notebook: {notebook_id}")
            self.poll_notebook_id = notebook_id

            if self._stop_event.is_set():
                self.cleanup_current_operation()
                return False
                
            # Generate Colab URL
            colab_url = f"https://colab.research.google.com/drive/{notebook_id}"
            self._current_colab_url = colab_url
            
            # Open the URL
            webbrowser.open(colab_url)
            
            # Update parent with notebook URL for persistent display
            self.parent.update_notebook_url_display(colab_url)
            
            # Update status
            self.update_status("waiting")
            
            # Create clickable link message
            link_message = (f"<b>{tr('colab_launched')}</b><br><br>"
                           f"{tr('reopen_notebook_msg')}<br>"
                           f"<a href='{colab_url}' style='color: #00c853;'>{colab_url}</a><br><br>"
                           f"<b>{tr('instructions')}:</b><br>"
                           f"1. {tr('colab_step1')}<br>"
                           f"2. {tr('colab_step2')}<br>"
                           f"3. {tr('colab_step3')}")
            
            # Show message with clickable link
            msg_box = QMessageBox(self.parent)
            msg_box.setWindowTitle(tr('colab_launched'))
            msg_box.setTextFormat(Qt.RichText)
            msg_box.setText(link_message)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

            self.poll_local_out = out_path
            self.parent.statusBar().showMessage(tr('online_waiting'), 12000)

            # Start polling
            self.poll_timer.stop()
            try:
                self.poll_timer.timeout.disconnect()
            except TypeError:
                pass
            self.poll_timer.timeout.connect(lambda: self.poll_for_output())
            self.poll_timer.start(8000)
            self._polling_active = True

            logger.info("Online workflow initiated successfully")
            return True

        except Exception as online_err:
            logger.error(f"Online mode failed: {traceback.format_exc()}")
            self.update_status("failed")
            self.cleanup_current_operation()
            QMessageBox.critical(self.parent, tr('failed'), str(online_err))
            return False

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
                    "import os\n",
                    "import shutil\n",
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
                    "import time\n",
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
                ]),
                code_cell([
                    "# Cleanup - Delete temporary files\n",
                    "print('Cleaning up temporary files...')\n",
                    "try:\n",
                    "    # Delete uploaded audio\n",
                    "    if os.path.exists(audio_path):\n",
                    "        os.remove(audio_path)\n",
                    "        print(f'Deleted audio file: {audio_path}')\n",
                    "    \n",
                    "    # Delete this notebook from Drive\n",
                    "    notebook_path = '/content/drive/My Drive/NotyCaption_Generator.ipynb'\n",
                    "    if os.path.exists(notebook_path):\n",
                    "        os.remove(notebook_path)\n",
                    "        print(f'Deleted notebook: {notebook_path}')\n",
                    "        \n",
                    "    print('Cleanup completed successfully')\n",
                    "except Exception as e:\n",
                    "    print(f'Cleanup error: {e}')\n",
                    "    # Don't fail if cleanup has issues\n",
                    "    pass\n",
                    "print('All temporary files have been deleted from Google Drive')"
                ])
            ]
        }
        logger.info("Notebook content generated")
        return notebook

    def poll_for_output(self):
        if not self.poll_output_name:
            logger.warning("Polling without output name set")
            return

        if self._canceled or self._cancel_requested or self._stop_event.is_set():
            self.poll_timer.stop()
            self._polling_active = False
            return

        self.poll_attempts += 1
        logger.debug(f"Poll attempt {self.poll_attempts}/{self.max_poll_attempts}")

        if self.poll_attempts > self.max_poll_attempts:
            self.poll_timer.stop()
            self._polling_active = False
            self.parent.is_generating = False
            self.parent.freeze_ui(False)
            self.parent.reset_progress_bars()
            self.cleanup_current_operation()
            self.update_status("timeout")
            
            # Show timeout message with reopen link
            link_message = (f"<b>{tr('colab_timeout')}</b><br><br>"
                           f"{tr('colab_timeout_msg')}<br><br>"
                           f"{tr('reopen_notebook_msg')}<br>"
                           f"<a href='{self._current_colab_url}' style='color: #00c853;'>{self._current_colab_url}</a><br><br>"
                           f"<b>{tr('next_steps')}:</b><br>"
                           f"1. {tr('check_notebook')}<br>"
                           f"2. {tr('download_manually')}<br>"
                           f"3. {tr('try_shorter')}")
            
            msg_box = QMessageBox(self.parent)
            msg_box.setWindowTitle(tr('colab_timeout'))
            msg_box.setTextFormat(Qt.RichText)
            msg_box.setText(link_message)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            
            logger.warning("Online polling reached max attempts")
            return

        query = f"name='{self.poll_output_name}' and trashed=false"
        try:
            results = self.service.files().list(q=query, fields="files(id,name)").execute()
            files = results.get("files", [])
            if files:
                file_id = files[0]["id"]
                logger.info(f"Output file found: {file_id}")
                self.update_status("downloading")
                self._download_start_time = time.time()
                self._downloaded_bytes = 0
                self._last_progress_update = 0
                
                try:
                    with open(self.poll_local_out, "wb") as f:
                        request = self.service.files().get_media(fileId=file_id)
                        downloader = MediaIoBaseDownload(f, request)
                        done = False
                        while not done:
                            if self._canceled or self._cancel_requested or self._stop_event.is_set():
                                logger.info("Download canceled during chunk download")
                                return
                            status, done = downloader.next_chunk()
                            if status:
                                progress_pct = int(status.progress() * 100)
                                self._downloaded_bytes = status.resumable_progress
                                
                                # Calculate download speed and ETA
                                if self._download_start_time:
                                    elapsed = time.time() - self._download_start_time
                                    if elapsed > 0 and self._downloaded_bytes > 0:
                                        speed = self._downloaded_bytes / elapsed
                                        remaining_bytes = status.total_size - self._downloaded_bytes
                                        if speed > 0:
                                            eta_seconds = remaining_bytes / speed
                                            eta_str = str(timedelta(seconds=int(eta_seconds)))
                                        else:
                                            eta_str = tr('calculating')
                                    else:
                                        eta_str = tr('calculating')
                                else:
                                    eta_str = tr('calculating')
                                
                                logger.info(f"Download progress: {progress_pct}%")
                                self.parent.progress_update(progress_pct, eta_str, speed if 'speed' in locals() else 0)
                    self.parent.load_downloaded_subtitles(self.poll_local_out)
                    
                    # Clean up - only delete the output file, notebook and audio already deleted by Colab
                    if file_id:
                        self.service.files().delete(fileId=file_id).execute()
                        logger.info(f"Deleted output file: {file_id}")
                        
                    self.poll_timer.stop()
                    self._polling_active = False
                    self.parent.is_generating = False
                    self.parent.freeze_ui(False)
                    self.parent.reset_progress_bars()
                    self.parent.update_notebook_url_display(None)
                    self.update_status("completed")
                        
                    QMessageBox.information(
                        self.parent,
                        tr('completed'),
                        f"{tr('generation_success')}\n{self.poll_local_out}\n\n{tr('cleanup_complete')}"
                    )
                    self.poll_attempts = 0
                    logger.info("Online polling complete - success")
                except Exception as dl_err:
                    logger.error(f"Download failed: {dl_err}")
                    self.update_status("failed")
                    QMessageBox.critical(self.parent, tr('failed'), str(dl_err))
            else:
                logger.debug(f"Poll attempt {self.poll_attempts}/{self.max_poll_attempts} — waiting...")
                self.update_status("waiting")
                if self.poll_attempts % 15 == 0:
                    mins = (self.poll_attempts * 8) // 60
                    self.parent.statusBar().showMessage(
                        f"{tr('waiting')}... ({mins} {tr('min_elapsed')})", 10000
                    )
        except Exception as poll_err:
            logger.warning(f"Poll network/drive error: {poll_err}")
            self.update_status("network_error")
            self.parent.show_error_details(tr('network_error'), str(poll_err), tr('retry_auto'))
            # Schedule retry
            if not self.retry_timer.isActive() and not self._stop_event.is_set():
                self.retry_timer.start(5000)  # Retry after 5 seconds

    def cleanup_drive(self):
        """Final cleanup on app close - only delete temporary files, not user data"""
        if not self.service:
            logger.info("No service for Drive cleanup")
            return
        try:
            # Only clean files in uploads folder
            uploads_id = self.get_or_create_folder(self.service, "uploads")
            query = f"'{uploads_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            for f in results.get("files", []):
                self.service.files().delete(fileId=f["id"]).execute()
                logger.info(f"Cleaned upload: {f['id']}")

            # Clean notebooks
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
    status_changed = pyqtSignal(str)
    speed_update = pyqtSignal(float, str)

    def __init__(self, audio_file, temp_dir, parent=None):
        super().__init__(parent)
        self.audio_file = audio_file
        self.temp_dir = temp_dir
        self._lock = threading.Lock()
        self._is_canceled = False
        self._cancel_requested = False
        self._stop_event = threading.Event()
        self._output_dir = None
        self._status = "initializing"
        self._start_time = None
        self._processed_seconds = 0
        logger.info(f"AudioEnhancerThread initialized for {audio_file}")

    def cancel(self):
        with self._lock:
            self._cancel_requested = True
            self._is_canceled = True
            self._stop_event.set()
        logger.info("Audio enhancement cancellation requested")
        self.update_status("canceled")

    def request_graceful_cancel(self):
        """Request graceful cancellation without immediate termination"""
        with self._lock:
            self._cancel_requested = True
            self._stop_event.set()
        logger.info("Audio enhancement graceful cancellation requested")
        self.update_status("canceling")

    def is_canceled(self):
        with self._lock:
            return self._is_canceled or self._cancel_requested or self._stop_event.is_set()

    def update_status(self, status):
        self._status = status
        self.status_changed.emit(status)

    @pyqtSlot()
    def run(self):
        try:
            self.progress.emit(10)
            self.update_status("starting")
            self._start_time = time.time()
            logger.info("Initializing Spleeter separator")
            
            if self.is_canceled():
                logger.info("Enhancement canceled before start")
                self.update_status("canceled")
                return
                
            self.update_status("processing")
            separator = Separator('spleeter:2stems')
            base_name = os.path.splitext(os.path.basename(self.audio_file))[0]
            self._output_dir = os.path.join(self.temp_dir, base_name)

            logger.info(f"Starting separation to {self._output_dir}")
            if self.is_canceled():
                logger.info("Enhancement canceled during initialization")
                self.update_status("canceled")
                return
                
            # Start processing in a way we can track progress
            separator.separate_to_file(
                self.audio_file,
                self._output_dir,
                synchronous=True
            )
            self.progress.emit(80)
            logger.info("Separation phase complete")
            
            # Calculate processing speed
            if self._start_time:
                elapsed = time.time() - self._start_time
                if elapsed > 0:
                    speed = 1.0 / elapsed  # Simplified speed metric
                    eta_str = tr('completed')
                    self.speed_update.emit(speed, eta_str)
            
            if self.is_canceled():
                logger.info("Enhancement canceled - cleaning up partial output")
                self.update_status("canceled")
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
            self.update_status("completed")
            logger.info("Spleeter separation completed")
            self.finished.emit(vocals_path, True)
        except Exception as enhance_err:
            error_msg = f"Spleeter error: {str(enhance_err)}"
            logger.error(f"Spleeter thread error: {traceback.format_exc()}")
            self.update_status("failed")
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
        self._cancel_requested = False
        self._progress_callback = None
        self._current_download = None
        self._downloaded = 0
        self._total_size = 0
        self._download_completed = False
        self._lock = threading.Lock()
        self._response = None
        self._temp_path = None
        self._stop_event = threading.Event()
        self._status = "idle"
        self._start_time = None
        self._speed_history = []
        
    def cancel(self):
        with self._lock:
            self._cancel_requested = True
            self._canceled = True
            self._stop_event.set()
            if self._response:
                try:
                    self._response.close()
                except:
                    pass
        logger.info("Download cancellation requested")
        self.update_status("canceled")

    def request_graceful_cancel(self):
        with self._lock:
            self._cancel_requested = True
            self._stop_event.set()
        logger.info("Download graceful cancellation requested")
        self.update_status("canceling")

    def is_canceled(self):
        with self._lock:
            return self._canceled or self._cancel_requested or self._stop_event.is_set()
        
    def update_status(self, status):
        self._status = status
        
    def calculate_speed_and_eta(self):
        """Calculate download speed and ETA"""
        if not self._start_time or self._downloaded == 0:
            return 0, tr('calculating')
            
        elapsed = time.time() - self._start_time
        if elapsed <= 0:
            return 0, tr('calculating')
            
        # Calculate current speed (smoothed average)
        current_speed = self._downloaded / elapsed
        self._speed_history.append(current_speed)
        if len(self._speed_history) > 10:
            self._speed_history.pop(0)
        
        avg_speed = sum(self._speed_history) / len(self._speed_history)
        
        # Calculate ETA
        if avg_speed > 0 and self._total_size > 0:
            remaining_bytes = self._total_size - self._downloaded
            eta_seconds = remaining_bytes / avg_speed
            eta_str = str(timedelta(seconds=int(eta_seconds)))
        else:
            eta_str = tr('calculating')
            
        return avg_speed, eta_str
        
    def patched_download_url_to_file(self, original_func, url, dst, *args, **kwargs):
        if self.is_canceled():
            raise Exception("DOWNLOAD_CANCELED_BY_USER")
        
        self._current_download = {'url': url, 'dst': dst}
        self._download_completed = False
        self._temp_path = dst + '.tmp'
        self._start_time = time.time()
        
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
                            # Calculate speed and ETA
                            speed, eta = self.calculate_speed_and_eta()
                            self._progress_callback(progress, speed, eta)
            
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
            self._cancel_requested = False
            self._stop_event.clear()
            self._speed_history = []
        self._progress_callback = progress_callback
        self._downloaded = 0
        self._total_size = 0
        self._download_completed = False
        self._response = None
        self._temp_path = None
        self._start_time = None
        self.update_status("starting")
        
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
            self.update_status("downloading")
            
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
                self.update_status("failed")
                if os.path.exists(model_path):
                    os.remove(model_path)
                raise Exception("Model validation failed")
                
            logger.info("Model downloaded and validated successfully")
            self.update_status("completed")
            
            if progress_callback:
                progress_callback(100, 0, tr('completed'))
                
            return model
            
        except Exception as e:
            error_str = str(e)
            if "DOWNLOAD_CANCELED_BY_USER" in error_str:
                logger.info("Download was canceled by user")
                self.update_status("canceled")
                model_path = os.path.join(download_root, f"{model_name}.pt")
                temp_path = model_path + '.tmp'
                for path in [model_path, temp_path]:
                    if os.path.exists(path):
                        os.remove(path)
                raise Exception(tr('canceled'))
            else:
                logger.error(f"Download error: {e}")
                self.update_status("failed")
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
    progress = pyqtSignal(int, float, str)  # progress, speed, eta
    finished = pyqtSignal(bool, str)
    canceled = pyqtSignal()
    status_changed = pyqtSignal(str)

    def __init__(self, model_dir, parent=None):
        super().__init__(parent)
        self.model_dir = model_dir
        self._is_canceled = False
        self._cancel_requested = False
        self._download_started = False
        self._download_completed = False
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._downloader = CancellableWhisperDownloader()
        self.progress_info = {"downloaded": 0, "total": 0}
        self._status = "idle"
        logger.info(f"ModelDownloadThread initialized for {model_dir}")

    def cancel(self):
        with self._lock:
            if not self._is_canceled and self._download_started and not self._download_completed:
                self._cancel_requested = True
                self._is_canceled = True
                self._stop_event.set()
                self._downloader.cancel()
                logger.info("Model download cancellation requested")
                self.update_status("canceled")

    def request_graceful_cancel(self):
        with self._lock:
            if not self._is_canceled and self._download_started and not self._download_completed:
                self._cancel_requested = True
                self._stop_event.set()
                self._downloader.request_graceful_cancel()
                logger.info("Model download graceful cancellation requested")
                self.update_status("canceling")

    def force_cancel(self):
        """Force cancel without waiting for graceful shutdown"""
        with self._lock:
            self._is_canceled = True
            self._cancel_requested = True
            self._stop_event.set()
            self._downloader.cancel()
        logger.info("Model download force canceled")
        self.update_status("force_canceled")
        if self.isRunning():
            self.terminate()
            self.wait(1000)

    def is_downloading(self):
        with self._lock:
            return self._download_started and not self._download_completed and not self._is_canceled

    def update_status(self, status):
        self._status = status
        self.status_changed.emit(status)

    @pyqtSlot()
    def run(self):
        try:
            cleanup_corrupt_models(self.model_dir)
            
            self.progress.emit(5, 0, tr('calculating'))
            logger.info("Starting model download process")
            self.update_status("starting")
            
            model_path_v1 = os.path.join(self.model_dir, "large-v1.pt")
            model_path = os.path.join(self.model_dir, "large.pt")
            
            if validate_model_file(model_path_v1):
                logger.info("Valid large-v1 model already exists, skipping download")
                self.progress.emit(100, 0, tr('completed'))
                self.update_status("completed")
                self.finished.emit(True, tr('model_exists'))
                return
            elif validate_model_file(model_path):
                logger.info("Valid large model already exists, skipping download")
                self.progress.emit(100, 0, tr('completed'))
                self.update_status("completed")
                self.finished.emit(True, tr('model_exists'))
                return
            
            with self._lock:
                self._download_started = True
                self._download_completed = False
            
            def progress_callback(p, speed, eta):
                if hasattr(self._downloader, '_downloaded') and hasattr(self._downloader, '_total_size'):
                    self.progress_info["downloaded"] = self._downloader._downloaded
                    self.progress_info["total"] = self._downloader._total_size
                self.progress.emit(p, speed, eta)
            
            self.update_status("downloading")
            model = self._downloader.download_model(
                "large-v1",
                self.model_dir,
                progress_callback=progress_callback
            )
            
            with self._lock:
                if self._cancel_requested or self._is_canceled or self._stop_event.is_set():
                    logger.info("Download was canceled after completion check")
                    self.update_status("canceled")
                    self.canceled.emit()
                    return
                self._download_completed = True
            
            if validate_model_file(model_path_v1):
                logger.info("Model downloaded and validated successfully")
                self.progress.emit(100, 0, tr('completed'))
                self.update_status("completed")
                self.finished.emit(True, tr('download_success'))
            else:
                raise Exception("Downloaded model validation failed")
                
        except Exception as dl_err:
            error_str = str(dl_err)
            if "canceled" in error_str.lower():
                logger.info("Download was canceled by user")
                with self._lock:
                    self._download_completed = True
                self.update_status("canceled")
                self.canceled.emit()
            elif not self._is_canceled and not self._cancel_requested:
                error_msg = f"Download error: {str(dl_err)}"
                logger.error(f"Model thread error: {traceback.format_exc()}")
                self.update_status("failed")
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
        self.setWindowTitle(tr('window_title'))
        self.setMinimumSize(1024, 768)
        logger.info("Initializing main window")

        # Set window icon
        icon_path = resource_path('App.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            logger.info("App icon set")

        # Load settings
        self.settings = load_settings()
        
        # Set language from settings
        _translator.set_language(self.settings.get("language", "en"))
        
        # Initialize session manager
        self.session_manager = SessionManager()
        
        # Clean up corrupt models
        cleanup_corrupt_models(self.settings.get("models_dir", APP_DATA_DIR))
        
        # Apply settings
        self.apply_ui_scale()
        self.apply_theme()

        self.center_window()

        # Restore window geometry if available
        if self.settings.get("window_geometry"):
            self.restoreGeometry(bytes.fromhex(self.settings["window_geometry"]))
        if self.settings.get("window_state"):
            self.restoreState(bytes.fromhex(self.settings["window_state"]))

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Status bar
        self.statusBar().showMessage(tr('ready'))

        # Create system tray icon
        self.create_tray_icon()

        # Main layout
        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        # Setup UI panels
        self.setup_left_panel()
        self.setup_right_panel()
        self.setup_bottom_panel()
        self.setup_footer()

        # Initialize state
        self.initialize_state()
        self.online_handler = OnlineHandler(self)

        # Threads
        self.enhancer_thread = None
        self.model_download_thread = None
        self.progress_whisper = None
        self.player_timer = QTimer(self)
        self.player_timer.timeout.connect(self.update_timeline)
        self.player_timer.start(50)
        self._closing = False
        self._cancel_lock = threading.Lock()
        self._operation_in_progress = False
        self._current_notebook_url = None
        self._force_cancel_timer = QTimer(self)
        self._force_cancel_timer.setSingleShot(True)
        self._force_cancel_timer.timeout.connect(self.show_force_cancel_option)

        # Load existing credentials
        self.load_existing_credentials()

        # Setup keyboard shortcuts
        self.setup_shortcuts()

        # Setup tooltips
        self.setup_tooltips()

        # Create overlays
        self.create_overlays()

        # Restore last session if available
        self.restore_session()

        logger.info("Main window fully initialized")

    def create_tray_icon(self):
        """Create system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = resource_path('App.ico')
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        
        # Create tray menu
        tray_menu = QMenu()
        show_action = tray_menu.addAction(tr('show_window'))
        show_action.triggered.connect(self.show_window)
        quit_action = tray_menu.addAction(tr('quit'))
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()

    def show_window(self):
        """Show and activate main window"""
        self.show()
        self.activateWindow()
        self.raise_()

    def quit_app(self):
        """Quit application"""
        self.close()

    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # File operations
        QShortcut(QKeySequence("Ctrl+O"), self, self.import_media_file)
        QShortcut(QKeySequence("Ctrl+G"), self, self.start_caption_generation)
        QShortcut(QKeySequence("Ctrl+E"), self, self.enhance_audio_vocals)
        QShortcut(QKeySequence("Ctrl+S"), self, self.toggle_edit_mode)
        
        # Playback
        QShortcut(QKeySequence("Space"), self, self.toggle_media_playback)
        QShortcut(QKeySequence("Ctrl+P"), self, self.toggle_media_playback)
        
        # Settings
        QShortcut(QKeySequence("Ctrl+,"), self, self.open_settings_dialog)
        
        # Cancel
        QShortcut(QKeySequence("Esc"), self, lambda: self.cancel_current_operation(with_confirmation=True))
        
        # Online mode
        QShortcut(QKeySequence("Ctrl+L"), self, self.initiate_google_login)
        QShortcut(QKeySequence("Ctrl+R"), self, self.reopen_notebook)

    def setup_tooltips(self):
        """Setup tooltips for all buttons"""
        if not self.settings.get("show_tooltips", True):
            return
            
        self.import_btn.setToolTip(tr('import_tooltip'))
        self.enhance_btn.setToolTip(tr('enhance_tooltip'))
        self.gen_btn.setToolTip(tr('generate_tooltip'))
        self.play_btn.setToolTip(tr('play_tooltip'))
        self.edit_btn.setToolTip(tr('edit_tooltip'))
        self.download_btn.setToolTip(tr('download_tooltip'))
        self.login_button.setToolTip(tr('login_tooltip'))
        self.reopen_btn.setToolTip(tr('reopen_tooltip'))
        self.copy_url_btn.setToolTip(tr('copy_tooltip'))
        
        # Settings
        self.mode_combo.setToolTip(tr('mode_tooltip'))
        self.lang_combo.setToolTip(tr('lang_tooltip'))
        self.words_spin.setToolTip(tr('words_tooltip'))
        self.format_combo.setToolTip(tr('format_tooltip'))
        self.out_folder_edit.setToolTip(tr('folder_tooltip'))

    def create_overlays(self):
        """Create overlay widgets"""
        # Main operation overlay
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

        self.overlay_layout = QVBoxLayout(self.overlay)
        self.overlay_layout.setAlignment(Qt.AlignCenter)

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

        self.prog_title = QLabel(tr('processing'))
        self.prog_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.prog_title.setAlignment(Qt.AlignCenter)
        prog_lay.addWidget(self.prog_title)

        self.prog_info = QLabel(tr('starting'))
        self.prog_info.setStyleSheet("color: #cccccc; font-size: 12px; margin-bottom: 15px;")
        self.prog_info.setAlignment(Qt.AlignCenter)
        prog_lay.addWidget(self.prog_info)

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

        # Speed and ETA labels
        speed_layout = QHBoxLayout()
        self.speed_label = QLabel(f"{tr('speed')} --")
        self.speed_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        speed_layout.addWidget(self.speed_label)
        
        self.eta_label = QLabel(f"{tr('eta')} --")
        self.eta_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        speed_layout.addWidget(self.eta_label)
        speed_layout.addStretch()
        prog_lay.addLayout(speed_layout)

        self.overlay_cancel_btn = QPushButton(tr('cancel'))
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
        self.overlay_cancel_btn.clicked.connect(lambda: self.cancel_current_operation(with_confirmation=self.settings.get("confirm_cancel", True)))
        self.overlay_cancel_btn.setEnabled(False)

        self.overlay_force_cancel_btn = QPushButton(tr('force_cancel'))
        self.overlay_force_cancel_btn.setStyleSheet("""
            QPushButton {
                background: #9a0000;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 25px;
                margin-top: 10px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: #7a0000;
            }
            QPushButton:pressed {
                background: #5a0000;
            }
            QPushButton:disabled {
                background: #666666;
                color: #999999;
            }
        """)
        self.overlay_force_cancel_btn.clicked.connect(self.force_cancel_operation)
        self.overlay_force_cancel_btn.setEnabled(False)
        self.overlay_force_cancel_btn.hide()

        self.overlay_layout.addWidget(self.progress_container)
        self.overlay_layout.addWidget(self.overlay_cancel_btn, alignment=Qt.AlignCenter)
        self.overlay_layout.addWidget(self.overlay_force_cancel_btn, alignment=Qt.AlignCenter)
        self.overlay_cancel_btn.setParent(self.overlay)
        self.overlay_force_cancel_btn.setParent(self.overlay)

        # Download overlay
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

        download_title = QLabel(tr('downloading'))
        download_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        download_title.setAlignment(Qt.AlignCenter)
        download_lay.addWidget(download_title)

        self.download_info = QLabel(tr('starting'))
        self.download_info.setStyleSheet("color: #cccccc; font-size: 12px; margin-bottom: 15px;")
        self.download_info.setAlignment(Qt.AlignCenter)
        download_lay.addWidget(self.download_info)

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

        # Download speed and ETA
        download_speed_layout = QHBoxLayout()
        self.download_speed_label = QLabel(f"{tr('speed')} --")
        self.download_speed_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        download_speed_layout.addWidget(self.download_speed_label)
        
        self.download_eta_label = QLabel(f"{tr('eta')} --")
        self.download_eta_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        download_speed_layout.addWidget(self.download_eta_label)
        download_speed_layout.addStretch()
        download_lay.addLayout(download_speed_layout)

        self.download_cancel_btn = QPushButton(tr('cancel'))
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
        self.download_cancel_btn.clicked.connect(lambda: self.cancel_current_operation(with_confirmation=self.settings.get("confirm_cancel", True)))
        
        self.download_force_cancel_btn = QPushButton(tr('force_cancel'))
        self.download_force_cancel_btn.setStyleSheet("""
            QPushButton {
                background: #9a0000;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 25px;
                margin-top: 10px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: #7a0000;
            }
            QPushButton:pressed {
                background: #5a0000;
            }
            QPushButton:disabled {
                background: #666666;
                color: #999999;
            }
        """)
        self.download_force_cancel_btn.clicked.connect(self.force_cancel_operation)
        self.download_force_cancel_btn.hide()
        
        download_overlay_layout.addWidget(download_container)
        download_overlay_layout.addWidget(self.download_cancel_btn, alignment=Qt.AlignCenter)
        download_overlay_layout.addWidget(self.download_force_cancel_btn, alignment=Qt.AlignCenter)

    def resizeEvent(self, event):
        """Handle window resize"""
        if hasattr(self, 'overlay') and self.overlay.isVisible():
            self.overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
            self.overlay.raise_()
            self.overlay_cancel_btn.raise_()
            self.overlay_force_cancel_btn.raise_()
        if hasattr(self, 'download_overlay') and self.download_overlay.isVisible():
            self.download_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
            self.download_overlay.raise_()
            self.download_cancel_btn.raise_()
            self.download_force_cancel_btn.raise_()
        super().resizeEvent(event)

    def closeEvent(self, event: QCloseEvent):
        """Handle window close event"""
        # Save window geometry
        self.settings["window_geometry"] = self.saveGeometry().toHex().data().decode()
        self.settings["window_state"] = self.saveState().toHex().data().decode()
        save_settings(self.settings)

        if self.settings.get("minimize_to_tray", False) and not self._closing:
            self.hide()
            self.tray_icon.show()
            self.tray_icon.showMessage(
                APP_NAME,
                tr('minimized_to_tray'),
                QSystemTrayIcon.Information,
                2000
            )
            event.ignore()
            return

        if self._operation_in_progress or self.is_generating:
            reply = QMessageBox.question(
                self,
                tr('operation_in_progress'),
                tr('exit_confirm'),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return

        logger.info("App close event triggered")
        self._closing = True
        
        # Clean up
        self.cleanup_before_exit()
        
        logger.info("=== NotyCaption Secure Shutdown ===")
        event.accept()

    def cleanup_before_exit(self):
        """Clean up resources before exit"""
        self.player.stop()
        self.player_timer.stop()
        
        if hasattr(self, 'online_handler'):
            self.online_handler.poll_timer.stop()
            self.online_handler.cleanup_timer.stop()
            self.online_handler.retry_timer.stop()

        if self.model_download_thread and self.model_download_thread.isRunning():
            logger.info("Download thread still running, requesting graceful cancellation...")
            self.model_download_thread.request_graceful_cancel()
            if not self.model_download_thread.wait(5000):
                logger.warning("Download thread did not finish gracefully, forcing termination...")
                self.model_download_thread.force_cancel()

        if self.enhancer_thread and self.enhancer_thread.isRunning():
            logger.info("Enhancer thread still running, requesting graceful cancellation...")
            self.enhancer_thread.request_graceful_cancel()
            if not self.enhancer_thread.wait(5000):
                logger.warning("Enhancer thread did not finish gracefully, forcing termination...")
                self.enhancer_thread.terminate()
                self.enhancer_thread.wait(1000)

        # Clean up temp files
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

        # Clean up Drive
        if hasattr(self, 'online_handler') and self.online_handler.service:
            self.online_handler.cleanup_drive()

        # Clean up corrupt models
        try:
            cleanup_corrupt_models(self.settings.get("models_dir", APP_DATA_DIR))
        except Exception as e:
            logger.warning(f"Failed to clean up models on exit: {e}")

    def restore_session(self):
        """Restore last session if available"""
        session = self.session_manager.load_session()
        if session and session.get('last_input_file'):
            last_file = session['last_input_file']
            if os.path.exists(last_file):
                self.import_media_file(last_file)
                logger.info(f"Restored last session with file: {last_file}")

    def setup_left_panel(self):
        """Setup left panel with caption editor"""
        self.left_panel = QWidget()
        self.left_panel.setMaximumWidth(700)
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        self.top_layout.addWidget(self.left_panel)

        title = QLabel(tr('ai_caption_editor'))
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
        self.caption_edit.setPlaceholderText(tr('captions_placeholder'))
        self.left_layout.addWidget(self.caption_edit, stretch=1)

        btn_row = QHBoxLayout()
        self.edit_btn = QPushButton(tr('edit_captions'))
        self.edit_btn.setMinimumHeight(60)
        self.edit_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0a84ff,stop:1 #0066cc); color: white; border-radius: 12px; font-weight: bold; font-size: 14px; padding: 12px; }
            QPushButton:disabled { background: #666; }
        """)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.edit_btn.setEnabled(False)
        btn_row.addWidget(self.edit_btn)

        settings_btn = QPushButton(tr('settings'))
        settings_btn.setMinimumHeight(60)
        settings_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #5e5ce6,stop:1 #4a4ad8); color: white; border-radius: 12px; font-weight: bold; font-size: 14px; padding: 12px; }
        """)
        settings_btn.clicked.connect(self.open_settings_dialog)
        btn_row.addWidget(settings_btn)

        self.download_btn = QPushButton(tr('download_model'))
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
        """Setup right panel with controls"""
        self.right_scroll = QScrollArea()
        self.right_scroll.setWidgetResizable(True)
        self.right_scroll.setStyleSheet("QScrollArea { border: none; }")
        self.top_layout.addWidget(self.right_scroll)

        self.right_panel = QWidget()
        self.right_layout = QGridLayout()
        self.right_panel.setLayout(self.right_layout)
        self.right_scroll.setWidget(self.right_panel)

        row = 0

        self.login_button = QPushButton(tr('login_google'))
        self.login_button.setMinimumHeight(60)
        self.login_button.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #4285f4,stop:1 #3367d6); color: white; border-radius: 15px; font-weight: bold; font-size: 14px; padding: 15px; }
            QPushButton:disabled { background: #ccc; color: #666; }
        """)
        self.login_button.clicked.connect(self.initiate_google_login)
        self.right_layout.addWidget(self.login_button, row, 0, 1, 2)
        row += 1

        mode_label = QLabel(tr('processing_mode'))
        mode_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(mode_label, row, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([tr('normal_mode'), tr('online_mode')])
        self.mode_combo.setMinimumHeight(50)
        self.mode_combo.currentTextChanged.connect(self.on_mode_change)
        self.right_layout.addWidget(self.mode_combo, row, 1)
        row += 1

        lang_label = QLabel(tr('language'))
        lang_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(lang_label, row, 0)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([
            tr('english_transcribe'), tr('japanese_translate'), tr('chinese_transcribe'),
            tr('french_transcribe'), tr('german_transcribe'), tr('spanish_transcribe'),
            tr('russian_transcribe'), tr('arabic_transcribe'), tr('hindi_transcribe'),
            tr('bengali_transcribe'), tr('urdu_transcribe'), tr('portuguese_transcribe'),
            tr('italian_transcribe'), tr('dutch_transcribe'), tr('polish_transcribe'),
            tr('turkish_transcribe'), tr('vietnamese_transcribe'), tr('thai_transcribe'),
            tr('korean_transcribe')
        ])
        self.lang_combo.setMinimumHeight(50)
        self.lang_combo.setCurrentText(self.settings.get("default_lang", tr('english_transcribe')))
        self.right_layout.addWidget(self.lang_combo, row, 1)
        row += 1

        wpl_label = QLabel(tr('words_per_line'))
        wpl_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(wpl_label, row, 0)
        self.words_spin = QSpinBox()
        self.words_spin.setRange(1, 20)
        self.words_spin.setValue(self.settings.get("words_per_line", 5))
        self.words_spin.setMinimumHeight(50)
        self.words_spin.setStyleSheet("QSpinBox { font-size: 14px; padding: 10px; }")
        self.right_layout.addWidget(self.words_spin, row, 1)
        row += 1

        self.import_btn = QPushButton(tr('import_media'))
        self.import_btn.setMinimumHeight(70)
        self.import_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #007aff,stop:1 #0056b3); color: white; border-radius: 15px; font-weight: bold; font-size: 16px; padding: 15px; }
        """)
        self.import_btn.clicked.connect(self.import_media_file)
        self.right_layout.addWidget(self.import_btn, row, 0, 1, 2)
        row += 1

        fmt_label = QLabel(tr('output_format'))
        fmt_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(fmt_label, row, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems([tr('srt_format'), tr('ass_format')])
        self.format_combo.setMinimumHeight(50)
        self.format_combo.setCurrentText(self.settings.get("output_format", tr('srt_format')))
        self.right_layout.addWidget(self.format_combo, row, 1)
        row += 1

        out_label = QLabel(tr('output_folder'))
        out_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.right_layout.addWidget(out_label, row, 0)
        self.out_folder_edit = QLineEdit()
        self.out_folder_edit.setReadOnly(True)
        self.out_folder_edit.setMinimumHeight(50)
        self.out_folder_edit.setPlaceholderText(tr('default_source'))
        self.out_folder_edit.setText(self.settings.get("last_output_folder", ""))
        self.right_layout.addWidget(self.out_folder_edit, row, 1)
        row += 1

        browse_btn = QPushButton(tr('browse_output'))
        browse_btn.setMinimumHeight(50)
        browse_btn.setStyleSheet("""
            QPushButton { background: #3a3a3c; color: white; border-radius: 10px; font-size: 12px; padding: 10px; }
        """)
        browse_btn.clicked.connect(self.browse_output_folder)
        self.right_layout.addWidget(browse_btn, row, 0, 1, 2)
        row += 1

        self.enhance_btn = QPushButton(tr('enhance_audio'))
        self.enhance_btn.setMinimumHeight(70)
        self.enhance_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ffcc00,stop:1 #cc9900); color: white; border-radius: 15px; font-weight: bold; font-size: 16px; padding: 15px; }
            QPushButton:disabled { background: #ccc; }
        """)
        self.enhance_btn.clicked.connect(self.enhance_audio_vocals)
        self.enhance_btn.setEnabled(False)
        self.right_layout.addWidget(self.enhance_btn, row, 0, 1, 2)
        
        row += 1
        
        # Status and URL display frame
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Box)
        status_frame.setStyleSheet("QFrame { background: #2d2d30; border: 1px solid #404040; border-radius: 5px; padding: 5px; }")
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(5, 5, 5, 5)
        
        # Status indicator
        status_row = QHBoxLayout()
        status_label = QLabel(tr('status'))
        status_label.setStyleSheet("color: #cccccc; font-size: 10px; font-weight: bold;")
        status_row.addWidget(status_label)
        
        self.status_value = QLabel(tr('idle'))
        self.status_value.setStyleSheet("color: #00c853; font-size: 10px;")
        status_row.addWidget(self.status_value)
        status_row.addStretch()
        status_layout.addLayout(status_row)
        
        # URL display
        url_row = QHBoxLayout()
        self.url_label = QLabel(f"{tr('notebook_url')} {tr('not_available')}")
        self.url_label.setStyleSheet("color: #cccccc; font-size: 10px;")
        self.url_label.setWordWrap(True)
        url_row.addWidget(self.url_label, 1)
        status_layout.addLayout(url_row)
        
        # Button row
        button_row = QHBoxLayout()
        
        self.reopen_btn = QPushButton(tr('reopen_notebook'))
        self.reopen_btn.setMinimumHeight(30)
        self.reopen_btn.setStyleSheet("""
            QPushButton { background: #00c853; color: white; border-radius: 5px; font-weight: bold; font-size: 10px; padding: 5px; }
            QPushButton:hover { background: #00b140; }
            QPushButton:disabled { background: #666; }
        """)
        self.reopen_btn.clicked.connect(self.reopen_notebook)
        self.reopen_btn.setEnabled(False)
        button_row.addWidget(self.reopen_btn)
        
        self.copy_url_btn = QPushButton(tr('copy_url'))
        self.copy_url_btn.setMinimumHeight(30)
        self.copy_url_btn.setStyleSheet("""
            QPushButton { background: #2196f3; color: white; border-radius: 5px; font-weight: bold; font-size: 10px; padding: 5px; }
            QPushButton:hover { background: #1976d2; }
            QPushButton:disabled { background: #666; }
        """)
        self.copy_url_btn.clicked.connect(self.copy_notebook_url)
        self.copy_url_btn.setEnabled(False)
        button_row.addWidget(self.copy_url_btn)
        
        status_layout.addLayout(button_row)
        
        self.right_layout.addWidget(status_frame, row, 0, 1, 2)
        
        logger.info("Right panel setup complete")

    def setup_bottom_panel(self):
        """Setup bottom panel with playback controls"""
        bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(bottom_layout)

        self.play_btn = QPushButton(tr('play_pause'))
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

        self.gen_btn = QPushButton(tr('generate'))
        self.gen_btn.setMinimumHeight(70)
        self.gen_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff3b30,stop:1 #d32f2f); color: white; border-radius: 15px; font-weight: bold; font-size: 16px; padding: 15px; min-width: 180px; }
            QPushButton:disabled { background: #ccc; }
        """)
        self.gen_btn.clicked.connect(self.start_caption_generation)
        bottom_layout.addWidget(self.gen_btn)

        self.main_progress = QProgressBar()
        self.main_progress.setStyleSheet("""
            QProgressBar { background: #22252a; border: 2px solid #3a3f44; border-radius: 10px; text-align: center; color: white; font-weight: bold; height: 25px; }
            QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0a84ff,stop:1 #0066cc); border-radius: 8px; }
        """)
        self.main_progress.setFormat(f"{tr('progress')}: %p%")
        bottom_layout.addWidget(self.main_progress)

        logger.info("Bottom panel setup complete")

    def setup_footer(self):
        """Setup footer with copyright"""
        footer = QLabel(tr('footer'))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #6c757d; font-size: 10px; margin: 15px 0; padding: 10px; border-top: 1px solid #404040;")
        self.main_layout.addWidget(footer)
        logger.info("Footer setup complete")

    def initialize_state(self):
        """Initialize application state"""
        self.input_file = None
        self.audio_file = None
        self.output_folder = self.settings.get("last_output_folder", None)
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
        self.mode_combo.setCurrentText(tr('online_mode') if self.mode == "online" else tr('normal_mode'))

        self.update_download_button_visibility()
        self.enhance_btn.setEnabled(bool(self.audio_file))
        self.play_btn.setEnabled(bool(self.audio_file))
        
        # Set output folder from settings if available
        if self.output_folder and os.path.exists(self.output_folder):
            self.out_folder_edit.setText(self.output_folder)
            
        logger.info("App state initialized")

    def center_window(self):
        """Center window on screen"""
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        logger.info("Window centered on screen")

    def apply_ui_scale(self):
        """Apply UI scaling"""
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
        """Apply UI theme"""
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

    def freeze_ui(self, freeze=True, message=tr('processing')):
        """Freeze/unfreeze UI"""
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

        for w in widgets_to_disable:
            if hasattr(w, 'setEnabled'):
                w.setEnabled(not freeze)

        if freeze:
            self._operation_in_progress = True
            self.overlay.show()
            self.overlay.raise_()
            self.overlay_cancel_btn.raise_()
            self.overlay_force_cancel_btn.hide()
            self.overlay_cancel_btn.setEnabled(True)
            self.overlay_cancel_btn.setFocus()
            self.prog_title.setText(message)
            self.prog_info.setText(tr('processing'))
            self.operation_progress.setValue(0)
            self.statusBar().showMessage(message, 0)
            self.show_cancel_only(True)
            
            # Start timer to show force cancel option
            timeout = self.settings.get("force_cancel_timeout", 30)
            self._force_cancel_timer.start(timeout * 1000)
        else:
            self._operation_in_progress = False
            self.overlay.hide()
            self.overlay_force_cancel_btn.hide()
            self._force_cancel_timer.stop()
            self.statusBar().clearMessage()
            self.show_cancel_only(False)

    def show_cancel_only(self, show=True):
        """Show only cancel button on overlay"""
        self.overlay_cancel_btn.setEnabled(show)
        if show:
            self.overlay_cancel_btn.raise_()
            self.overlay_cancel_btn.setFocus()

    def show_force_cancel_option(self):
        """Show force cancel button"""
        if self._operation_in_progress and self.overlay.isVisible():
            self.overlay_force_cancel_btn.show()
            self.overlay_force_cancel_btn.raise_()
            self.overlay_force_cancel_btn.setEnabled(True)

    def reset_progress_bars(self):
        """Reset all progress bars"""
        self.operation_progress.setValue(0)
        self.main_progress.setValue(0)
        self.download_progress.setValue(0)
        self.prog_info.setText(tr('ready'))
        self.download_info.setText(tr('ready'))
        self.speed_label.setText(f"{tr('speed')} --")
        self.eta_label.setText(f"{tr('eta')} --")
        self.download_speed_label.setText(f"{tr('speed')} --")
        self.download_eta_label.setText(f"{tr('eta')} --")

    def progress_update(self, value, eta=None, speed=None):
        """Update progress bars with speed and ETA"""
        self.operation_progress.setValue(value)
        self.main_progress.setValue(value)
        
        if eta:
            self.eta_label.setText(f"{tr('eta')} {eta}")
            self.download_eta_label.setText(f"{tr('eta')} {eta}")
        if speed:
            if speed > 1024 * 1024:
                speed_str = f"{speed/(1024*1024):.1f} MB/s"
            elif speed > 1024:
                speed_str = f"{speed/1024:.1f} KB/s"
            else:
                speed_str = f"{speed:.1f} B/s"
            self.speed_label.setText(f"{tr('speed')} {speed_str}")
            self.download_speed_label.setText(f"{tr('speed')} {speed_str}")

    def show_error_details(self, title, error, details):
        """Show detailed error message"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(error)
        msg_box.setDetailedText(details)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def update_notebook_url_display(self, url):
        """Update notebook URL display"""
        self._current_notebook_url = url
        if url:
            display_url = url if len(url) < 50 else url[:47] + "..."
            self.url_label.setText(f"{tr('notebook_url')} {display_url}")
            self.url_label.setToolTip(url)
            self.reopen_btn.setEnabled(True)
            self.copy_url_btn.setEnabled(True)
        else:
            self.url_label.setText(f"{tr('notebook_url')} {tr('not_available')}")
            self.url_label.setToolTip("")
            self.reopen_btn.setEnabled(False)
            self.copy_url_btn.setEnabled(False)

    def update_online_status_display(self, status):
        """Update online status display"""
        status_colors = {
            "idle": "#cccccc",
            "uploading": "#ff9800",
            "waiting": "#2196f3",
            "processing": "#9c27b0",
            "downloading": "#4caf50",
            "completed": "#00c853",
            "failed": "#f44336",
            "canceled": "#ff9800",
            "force_canceled": "#9a0000",
            "canceling": "#ff9800",
            "timeout": "#f44336",
            "network_error": "#ff9800",
            "starting": "#2196f3",
            "initializing": "#2196f3"
        }
        color = status_colors.get(status, "#cccccc")
        status_text = status.replace("_", " ").title()
        self.status_value.setText(status_text)
        self.status_value.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: bold;")

    def reopen_notebook(self):
        """Reopen Colab notebook"""
        if self._current_notebook_url:
            webbrowser.open(self._current_notebook_url)
            self.statusBar().showMessage(tr('reopening_notebook'), 3000)
        else:
            QMessageBox.information(self, tr('no_notebook'), tr('no_notebook_msg'))

    def copy_notebook_url(self):
        """Copy notebook URL to clipboard"""
        if self._current_notebook_url:
            clipboard = QApplication.clipboard()
            clipboard.setText(self._current_notebook_url)
            self.statusBar().showMessage(tr('url_copied'), 3000)
        else:
            QMessageBox.information(self, tr('no_url'), tr('no_url_msg'))

    def open_settings_dialog(self):
        """Open settings dialog"""
        logger.info("Opening settings dialog")
        dlg = SettingsDialog(self.settings, self)
        dlg.settingsChanged.connect(self.update_from_settings)
        if dlg.exec_() == QDialog.Accepted:
            logger.info("Settings dialog accepted")
            # Force UI update for theme and language
            self.apply_theme()
            self.retranslate_ui()
        else:
            logger.info("Settings dialog canceled")

    def retranslate_ui(self):
        """Retranslate all UI elements"""
        self.setWindowTitle(tr('window_title'))
        self.statusBar().showMessage(tr('ready'))
        
        # Left panel
        self.edit_btn.setText(tr('edit_captions'))
        self.download_btn.setText(tr('download_model'))
        
        # Right panel
        self.login_button.setText(tr('login_google'))
        self.import_btn.setText(tr('import_media'))
        self.enhance_btn.setText(tr('enhance_audio'))
        self.reopen_btn.setText(tr('reopen_notebook'))
        self.copy_url_btn.setText(tr('copy_url'))
        
        # Bottom panel
        self.play_btn.setText(tr('play_pause'))
        self.gen_btn.setText(tr('generate'))
        
        # Update comboboxes
        current_mode = self.mode_combo.currentText()
        self.mode_combo.clear()
        self.mode_combo.addItems([tr('normal_mode'), tr('online_mode')])
        if current_mode == tr('online_mode') or current_mode == "☁️ Online (Colab + Drive)":
            self.mode_combo.setCurrentText(tr('online_mode'))
        else:
            self.mode_combo.setCurrentText(tr('normal_mode'))
            
        current_lang = self.lang_combo.currentText()
        self.lang_combo.clear()
        self.lang_combo.addItems([
            tr('english_transcribe'), tr('japanese_translate'), tr('chinese_transcribe'),
            tr('french_transcribe'), tr('german_transcribe'), tr('spanish_transcribe'),
            tr('russian_transcribe'), tr('arabic_transcribe'), tr('hindi_transcribe'),
            tr('bengali_transcribe'), tr('urdu_transcribe'), tr('portuguese_transcribe'),
            tr('italian_transcribe'), tr('dutch_transcribe'), tr('polish_transcribe'),
            tr('turkish_transcribe'), tr('vietnamese_transcribe'), tr('thai_transcribe'),
            tr('korean_transcribe')
        ])
        if current_lang:
            self.lang_combo.setCurrentText(current_lang)
            
        current_format = self.format_combo.currentText()
        self.format_combo.clear()
        self.format_combo.addItems([tr('srt_format'), tr('ass_format')])
        if current_format:
            self.format_combo.setCurrentText(current_format)
            
        # Status display
        self.status_value.setText(tr('idle'))
        self.url_label.setText(f"{tr('notebook_url')} {tr('not_available')}")
        
        # Progress bars
        self.main_progress.setFormat(f"{tr('progress')}: %p%")
        self.prog_title.setText(tr('processing'))
        self.prog_info.setText(tr('ready'))
        self.speed_label.setText(f"{tr('speed')} --")
        self.eta_label.setText(f"{tr('eta')} --")
        self.download_speed_label.setText(f"{tr('speed')} --")
        self.download_eta_label.setText(f"{tr('eta')} --")
        
        # Footer
        footer = self.findChild(QLabel)
        if footer:
            footer.setText(tr('footer'))
            
        logger.info("UI retranslated")

    def update_from_settings(self, new_settings):
        """Update from new settings"""
        self.settings = new_settings
        self.apply_ui_scale()
        self.lang_combo.setCurrentText(new_settings.get("default_lang", tr('english_transcribe')))
        self.words_spin.setValue(new_settings.get("words_per_line", 5))
        self.format_combo.setCurrentText(new_settings.get("output_format", tr('srt_format')))
        self.update_download_button_visibility()
        
        # Update online handler settings
        if hasattr(self, 'online_handler'):
            self.online_handler.max_retry_attempts = new_settings.get("max_retry_attempts", 5)
            
        # Update tooltips
        self.setup_tooltips()
        
        logger.info("Settings updated and applied globally")

    def update_download_button_visibility(self):
        """Update download button visibility"""
        if self.mode == "online":
            self.download_btn.setVisible(False)
            logger.info("Download button hidden in online mode")
            return

        model_dir = self.settings.get("models_dir", APP_DATA_DIR)
        model_path_v1 = os.path.join(model_dir, "large-v1.pt")
        model_path = os.path.join(model_dir, "large.pt")
        
        exists = validate_model_file(model_path_v1) or validate_model_file(model_path)
        self.download_btn.setVisible(not exists)
        logger.info(f"Valid model exists: {exists} → Button visible: {not exists}")

    def initiate_google_login(self):
        """Initiate Google login"""
        client_secrets = load_client_secrets()
        if not client_secrets:
            msg = tr('missing_credentials')
            logger.warning(msg)
            QMessageBox.warning(self, tr('missing_credentials'), msg)
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
            self.mode = "online"
            self.mode_combo.setCurrentText(tr('online_mode'))
            self.update_download_button_visibility()
            logger.info("Google login successful - Online mode enabled")
            QMessageBox.information(self, tr('login_success'), tr('drive_connected'))
        except Exception as login_err:
            logger.error(f"Google login failed: {traceback.format_exc()}")
            QMessageBox.critical(self, tr('login_error'), f"{tr('auth_failed')}\n{str(login_err)}")
        finally:
            if os.path.exists(client_path):
                os.remove(client_path)
                logger.info("Temp client file removed")

    def load_existing_credentials(self):
        """Load existing Google credentials"""
        if os.path.exists(TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                self.online_handler.service = build("drive", "v3", credentials=creds)
                self.login_button.setVisible(False)
                self.mode = "online"
                self.mode_combo.setCurrentText(tr('online_mode'))
                self.update_download_button_visibility()
                logger.info("Existing credentials loaded and refreshed - Online mode activated")
            except Exception as cred_err:
                logger.error(f"Credential load failed: {cred_err}")
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                    logger.info("Invalid token removed")

    def on_mode_change(self, text):
        """Handle mode change"""
        self.mode = "online" if text == tr('online_mode') else "normal"
        self.settings["last_mode"] = self.mode
        save_settings(self.settings)
        self.update_download_button_visibility()
        logger.info(f"Mode switched to: {self.mode}")

    def load_whisper_model(self):
        """Load Whisper model"""
        try:
            model_dir = self.settings.get("models_dir", APP_DATA_DIR)
            logger.info(f"Loading Whisper large-v1 from: {model_dir}")
            
            cleanup_corrupt_models(model_dir)
            
            model = whisper.load_model("large-v1", download_root=model_dir)
            logger.info("Whisper model loaded successfully")
            return model
        except Exception as load_err:
            logger.error(f"Whisper load failed: {traceback.format_exc()}")
            QMessageBox.critical(self, tr('model_load_error'), f"{tr('model_load_failed')}\n{str(load_err)}")
            raise RuntimeError(f"Model load error: {str(load_err)}")

    def on_media_status_changed(self, status):
        """Handle media status change"""
        if status == QMediaPlayer.LoadedMedia:
            self.play_btn.setEnabled(True)
            logger.info("Media loaded for playback")
        elif status in (QMediaPlayer.NoMedia, QMediaPlayer.InvalidMedia):
            self.play_btn.setEnabled(False)
            self.play_btn.setText(tr('play_pause'))
            logger.warning("Media status invalid")

    def on_position_changed(self, position):
        """Handle position change"""
        self.update_caption_highlight(position)

    def on_duration_changed(self, duration):
        """Handle duration change"""
        self.duration_ms = duration
        self.timeline.setRange(0, duration)
        logger.debug(f"Media duration set: {duration} ms")

    def on_player_error(self, error):
        """Handle player error"""
        err_str = self.player.errorString() or tr('unknown_error')
        logger.warning(f"Media player error: {err_str}")
        QMessageBox.warning(self, tr('playback_error'), f"{tr('playback_failed')}\n{err_str}")

    def update_timeline(self):
        """Update timeline slider"""
        if self.duration_ms > 0 and self.player.state() == QMediaPlayer.PlayingState:
            self.timeline.setValue(self.player.position())

    def toggle_media_playback(self):
        """Toggle media playback"""
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, tr('no_audio'), tr('no_audio_msg'))
            logger.warning("Play clicked → no audio_file")
            return

        logger.info(f"Play/Pause clicked | File: {self.audio_file}")

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText(tr('play_pause'))
            logger.info("→ Paused")
            return

        try:
            url = QUrl.fromLocalFile(self.audio_file)
            media = QMediaContent(url)
            self.player.setMedia(media)
            self.loaded_media = self.audio_file
            logger.info("Media reloaded successfully")

            self.player.play()
            self.play_btn.setText(tr('playing'))
            logger.info("→ Play command sent")

            QTimer.singleShot(1500, self.check_playback_status)

        except Exception as play_err:
            logger.error(f"Playback setup failed: {play_err}", exc_info=True)
            QMessageBox.critical(self, tr('playback_error'),
                                f"{tr('qt_prepare_failed')}\n{str(play_err)}\n\n"
                                f"{tr('playback_tips')}")

    def check_playback_status(self):
        """Check playback status"""
        status = self.player.mediaStatus()
        logger.info(f"Playback status check: {status}")
        if status == QMediaPlayer.LoadedMedia:
            logger.info("Media loaded OK")
        elif status in (QMediaPlayer.NoMedia, QMediaPlayer.InvalidMedia):
            logger.error("Media invalid after load attempt")
            QMessageBox.warning(self, tr('cannot_play'),
                               tr('media_invalid_msg'))

    def seek_media_position(self, position):
        """Seek to position"""
        self.player.setPosition(position)
        logger.debug(f"Seek to: {position} ms")

    def update_caption_highlight(self, ms):
        """Update caption highlight"""
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

    def import_media_file(self, file_path=None):
        """Import media file"""
        logger.info("Media import dialog opened")
        if not file_path:
            filter_str = tr('media_filter')
            file_path, _ = QFileDialog.getOpenFileName(self, tr('import_media'), self.settings.get("last_input_file", ""), filter_str)
            
        if not file_path:
            logger.info("Import cancelled by user")
            return

        logger.info(f"Importing: {file_path}")
        self.input_file = file_path
        self.output_folder = self.output_folder or os.path.dirname(file_path)
        self.out_folder_edit.setText(self.output_folder)
        self.enhance_btn.setEnabled(True)
        
        # Save to settings
        self.settings["last_input_file"] = file_path
        self.settings["last_output_folder"] = self.output_folder
        save_settings(self.settings)
        
        # Save session
        self.session_manager.save_operation_state("import", {
            "file": file_path,
            "timestamp": datetime.datetime.now().isoformat()
        })

        temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
        temp_name = os.path.splitext(os.path.basename(file_path))[0] + ".temp.wav"
        new_temp = os.path.join(temp_dir, temp_name)

        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
                logger.info(f"Previous temp removed: {self.last_temp_wav}")
            except Exception as rm_err:
                logger.warning(f"Previous temp removal failed: {rm_err}")

        success = False
        if file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv')):
            try:
                logger.info("Extracting audio from video...")
                clip = VideoFileClip(file_path)
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
                audio_clip = AudioFileClip(file_path)
                audio_clip.write_audiofile(new_temp, codec='pcm_s16le', logger=None, verbose=False)
                self.audio_file = new_temp
                self.debug_audio_file()
                audio_clip.close()
                success = True
                logger.info("Audio conversion to WAV complete")
            except Exception as aud_err:
                logger.warning(f"Audio conversion failed: {aud_err}")
                self.audio_file = file_path
                QMessageBox.warning(self, tr('conversion_warning'), tr('conversion_warning_msg'))

        self.last_temp_wav = new_temp if success else None
        self.loaded_media = None
        self.play_btn.setEnabled(True)
        logger.info(f"Audio prepared: {self.audio_file}")
        QMessageBox.information(self, tr('import_complete'), tr('import_success'))

    def debug_audio_file(self):
        """Debug audio file"""
        if not self.audio_file:
            logger.info("No audio file set")
            return
        logger.info(f"Audio file path: {self.audio_file}")
        logger.info(f"Exists: {os.path.exists(self.audio_file)}")
        logger.info(f"Size: {os.path.getsize(self.audio_file) / 1024 / 1024:.2f} MB")

    def browse_output_folder(self):
        """Browse output folder"""
        d = QFileDialog.getExistingDirectory(self, tr('browse_output'), self.output_folder or "")
        if d:
            self.output_folder = d
            self.out_folder_edit.setText(d)
            self.settings["last_output_folder"] = d
            save_settings(self.settings)
            logger.info(f"Output folder set: {d}")

    def enhance_audio_vocals(self):
        """Enhance audio vocals"""
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, tr('no_audio'), tr('import_first'))
            logger.warning("Enhance clicked without audio")
            return

        logger.info("Starting vocal enhancement...")
        self.freeze_ui(True, tr('enhancing'))
        temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
        self.enhancer_thread = AudioEnhancerThread(self.audio_file, temp_dir, self)
        self.enhancer_thread.progress.connect(self.on_enhance_progress)
        self.enhancer_thread.finished.connect(self.on_enhance_finished)
        self.enhancer_thread.error.connect(self.on_enhance_error)
        self.enhancer_thread.status_changed.connect(lambda s: self.update_online_status_display(s))
        self.enhancer_thread.speed_update.connect(lambda s, e: self.progress_update(self.operation_progress.value(), e, s))
        self.enhancer_thread.start()
        logger.info("Enhancer thread started")

    def on_enhance_progress(self, value):
        """Handle enhance progress"""
        self.progress_update(value)

    def on_enhance_finished(self, vocals_path, success):
        """Handle enhance finished"""
        self.freeze_ui(False)
        if success:
            base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
            final_name = f"{base}_enhanced_vocals.wav"
            final_path = os.path.join(self.output_folder or APP_DATA_DIR, final_name)
            try:
                shutil.move(vocals_path, final_path)
                self.audio_file = final_path
                self.last_temp_wav = final_path
                self.play_btn.setEnabled(True)
                logger.info(f"Enhanced audio saved: {final_path}")
                QMessageBox.information(self, tr('enhancement_complete'), f"{tr('enhancement_success')}\n{final_path}")
            except Exception as move_err:
                logger.error(f"Move enhanced file failed: {move_err}")
                QMessageBox.warning(self, tr('save_error'), str(move_err))
        self.enhancer_thread = None
        logger.info("Enhancer thread finished")

    def on_enhance_error(self, error_msg):
        """Handle enhance error"""
        self.freeze_ui(False)
        logger.error(f"Enhancement error: {error_msg}")
        QMessageBox.critical(self, tr('enhancement_failed'), error_msg)
        self.enhancer_thread = None

    def open_model_download_dialog(self):
        """Open model download dialog"""
        if self._closing:
            return
            
        logger.info("Opening model download dialog")
        dlg = QDialog(self)
        dlg.setWindowTitle(tr('download_model'))
        dlg.setFixedSize(520, 340)
        lay = QVBoxLayout()
        dlg.setLayout(lay)

        title = QLabel(tr('download_model_desc'))
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        lay.addWidget(title)

        desc = QLabel(tr('model_info'))
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        lay.addWidget(desc)

        options = [
            tr('download_default'),
            tr('download_custom'),
            tr('link_existing')
        ]
        rb_group = QButtonGroup()
        rbs = [QRadioButton(opt) for opt in options]
        rbs[0].setChecked(True)
        for rb in rbs:
            lay.addWidget(rb)
            rb_group.addButton(rb)

        btn_lay = QHBoxLayout()
        ok_btn = QPushButton(tr('start_download'))
        ok_btn.setStyleSheet("background:#00c853; color:white; padding:12px; border-radius:8px; font-weight:bold;")
        ok_btn.clicked.connect(dlg.accept)
        cancel_btn = QPushButton(tr('cancel'))
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
            file_path, _ = QFileDialog.getOpenFileName(self, tr('select_model'), "", "PyTorch Model (*.pt)")
            if file_path and os.path.basename(file_path) == "large-v1.pt":
                if validate_model_file(file_path):
                    model_dir = os.path.dirname(file_path)
                    self.settings["models_dir"] = model_dir
                    save_settings(self.settings)
                    self.update_download_button_visibility()
                    QMessageBox.information(self, tr('success'), tr('model_linked'))
                    logger.info(f"Valid model linked from: {model_dir}")
                else:
                    QMessageBox.warning(self, tr('invalid_file'), tr('model_corrupt'))
            else:
                QMessageBox.warning(self, tr('invalid_file'), tr('select_large_v1'))
            return

        if selected == 1:
            path = QFileDialog.getExistingDirectory(self, tr('select_folder'))
            if not path:
                logger.info("Custom folder selection canceled")
                return
        else:
            path = self.settings.get("models_dir", APP_DATA_DIR)

        cleanup_corrupt_models(path)

        self.settings["models_dir"] = path
        save_settings(self.settings)
        self.update_download_button_visibility()

        self.download_overlay.show()
        self.download_overlay.raise_()
        self.download_cancel_btn.raise_()
        self.download_force_cancel_btn.hide()
        self.download_progress.setValue(0)
        self.download_info.setText(tr('starting'))
        self.download_cancel_btn.setEnabled(True)

        self.freeze_ui(True, tr('downloading_model'))

        self.model_download_thread = ModelDownloadThread(path, self)
        self.model_download_thread.progress.connect(self.on_download_progress)
        self.model_download_thread.finished.connect(self.on_model_download_finished)
        self.model_download_thread.canceled.connect(self.on_model_download_canceled)
        self.model_download_thread.status_changed.connect(lambda s: self.update_online_status_display(s))
        self.model_download_thread.start()

        logger.info(f"Model download started to: {path}")

    def on_download_progress(self, value, speed, eta):
        """Handle download progress"""
        if self._closing:
            return
            
        self.download_progress.setValue(value)
        self.progress_update(value, eta, speed)
        
        try:
            if (hasattr(self, 'model_download_thread') and 
                self.model_download_thread and 
                hasattr(self.model_download_thread, 'progress_info')):
                
                info = self.model_download_thread.progress_info
                
                if info["total"] > 0:
                    downloaded_mb = info["downloaded"] / (1024 * 1024)
                    total_mb = info["total"] / (1024 * 1024)
                    self.download_info.setText(f"{tr('downloading')}... {downloaded_mb:.1f} MB / {total_mb:.1f} MB ({value}%)")
                    self.prog_info.setText(f"{tr('downloading')}... {downloaded_mb:.1f} MB / {total_mb:.1f} MB")
                else:
                    self.download_info.setText(f"{tr('downloading')}... ({value}%)")
                    self.prog_info.setText(f"{tr('downloading')}... ({value}%)")
            else:
                self.download_info.setText(f"{tr('downloading')}... ({value}%)")
                self.prog_info.setText(f"{tr('downloading')}... ({value}%)")
        except Exception as e:
            logger.debug(f"Progress display error: {e}")
            self.download_info.setText(f"{tr('downloading')}... ({value}%)")
            self.prog_info.setText(f"{tr('downloading')}... ({value}%)")

    def on_model_download_finished(self, success, message):
        """Handle download finished"""
        self.download_overlay.hide()
        self.freeze_ui(False)
        self.reset_progress_bars()
        
        if success:
            self.update_download_button_visibility()
            QMessageBox.information(self, tr('success'), message)
            logger.info("Model download finished successfully")
        else:
            QMessageBox.critical(self, tr('download_failed'), message)
            logger.error("Model download failed")
        self.model_download_thread = None
        self._cancel_processed = False

    def on_model_download_canceled(self):
        """Handle download canceled"""
        self.download_overlay.hide()
        self.freeze_ui(False)
        self.reset_progress_bars()
        logger.info("UI buttons re-enabled after cancel")
        
        try:
            cleanup_corrupt_models(self.settings.get("models_dir", APP_DATA_DIR))
        except Exception as e:
            logger.warning(f"Failed to clean up models after cancel: {e}")
        
        QMessageBox.information(
            self, 
            tr('download_canceled'), 
            tr('canceled_msg')
        )
        self.model_download_thread = None
        self._cancel_processed = False

    def start_caption_generation(self):
        """Start caption generation"""
        if self.is_generating:
            QMessageBox.warning(self, tr('in_progress'), tr('already_running'))
            logger.warning("Generation attempted while in progress")
            return

        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, tr('no_media'), tr('import_first'))
            logger.warning("Generation attempted without media")
            return

        self.is_generating = True
        self.freeze_ui(True, tr('generating'))
        self.reset_progress_bars()
        logger.info("=== Secure Caption Generation Started ===")

        auto_enhance = self.settings.get("auto_enhance", False)
        if auto_enhance:
            logger.info("Auto-enhancing audio before generation...")
            temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
            self.enhancer_thread = AudioEnhancerThread(self.audio_file, temp_dir, self)
            self.enhancer_thread.progress.connect(lambda v: self.progress_update(v // 2))
            self.enhancer_thread.finished.connect(lambda p, s: self.on_auto_enhance_done(p, s))
            self.enhancer_thread.error.connect(self.on_auto_enhance_error)
            self.enhancer_thread.status_changed.connect(lambda s: self.update_online_status_display(s))
            self.enhancer_thread.speed_update.connect(lambda s, e: self.progress_update(self.operation_progress.value(), e, s))
            self.enhancer_thread.start()
            return

        self.proceed_to_transcription(self.audio_file)

    def on_auto_enhance_done(self, vocals_path, success):
        """Handle auto enhance done"""
        if success:
            enhanced_path = vocals_path
            base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
            final_name = f"{base}_auto_enhanced.wav"
            final_path = os.path.join(self.output_folder or APP_DATA_DIR, final_name)
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
        """Handle auto enhance error"""
        logger.error(f"Auto-enhance error: {error}")
        QMessageBox.warning(self, tr('enhancement_failed'), error)
        self.enhancer_thread = None
        self.proceed_to_transcription(self.audio_file)

    def proceed_to_transcription(self, audio_to_use):
        """Proceed to transcription"""
        lang_text = self.lang_combo.currentText()
        
        # Map UI language text to Whisper language codes
        lang_map = {
            tr('english_transcribe'): 'en',
            tr('japanese_translate'): 'ja',
            tr('japanese_transcribe'): 'ja',
            tr('chinese_transcribe'): 'zh',
            tr('french_transcribe'): 'fr',
            tr('german_transcribe'): 'de',
            tr('spanish_transcribe'): 'es',
            tr('russian_transcribe'): 'ru',
            tr('arabic_transcribe'): 'ar',
            tr('hindi_transcribe'): 'hi',
            tr('bengali_transcribe'): 'bn',
            tr('urdu_transcribe'): 'ur',
            tr('portuguese_transcribe'): 'pt',
            tr('italian_transcribe'): 'it',
            tr('dutch_transcribe'): 'nl',
            tr('polish_transcribe'): 'pl',
            tr('turkish_transcribe'): 'tr',
            tr('vietnamese_transcribe'): 'vi',
            tr('thai_transcribe'): 'th',
            tr('korean_transcribe'): 'ko'
        }
        
        lang_code = lang_map.get(lang_text, 'en')
        task = "translate" if "Translate" in lang_text or "翻译" in lang_text or "traduire" in lang_text or "übersetzen" in lang_text else "transcribe"

        wpl = self.words_spin.value()
        fmt_map = {
            tr('srt_format'): ".srt",
            tr('ass_format'): ".ass",
        }
        fmt = fmt_map.get(self.format_combo.currentText(), ".srt")
        base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
        out_path = os.path.join(self.output_folder or APP_DATA_DIR, f"{base}_captions{fmt}")

        if os.path.exists(out_path):
            reply = QMessageBox.question(self, tr('overwrite'), tr('overwrite_msg').format(out_path), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                self.is_generating = False
                self.freeze_ui(False)
                self.reset_progress_bars()
                logger.info("Overwrite canceled")
                return

        logger.info(f"Transcription params: lang={lang_code}, task={task}, wpl={wpl}, fmt={fmt}, out={out_path}")

        self.progress_update(10)

        if self.mode == "online":
            success = self.online_handler.handle_online(audio_to_use, lang_code, task, wpl, fmt, base, out_path)
            if not success:
                self.is_generating = False
                self.freeze_ui(False)
                self.reset_progress_bars()
        else:
            self.perform_local_transcription(audio_to_use, lang_code, task, wpl, fmt, out_path)

    def perform_local_transcription(self, audio_path, lang_code, task, wpl, fmt, out_path):
        """Perform local transcription with real progress"""
        try:
            self.progress_update(10)
            model = self.load_whisper_model()
            
            # Create progress wrapper
            self.progress_whisper = ProgressWhisper(lambda p, msg: self.update_transcription_progress(p, msg))
            
            logger.info("Starting local transcription with progress tracking...")
            
            # Run transcription with progress
            result = model.transcribe(
                audio_path,
                language=lang_code,
                task=task,
                word_timestamps=True,
                verbose=False
            )
            
            # Manual progress simulation since whisper doesn't provide real progress
            total_segments = len(result.get("segments", []))
            for i, seg in enumerate(result.get("segments", [])):
                if self.progress_whisper and self.progress_whisper.is_canceled():
                    raise Exception(tr('canceled'))
                    
                progress = 20 + int((i / max(1, total_segments)) * 60)
                self.update_transcription_progress(progress, f"{tr('processing_segment')} {i+1}/{total_segments}")
                
                # Process segment for word-level timestamps
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

                for j in range(0, len(word_texts), wpl):
                    chunk = word_texts[j:j + wpl]
                    line_text = " ".join(chunk).strip()
                    if not line_text:
                        continue
                    chunk_start = word_starts[j]
                    chunk_end = word_ends[min(j + wpl - 1, len(word_ends) - 1)]

                    self.subtitles.append({
                        "index": len(self.subtitles) + 1,
                        "start": timedelta(seconds=chunk_start),
                        "end": timedelta(seconds=chunk_end),
                        "text": line_text
                    })
                    self.display_lines.append(line_text)

            self.progress_update(90)
            logger.info("Transcription complete")

            preview_text = "\n\n".join(self.display_lines)
            self.caption_edit.setText(preview_text)
            self.generated = True
            self.edit_btn.setEnabled(True)

            self.save_subtitles_to_file(self.subtitles, fmt, out_path)
            self.progress_update(100)

            logger.info(f"Local generation saved: {out_path}")
            QMessageBox.information(self, tr('generation_complete'), f"{tr('generation_success')}\n{out_path}")

        except Exception as trans_err:
            if "canceled" in str(trans_err).lower():
                logger.info("Transcription canceled by user")
            else:
                logger.error(f"Local transcription failed: {traceback.format_exc()}")
                QMessageBox.critical(self, tr('generation_error'), f"{tr('processing_failed')}\n{str(trans_err)}")
        finally:
            self.is_generating = False
            self.freeze_ui(False)
            self.reset_progress_bars()
            self.progress_whisper = None

    def update_transcription_progress(self, progress, message):
        """Update transcription progress"""
        self.progress_update(progress)
        self.prog_info.setText(message)
        QApplication.processEvents()

    def save_subtitles_to_file(self, subtitles, fmt, out_path):
        """Save subtitles to file"""
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
        """Load downloaded subtitles"""
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
            QMessageBox.warning(self, tr('load_error'), f"{tr('preview_failed')}\n{str(load_err)}")

    def toggle_edit_mode(self):
        """Toggle edit mode"""
        if not self.generated:
            logger.warning("Edit toggled without generated captions")
            return
        self.edit_active = not self.edit_active
        self.caption_edit.setReadOnly(not self.edit_active)
        self.edit_btn.setText(tr('save_exit_edit') if self.edit_active else tr('edit_captions'))
        if self.edit_active:
            self.caption_edit.setFocus()
        else:
            self.apply_edited_captions()
        logger.info(f"Edit mode: {'enabled' if self.edit_active else 'disabled'}")

    def apply_edited_captions(self):
        """Apply edited captions"""
        text_content = self.caption_edit.toPlainText().strip()
        edited_lines = [line.strip() for line in text_content.split('\n\n') if line.strip()]

        if len(edited_lines) != len(self.subtitles):
            QMessageBox.warning(self, tr('mismatch'), tr('line_count_changed'))
            self.refresh_caption_preview()
            logger.warning("Edit discarded due to line mismatch")
            return

        for i, new_text in enumerate(edited_lines):
            self.subtitles[i]["text"] = new_text
            self.display_lines[i] = new_text

        self.refresh_caption_preview()
        logger.info("Edits applied to subtitles")
        QMessageBox.information(self, tr('saved'), tr('edits_applied'))

    def refresh_caption_preview(self):
        """Refresh caption preview"""
        preview = "\n\n".join(self.display_lines)
        self.caption_edit.setText(preview)
        logger.debug("Caption preview refreshed")

    def cancel_current_operation(self, with_confirmation=False):
        """Cancel current operation"""
        logger.info("Cancel button pressed - stopping current operation")
        
        if with_confirmation and self.settings.get("confirm_cancel", True):
            reply = QMessageBox.question(
                self,
                tr('cancel_confirm'),
                tr('cancel_confirm_msg'),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        with self._cancel_lock:
            stopped = False

            # Cancel transcription progress
            if self.progress_whisper:
                logger.info("Canceling transcription...")
                self.progress_whisper.cancel()
                stopped = True

            if hasattr(self, 'online_handler') and self.online_handler.poll_timer.isActive():
                logger.info("Canceling online operation...")
                self.online_handler.cancel_operation()
                self.is_generating = False
                self.freeze_ui(False)
                self.reset_progress_bars()
                self.update_notebook_url_display(None)
                stopped = True

            if self.enhancer_thread and self.enhancer_thread.isRunning():
                logger.info("Canceling Spleeter enhancement...")
                self.enhancer_thread.request_graceful_cancel()
                if not self.enhancer_thread.wait(5000):
                    logger.warning("Enhancement did not cancel gracefully, forcing...")
                    self.enhancer_thread.terminate()
                    self.enhancer_thread.wait(1000)
                self.enhancer_thread = None
                self.is_generating = False
                self.freeze_ui(False)
                self.reset_progress_bars()
                stopped = True

            if self.model_download_thread and self.model_download_thread.isRunning():
                logger.info("Canceling model download...")
                self.model_download_thread.request_graceful_cancel()
                stopped = True

            if self.is_generating and not stopped:
                self.is_generating = False
                self.freeze_ui(False)
                self.reset_progress_bars()
                stopped = True

            if stopped:
                self.statusBar().showMessage(tr('canceled'), 5000)
            else:
                self.statusBar().showMessage(tr('nothing_to_cancel'), 3000)

    def force_cancel_operation(self):
        """Force cancel operation"""
        logger.info("Force cancel button pressed - forcefully stopping operation")
        
        reply = QMessageBox.warning(
            self,
            tr('force_cancel'),
            tr('force_cancel_confirm'),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        
        with self._cancel_lock:
            # Force cancel transcription
            if self.progress_whisper:
                self.progress_whisper.cancel()
                
            if hasattr(self, 'online_handler'):
                logger.info("Force canceling online operation...")
                self.online_handler.force_cancel_operation()
                
            if self.enhancer_thread and self.enhancer_thread.isRunning():
                logger.info("Force canceling enhancement...")
                self.enhancer_thread.terminate()
                self.enhancer_thread.wait(1000)
                self.enhancer_thread = None
                
            if self.model_download_thread and self.model_download_thread.isRunning():
                logger.info("Force canceling download...")
                self.model_download_thread.force_cancel()
                
            self.is_generating = False
            self.freeze_ui(False)
            self.reset_progress_bars()
            self.update_notebook_url_display(None)
            self.statusBar().showMessage(tr('force_canceled'), 5000)

    def _check_cancel_complete(self):
        """Check if cancel is complete"""
        try:
            if self._closing:
                return
                
            if self.model_download_thread and self.model_download_thread.isRunning():
                logger.warning("Download thread still running after cancel - forcing termination")
                self.model_download_thread.force_cancel()
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
        QMessageBox.warning(None, tr('already_running'), tr('already_running_msg'))
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_AUTHOR)
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