#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NotyCaption Pro - Professional AI Caption Generator
Version: 2026.3.0
Author: NotY215
License: Proprietary

This application provides professional caption generation with:
- AI-powered transcription using OpenAI Whisper
- Hardware acceleration detection (NVIDIA CUDA, AMD ROCm, Intel, OpenCL, Vulkan, Metal)
- Real-time hardware monitoring (CPU, GPU, RAM, temperature, usage)
- Performance history graphs
- Multi-monitor support with independent windows
- Smooth animations with 60 FPS rendering
- Comprehensive language support (English, Japanese, Russian, German, Hindi, Urdu, Arabic)
- Google Drive integration for cloud processing
- Vocal enhancement with Spleeter
- Advanced subtitle editing
- Dark/Light themes with customizable accents
"""

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
import platform
import math
import random
import hashlib
import pickle
import gzip
import zlib
import re
import uuid
import weakref
import gc
import ctypes
import signal
import atexit
import queue
import collections
import itertools
import functools
import operator
import pathlib
import glob
import fnmatch
import csv
import xml.etree.ElementTree as ET
import html
import urllib.parse
import urllib.request
import http.client
import http.cookiejar
import ssl
import certifi
import numpy as np
from tqdm import tqdm
from datetime import timedelta, datetime
from io import BytesIO, StringIO
from collections import deque, defaultdict, OrderedDict
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import Optional, Dict, List, Any, Tuple, Union, Callable, Generator, Iterator
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count, Manager
from ctypes import wintypes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

# PyQt5 imports
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QTextEdit, QFileDialog,
    QMessageBox, QLineEdit, QScrollArea, QSlider, QProgressBar, QDialog,
    QGroupBox, QRadioButton, QStyleFactory, QTabWidget, QButtonGroup,
    QFrame, QGraphicsOpacityEffect, QStackedWidget, QStatusBar, QSystemTrayIcon,
    QMenu, QShortcut, QToolTip, QApplication, QSizePolicy, QSpacerItem,
    QDesktopWidget, QColorDialog, QFontDialog, QListWidget, QListWidgetItem,
    QSplitter, QSplitterHandle, QToolBar, QAction, QActionGroup, QDockWidget,
    QMainWindow, QMdiArea, QMdiSubWindow, QDesktopWidget, QSplashScreen,
    QProgressDialog, QInputDialog, QWizard, QWizardPage, QFormLayout,
    QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem,
    QGraphicsTextItem, QGraphicsDropShadowEffect, QGraphicsBlurEffect,
    QGraphicsOpacityEffect, QGraphicsColorizeEffect, QGraphicsScale,
    QGraphicsRotation, QGraphicsPixmapItem, QGraphicsProxyWidget,
    QStyleOption, QStylePainter, QCommonStyle, QProxyStyle, QStyle,
    QWhatsThis, QUndoView, QUndoStack, QUndoCommand, QUndoGroup,
    QToolButton, QCommandLinkButton, QDialogButtonBox, QButtonGroup,
    QCheckBox, QAbstractButton, QAbstractSpinBox, QDateTimeEdit,
    QDateEdit, QTimeEdit, QCalendarWidget, QLCDNumber, QDial, QRubberBand,
    QDesktopServices, QShortcut, QKeySequenceEdit, QFontComboBox,
    QDoubleSpinBox, QTextBrowser, QPlainTextEdit, QStackedLayout,
    QFormLayout, QGridLayout, QBoxLayout, QLayout, QSizePolicy,
    QSpacerItem, QWidgetItem, QLayoutItem, QBoxLayout, QHBoxLayout,
    QVBoxLayout, QGridLayout, QFormLayout, QStackedLayout, QDockWidget,
    QMainWindow, QMdiArea, QMdiSubWindow, QToolBar, QAction, QActionGroup,
    QMenuBar, QMenu, QStatusBar, QToolTip, QWhatsThis, QSizeGrip,
    QDesktopWidget, QSplashScreen, QProgressDialog, QInputDialog,
    QWizard, QWizardPage, QWizard, QErrorMessage, QErrorMessage,
    QMessageBox, QApplication, QStyleFactory
)
from PyQt5.QtGui import (
    QIcon, QColor, QTextCharFormat, QTextCursor, QFont, QPalette, QCloseEvent,
    QPixmap, QBrush, QLinearGradient, QDesktopServices, QKeySequence, QPainter,
    QPen, QRadialGradient, QFontDatabase, QPainterPath, QImage, QImageWriter,
    QTextDocument, QAbstractTextDocumentLayout, QTextBlock, QTextLayout,
    QTextOption, QTextFormat, QTextList, QTextTable, QTextFrame, QTextCursor,
    QTextCharFormat, QTextBlockFormat, QTextListFormat, QTextTableFormat,
    QTextFrameFormat, QTextImageFormat, QSyntaxHighlighter, QTextDocument,
    QTextCursor, QTextCharFormat, QTextBlockFormat, QTextListFormat,
    QTextTableFormat, QTextFrameFormat, QTextImageFormat, QSyntaxHighlighter,
    QFontMetrics, QFontMetricsF, QRegion, QTransform, QMatrix, QPolygon,
    QPolygonF, QLine, QLineF, QRect, QRectF, QPoint, QPointF, QSize, QSizeF,
    QMatrix4x4, QVector2D, QVector3D, QVector4D, QQuaternion, QOpenGLContext,
    QOpenGLFunctions, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer,
    QOpenGLVertexArrayObject, QOpenGLTexture, QOpenGLFramebufferObject,
    QOpenGLPaintDevice, QOpenGLWidget, QOpenGLWindow, QSurfaceFormat,
    QWindow, QScreen, QGuiApplication, QCursor, QClipboard, QDrag,
    QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent,
    QFileOpenEvent, QInputMethod, QInputMethodEvent, QKeyEvent, QMouseEvent,
    QMoveEvent, QPaintEvent, QResizeEvent, QShowEvent, QHideEvent,
    QCloseEvent, QFocusEvent, QWheelEvent, QTabletEvent, QTouchEvent,
    QGestureEvent, QNativeGestureEvent, QShortcutEvent, QHelpEvent,
    QStatusTipEvent, QWhatsThisClickedEvent, QActionEvent, QContextMenuEvent
)
from PyQt5.QtCore import (
    QTimer, Qt, QUrl, QDir, pyqtSignal, QThread, pyqtSlot, QPropertyAnimation,
    QEasingCurve, QProcess, QSettings, QTranslator, QLocale, QPoint, QRect,
    QSize, QParallelAnimationGroup, QPauseAnimation, QPointF, QRectF,
    QByteArray, QDataStream, QIODevice, QBuffer, QFile, QFileInfo, QDir,
    QFileSystemWatcher, QTime, QDate, QDateTime, QElapsedTimer, QBasicTimer,
    QTimerEvent, QEvent, QCoreApplication, QObject, QThread, QRunnable,
    QThreadPool, QMutex, QMutexLocker, QReadWriteLock, QReadLocker, QWriteLocker,
    QSemaphore, QWaitCondition, QAtomicInt, QAtomicPointer, QFuture,
    QFutureWatcher, QFutureSynchronizer, QtConcurrent, QOperatingSystemVersion,
    QLibrary, QLibraryInfo, QPluginLoader, QFactoryInterface, QMetaObject,
    QMetaEnum, QMetaClassInfo, QMetaProperty, QMetaMethod, QVariant,
    QGenericArgument, QGenericReturnArgument, Q_ARG, Q_RETURN_ARG,
    QT_VERSION, QT_VERSION_STR, PYQT_VERSION, PYQT_VERSION_STR,
    qVersion, qFatal, qWarning, qDebug, qInstallMessageHandler,
    qRegisterResourceData, qUnregisterResourceData, qCompress, qUncompress
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebSockets import QWebSocket, QWebSocketServer
from PyQt5.QtSvg import QSvgRenderer, QSvgWidget, QGraphicsSvgItem
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog, QPrinterInfo
from PyQt5.QtTest import QTest
from PyQt5.QtHelp import QHelpEngine, QHelpContentWidget, QHelpIndexWidget, QHelpSearchEngine
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin, QPyDesignerTaskMenuExtension
from PyQt5.QtUiTools import QUiLoader
from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode, QDomNodeList
from PyQt5.QtXmlPatterns import QXmlQuery, QXmlResultItems, QXmlSerializer
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel, QSqlRelationalTableModel
from PyQt5.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QBluetoothSocket
from PyQt5.QtNfc import QNearFieldManager, QNdefMessage, QNdefRecord, QNdefFilter
from PyQt5.QtPositioning import QGeoCoordinate, QGeoPositionInfo, QGeoPositionInfoSource
from PyQt5.QtSensors import QSensor, QSensorReading, QAccelerometer, QGyroscope, QMagnetometer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtLocation import QGeoServiceProvider, QGeoCodingManager, QGeoRoutingManager
from PyQt5.QtTextToSpeech import QTextToSpeech
from PyQt5.QtSpeech import QTextToSpeech as QTextToSpeech5

# Media processing
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.video.VideoClip import VideoClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.audio.fx.all import audio_fadein, audio_fadeout
from moviepy.video.fx.all import fadein, fadeout, resize, rotate, speedx
import pysrt
import pysubs2
import whisper
import whisper.utils
import whisper.audio
import whisper.tokenizer
import whisper.decoding
import whisper.model

# Google APIs
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import google.auth
import google.oauth2
import google_auth_oauthlib
import googleapiclient

# Audio processing
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from spleeter.model import ModelManager
from spleeter.utils.configuration import load_configuration
import librosa
import soundfile as sf
import audioread
import pydub
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
import noisereduce as nr
import pyloudnorm as pyln
import pyrubberband as pyrb
import pedalboard
from pedalboard import Pedalboard, Compressor, Limiter, NoiseGate, Reverb, Gain
import resampy
import sox
import wave
import contextlib

# Hardware detection and monitoring
import GPUtil
import psutil
import cpuinfo
import pynvml
import pyamdgpuinfo
import pyadl
import OpenGL
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu
import pyopencl as cl
import pyopencl.array
import vulkan as vk
import dxgi
import wmi
import pythoncom
import comtypes
import comtypes.client
import win32api
import win32con
import win32gui
import win32process
import win32security
import win32service
import win32serviceutil
import win32event
import win32file
import win32pipe
import win32print
import win32ui
import win32clipboard
import win32cred
import win32crypt
import win32net
import win32netcon
import win32profile
import win32ras
import win32ts
import win32verstamp
import win32wnet
import winerror
import pywintypes
import pythoncom
from ctypes import wintypes, byref, Structure, c_uint, c_ulong, c_char, c_int, c_long, c_short, c_ushort, c_void_p, POINTER, WINFUNCTYPE

# Visualization and graphics
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Polygon
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.colors import LinearSegmentedColormap, ColorConverter
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import pyqtgraph as pg
import vispy
import vispy.app
import vispy.scene
import vispy.scene.visuals
from vispy import gloo
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import mayavi.mlab as mlab
from mayavi import mlab
import mayavi.tools as mtools

# Machine Learning and AI
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, optimizers, losses, metrics
from transformers import (
    AutoTokenizer, AutoModel, AutoModelForCausalLM, AutoModelForSeq2SeqLM,
    pipeline, set_seed, Trainer, TrainingArguments, DataCollator
)
import transformers
from sentence_transformers import SentenceTransformer
import langdetect
from langdetect import detect, detect_langs
import googletrans
from googletrans import Translator as GoogleTranslator
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import spacy
import textblob
from textblob import TextBlob
import fasttext
import fasttext.util
import ctranslate2
import onnxruntime as ort
import onnx
import openvino
import openvino.inference_engine as ie
import tritonclient
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import cupy as cp
import numba
from numba import cuda as numba_cuda, jit, vectorize
import dask
import dask.array as da
import dask.dataframe as dd
import ray
import modin
import vaex

# Database and storage
import sqlite3
import pymongo
from pymongo import MongoClient
import redis
from redis import Redis
import elasticsearch
from elasticsearch import Elasticsearch
import cassandra
from cassandra.cluster import Cluster
import influxdb
from influxdb import InfluxDBClient
import timescaledb
import clickhouse_driver
from clickhouse_driver import Client as ClickHouseClient
import duckdb
import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.feather as feather
import h5py
import zarr
import xarray as xr
import netCDF4
import blosc
import lz4
import snappy
import zstandard as zstd
import bz2
import lzma
import brotli

# Web and networking
import aiohttp
import asyncio
import websockets
import socketio
import flask
from flask import Flask, request, jsonify, render_template
import fastapi
from fastapi import FastAPI, HTTPException, WebSocket
import uvicorn
import gunicorn
import nginx
import apache
import tornado
import twisted
import scrapy
import beautifulsoup4 as bs4
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import urllib3
import httpx
import curl
import pycurl
import mechanize
import robobrowser
import mechanicalsoup
import cloudscraper
import cfscrape
import twill
import webbot

# Cryptography and security
import jwt
from jose import JWTError, jwt as jose_jwt
import passlib
from passlib.hash import bcrypt, argon2, scrypt
import argon2
from argon2 import PasswordHasher
import bcrypt
import scrypt
import hashlib
import hmac
import secrets
import pyotp
import qrcode
import keyring
import keyczar
from keyczar import keyczar
import pyarmor
import pytransform
import obfuscator
import pyminifier
import uncompyle6
import xdis
import pycdc
import unpy2exe
import pyinstxtractor
import pyi_archive_viewer

# System and OS
import ctypes.wintypes
import winreg
import _winreg
import msilib
import msi
import pywintypes
import pythoncom
import win32com
import win32com.client
import win32com.server
import win32com.universal
import win32com.storagecon
import win32com.shell
import win32com.shell.shell
import win32com.shell.shellcon
import win32com.propsys
import win32com.propsys.pscon
import win32com.bits
import win32com.taskscheduler
import win32com.adsi
import win32com.axdebug
import win32com.axcontrol
import win32com.axscript
import win32com.axscript.client
import win32com.axscript.server
import win32com.axscript.script
import win32com.demos
import win32com.html
import win32com.iface
import win32com.internet
import win32com.mapi
import win32com.mapi.mapitags
import win32com.mapi.mapiutil
import win32com.ole
import win32com.oleacc
import win32com.oledb
import win32com.pythoncom
import win32com.record
import win32com.scripter
import win32com.storagecon
import win32com.sysmon
import win32com.test
import win32com.universal
import win32com.util
import win32com.webbrowser
import win32com.windows
import win32com.windowsx
import win32com.win32com
import win32com.win32com.client
import win32com.win32com.server

# ========================================
# LOGGING SETUP (MUST BE FIRST)
# ========================================
def setup_logging():
    """Initialize logging with rotation and compression"""
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
    log_file = os.path.join(log_dir, f"NotyCaption_{timestamp}.log")
    
    # Create rotating file handler with compression
    class CompressedRotatingFileHandler(logging.Handler):
        def __init__(self, filename, max_bytes=10485760, backup_count=5):
            super().__init__()
            self.filename = filename
            self.max_bytes = max_bytes
            self.backup_count = backup_count
            self.stream = None
            self._open()
            
        def _open(self):
            if self.stream:
                self.stream.close()
            self.stream = open(self.filename, 'a', encoding='utf-8')
            
        def _rotate(self):
            if self.stream:
                self.stream.close()
                
            if os.path.exists(self.filename):
                if os.path.getsize(self.filename) > self.max_bytes:
                    # Rotate existing files
                    for i in range(self.backup_count - 1, 0, -1):
                        src = f"{self.filename}.{i}.gz"
                        dst = f"{self.filename}.{i+1}.gz"
                        if os.path.exists(src):
                            os.rename(src, dst)
                    
                    # Compress current log
                    with open(self.filename, 'rb') as f_in:
                        with gzip.open(f"{self.filename}.1.gz", 'wb') as f_out:
                            f_out.write(f_in.read())
                    
                    # Truncate current log
                    open(self.filename, 'w').close()
                    
            self._open()
            
        def emit(self, record):
            try:
                msg = self.format(record)
                self.stream.write(msg + '\n')
                self.stream.flush()
                self._rotate()
            except Exception:
                self.handleError(record)
                
    handler = CompressedRotatingFileHandler(log_file)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s'
    ))
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            handler,
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )
    
    logger = logging.getLogger("NotyCaption")
    logger.info("=" * 80)
    logger.info("NotyCaption Pro Secure Launch 2026")
    logger.info("=" * 80)
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Processor: {platform.processor()}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Log file: {log_file}")
    logger.info(f"Executable: {sys.executable if getattr(sys, 'frozen', False) else 'development mode'}")
    
    return logger

# Initialize logger immediately
logger = setup_logging()

# ========================================
# CONFIGURATION AND CONSTANTS
# ========================================
APP_NAME = "NotyCaption Pro"
APP_AUTHOR = "NotY215"
APP_VERSION = "2026.3.0"
APP_BUILD = datetime.now().strftime("%Y%m%d")
APP_COPYRIGHT = f"Copyright © 2026 {APP_AUTHOR}. All rights reserved."

# Get app data directory for settings
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    if platform.system() == "Windows":
        APP_DATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), f"{APP_NAME.replace(' ', '')}Saves")
    else:
        # Linux/Mac fallback
        APP_DATA_DIR = os.path.join(os.path.expanduser('~'), f".{APP_NAME.lower().replace(' ', '')}saves")
else:
    # Running in development
    APP_DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Create app data directory if it doesn't exist
os.makedirs(APP_DATA_DIR, exist_ok=True)

# Configuration file paths
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.notcapz")
KEY_FILE = os.path.join(APP_DATA_DIR, "key.notcapz")
SESSION_FILE = os.path.join(APP_DATA_DIR, "session.json")
TOKEN_FILE = os.path.join(APP_DATA_DIR, "token.json")
CLIENT_JSON = os.path.join(APP_DATA_DIR, "client.json")
CLIENT_ENCRYPTED = os.path.join(APP_DATA_DIR, "client.notycapz")
LAYOUTS_DIR = os.path.join(APP_DATA_DIR, "layouts")
PRESETS_DIR = os.path.join(APP_DATA_DIR, "presets")
CACHE_DIR = os.path.join(APP_DATA_DIR, "cache")
THEMES_DIR = os.path.join(APP_DATA_DIR, "themes")
PLUGINS_DIR = os.path.join(APP_DATA_DIR, "plugins")
EXPORTS_DIR = os.path.join(APP_DATA_DIR, "exports")
BACKUPS_DIR = os.path.join(APP_DATA_DIR, "backups")
PROFILES_DIR = os.path.join(APP_DATA_DIR, "profiles")
MONITORING_DIR = os.path.join(APP_DATA_DIR, "monitoring")
GRAPHS_DIR = os.path.join(APP_DATA_DIR, "graphs")
TEMP_DIR = os.path.join(APP_DATA_DIR, "temp")

# Create all directories
for dir_path in [LAYOUTS_DIR, PRESETS_DIR, CACHE_DIR, THEMES_DIR, PLUGINS_DIR,
                 EXPORTS_DIR, BACKUPS_DIR, PROFILES_DIR, MONITORING_DIR,
                 GRAPHS_DIR, TEMP_DIR]:
    os.makedirs(dir_path, exist_ok=True)

logger.info(f"App data directory: {APP_DATA_DIR}")
logger.info(f"All application directories created successfully")

# ========================================
# ENCRYPTION UTILS
# ========================================
def generate_key_from_password(password: str, salt: bytes = None) -> tuple:
    """Generate encryption key from password using PBKDF2"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def load_or_create_key() -> bytes:
    """Load existing encryption key or create new one"""
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
            key_path = KEY_FILE
            if os.path.exists(key_path):
                with open(key_path, "rb") as f:
                    key_data = f.read()
                logger.info("Fallback key loaded from app data")
                return key_data
            else:
                # Generate new key with password
                password = APP_NAME + APP_AUTHOR + APP_VERSION
                key, salt = generate_key_from_password(password)
                
                # Save salt with key
                with open(KEY_FILE, "wb") as f:
                    f.write(salt + key)
                logger.info("New encryption key generated")
                return key

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            data = f.read()
            salt = data[:16]
            key = data[16:]
        logger.info("Local dev key loaded")
        return key

    logger.info("No key found - generating new one")
    password = APP_NAME + APP_AUTHOR + APP_VERSION
    key, salt = generate_key_from_password(password)
    with open(KEY_FILE, "wb") as f:
        f.write(salt + key)
    return key

# Initialize Fernet cipher
try:
    key = load_or_create_key()
    fernet = Fernet(key)
    logger.info("Encryption initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize encryption: {e}")
    # Create fallback key
    key = Fernet.generate_key()
    fernet = Fernet(key)
    logger.warning("Using fallback encryption key")

def encrypt_data(data: Any) -> str:
    """Encrypt data with compression"""
    try:
        # Convert to JSON and compress
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        compressed = zlib.compress(json_str.encode('utf-8'), level=9)
        
        # Encrypt
        encrypted = fernet.encrypt(compressed)
        
        # Base64 encode for storage
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        return base64.b64encode(json.dumps(data).encode()).decode()

def decrypt_data(encrypted_b64: str) -> Optional[Any]:
    """Decrypt and decompress data"""
    try:
        # Base64 decode
        encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
        
        # Decrypt
        decrypted = fernet.decrypt(encrypted)
        
        # Decompress
        decompressed = zlib.decompress(decrypted)
        
        # Parse JSON
        return json.loads(decompressed.decode('utf-8'))
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        try:
            # Try without compression (backward compatibility)
            encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
            decrypted = fernet.decrypt(encrypted)
            return json.loads(decrypted.decode('utf-8'))
        except:
            return None

def save_settings(settings_dict: dict) -> bool:
    """Save settings encrypted"""
    try:
        encrypted_b64 = encrypt_data(settings_dict)
        with open(SETTINGS_FILE, "w", encoding='utf-8') as f:
            f.write(encrypted_b64)
        logger.info(f"Settings saved securely to {SETTINGS_FILE}")
        return True
    except Exception as e:
        logger.error(f"Failed to save settings: {e}")
        return False

def load_settings() -> dict:
    """Load settings with defaults"""
    defaults = {
        "ui_scale": "100%",
        "theme": "Dark",
        "temp_dir": tempfile.gettempdir(),
        "models_dir": APP_DATA_DIR,
        "cache_dir": CACHE_DIR,
        "last_mode": "normal",
        "auto_enhance": False,
        "default_lang": "English",
        "force_cancel_timeout": 30,
        "max_retry_attempts": 5,
        "confirm_cancel": True,
        "minimize_to_tray": True,
        "show_tooltips": True,
        "words_per_line": 5,
        "output_format": "SRT",
        "last_input_file": "",
        "last_output_folder": "",
        "window_geometry": None,
        "window_state": None,
        "language": "en",
        "window_width": 1280,
        "window_height": 800,
        "window_maximized": False,
        "accent_color": "#4a6fa5",
        "glow_intensity": 50,
        "animation_speed": "normal",
        "enable_animations": True,
        "card_opacity": 80,
        "font_family": "Segoe UI",
        "font_size": 14,
        "hardware_monitoring": True,
        "monitoring_interval": 1000,  # ms
        "performance_graphs": True,
        "graph_history": 300,  # seconds
        "multi_monitor": False,
        "monitor_index": 0,
        "preview_widget_enabled": True,
        "auto_save": True,
        "auto_save_interval": 300,  # seconds
        "backup_count": 10,
        "export_format": "SRT",
        "export_encoding": "utf-8",
        "export_newline": "\r\n",
        "export_bom": False,
        "timestamp_format": "HH:MM:SS,mmm",
        "subtitle_offset": 0,  # ms
        "subtitle_duration_factor": 1.0,
        "max_line_length": 42,
        "max_lines": 2,
        "word_break": True,
        "highlight_current": True,
        "highlight_color": "#ffd700",
        "highlight_opacity": 180,
        "player_volume": 100,
        "player_speed": 1.0,
        "player_loop": False,
        "player_shuffle": False,
        "auto_scroll": True,
        "scroll_smooth": True,
        "scroll_speed": 50,
        "keyboard_shortcuts": True,
        "mouse_wheel": True,
        "touch_support": True,
        "gesture_support": True,
        "high_dpi": True,
        "opengl_rendering": True,
        "vsync": True,
        "fps_limit": 60,
        "smooth_animation": True,
        "particle_effects": False,
        "transparency_effects": True,
        "shadow_effects": True,
        "blur_effects": False,
        "colorize_effects": False,
        "custom_cursor": False,
        "custom_scrollbar": True,
        "custom_titlebar": False,
        "native_menubar": True,
        "native_dialogs": True,
        "system_tray": True,
        "start_minimized": False,
        "auto_update": True,
        "update_check_interval": 86400,  # seconds
        "beta_updates": False,
        "telemetry": False,
        "crash_reporting": True,
        "log_level": "INFO",
        "log_rotation": True,
        "log_max_size": 10485760,  # 10 MB
        "log_backup_count": 5,
        "log_compress": True,
        "debug_mode": False,
        "developer_mode": False,
        "plugin_enabled": True,
        "plugin_auto_load": False,
        "plugin_sandbox": True,
        "scripting_enabled": False,
        "macro_enabled": False,
        "batch_mode": False,
        "headless_mode": False,
        "remote_control": False,
        "web_interface": False,
        "api_enabled": False,
        "api_port": 8080,
        "api_key": "",
        "api_ssl": False,
        "api_cert": "",
        "api_key_file": "",
        "database_enabled": False,
        "database_type": "sqlite",
        "database_host": "localhost",
        "database_port": 3306,
        "database_name": "notycaption",
        "database_user": "",
        "database_password": "",
        "database_ssl": False,
        "cloud_sync": False,
        "cloud_provider": "google",
        "cloud_folder": "NotyCaption",
        "cloud_auto_sync": False,
        "cloud_sync_interval": 3600,  # seconds
        "encryption_enabled": True,
        "encryption_method": "fernet",
        "password_protect": False,
        "master_password": "",
        "session_restore": True,
        "session_autosave": True,
        "session_max": 10,
        "undo_depth": 100,
        "redo_depth": 100,
        "history_enabled": True,
        "history_max": 1000,
        "recent_files": [],
        "recent_max": 10,
        "favorite_files": [],
        "favorite_folders": [],
        "bookmarks": [],
        "notes": [],
        "tags": [],
        "categories": [],
        "collections": [],
        "playlists": [],
        "queues": [],
        "templates": [],
        "snippets": [],
        "macros": [],
        "scripts": [],
        "plugins": [],
        "themes": [],
        "layouts": [],
        "presets": [],
        "profiles": [],
        "workspaces": [],
        "projects": []
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
            # Merge with defaults (keep defaults for missing keys)
            for key, value in loaded.items():
                if key in defaults:
                    defaults[key] = value
                else:
                    logger.warning(f"Unknown setting in saved config: {key}")
            
            # Ensure all paths exist
            for path_key in ['temp_dir', 'models_dir', 'cache_dir']:
                if path_key in defaults:
                    path = defaults[path_key]
                    if not os.path.exists(path):
                        os.makedirs(path, exist_ok=True)
                        logger.info(f"Created missing directory: {path}")
            
            logger.info("Settings loaded and merged with defaults")
            return defaults
        else:
            logger.warning("Decryption failed, saving defaults")
            save_settings(defaults)
            return defaults
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        save_settings(defaults)
        return defaults

def load_client_secrets() -> Optional[dict]:
    """Load Google OAuth client secrets"""
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
# ENUMS AND DATA CLASSES
# ========================================
class ProcessingMode(Enum):
    """Processing mode enumeration"""
    LOCAL = auto()
    ONLINE = auto()
    HYBRID = auto()
    BATCH = auto()
    DISTRIBUTED = auto()

class Theme(Enum):
    """Theme enumeration"""
    SYSTEM = auto()
    LIGHT = auto()
    DARK = auto()
    CUSTOM = auto()

class Language(Enum):
    """Supported languages"""
    ENGLISH = "en"
    JAPANESE = "ja"
    RUSSIAN = "ru"
    GERMAN = "de"
    HINDI = "hi"
    URDU = "ur"
    ARABIC = "ar"
    SPANISH = "es"
    FRENCH = "fr"
    CHINESE = "zh"
    KOREAN = "ko"
    PORTUGUESE = "pt"
    ITALIAN = "it"
    DUTCH = "nl"
    POLISH = "pl"
    TURKISH = "tr"
    VIETNAMESE = "vi"
    THAI = "th"
    BENGALI = "bn"
    PUNJABI = "pa"
    TAMIL = "ta"
    TELUGU = "te"
    MARATHI = "mr"
    GUJARATI = "gu"
    KANNADA = "kn"
    MALAYALAM = "ml"
    ORIYA = "or"
    ASSAMESE = "as"
    MAITHILI = "mai"
    SANTALI = "sat"
    KASHMIRI = "ks"
    NEPALI = "ne"
    SINHALA = "si"
    BURMESE = "my"
    KHMER = "km"
    LAO = "lo"
    MONGOLIAN = "mn"
    TIBETAN = "bo"
    UIGHUR = "ug"
    KAZAKH = "kk"
    KYRGYZ = "ky"
    TAJIK = "tg"
    TURKMEN = "tk"
    UZBEK = "uz"
    AZERBAIJANI = "az"
    GEORGIAN = "ka"
    ARMENIAN = "hy"
    GREEK = "el"
    ALBANIAN = "sq"
    BOSNIAN = "bs"
    BULGARIAN = "bg"
    CROATIAN = "hr"
    CZECH = "cs"
    DANISH = "da"
    ESTONIAN = "et"
    FINNISH = "fi"
    HUNGARIAN = "hu"
    ICELANDIC = "is"
    IRISH = "ga"
    LATVIAN = "lv"
    LITHUANIAN = "lt"
    MACEDONIAN = "mk"
    MALTESE = "mt"
    NORWEGIAN = "no"
    ROMANIAN = "ro"
    SERBIAN = "sr"
    SLOVAK = "sk"
    SLOVENIAN = "sl"
    SWEDISH = "sv"
    UKRAINIAN = "uk"
    WELSH = "cy"
    YIDDISH = "yi"
    AFRIKAANS = "af"
    AMHARIC = "am"
    HAUSA = "ha"
    IGBO = "ig"
    SOMALI = "so"
    SWAHILI = "sw"
    YORUBA = "yo"
    ZULU = "zu"
    CEBUANO = "ceb"
    HAWAIIAN = "haw"
    HMONG = "hmn"
    JAVANESE = "jv"
    SUNDANESE = "su"
    TAGALOG = "tl"
    WARAY = "war"
    XHOSA = "xh"
    SESOTHO = "st"
    TSONGA = "ts"
    TSWANA = "tn"
    VENDA = "ve"
    NDEBELE = "nr"
    SWATI = "ss"
    SAMOAN = "sm"
    TAHITIAN = "ty"
    TONGAN = "to"
    MAORI = "mi"
    FIJIAN = "fj"
    MARSHALLESE = "mh"
    PALAUAN = "pw"
    CHAMORRO = "ch"
    CAROLINIAN = "cal"
    YAPESE = "yap"
    POHNPEIAN = "pon"
    KOSRAEAN = "kos"
    CHUUKESE = "chk"
    ULITHIAN = "uli"
    WOLEAIAN = "woe"
    NUKUORO = "nkr"
    KAPINGAMARANGI = "kpg"
    MORTLOCKESE = "mrl"
    NAMONUITO = "nmt"
    PULUWAT = "puw"
    SATTAWAL = "stw"
    CAROLINIAN = "cal"

class SubtitleFormat(Enum):
    """Subtitle format enumeration"""
    SRT = ".srt"
    ASS = ".ass"
    SSA = ".ssa"
    SUB = ".sub"
    TXT = ".txt"
    VTT = ".vtt"
    SCC = ".scc"
    TTML = ".ttml"
    DFXP = ".dfxp"
    SBV = ".sbv"
    LRC = ".lrc"
    SMI = ".smi"
    RT = ".rt"
    STL = ".stl"
    PAC = ".pac"
    CHK = ".chk"
    CAP = ".cap"
    ASC = ".asc"
    AQT = ".aqt"
    JSS = ".jss"
    PJS = ".pjs"
    PSB = ".psb"
    USF = ".usf"
    XML = ".xml"

class GPUType(Enum):
    """GPU type enumeration"""
    NVIDIA_CUDA = auto()
    AMD_ROCM = auto()
    INTEL_OPENCL = auto()
    APPLE_METAL = auto()
    VULKAN = auto()
    DIRECTX = auto()
    OPENGL = auto()
    SOFTWARE = auto()

class HardwareStatus(Enum):
    """Hardware status enumeration"""
    AVAILABLE = auto()
    UNAVAILABLE = auto()
    LIMITED = auto()
    ERROR = auto()
    UNKNOWN = auto()

@dataclass
class GPUInfo:
    """GPU information data class"""
    name: str
    type: GPUType
    vendor: str
    memory_total: int  # bytes
    memory_used: int
    memory_free: int
    temperature: float
    utilization: float
    power_usage: float
    clock_core: int
    clock_memory: int
    driver_version: str
    cuda_cores: Optional[int] = None
    rocm_cores: Optional[int] = None
    opencl_units: Optional[int] = None
    vulkan_version: Optional[str] = None
    directx_version: Optional[str] = None
    opengl_version: Optional[str] = None
    metal_version: Optional[str] = None
    pcie_version: Optional[str] = None
    pcie_lanes: Optional[int] = None
    pcie_speed: Optional[int] = None
    serial: Optional[str] = None
    uuid: Optional[str] = None
    bios_version: Optional[str] = None
    vbios_version: Optional[str] = None
    subsystem_id: Optional[str] = None
    device_id: Optional[str] = None
    revision_id: Optional[str] = None
    board_id: Optional[str] = None
    bus_id: Optional[str] = None
    domain_id: Optional[str] = None
    slot_id: Optional[str] = None
    link_width: Optional[int] = None
    link_speed: Optional[str] = None
    max_link_width: Optional[int] = None
    max_link_speed: Optional[str] = None
    performance_state: Optional[str] = None
    throttling_reason: Optional[str] = None
    ecc_enabled: bool = False
    ecc_errors: Optional[dict] = None
    compute_mode: Optional[str] = None
    persistence_mode: bool = False
    accounting_mode: bool = False
    display_mode: bool = False
    display_active: bool = False
    fan_speed: Optional[int] = None
    fan_rpm: Optional[int] = None
    voltage: Optional[float] = None
    current: Optional[float] = None
    power_limit: Optional[float] = None
    power_default_limit: Optional[float] = None
    power_min_limit: Optional[float] = None
    power_max_limit: Optional[float] = None
    thermal_limit: Optional[float] = None
    memory_temperature: Optional[float] = None
    board_temperature: Optional[float] = None
    hotspot_temperature: Optional[float] = None
    gpu_slowdown_temperature: Optional[float] = None
    shutdown_temperature: Optional[float] = None

@dataclass
class CPUInfo:
    """CPU information data class"""
    name: str
    vendor: str
    architecture: str
    cores_physical: int
    cores_logical: int
    threads: int
    base_frequency: float
    max_frequency: float
    current_frequency: float
    temperature: float
    utilization: float
    power_usage: float
    cache_l1: int
    cache_l2: int
    cache_l3: int
    instructions_sets: List[str]
    virtualization: bool
    hypervisor: bool
    smt_enabled: bool
    turbo_enabled: bool
    overclocked: bool
    voltage: Optional[float] = None
    tdp: Optional[int] = None
    socket: Optional[str] = None
    stepping: Optional[int] = None
    model: Optional[int] = None
    family: Optional[int] = None
    ext_family: Optional[int] = None
    ext_model: Optional[int] = None
    microcode: Optional[str] = None
    cpuid: Optional[str] = None
    serial: Optional[str] = None

@dataclass
class RAMInfo:
    """RAM information data class"""
    total: int  # bytes
    available: int
    used: int
    free: int
    cached: int
    buffers: int
    shared: int
    swap_total: int
    swap_used: int
    swap_free: int
    utilization: float
    swap_utilization: float
    speed: Optional[int] = None
    type: Optional[str] = None
    channels: Optional[int] = None
    slots: Optional[int] = None
    slots_used: Optional[int] = None
    form_factor: Optional[str] = None
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None
    serial_number: Optional[str] = None
    voltage: Optional[float] = None
    timing: Optional[str] = None
    ecc: bool = False
    registered: bool = False
    buffered: bool = False

@dataclass
class DiskInfo:
    """Disk information data class"""
    device: str
    mountpoint: str
    filesystem: str
    total: int
    used: int
    free: int
    utilization: float
    read_speed: float
    write_speed: float
    read_iops: int
    write_iops: int
    read_latency: float
    write_latency: float
    model: Optional[str] = None
    serial: Optional[str] = None
    firmware: Optional[str] = None
    interface: Optional[str] = None
    media_type: Optional[str] = None  # SSD, HDD, NVMe
    form_factor: Optional[str] = None
    temperature: Optional[float] = None
    health: Optional[str] = None
    power_on_hours: Optional[int] = None
    power_cycle_count: Optional[int] = None
    wear_level: Optional[float] = None
    bad_sectors: Optional[int] = None
    reallocated_sectors: Optional[int] = None
    pending_sectors: Optional[int] = None
    uncorrectable_sectors: Optional[int] = None
    crc_errors: Optional[int] = None
    trim_support: bool = False
    smart_support: bool = False
    nvme_support: bool = False
    ahci_support: bool = False
    raid_support: bool = False

@dataclass
class NetworkInfo:
    """Network information data class"""
    interface: str
    mac_address: str
    ip_addresses: List[str]
    gateway: str
    dns_servers: List[str]
    dhcp_enabled: bool
    dhcp_server: Optional[str] = None
    lease_obtained: Optional[datetime] = None
    lease_expires: Optional[datetime] = None
    speed: int
    mtu: int
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
    errors_in: int
    errors_out: int
    drops_in: int
    drops_out: int
    link_status: bool
    wireless: bool = False
    ssid: Optional[str] = None
    signal_strength: Optional[int] = None
    channel: Optional[int] = None
    frequency: Optional[int] = None
    encryption: Optional[str] = None
    mode: Optional[str] = None
    bssid: Optional[str] = None
    quality: Optional[float] = None

@dataclass
class BatteryInfo:
    """Battery information data class"""
    present: bool
    charging: bool
    percent: float
    time_remaining: Optional[int] = None  # seconds
    energy_full: Optional[int] = None
    energy_full_design: Optional[int] = None
    energy_now: Optional[int] = None
    power_now: Optional[int] = None
    voltage_now: Optional[int] = None
    cycle_count: Optional[int] = None
    technology: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial: Optional[str] = None
    temperature: Optional[float] = None
    health: Optional[str] = None
    status: Optional[str] = None

@dataclass
class HardwareSnapshot:
    """Hardware snapshot for performance history"""
    timestamp: datetime
    cpu_usage: float
    cpu_temp: float
    cpu_freq: float
    cpu_power: float
    gpu_usage: List[float]
    gpu_temp: List[float]
    gpu_memory: List[int]
    gpu_power: List[float]
    ram_usage: float
    ram_available: int
    swap_usage: float
    disk_usage: Dict[str, float]
    disk_io: Dict[str, tuple]  # (read, write)
    network_io: tuple  # (sent, received)
    battery_percent: Optional[float] = None
    process_count: int = 0
    thread_count: int = 0
    handle_count: int = 0
    uptime: int = 0
    load_average: Optional[tuple] = None

# ========================================
# HARDWARE DETECTION AND MONITORING
# ========================================
class HardwareMonitor:
    """Comprehensive hardware monitoring with all GPU support"""
    
    def __init__(self):
        self.gpus: List[GPUInfo] = []
        self.cpu: Optional[CPUInfo] = None
        self.ram: Optional[RAMInfo] = None
        self.disks: List[DiskInfo] = []
        self.networks: List[NetworkInfo] = []
        self.battery: Optional[BatteryInfo] = None
        
        self.history: deque = deque(maxlen=3600)  # 1 hour at 1 second intervals
        self.snapshots: List[HardwareSnapshot] = []
        
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.monitor_lock = threading.Lock()
        self.stop_event = threading.Event()
        
        self.nvml_initialized = False
        self.amd_initialized = False
        self.opencl_initialized = False
        self.vulkan_initialized = False
        
        self._init_nvml()
        self._init_amd()
        self._init_opencl()
        self._init_vulkan()
        self._init_wmi()
        
        # Initial detection
        self.detect_all()
        
        logger.info("Hardware monitor initialized")
        
    def _init_nvml(self):
        """Initialize NVIDIA NVML"""
        try:
            pynvml.nvmlInit()
            self.nvml_initialized = True
            logger.info("NVML initialized successfully")
        except Exception as e:
            logger.debug(f"NVML initialization failed: {e}")
            
    def _init_amd(self):
        """Initialize AMD GPU monitoring"""
        try:
            if pyamdgpuinfo.detect_gpus():
                self.amd_initialized = True
                logger.info(f"AMD GPU monitoring initialized: {pyamdgpuinfo.get_gpu_count()} GPUs detected")
        except Exception as e:
            logger.debug(f"AMD GPU monitoring initialization failed: {e}")
            
    def _init_opencl(self):
        """Initialize OpenCL"""
        try:
            platforms = cl.get_platforms()
            if platforms:
                self.opencl_initialized = True
                logger.info(f"OpenCL initialized: {len(platforms)} platforms")
        except Exception as e:
            logger.debug(f"OpenCL initialization failed: {e}")
            
    def _init_vulkan(self):
        """Initialize Vulkan"""
        try:
            vk.vkEnumerateInstanceVersion()
            self.vulkan_initialized = True
            logger.info("Vulkan initialized successfully")
        except Exception as e:
            logger.debug(f"Vulkan initialization failed: {e}")
            
    def _init_wmi(self):
        """Initialize WMI for Windows"""
        if platform.system() == "Windows":
            try:
                pythoncom.CoInitialize()
                self.wmi_conn = wmi.WMI()
                logger.info("WMI initialized successfully")
            except Exception as e:
                logger.debug(f"WMI initialization failed: {e}")
                
    def detect_gpu_nvidia(self) -> List[GPUInfo]:
        """Detect NVIDIA GPUs using NVML"""
        gpus = []
        if not self.nvml_initialized:
            return gpus
            
        try:
            device_count = pynvml.nvmlDeviceGetCount()
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                
                # Basic info
                name = pynvml.nvmlDeviceGetName(handle)
                uuid = pynvml.nvmlDeviceGetUUID(handle)
                serial = pynvml.nvmlDeviceGetSerial(handle)
                
                # Memory info
                memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                memory_total = memory_info.total
                memory_used = memory_info.used
                memory_free = memory_info.free
                
                # Utilization
                utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                gpu_util = utilization.gpu
                memory_util = utilization.memory
                
                # Temperature
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                
                # Power
                power_usage = pynvml.nvmlDeviceGetPowerUsage(handle)
                power_limit = pynvml.nvmlDeviceGetEnforcedPowerLimit(handle)
                
                # Clocks
                clock_core = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
                clock_memory = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
                clock_sm = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_SM)
                clock_video = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_VIDEO)
                
                # PCIe info
                pcie_info = pynvml.nvmlDeviceGetMaxPcieLinkGeneration(handle)
                pcie_width = pynvml.nvmlDeviceGetMaxPcieLinkWidth(handle)
                
                # Fan speed
                try:
                    fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
                except:
                    fan_speed = None
                    
                # ECC info
                try:
                    ecc_info = pynvml.nvmlDeviceGetMemoryErrorCounter(handle, pynvml.NVML_MEMORY_ERROR_TYPE_CORRECTED, pynvml.NVML_VOLATILE_ECC)
                except:
                    ecc_info = None
                    
                # Compute mode
                try:
                    compute_mode = pynvml.nvmlDeviceGetComputeMode(handle)
                except:
                    compute_mode = None
                    
                # Performance state
                try:
                    perf_state = pynvml.nvmlDeviceGetPerformanceState(handle)
                except:
                    perf_state = None
                    
                # Throttling reasons
                try:
                    throttle_reasons = pynvml.nvmlDeviceGetCurrentClocksThrottleReasons(handle)
                except:
                    throttle_reasons = None
                    
                # Driver version
                driver_version = pynvml.nvmlSystemGetDriverVersion()
                
                # CUDA cores (approximate)
                try:
                    cuda_cores = pynvml.nvmlDeviceGetCudaComputeCapability(handle)
                except:
                    cuda_cores = None
                    
                gpu = GPUInfo(
                    name=name.decode() if isinstance(name, bytes) else name,
                    type=GPUType.NVIDIA_CUDA,
                    vendor="NVIDIA",
                    memory_total=memory_total,
                    memory_used=memory_used,
                    memory_free=memory_free,
                    temperature=temp,
                    utilization=gpu_util,
                    power_usage=power_usage,
                    clock_core=clock_core,
                    clock_memory=clock_memory,
                    driver_version=driver_version.decode() if isinstance(driver_version, bytes) else driver_version,
                    cuda_cores=cuda_cores,
                    pcie_version=f"PCIe Gen{pcie_info}",
                    pcie_lanes=pcie_width,
                    uuid=uuid.decode() if isinstance(uuid, bytes) else uuid,
                    serial=serial.decode() if isinstance(serial, bytes) else serial,
                    fan_speed=fan_speed,
                    power_limit=power_limit,
                    performance_state=perf_state,
                    throttling_reason=throttle_reasons,
                    ecc_errors=ecc_info,
                    compute_mode=compute_mode
                )
                gpus.append(gpu)
                logger.info(f"NVIDIA GPU detected: {gpu.name}")
                
        except Exception as e:
            logger.error(f"Error detecting NVIDIA GPUs: {e}")
            
        return gpus
        
    def detect_gpu_amd(self) -> List[GPUInfo]:
        """Detect AMD GPUs using pyamdgpuinfo"""
        gpus = []
        if not self.amd_initialized:
            return gpus
            
        try:
            for i in range(pyamdgpuinfo.get_gpu_count()):
                gpu = pyamdgpuinfo.get_gpu(i)
                
                # Basic info
                name = gpu.name
                vendor = "AMD"
                memory_total = gpu.memory_total
                memory_used = gpu.memory_used
                memory_free = gpu.memory_free
                
                # Utilization
                gpu_util = gpu.load
                
                # Temperature
                temp = gpu.temperature
                
                # Power
                power_usage = gpu.power_draw
                power_limit = gpu.power_cap
                
                # Clocks
                clock_core = gpu.core_clock
                clock_memory = gpu.memory_clock
                
                # Fan speed
                fan_speed = gpu.fan_speed
                
                # Voltage
                voltage = gpu.voltage
                
                # PCIe info
                pcie_version = gpu.pcie_version
                pcie_lanes = gpu.pcie_lanes
                
                # GPU utilization
                utilization = gpu.utilization
                
                gpu_info = GPUInfo(
                    name=name,
                    type=GPUType.AMD_ROCM,
                    vendor=vendor,
                    memory_total=memory_total,
                    memory_used=memory_used,
                    memory_free=memory_free,
                    temperature=temp,
                    utilization=utilization,
                    power_usage=power_usage,
                    clock_core=clock_core,
                    clock_memory=clock_memory,
                    driver_version=gpu.driver_version,
                    rocm_cores=gpu.compute_units,
                    pcie_version=pcie_version,
                    pcie_lanes=pcie_lanes,
                    fan_speed=fan_speed,
                    power_limit=power_limit,
                    voltage=voltage
                )
                gpus.append(gpu_info)
                logger.info(f"AMD GPU detected: {gpu_info.name}")
                
        except Exception as e:
            logger.error(f"Error detecting AMD GPUs: {e}")
            
        return gpus
        
    def detect_gpu_intel(self) -> List[GPUInfo]:
        """Detect Intel GPUs using OpenCL and WMI"""
        gpus = []
        
        # Try OpenCL first
        if self.opencl_initialized:
            try:
                platforms = cl.get_platforms()
                for platform in platforms:
                    devices = platform.get_devices(device_type=cl.device_type.GPU)
                    for device in devices:
                        if "Intel" in device.vendor:
                            name = device.name
                            memory_total = device.global_mem_size
                            compute_units = device.max_compute_units
                            clock_core = device.max_clock_frequency
                            
                            gpu_info = GPUInfo(
                                name=name,
                                type=GPUType.INTEL_OPENCL,
                                vendor="Intel",
                                memory_total=memory_total,
                                memory_used=0,
                                memory_free=memory_total,
                                temperature=0,
                                utilization=0,
                                power_usage=0,
                                clock_core=clock_core,
                                clock_memory=0,
                                driver_version=platform.version,
                                opencl_units=compute_units
                            )
                            gpus.append(gpu_info)
                            logger.info(f"Intel GPU detected via OpenCL: {gpu_info.name}")
            except Exception as e:
                logger.error(f"Error detecting Intel GPU via OpenCL: {e}")
                
        # Try WMI on Windows
        if platform.system() == "Windows" and hasattr(self, 'wmi_conn'):
            try:
                for gpu in self.wmi_conn.Win32_VideoController():
                    if "Intel" in gpu.Name:
                        name = gpu.Name
                        try:
                            memory_total = int(gpu.AdapterRAM)
                        except:
                            memory_total = 0
                            
                        driver_version = gpu.DriverVersion
                        
                        gpu_info = GPUInfo(
                            name=name,
                            type=GPUType.INTEL_OPENCL,
                            vendor="Intel",
                            memory_total=memory_total,
                            memory_used=0,
                            memory_free=memory_total,
                            temperature=0,
                            utilization=0,
                            power_usage=0,
                            clock_core=0,
                            clock_memory=0,
                            driver_version=driver_version
                        )
                        
                        # Check if already added
                        if not any(g.name == name for g in gpus):
                            gpus.append(gpu_info)
                            logger.info(f"Intel GPU detected via WMI: {gpu_info.name}")
            except Exception as e:
                logger.error(f"Error detecting Intel GPU via WMI: {e}")
                
        return gpus
        
    def detect_gpu_apple(self) -> List[GPUInfo]:
        """Detect Apple GPUs using Metal (macOS only)"""
        gpus = []
        if platform.system() != "Darwin":
            return gpus
            
        try:
            # Use system_profiler to get GPU info
            result = subprocess.run(
                ['system_profiler', 'SPDisplaysDataType', '-json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if 'SPDisplaysDataType' in data:
                    for display in data['SPDisplaysDataType']:
                        if 'sppci_model' in display:
                            name = display['sppci_model']
                            metal_support = display.get('metal_support', 'Unknown')
                            
                            gpu_info = GPUInfo(
                                name=name,
                                type=GPUType.APPLE_METAL,
                                vendor="Apple",
                                memory_total=0,
                                memory_used=0,
                                memory_free=0,
                                temperature=0,
                                utilization=0,
                                power_usage=0,
                                clock_core=0,
                                clock_memory=0,
                                driver_version=platform.mac_ver()[0],
                                metal_version=metal_support
                            )
                            gpus.append(gpu_info)
                            logger.info(f"Apple GPU detected: {gpu_info.name}")
        except Exception as e:
            logger.error(f"Error detecting Apple GPU: {e}")
            
        return gpus
        
    def detect_gpu_vulkan(self) -> List[GPUInfo]:
        """Detect GPUs using Vulkan"""
        gpus = []
        if not self.vulkan_initialized:
            return gpus
            
        try:
            # Get Vulkan instance
            app_info = vk.VkApplicationInfo(
                sType=vk.VK_STRUCTURE_TYPE_APPLICATION_INFO,
                pApplicationName="NotyCaption",
                applicationVersion=1,
                pEngineName="NotyCaption Engine",
                engineVersion=1,
                apiVersion=vk.VK_API_VERSION_1_3
            )
            
            instance_info = vk.VkInstanceCreateInfo(
                sType=vk.VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
                pApplicationInfo=app_info
            )
            
            instance = vk.vkCreateInstance(instance_info, None)
            
            # Enumerate physical devices
            physical_devices = vk.vkEnumeratePhysicalDevices(instance)
            
            for device in physical_devices:
                properties = vk.vkGetPhysicalDeviceProperties(device)
                memory_properties = vk.vkGetPhysicalDeviceMemoryProperties(device)
                
                name = properties.deviceName
                device_type = properties.deviceType
                vendor_id = properties.vendorID
                device_id = properties.deviceID
                api_version = f"{vk.VK_VERSION_MAJOR(properties.apiVersion)}.{vk.VK_VERSION_MINOR(properties.apiVersion)}.{vk.VK_VERSION_PATCH(properties.apiVersion)}"
                driver_version = properties.driverVersion
                
                # Determine vendor
                if vendor_id == 0x10DE:
                    vendor = "NVIDIA"
                    gpu_type = GPUType.NVIDIA_CUDA
                elif vendor_id == 0x1002:
                    vendor = "AMD"
                    gpu_type = GPUType.AMD_ROCM
                elif vendor_id == 0x8086:
                    vendor = "Intel"
                    gpu_type = GPUType.INTEL_OPENCL
                elif vendor_id == 0x106B:
                    vendor = "Apple"
                    gpu_type = GPUType.APPLE_METAL
                else:
                    vendor = "Unknown"
                    gpu_type = GPUType.VULKAN
                    
                gpu_info = GPUInfo(
                    name=name,
                    type=gpu_type,
                    vendor=vendor,
                    memory_total=memory_properties.memoryHeaps[0].size if memory_properties.memoryHeaps else 0,
                    memory_used=0,
                    memory_free=0,
                    temperature=0,
                    utilization=0,
                    power_usage=0,
                    clock_core=0,
                    clock_memory=0,
                    driver_version=str(driver_version),
                    vulkan_version=api_version,
                    device_id=str(device_id)
                )
                gpus.append(gpu_info)
                logger.info(f"GPU detected via Vulkan: {gpu_info.name}")
                
            vk.vkDestroyInstance(instance, None)
            
        except Exception as e:
            logger.error(f"Error detecting GPUs via Vulkan: {e}")
            
        return gpus
        
    def detect_gpu_directx(self) -> List[GPUInfo]:
        """Detect GPUs using DirectX (Windows only)"""
        gpus = []
        if platform.system() != "Windows":
            return gpus
            
        try:
            # Use dxgi to enumerate adapters
            factory = dxgi.CreateDXGIFactory()
            adapter_index = 0
            while True:
                try:
                    adapter = factory.EnumAdapters(adapter_index)
                    desc = adapter.GetDesc()
                    
                    name = desc.Description
                    vendor_id = desc.VendorId
                    device_id = desc.DeviceId
                    subsystem_id = desc.SubSysId
                    revision = desc.Revision
                    
                    # Get adapter details
                    try:
                        output = adapter.EnumOutputs(0)
                        output_desc = output.GetDesc()
                    except:
                        output_desc = None
                        
                    # Determine vendor
                    if vendor_id == 0x10DE:
                        vendor = "NVIDIA"
                        gpu_type = GPUType.NVIDIA_CUDA
                    elif vendor_id == 0x1002:
                        vendor = "AMD"
                        gpu_type = GPUType.AMD_ROCM
                    elif vendor_id == 0x8086:
                        vendor = "Intel"
                        gpu_type = GPUType.INTEL_OPENCL
                    else:
                        vendor = "Unknown"
                        gpu_type = GPUType.DIRECTX
                        
                    # Get dedicated video memory
                    try:
                        memory_info = adapter.GetDesc().DedicatedVideoMemory
                    except:
                        memory_info = 0
                        
                    gpu_info = GPUInfo(
                        name=name,
                        type=gpu_type,
                        vendor=vendor,
                        memory_total=memory_info,
                        memory_used=0,
                        memory_free=memory_info,
                        temperature=0,
                        utilization=0,
                        power_usage=0,
                        clock_core=0,
                        clock_memory=0,
                        driver_version="",
                        directx_version="12",
                        device_id=str(device_id),
                        subsystem_id=str(subsystem_id),
                        revision_id=str(revision)
                    )
                    gpus.append(gpu_info)
                    logger.info(f"GPU detected via DirectX: {gpu_info.name}")
                    
                    adapter_index += 1
                    
                except:
                    break
                    
        except Exception as e:
            logger.error(f"Error detecting GPUs via DirectX: {e}")
            
        return gpus
        
    def detect_gpu_gputil(self) -> List[GPUInfo]:
        """Detect GPUs using GPUtil (NVIDIA only)"""
        gpus = []
        try:
            import GPUtil
            gputil_gpus = GPUtil.getGPUs()
            for gpu in gputil_gpus:
                gpu_info = GPUInfo(
                    name=gpu.name,
                    type=GPUType.NVIDIA_CUDA,
                    vendor="NVIDIA",
                    memory_total=int(gpu.memoryTotal * 1024 * 1024),
                    memory_used=int(gpu.memoryUsed * 1024 * 1024),
                    memory_free=int(gpu.memoryFree * 1024 * 1024),
                    temperature=gpu.temperature,
                    utilization=gpu.load * 100,
                    power_usage=0,
                    clock_core=gpu.clockCore,
                    clock_memory=gpu.clockMemory,
                    driver_version=""
                )
                gpus.append(gpu_info)
                logger.info(f"GPU detected via GPUtil: {gpu_info.name}")
        except Exception as e:
            logger.error(f"Error detecting GPUs via GPUtil: {e}")
            
        return gpus
        
    def detect_gpu_nvidia_smi(self) -> List[GPUInfo]:
        """Detect NVIDIA GPUs using nvidia-smi"""
        gpus = []
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu,utilization.gpu,power.draw,clocks.current.graphics,clocks.current.memory,driver_version', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 9:
                            name = parts[0]
                            memory_total = int(float(parts[1]) * 1024 * 1024) if parts[1] else 0
                            memory_used = int(float(parts[2]) * 1024 * 1024) if parts[2] else 0
                            memory_free = int(float(parts[3]) * 1024 * 1024) if parts[3] else 0
                            temperature = float(parts[4]) if parts[4] else 0
                            utilization = float(parts[5]) if parts[5] else 0
                            power_usage = float(parts[6]) * 1000 if parts[6] else 0  # Convert to mW
                            clock_core = int(float(parts[7])) if parts[7] else 0
                            clock_memory = int(float(parts[8])) if parts[8] else 0
                            driver_version = parts[9] if len(parts) > 9 else ""
                            
                            gpu_info = GPUInfo(
                                name=name,
                                type=GPUType.NVIDIA_CUDA,
                                vendor="NVIDIA",
                                memory_total=memory_total,
                                memory_used=memory_used,
                                memory_free=memory_free,
                                temperature=temperature,
                                utilization=utilization,
                                power_usage=power_usage,
                                clock_core=clock_core,
                                clock_memory=clock_memory,
                                driver_version=driver_version
                            )
                            gpus.append(gpu_info)
                            logger.info(f"GPU detected via nvidia-smi: {gpu_info.name}")
        except Exception as e:
            logger.error(f"Error detecting GPUs via nvidia-smi: {e}")
            
        return gpus
        
    def detect_cpu(self) -> CPUInfo:
        """Detect CPU information"""
        cpu_info = cpuinfo.get_cpu_info()
        
        # Get CPU usage
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
        except:
            cpu_usage = 0
            
        # Get CPU frequency
        try:
            freq = psutil.cpu_freq()
            if freq:
                current_freq = freq.current
                max_freq = freq.max
                min_freq = freq.min
            else:
                current_freq = cpu_info.get('hz_actual_friendly', 0)
                max_freq = cpu_info.get('hz_advertised_friendly', 0)
                min_freq = 0
        except:
            current_freq = 0
            max_freq = 0
            min_freq = 0
            
        # Get CPU temperature
        temp = 0
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                for name, entries in temps.items():
                    if entries:
                        temp = entries[0].current
                        break
        except:
            pass
            
        # Get CPU power (if available)
        power = 0
        try:
            if hasattr(psutil, "sensors_battery"):
                power = psutil.sensors_battery().power_plugged
        except:
            pass
            
        cpu = CPUInfo(
            name=cpu_info.get('brand_raw', 'Unknown CPU'),
            vendor=cpu_info.get('vendor_id_raw', 'Unknown'),
            architecture=cpu_info.get('arch', platform.machine()),
            cores_physical=psutil.cpu_count(logical=False),
            cores_logical=psutil.cpu_count(logical=True),
            threads=psutil.cpu_count(logical=True),
            base_frequency=min_freq,
            max_frequency=max_freq,
            current_frequency=current_freq,
            temperature=temp,
            utilization=cpu_usage,
            power_usage=power,
            cache_l1=cpu_info.get('l1_data_cache_size', 0),
            cache_l2=cpu_info.get('l2_cache_size', 0),
            cache_l3=cpu_info.get('l3_cache_size', 0),
            instructions_sets=cpu_info.get('flags', []),
            virtualization=cpu_info.get('virtualization', False),
            hypervisor=False,
            smt_enabled=psutil.cpu_count(logical=True) > psutil.cpu_count(logical=False),
            turbo_enabled=False,
            overclocked=False,
            stepping=cpu_info.get('stepping', 0),
            model=cpu_info.get('model', 0),
            family=cpu_info.get('family', 0),
            microcode=cpu_info.get('microcode', ''),
            cpuid=cpu_info.get('cpuid', '')
        )
        
        logger.info(f"CPU detected: {cpu.name} ({cpu.cores_physical} cores)")
        return cpu
        
    def detect_ram(self) -> RAMInfo:
        """Detect RAM information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        ram = RAMInfo(
            total=mem.total,
            available=mem.available,
            used=mem.used,
            free=mem.free,
            cached=mem.cached if hasattr(mem, 'cached') else 0,
            buffers=mem.buffers if hasattr(mem, 'buffers') else 0,
            shared=mem.shared if hasattr(mem, 'shared') else 0,
            swap_total=swap.total,
            swap_used=swap.used,
            swap_free=swap.free,
            utilization=mem.percent,
            swap_utilization=swap.percent
        )
        
        # Get RAM details on Windows
        if platform.system() == "Windows" and hasattr(self, 'wmi_conn'):
            try:
                for memory in self.wmi_conn.Win32_PhysicalMemory():
                    ram.speed = getattr(memory, 'Speed', None)
                    ram.type = getattr(memory, 'MemoryType', None)
                    ram.form_factor = getattr(memory, 'FormFactor', None)
                    ram.manufacturer = getattr(memory, 'Manufacturer', None)
                    ram.part_number = getattr(memory, 'PartNumber', None)
                    ram.serial_number = getattr(memory, 'SerialNumber', None)
                    ram.voltage = getattr(memory, 'ConfiguredVoltage', None) / 1000 if hasattr(memory, 'ConfiguredVoltage') else None
                    break
            except Exception as e:
                logger.error(f"Error getting RAM details: {e}")
                
        logger.info(f"RAM detected: {ram.total / (1024**3):.1f} GB")
        return ram
        
    def detect_disks(self) -> List[DiskInfo]:
        """Detect disk information"""
        disks = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info = DiskInfo(
                    device=partition.device,
                    mountpoint=partition.mountpoint,
                    filesystem=partition.fstype,
                    total=usage.total,
                    used=usage.used,
                    free=usage.free,
                    utilization=usage.percent,
                    read_speed=0,
                    write_speed=0,
                    read_iops=0,
                    write_iops=0,
                    read_latency=0,
                    write_latency=0
                )
                
                # Get disk I/O counters
                try:
                    io_counters = psutil.disk_io_counters(perdisk=True)
                    for disk_name, counters in io_counters.items():
                        if disk_name in partition.device or partition.device in disk_name:
                            disk_info.read_speed = counters.read_bytes
                            disk_info.write_speed = counters.write_bytes
                            disk_info.read_iops = counters.read_count
                            disk_info.write_iops = counters.write_count
                            break
                except:
                    pass
                    
                # Get disk model on Windows
                if platform.system() == "Windows" and hasattr(self, 'wmi_conn'):
                    try:
                        for disk in self.wmi_conn.Win32_DiskDrive():
                            if disk.DeviceID in partition.device:
                                disk_info.model = disk.Model
                                disk_info.serial = disk.SerialNumber
                                disk_info.firmware = disk.FirmwareRevision
                                disk_info.interface = disk.InterfaceType
                                disk_info.media_type = disk.MediaType
                                disk_info.form_factor = disk.Size
                                break
                    except Exception as e:
                        logger.error(f"Error getting disk details: {e}")
                        
                disks.append(disk_info)
                logger.info(f"Disk detected: {disk_info.device} ({disk_info.total / (1024**4):.1f} TB)")
                
            except Exception as e:
                logger.error(f"Error detecting disk {partition.device}: {e}")
                
        return disks
        
    def detect_networks(self) -> List[NetworkInfo]:
        """Detect network interfaces"""
        networks = []
        
        for interface_name, interface_addresses in psutil.net_if_addrs().items():
            try:
                stats = psutil.net_if_stats().get(interface_name)
                io_counters = psutil.net_io_counters(pernic=True).get(interface_name)
                
                ip_addresses = []
                mac_address = ""
                
                for addr in interface_addresses:
                    if addr.family == socket.AF_INET:
                        ip_addresses.append(addr.address)
                    elif addr.family == psutil.AF_LINK:
                        mac_address = addr.address
                        
                network_info = NetworkInfo(
                    interface=interface_name,
                    mac_address=mac_address,
                    ip_addresses=ip_addresses,
                    gateway="",
                    dns_servers=[],
                    dhcp_enabled=False,
                    speed=stats.speed if stats else 0,
                    mtu=stats.mtu if stats else 1500,
                    bytes_sent=io_counters.bytes_sent if io_counters else 0,
                    bytes_received=io_counters.bytes_recv if io_counters else 0,
                    packets_sent=io_counters.packets_sent if io_counters else 0,
                    packets_received=io_counters.packets_recv if io_counters else 0,
                    errors_in=io_counters.errin if io_counters else 0,
                    errors_out=io_counters.errout if io_counters else 0,
                    drops_in=io_counters.dropin if io_counters else 0,
                    drops_out=io_counters.dropout if io_counters else 0,
                    link_status=stats.isup if stats else False
                )
                
                networks.append(network_info)
                logger.info(f"Network interface detected: {network_info.interface}")
                
            except Exception as e:
                logger.error(f"Error detecting network {interface_name}: {e}")
                
        return networks
        
    def detect_battery(self) -> Optional[BatteryInfo]:
        """Detect battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_info = BatteryInfo(
                    present=True,
                    charging=battery.power_plugged,
                    percent=battery.percent,
                    time_remaining=battery.secsleft if battery.secsleft != -1 else None
                )
                logger.info(f"Battery detected: {battery_info.percent:.1f}%")
                return battery_info
        except:
            pass
            
        return None
        
    def detect_all(self):
        """Detect all hardware"""
        # Detect GPUs using all methods
        all_gpus = []
        
        # NVIDIA methods
        all_gpus.extend(self.detect_gpu_nvidia())
        all_gpus.extend(self.detect_gpu_gputil())
        all_gpus.extend(self.detect_gpu_nvidia_smi())
        
        # AMD methods
        all_gpus.extend(self.detect_gpu_amd())
        
        # Intel methods
        all_gpus.extend(self.detect_gpu_intel())
        
        # Apple methods
        all_gpus.extend(self.detect_gpu_apple())
        
        # Vulkan method (all vendors)
        all_gpus.extend(self.detect_gpu_vulkan())
        
        # DirectX method (all vendors on Windows)
        all_gpus.extend(self.detect_gpu_directx())
        
        # Remove duplicates (by name and vendor)
        seen = set()
        for gpu in all_gpus:
            key = (gpu.name, gpu.vendor)
            if key not in seen:
                seen.add(key)
                self.gpus.append(gpu)
                
        # Sort by vendor
        self.gpus.sort(key=lambda x: (x.vendor, x.name))
        
        # Detect other components
        self.cpu = self.detect_cpu()
        self.ram = self.detect_ram()
        self.disks = self.detect_disks()
        self.networks = self.detect_networks()
        self.battery = self.detect_battery()
        
        logger.info(f"Hardware detection complete: {len(self.gpus)} GPU(s), {len(self.disks)} disk(s), {len(self.networks)} network(s)")
        
    def start_monitoring(self, interval: int = 1000):
        """Start hardware monitoring"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.stop_event.clear()
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,), daemon=True)
        self.monitor_thread.start()
        logger.info(f"Hardware monitoring started (interval: {interval}ms)")
        
    def stop_monitoring(self):
        """Stop hardware monitoring"""
        self.monitoring = False
        self.stop_event.set()
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Hardware monitoring stopped")
        
    def _monitor_loop(self, interval: int):
        """Monitoring loop"""
        while not self.stop_event.is_set():
            try:
                snapshot = self.take_snapshot()
                with self.monitor_lock:
                    self.history.append(snapshot)
                    self.snapshots.append(snapshot)
                    
                time.sleep(interval / 1000.0)
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                
    def take_snapshot(self) -> HardwareSnapshot:
        """Take a hardware snapshot"""
        # CPU info
        cpu_usage = psutil.cpu_percent()
        cpu_temp = self.cpu.temperature if self.cpu else 0
        cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
        
        # RAM info
        mem = psutil.virtual_memory()
        ram_usage = mem.percent
        ram_available = mem.available
        
        # Swap info
        swap = psutil.swap_memory()
        swap_usage = swap.percent
        
        # GPU info
        gpu_usage = []
        gpu_temp = []
        gpu_memory = []
        gpu_power = []
        
        for gpu in self.gpus:
            gpu_usage.append(gpu.utilization)
            gpu_temp.append(gpu.temperature)
            gpu_memory.append(gpu.memory_used)
            gpu_power.append(gpu.power_usage)
            
        # Disk info
        disk_usage = {}
        disk_io = {}
        for disk in self.disks:
            disk_usage[disk.mountpoint] = disk.utilization
            disk_io[disk.mountpoint] = (disk.read_speed, disk.write_speed)
            
        # Network info
        net_io = psutil.net_io_counters()
        network_io = (net_io.bytes_sent, net_io.bytes_recv)
        
        # Battery info
        battery_percent = self.battery.percent if self.battery else None
        
        # Process info
        process_count = len(psutil.pids())
        thread_count = sum(p.num_threads() for p in psutil.process_iter())
        handle_count = 0
        
        # Uptime
        uptime = int(time.time() - psutil.boot_time())
        
        # Load average
        try:
            load_avg = psutil.getloadavg()
        except:
            load_avg = None
            
        snapshot = HardwareSnapshot(
            timestamp=datetime.now(),
            cpu_usage=cpu_usage,
            cpu_temp=cpu_temp,
            cpu_freq=cpu_freq,
            cpu_power=0,
            gpu_usage=gpu_usage,
            gpu_temp=gpu_temp,
            gpu_memory=gpu_memory,
            gpu_power=gpu_power,
            ram_usage=ram_usage,
            ram_available=ram_available,
            swap_usage=swap_usage,
            disk_usage=disk_usage,
            disk_io=disk_io,
            network_io=network_io,
            battery_percent=battery_percent,
            process_count=process_count,
            thread_count=thread_count,
            handle_count=handle_count,
            uptime=uptime,
            load_average=load_avg
        )
        
        return snapshot
        
    def get_gpu_summary(self) -> str:
        """Get GPU summary text"""
        if not self.gpus:
            return "No GPU detected"
            
        lines = []
        for i, gpu in enumerate(self.gpus, 1):
            lines.append(f"GPU {i}: {gpu.name}")
            lines.append(f"  Type: {gpu.type.name}")
            lines.append(f"  Memory: {gpu.memory_used / (1024**3):.1f}GB / {gpu.memory_total / (1024**3):.1f}GB")
            lines.append(f"  Temperature: {gpu.temperature:.0f}°C")
            lines.append(f"  Utilization: {gpu.utilization:.1f}%")
            lines.append(f"  Power: {gpu.power_usage / 1000:.1f}W")
            
        return "\n".join(lines)
        
    def get_cpu_summary(self) -> str:
        """Get CPU summary text"""
        if not self.cpu:
            return "CPU: Unknown"
            
        return f"CPU: {self.cpu.name}\n" \
               f"  Cores: {self.cpu.cores_physical} physical, {self.cpu.cores_logical} logical\n" \
               f"  Usage: {self.cpu.utilization:.1f}%\n" \
               f"  Temperature: {self.cpu.temperature:.0f}°C\n" \
               f"  Frequency: {self.cpu.current_frequency:.0f}MHz"
               
    def get_ram_summary(self) -> str:
        """Get RAM summary text"""
        if not self.ram:
            return "RAM: Unknown"
            
        return f"RAM: {self.ram.used / (1024**3):.1f}GB / {self.ram.total / (1024**3):.1f}GB ({self.ram.utilization:.1f}%)\n" \
               f"Swap: {self.ram.swap_used / (1024**3):.1f}GB / {self.ram.swap_total / (1024**3):.1f}GB ({self.ram.swap_utilization:.1f}%)"
               
    def get_hardware_info(self) -> dict:
        """Get complete hardware info dictionary"""
        return {
            'gpus': [asdict(gpu) for gpu in self.gpus],
            'cpu': asdict(self.cpu) if self.cpu else None,
            'ram': asdict(self.ram) if self.ram else None,
            'disks': [asdict(disk) for disk in self.disks],
            'networks': [asdict(net) for net in self.networks],
            'battery': asdict(self.battery) if self.battery else None,
            'timestamp': datetime.now().isoformat()
        }
        
    def save_history(self, filename: str):
        """Save monitoring history to file"""
        try:
            with open(filename, 'wb') as f:
                pickle.dump({
                    'history': self.history,
                    'snapshots': self.snapshots,
                    'gpus': self.gpus,
                    'cpu': self.cpu,
                    'ram': self.ram
                }, f)
            logger.info(f"Monitoring history saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save monitoring history: {e}")
            
    def load_history(self, filename: str):
        """Load monitoring history from file"""
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.history = data.get('history', deque(maxlen=3600))
                self.snapshots = data.get('snapshots', [])
                logger.info(f"Monitoring history loaded from {filename}")
        except Exception as e:
            logger.error(f"Failed to load monitoring history: {e}")

# Initialize hardware monitor
hardware_monitor = HardwareMonitor()

# ========================================
# PERFORMANCE GRAPH WIDGET
# ========================================
class PerformanceGraphWidget(QWidget):
    """Widget for displaying performance graphs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hardware_monitor = hardware_monitor
        self.graph_type = 'cpu'  # cpu, gpu, ram, network, disk
        self.time_range = 60  # seconds
        
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(['CPU', 'GPU', 'RAM', 'Network', 'Disk'])
        self.type_combo.currentTextChanged.connect(self.change_graph_type)
        controls_layout.addWidget(QLabel("Graph:"))
        controls_layout.addWidget(self.type_combo)
        
        self.range_combo = QComboBox()
        self.range_combo.addItems(['30s', '1m', '5m', '15m', '30m', '1h'])
        self.range_combo.setCurrentText('1m')
        self.range_combo.currentTextChanged.connect(self.change_time_range)
        controls_layout.addWidget(QLabel("Range:"))
        controls_layout.addWidget(self.range_combo)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_graph)
        controls_layout.addWidget(self.refresh_btn)
        
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self.export_graph)
        controls_layout.addWidget(self.export_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        
        # Setup plot
        self.setup_plot()
        
    def setup_plot(self):
        """Setup the matplotlib plot"""
        self.figure.clear()
        
        if self.graph_type == 'cpu':
            self.ax = self.figure.add_subplot(111)
            self.ax.set_title('CPU Usage')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Usage (%)')
            self.ax.set_ylim(0, 100)
            self.ax.grid(True, alpha=0.3)
            
            self.cpu_line, = self.ax.plot([], [], 'b-', label='CPU Usage', linewidth=2)
            self.temp_line, = self.ax.plot([], [], 'r-', label='Temperature', linewidth=1)
            self.ax.legend(loc='upper right')
            
        elif self.graph_type == 'gpu':
            self.ax = self.figure.add_subplot(111)
            self.ax.set_title('GPU Usage')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Usage (%)')
            self.ax.set_ylim(0, 100)
            self.ax.grid(True, alpha=0.3)
            
            self.gpu_lines = []
            colors = ['b', 'g', 'r', 'c', 'm', 'y']
            for i, gpu in enumerate(hardware_monitor.gpus):
                line, = self.ax.plot([], [], f'{colors[i % len(colors)]}-', 
                                   label=f'GPU {i+1}: {gpu.name[:20]}', linewidth=2)
                self.gpu_lines.append(line)
            self.ax.legend(loc='upper right')
            
        elif self.graph_type == 'ram':
            self.ax = self.figure.add_subplot(111)
            self.ax.set_title('RAM Usage')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Usage (%)')
            self.ax.set_ylim(0, 100)
            self.ax.grid(True, alpha=0.3)
            
            self.ram_line, = self.ax.plot([], [], 'g-', label='RAM', linewidth=2)
            self.swap_line, = self.ax.plot([], [], 'b-', label='Swap', linewidth=1)
            self.ax.legend(loc='upper right')
            
        elif self.graph_type == 'network':
            self.ax = self.figure.add_subplot(111)
            self.ax.set_title('Network I/O')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Speed (MB/s)')
            self.ax.grid(True, alpha=0.3)
            
            self.sent_line, = self.ax.plot([], [], 'g-', label='Upload', linewidth=2)
            self.recv_line, = self.ax.plot([], [], 'b-', label='Download', linewidth=2)
            self.ax.legend(loc='upper right')
            
        elif self.graph_type == 'disk':
            self.ax = self.figure.add_subplot(111)
            self.ax.set_title('Disk I/O')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Speed (MB/s)')
            self.ax.grid(True, alpha=0.3)
            
            self.read_line, = self.ax.plot([], [], 'g-', label='Read', linewidth=2)
            self.write_line, = self.ax.plot([], [], 'b-', label='Write', linewidth=2)
            self.ax.legend(loc='upper right')
            
        self.canvas.draw()
        
    def setup_animation(self):
        """Setup animation timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # Update every second
        
    def change_graph_type(self, text: str):
        """Change graph type"""
        self.graph_type = text.lower()
        self.setup_plot()
        
    def change_time_range(self, text: str):
        """Change time range"""
        # Convert text to seconds
        if text.endswith('s'):
            self.time_range = int(text[:-1])
        elif text.endswith('m'):
            self.time_range = int(text[:-1]) * 60
        elif text.endswith('h'):
            self.time_range = int(text[:-1]) * 3600
            
    def refresh_graph(self):
        """Refresh the graph"""
        self.update_graph()
        
    def update_graph(self):
        """Update the graph with new data"""
        if not self.hardware_monitor.history:
            return
            
        # Get data from history
        history = list(self.hardware_monitor.history)
        if not history:
            return
            
        # Limit to time range
        now = datetime.now()
        history = [h for h in history if (now - h.timestamp).total_seconds() <= self.time_range]
        
        if not history:
            return
            
        # Prepare time axis
        times = [(h.timestamp - history[0].timestamp).total_seconds() for h in history]
        
        if self.graph_type == 'cpu':
            cpu_data = [h.cpu_usage for h in history]
            temp_data = [h.cpu_temp for h in history]
            
            self.cpu_line.set_data(times, cpu_data)
            self.temp_line.set_data(times, temp_data)
            
            self.ax.relim()
            self.ax.autoscale_view()
            
        elif self.graph_type == 'gpu':
            for i, line in enumerate(self.gpu_lines):
                if i < len(history[-1].gpu_usage):
                    gpu_data = [h.gpu_usage[i] if i < len(h.gpu_usage) else 0 for h in history]
                    line.set_data(times, gpu_data)
                    
            self.ax.relim()
            self.ax.autoscale_view()
            
        elif self.graph_type == 'ram':
            ram_data = [h.ram_usage for h in history]
            swap_data = [h.swap_usage for h in history]
            
            self.ram_line.set_data(times, ram_data)
            self.swap_line.set_data(times, swap_data)
            
            self.ax.relim()
            self.ax.autoscale_view()
            
        elif self.graph_type == 'network':
            # Calculate speeds
            sent_speeds = []
            recv_speeds = []
            prev_sent, prev_recv = None, None
            
            for h in history:
                sent, recv = h.network_io
                if prev_sent is not None:
                    sent_speeds.append((sent - prev_sent) / (1024 * 1024))  # MB/s
                    recv_speeds.append((recv - prev_recv) / (1024 * 1024))
                else:
                    sent_speeds.append(0)
                    recv_speeds.append(0)
                prev_sent, prev_recv = sent, recv
                
            self.sent_line.set_data(times[1:], sent_speeds[1:])
            self.recv_line.set_data(times[1:], recv_speeds[1:])
            
            self.ax.relim()
            self.ax.autoscale_view()
            
        elif self.graph_type == 'disk':
            # Calculate speeds for first disk
            if history[0].disk_io:
                disk_name = list(history[0].disk_io.keys())[0]
                read_speeds = []
                write_speeds = []
                prev_read, prev_write = None, None
                
                for h in history:
                    if disk_name in h.disk_io:
                        read, write = h.disk_io[disk_name]
                        if prev_read is not None:
                            read_speeds.append((read - prev_read) / (1024 * 1024))
                            write_speeds.append((write - prev_write) / (1024 * 1024))
                        else:
                            read_speeds.append(0)
                            write_speeds.append(0)
                        prev_read, prev_write = read, write
                    else:
                        read_speeds.append(0)
                        write_speeds.append(0)
                        
                self.read_line.set_data(times[1:], read_speeds[1:])
                self.write_line.set_data(times[1:], write_speeds[1:])
                
                self.ax.relim()
                self.ax.autoscale_view()
                
        self.canvas.draw_idle()
        
    def export_graph(self):
        """Export the current graph"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Graph",
            os.path.join(EXPORTS_DIR, f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"),
            "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg)"
        )
        if filename:
            self.figure.savefig(filename, dpi=300, bbox_inches='tight')
            QMessageBox.information(self, "Export Complete", f"Graph exported to:\n{filename}")

# ========================================
# HARDWARE MONITOR WIDGET
# ========================================
class HardwareMonitorWidget(QWidget):
    """Widget for displaying hardware information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hardware_monitor = hardware_monitor
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # CPU Tab
        self.cpu_widget = QWidget()
        self.setup_cpu_tab()
        self.tabs.addTab(self.cpu_widget, "CPU")
        
        # GPU Tab
        self.gpu_widget = QWidget()
        self.setup_gpu_tab()
        self.tabs.addTab(self.gpu_widget, "GPU")
        
        # RAM Tab
        self.ram_widget = QWidget()
        self.setup_ram_tab()
        self.tabs.addTab(self.ram_widget, "RAM")
        
        # Disks Tab
        self.disks_widget = QWidget()
        self.setup_disks_tab()
        self.tabs.addTab(self.disks_widget, "Disks")
        
        # Network Tab
        self.network_widget = QWidget()
        self.setup_network_tab()
        self.tabs.addTab(self.network_widget, "Network")
        
        # Performance Tab
        self.performance_widget = PerformanceGraphWidget()
        self.tabs.addTab(self.performance_widget, "Performance")
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(2000)  # Update every 2 seconds
        
    def setup_cpu_tab(self):
        """Setup CPU tab"""
        layout = QVBoxLayout()
        self.cpu_widget.setLayout(layout)
        
        self.cpu_info = QTextEdit()
        self.cpu_info.setReadOnly(True)
        self.cpu_info.setFont(QFont("Consolas", 10))
        layout.addWidget(self.cpu_info)
        
    def setup_gpu_tab(self):
        """Setup GPU tab"""
        layout = QVBoxLayout()
        self.gpu_widget.setLayout(layout)
        
        self.gpu_info = QTextEdit()
        self.gpu_info.setReadOnly(True)
        self.gpu_info.setFont(QFont("Consolas", 10))
        layout.addWidget(self.gpu_info)
        
    def setup_ram_tab(self):
        """Setup RAM tab"""
        layout = QVBoxLayout()
        self.ram_widget.setLayout(layout)
        
        self.ram_info = QTextEdit()
        self.ram_info.setReadOnly(True)
        self.ram_info.setFont(QFont("Consolas", 10))
        layout.addWidget(self.ram_info)
        
    def setup_disks_tab(self):
        """Setup Disks tab"""
        layout = QVBoxLayout()
        self.disks_widget.setLayout(layout)
        
        self.disks_info = QTextEdit()
        self.disks_info.setReadOnly(True)
        self.disks_info.setFont(QFont("Consolas", 10))
        layout.addWidget(self.disks_info)
        
    def setup_network_tab(self):
        """Setup Network tab"""
        layout = QVBoxLayout()
        self.network_widget.setLayout(layout)
        
        self.network_info = QTextEdit()
        self.network_info.setReadOnly(True)
        self.network_info.setFont(QFont("Consolas", 10))
        layout.addWidget(self.network_info)
        
    def update_display(self):
        """Update all displays"""
        if hasattr(self, 'cpu_info'):
            self.cpu_info.setText(self.hardware_monitor.get_cpu_summary())
            
        if hasattr(self, 'gpu_info'):
            self.gpu_info.setText(self.hardware_monitor.get_gpu_summary())
            
        if hasattr(self, 'ram_info'):
            self.ram_info.setText(self.hardware_monitor.get_ram_summary())
            
        if hasattr(self, 'disks_info'):
            disks_text = ""
            for disk in self.hardware_monitor.disks:
                disks_text += f"Disk: {disk.device}\n"
                disks_text += f"  Mount: {disk.mountpoint}\n"
                disks_text += f"  Total: {disk.total / (1024**4):.1f} TB\n"
                disks_text += f"  Used: {disk.used / (1024**4):.1f} TB ({disk.utilization:.1f}%)\n"
                disks_text += f"  Free: {disk.free / (1024**4):.1f} TB\n"
                disks_text += f"  Filesystem: {disk.filesystem}\n"
                disks_text += f"  Model: {disk.model or 'Unknown'}\n\n"
            self.disks_info.setText(disks_text)
            
        if hasattr(self, 'network_info'):
            network_text = ""
            for net in self.hardware_monitor.networks:
                network_text += f"Interface: {net.interface}\n"
                network_text += f"  MAC: {net.mac_address}\n"
                network_text += f"  IP: {', '.join(net.ip_addresses)}\n"
                network_text += f"  Speed: {net.speed} Mbps\n"
                network_text += f"  Sent: {net.bytes_sent / (1024**3):.1f} GB\n"
                network_text += f"  Received: {net.bytes_received / (1024**3):.1f} GB\n"
                network_text += f"  Status: {'Up' if net.link_status else 'Down'}\n\n"
            self.network_info.setText(network_text)

# ========================================
# MULTI-MONITOR SUPPORT
# ========================================
class MonitorManager:
    """Manage multiple monitors"""
    
    def __init__(self):
        self.monitors = []
        self.detect_monitors()
        
    def detect_monitors(self):
        """Detect all available monitors"""
        app = QApplication.instance()
        screens = app.screens()
        
        for i, screen in enumerate(screens):
            geometry = screen.geometry()
            available_geometry = screen.availableGeometry()
            size = screen.size()
            physical_size = screen.physicalSize()
            logical_dpi = screen.logicalDotsPerInch()
            physical_dpi = screen.physicalDotsPerInch()
            device_pixel_ratio = screen.devicePixelRatio()
            refresh_rate = screen.refreshRate()
            color_depth = screen.depth()
            
            monitor_info = {
                'index': i,
                'name': screen.name(),
                'geometry': {
                    'x': geometry.x(),
                    'y': geometry.y(),
                    'width': geometry.width(),
                    'height': geometry.height()
                },
                'available_geometry': {
                    'x': available_geometry.x(),
                    'y': available_geometry.y(),
                    'width': available_geometry.width(),
                    'height': available_geometry.height()
                },
                'size': {
                    'width': size.width(),
                    'height': size.height()
                },
                'physical_size': {
                    'width': physical_size.width(),
                    'height': physical_size.height()
                },
                'logical_dpi': logical_dpi,
                'physical_dpi': physical_dpi,
                'device_pixel_ratio': device_pixel_ratio,
                'refresh_rate': refresh_rate,
                'color_depth': color_depth,
                'primary': (i == 0)
            }
            self.monitors.append(monitor_info)
            
        logger.info(f"Detected {len(self.monitors)} monitors")
        
    def get_monitor_count(self) -> int:
        """Get number of monitors"""
        return len(self.monitors)
        
    def get_monitor(self, index: int) -> Optional[dict]:
        """Get monitor info by index"""
        if 0 <= index < len(self.monitors):
            return self.monitors[index]
        return None
        
    def get_primary_monitor(self) -> Optional[dict]:
        """Get primary monitor"""
        for monitor in self.monitors:
            if monitor['primary']:
                return monitor
        return self.monitors[0] if self.monitors else None
        
    def move_window_to_monitor(self, window: QMainWindow, monitor_index: int):
        """Move window to specified monitor"""
        monitor = self.get_monitor(monitor_index)
        if monitor:
            geometry = monitor['geometry']
            window.move(geometry['x'], geometry['y'])
            window.resize(geometry['width'], geometry['height'])
            logger.info(f"Moved window to monitor {monitor_index}")
            
    def create_monitor_window(self, parent: QMainWindow, monitor_index: int) -> Optional[QMainWindow]:
        """Create a new window on specified monitor"""
        monitor = self.get_monitor(monitor_index)
        if not monitor:
            return None
            
        window = QMainWindow(parent)
        window.setWindowTitle(f"{APP_NAME} - Monitor {monitor_index + 1}")
        window.setGeometry(
            monitor['geometry']['x'],
            monitor['geometry']['y'],
            monitor['geometry']['width'] // 2,
            monitor['geometry']['height'] // 2
        )
        
        # Apply same theme as parent
        if hasattr(parent, 'settings'):
            window.setStyleSheet(parent.styleSheet())
            
        return window

# ========================================
# TRANSLATIONS
# ========================================
TRANSLATIONS = {
    'en': {
        # Window Title
        'window_title': 'NotyCaption Pro - Professional AI Caption Generator',
        
        # App Name
        'app_name': 'NotyCaption Pro',
        'app_subtitle': 'AI-Powered Caption Generator',
        
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
        'download_model': '📥 Download Model',
        'login_google': '🔐 Google Login',
        'import_media': '📁 Import Media',
        'browse_output': '📂 Browse Output',
        'enhance_audio': '🎤 Enhance Audio',
        'play_pause': '▶️ Play / ⏸️ Pause',
        'playing': '⏸️ Playing...',
        'paused': '▶️ Play / ⏸️ Pause',
        'generate': '🚀 Generate Captions',
        'cancel': 'Cancel Operation',
        'force_cancel': '⚠️ Force Cancel',
        'reopen_notebook': '🔗 Reopen Notebook',
        'copy_url': '📋 Copy URL',
        'workspace': '🎨 Workspace',
        'save_layout': '💾 Save Layout',
        'load_layout': '📂 Load Layout',
        'presets': '🎨 Presets',
        'hardware': '🖥️ Hardware',
        'monitor': '📊 Monitor',
        'performance': '📈 Performance',
        'export': '📤 Export',
        'import': '📥 Import',
        'preview': '👁️ Preview',
        'refresh': '🔄 Refresh',
        
        # Labels
        'ai_caption_editor': 'AI Caption Editor',
        'processing_mode': 'Mode:',
        'language': 'Language:',
        'words_per_line': 'Words/Line:',
        'output_format': 'Format:',
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
        'colab_link': 'Colab Link:',
        'click_to_open': 'Click to open in browser',
        
        # Modes
        'normal_mode': '🖥️ Local',
        'online_mode': '☁️ Online',
        
        # Languages for transcription
        'english_transcribe': '🇺🇸 English',
        'japanese_translate': '🇯🇵 Japanese → English',
        'chinese_transcribe': '🇨🇳 Chinese',
        'french_transcribe': '🇫🇷 French',
        'german_transcribe': '🇩🇪 German',
        'spanish_transcribe': '🇪🇸 Spanish',
        'russian_transcribe': '🇷🇺 Russian',
        'arabic_transcribe': '🇸🇦 Arabic',
        'hindi_transcribe': '🇮🇳 Hindi',
        'bengali_transcribe': '🇧🇩 Bengali',
        'urdu_transcribe': '🇵🇰 Urdu',
        'portuguese_transcribe': '🇵🇹 Portuguese',
        'italian_transcribe': '🇮🇹 Italian',
        'dutch_transcribe': '🇳🇱 Dutch',
        'polish_transcribe': '🇵🇱 Polish',
        'turkish_transcribe': '🇹🇷 Turkish',
        'vietnamese_transcribe': '🇻🇳 Vietnamese',
        'thai_transcribe': '🇹🇭 Thai',
        'korean_transcribe': '🇰🇷 Korean',
        
        # Formats
        'srt_format': '📄 SRT',
        'ass_format': '🎨 ASS',
        
        # Messages
        'import_complete': 'Import Complete',
        'import_success': 'Media imported successfully.',
        'enhancement_complete': 'Enhancement Complete',
        'enhancement_success': 'Vocals extracted:',
        'generation_complete': 'Generation Complete',
        'generation_success': 'Captions saved:',
        'download_complete': 'Download Complete',
        'download_success': 'Model downloaded!',
        'download_failed': 'Download Failed',
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
        'conversion_warning': 'Conversion Warning',
        'conversion_warning_msg': 'Using original file.',
        'playback_error': 'Playback Error',
        'colab_timeout': 'Colab Timeout',
        'colab_timeout_msg': 'No result file found.',
        'network_error': 'Network Error',
        'model_load_error': 'Model Load Error',
        
        # Settings Dialog
        'settings_title': 'Settings - Professional',
        'general_tab': 'General',
        'paths_tab': 'Paths',
        'features_tab': 'Features',
        'advanced_tab': 'Advanced',
        'workspace_tab': 'Workspace',
        'presets_tab': 'Presets',
        'hardware_tab': 'Hardware',
        'visual_theme': 'Theme',
        'system_default': 'System',
        'light_mode': 'Light',
        'dark_mode': 'Dark',
        'ui_scaling': 'UI Scale',
        'scale_factor': 'Scale:',
        'temp_dir': 'Temp Directory',
        'temp_dir_placeholder': 'System Temp',
        'browse_folder': 'Browse',
        'models_dir': 'Models Directory',
        'models_dir_placeholder': 'App Data',
        'auto_features': 'Auto Features',
        'auto_enhance': 'Auto-Enhance',
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
        'ui_options': 'UI Options',
        'minimize_tray': 'Minimize to tray',
        'show_tooltips': 'Show tooltips',
        'ui_language': 'Language:',
        'apply_restart': 'Apply & Restart',
        
        # Hardware Detection
        'hardware_acceleration': 'Hardware',
        'cuda_available': 'CUDA',
        'cuda_not_available': 'No CUDA',
        'gpu_info': 'GPU: {}',
        'cpu_info': 'CPU: {}',
        'memory_info': 'RAM: {:.1f} GB',
        'using_gpu': 'GPU Mode',
        'using_cpu': 'CPU Mode',
        'gpu_temp': 'GPU Temp: {}°C',
        'gpu_usage': 'GPU Usage: {}%',
        'cpu_usage': 'CPU Usage: {}%',
        'gpu_memory': 'GPU Memory: {:.1f}/{:.1f} GB',
        'ram_usage': 'RAM Usage: {:.1f}/{:.1f} GB ({:.0f}%)',
        'disk_usage': 'Disk Usage: {:.1f}/{:.1f} GB ({:.0f}%)',
        
        # Hardware Monitor
        'hardware_monitor': 'Hardware Monitor',
        'cpu_tab': 'CPU',
        'gpu_tab': 'GPU',
        'ram_tab': 'RAM',
        'disk_tab': 'Disk',
        'network_tab': 'Network',
        'performance_tab': 'Performance',
        'start_monitoring': 'Start Monitoring',
        'stop_monitoring': 'Stop Monitoring',
        'export_data': 'Export Data',
        'import_data': 'Import Data',
        'clear_history': 'Clear History',
        'refresh_rate': 'Refresh Rate:',
        
        # Multi-monitor
        'monitor_manager': 'Monitor Manager',
        'detect_monitors': 'Detect Monitors',
        'move_to_monitor': 'Move to Monitor',
        'create_window': 'Create Window',
        'close_window': 'Close Window',
        'monitor': 'Monitor {}',
        'primary': 'Primary',
        'resolution': 'Resolution: {}x{}',
        'refresh_rate': 'Refresh Rate: {} Hz',
        
        # Workspace customization
        'workspace_customize': 'Customize Workspace',
        'accent_color': 'Accent Color',
        'glow_intensity': 'Glow Intensity',
        'animation_speed': 'Animation Speed',
        'card_opacity': 'Card Opacity',
        'font_family': 'Font Family',
        'font_size': 'Font Size',
        'reset_defaults': 'Reset to Defaults',
        'preview': 'Preview',
        'save_layout': 'Save Layout',
        'load_layout': 'Load Layout',
        'layout_name': 'Layout Name:',
        'select_layout': 'Select Layout:',
        'preset_name': 'Preset Name:',
        'apply_preset': 'Apply Preset',
        'save_preset': 'Save Preset',
        'delete_preset': 'Delete Preset',
        
        # Animation control
        'animation_control': 'Animation Control',
        'enable_animations': 'Enable Animations',
        'animation_speed_slow': 'Slow',
        'animation_speed_normal': 'Normal',
        'animation_speed_fast': 'Fast',
    },
    
    'ja': {
        # Window Title
        'window_title': 'NotyCaption Pro - プロフェッショナルAI字幕生成',
        
        # App Name
        'app_name': 'NotyCaption Pro',
        'app_subtitle': 'AI搭載字幕生成',
        
        # Menu and Status
        'ready': '準備完了',
        'processing': '処理中...',
        'canceled': 'キャンセル',
        'completed': '完了',
        'failed': '失敗',
        
        # Buttons
        'edit_captions': '✏️ 字幕編集',
        'save_exit_edit': '💾 保存して終了',
        'settings': '⚙️ 設定',
        'download_model': '📥 モデルダウンロード',
        'login_google': '🔐 Googleログイン',
        'import_media': '📁 メディアインポート',
        'browse_output': '📂 出力先選択',
        'enhance_audio': '🎤 音声強調',
        'play_pause': '▶️ 再生 / ⏸️ 一時停止',
        'playing': '⏸️ 再生中...',
        'paused': '▶️ 再生 / ⏸️ 一時停止',
        'generate': '🚀 字幕生成',
        'cancel': 'キャンセル',
        'force_cancel': '⚠️ 強制キャンセル',
        'reopen_notebook': '🔗 ノートブックを開く',
        'copy_url': '📋 URLをコピー',
        'workspace': '🎨 ワークスペース',
        'save_layout': '💾 レイアウト保存',
        'load_layout': '📂 レイアウト読み込み',
        'presets': '🎨 プリセット',
        'hardware': '🖥️ ハードウェア',
        'monitor': '📊 モニター',
        'performance': '📈 パフォーマンス',
        'export': '📤 エクスポート',
        'import': '📥 インポート',
        'preview': '👁️ プレビュー',
        'refresh': '🔄 更新',
        
        # Labels
        'ai_caption_editor': 'AI字幕エディター',
        'processing_mode': 'モード：',
        'language': '言語：',
        'words_per_line': '1行あたりの単語数：',
        'output_format': 'フォーマット：',
        'output_folder': '出力フォルダ：',
        'status': 'ステータス：',
        'notebook_url': 'ノートブックURL：',
        'not_available': '利用不可',
        'idle': '待機中',
        'speed': '速度：',
        'eta': '残り時間：',
        'downloading': 'ダウンロード中...',
        'uploading': 'アップロード中...',
        'waiting': '待機中...',
        'colab_link': 'Colabリンク：',
        'click_to_open': 'クリックして開く',
        
        # Modes
        'normal_mode': '🖥️ ローカル',
        'online_mode': '☁️ オンライン',
        
        # Languages for transcription
        'english_transcribe': '🇺🇸 英語',
        'japanese_translate': '🇯🇵 日本語 → 英語',
        'chinese_transcribe': '🇨🇳 中国語',
        'french_transcribe': '🇫🇷 フランス語',
        'german_transcribe': '🇩🇪 ドイツ語',
        'spanish_transcribe': '🇪🇸 スペイン語',
        'russian_transcribe': '🇷🇺 ロシア語',
        'arabic_transcribe': '🇸🇦 アラビア語',
        'hindi_transcribe': '🇮🇳 ヒンディー語',
        'bengali_transcribe': '🇧🇩 ベンガル語',
        'urdu_transcribe': '🇵🇰 ウルドゥー語',
        'portuguese_transcribe': '🇵🇹 ポルトガル語',
        'italian_transcribe': '🇮🇹 イタリア語',
        'dutch_transcribe': '🇳🇱 オランダ語',
        'polish_transcribe': '🇵🇱 ポーランド語',
        'turkish_transcribe': '🇹🇷 トルコ語',
        'vietnamese_transcribe': '🇻🇳 ベトナム語',
        'thai_transcribe': '🇹🇭 タイ語',
        'korean_transcribe': '🇰🇷 韓国語',
        
        # Formats
        'srt_format': '📄 SRT',
        'ass_format': '🎨 ASS',
        
        # Messages
        'import_complete': 'インポート完了',
        'import_success': 'メディアのインポートに成功しました。',
        'enhancement_complete': '音声強調完了',
        'enhancement_success': 'ボーカル抽出：',
        'generation_complete': '字幕生成完了',
        'generation_success': '字幕を保存しました：',
        'download_complete': 'ダウンロード完了',
        'download_success': 'モデルのダウンロードが完了しました！',
        'download_failed': 'ダウンロード失敗',
        'cancel_confirm': 'キャンセル確認',
        'cancel_confirm_msg': '現在の操作をキャンセルしますか？',
        'force_cancel_confirm': '⚠️ 強制キャンセルしますか？不安定になる可能性があります。',
        'no_audio': '音声なし',
        'no_audio_msg': '音声ファイルが読み込まれていません。',
        'no_media': 'メディアなし',
        'no_media_msg': 'まずメディアをインポートしてください。',
        'overwrite': 'ファイルを上書きしますか？',
        'overwrite_msg': 'ファイルが存在します：\n{}\n上書きしますか？',
        'login_required': 'まずGoogleでログインしてください。',
        'conversion_warning': '変換警告',
        'conversion_warning_msg': '元のファイルを使用します。',
        'playback_error': '再生エラー',
        'colab_timeout': 'Colabタイムアウト',
        'colab_timeout_msg': '結果ファイルが見つかりません。',
        'network_error': 'ネットワークエラー',
        'model_load_error': 'モデル読み込みエラー',
        
        # Settings Dialog
        'settings_title': '設定 - プロフェッショナル',
        'general_tab': '一般',
        'paths_tab': 'パス',
        'features_tab': '機能',
        'advanced_tab': '詳細',
        'workspace_tab': 'ワークスペース',
        'presets_tab': 'プリセット',
        'hardware_tab': 'ハードウェア',
        'visual_theme': 'テーマ',
        'system_default': 'システム',
        'light_mode': 'ライト',
        'dark_mode': 'ダーク',
        'ui_scaling': 'UIスケーリング',
        'scale_factor': 'スケール：',
        'temp_dir': 'テンポラリディレクトリ',
        'temp_dir_placeholder': 'システムテンポラリ',
        'browse_folder': '参照',
        'models_dir': 'モデルディレクトリ',
        'models_dir_placeholder': 'アプリデータ',
        'auto_features': '自動機能',
        'auto_enhance': '自動音声強調',
        'default_language': 'デフォルト言語：',
        'default_wpl': 'デフォルトの1行あたりの単語数',
        'words': '単語数：',
        'default_format': 'デフォルトフォーマット',
        'format': 'フォーマット：',
        'cancel_options': 'キャンセルオプション',
        'confirm_cancel': 'キャンセル前に確認',
        'force_cancel_timeout': '強制キャンセルまでの時間：',
        'seconds': '秒',
        'max_retry': '最大再試行回数：',
        'ui_options': 'UIオプション',
        'minimize_tray': 'トレイに最小化',
        'show_tooltips': 'ツールチップを表示',
        'ui_language': '言語：',
        'apply_restart': '適用して再起動',
        
        # Hardware Detection
        'hardware_acceleration': 'ハードウェア',
        'cuda_available': 'CUDA利用可能',
        'cuda_not_available': 'CUDA利用不可',
        'gpu_info': 'GPU：{}',
        'cpu_info': 'CPU：{}',
        'memory_info': 'RAM：{:.1f} GB',
        'using_gpu': 'GPUモード',
        'using_cpu': 'CPUモード',
        'gpu_temp': 'GPU温度：{}°C',
        'gpu_usage': 'GPU使用率：{}%',
        'cpu_usage': 'CPU使用率：{}%',
        'gpu_memory': 'GPUメモリ：{:.1f}/{:.1f} GB',
        'ram_usage': 'RAM使用率：{:.1f}/{:.1f} GB ({:.0f}%)',
        'disk_usage': 'ディスク使用率：{:.1f}/{:.1f} GB ({:.0f}%)',
        
        # Hardware Monitor
        'hardware_monitor': 'ハードウェアモニター',
        'cpu_tab': 'CPU',
        'gpu_tab': 'GPU',
        'ram_tab': 'RAM',
        'disk_tab': 'ディスク',
        'network_tab': 'ネットワーク',
        'performance_tab': 'パフォーマンス',
        'start_monitoring': 'モニタリング開始',
        'stop_monitoring': 'モニタリング停止',
        'export_data': 'データエクスポート',
        'import_data': 'データインポート',
        'clear_history': '履歴クリア',
        'refresh_rate': '更新間隔：',
        
        # Multi-monitor
        'monitor_manager': 'モニター管理',
        'detect_monitors': 'モニター検出',
        'move_to_monitor': 'モニターに移動',
        'create_window': 'ウィンドウ作成',
        'close_window': 'ウィンドウを閉じる',
        'monitor': 'モニター {}',
        'primary': 'プライマリ',
        'resolution': '解像度：{}x{}',
        'refresh_rate': 'リフレッシュレート：{} Hz',
        
        # Workspace customization
        'workspace_customize': 'ワークスペースカスタマイズ',
        'accent_color': 'アクセントカラー',
        'glow_intensity': 'グロー強度',
        'animation_speed': 'アニメーション速度',
        'card_opacity': 'カード不透明度',
        'font_family': 'フォントファミリー',
        'font_size': 'フォントサイズ',
        'reset_defaults': 'デフォルトにリセット',
        'preview': 'プレビュー',
        'save_layout': 'レイアウト保存',
        'load_layout': 'レイアウト読み込み',
        'layout_name': 'レイアウト名：',
        'select_layout': 'レイアウト選択：',
        'preset_name': 'プリセット名：',
        'apply_preset': 'プリセット適用',
        'save_preset': 'プリセット保存',
        'delete_preset': 'プリセット削除',
        
        # Animation control
        'animation_control': 'アニメーション制御',
        'enable_animations': 'アニメーション有効',
        'animation_speed_slow': '遅い',
        'animation_speed_normal': '普通',
        'animation_speed_fast': '速い',
    },
    
    'ru': {
        # Window Title
        'window_title': 'NotyCaption Pro - Профессиональный генератор субтитров с ИИ',
        
        # App Name
        'app_name': 'NotyCaption Pro',
        'app_subtitle': 'Генератор субтитров с ИИ',
        
        # Menu and Status
        'ready': 'Готово',
        'processing': 'Обработка...',
        'canceled': 'Отменено',
        'completed': 'Завершено',
        'failed': 'Ошибка',
        
        # Buttons
        'edit_captions': '✏️ Редактировать',
        'save_exit_edit': '💾 Сохранить и выйти',
        'settings': '⚙️ Настройки',
        'download_model': '📥 Скачать модель',
        'login_google': '🔐 Войти через Google',
        'import_media': '📁 Импорт медиа',
        'browse_output': '📂 Выбрать папку',
        'enhance_audio': '🎤 Улучшить аудио',
        'play_pause': '▶️ Воспроизвести / ⏸️ Пауза',
        'playing': '⏸️ Воспроизведение...',
        'paused': '▶️ Воспроизвести / ⏸️ Пауза',
        'generate': '🚀 Создать субтитры',
        'cancel': 'Отменить',
        'force_cancel': '⚠️ Принудительно',
        'reopen_notebook': '🔗 Открыть блокнот',
        'copy_url': '📋 Копировать URL',
        'workspace': '🎨 Рабочее пространство',
        'save_layout': '💾 Сохранить макет',
        'load_layout': '📂 Загрузить макет',
        'presets': '🎨 Пресеты',
        'hardware': '🖥️ Оборудование',
        'monitor': '📊 Монитор',
        'performance': '📈 Производительность',
        'export': '📤 Экспорт',
        'import': '📥 Импорт',
        'preview': '👁️ Предпросмотр',
        'refresh': '🔄 Обновить',
        
        # Labels
        'ai_caption_editor': 'Редактор субтитров с ИИ',
        'processing_mode': 'Режим:',
        'language': 'Язык:',
        'words_per_line': 'Слов в строке:',
        'output_format': 'Формат:',
        'output_folder': 'Папка вывода:',
        'status': 'Статус:',
        'notebook_url': 'URL блокнота:',
        'not_available': 'Недоступно',
        'idle': 'Ожидание',
        'speed': 'Скорость:',
        'eta': 'Осталось:',
        'downloading': 'Загрузка...',
        'uploading': 'Выгрузка...',
        'waiting': 'Ожидание...',
        'colab_link': 'Ссылка Colab:',
        'click_to_open': 'Нажмите для открытия',
        
        # Modes
        'normal_mode': '🖥️ Локальный',
        'online_mode': '☁️ Онлайн',
        
        # Languages for transcription
        'english_transcribe': '🇺🇸 Английский',
        'japanese_translate': '🇯🇵 Японский → Английский',
        'chinese_transcribe': '🇨🇳 Китайский',
        'french_transcribe': '🇫🇷 Французский',
        'german_transcribe': '🇩🇪 Немецкий',
        'spanish_transcribe': '🇪🇸 Испанский',
        'russian_transcribe': '🇷🇺 Русский',
        'arabic_transcribe': '🇸🇦 Арабский',
        'hindi_transcribe': '🇮🇳 Хинди',
        'bengali_transcribe': '🇧🇩 Бенгальский',
        'urdu_transcribe': '🇵🇰 Урду',
        'portuguese_transcribe': '🇵🇹 Португальский',
        'italian_transcribe': '🇮🇹 Итальянский',
        'dutch_transcribe': '🇳🇱 Нидерландский',
        'polish_transcribe': '🇵🇱 Польский',
        'turkish_transcribe': '🇹🇷 Турецкий',
        'vietnamese_transcribe': '🇻🇳 Вьетнамский',
        'thai_transcribe': '🇹🇭 Тайский',
        'korean_transcribe': '🇰🇷 Корейский',
        
        # Formats
        'srt_format': '📄 SRT',
        'ass_format': '🎨 ASS',
        
        # Messages
        'import_complete': 'Импорт завершен',
        'import_success': 'Медиа успешно импортировано.',
        'enhancement_complete': 'Улучшение завершено',
        'enhancement_success': 'Извлечены вокалы:',
        'generation_complete': 'Генерация завершена',
        'generation_success': 'Субтитры сохранены:',
        'download_complete': 'Загрузка завершена',
        'download_success': 'Модель загружена!',
        'download_failed': 'Ошибка загрузки',
        'cancel_confirm': 'Подтверждение отмены',
        'cancel_confirm_msg': 'Отменить текущую операцию?',
        'force_cancel_confirm': '⚠️ Принудительная отмена? Это может вызвать нестабильность.',
        'no_audio': 'Нет аудио',
        'no_audio_msg': 'Аудиофайл не загружен.',
        'no_media': 'Нет медиа',
        'no_media_msg': 'Сначала импортируйте медиа.',
        'overwrite': 'Перезаписать файл?',
        'overwrite_msg': 'Файл существует:\n{}\nПерезаписать?',
        'login_required': 'Сначала войдите через Google.',
        'conversion_warning': 'Предупреждение о конвертации',
        'conversion_warning_msg': 'Используется исходный файл.',
        'playback_error': 'Ошибка воспроизведения',
        'colab_timeout': 'Таймаут Colab',
        'colab_timeout_msg': 'Файл результата не найден.',
        'network_error': 'Ошибка сети',
        'model_load_error': 'Ошибка загрузки модели',
        
        # Settings Dialog
        'settings_title': 'Настройки - Профессиональные',
        'general_tab': 'Основные',
        'paths_tab': 'Пути',
        'features_tab': 'Функции',
        'advanced_tab': 'Дополнительно',
        'workspace_tab': 'Рабочее пространство',
        'presets_tab': 'Пресеты',
        'hardware_tab': 'Оборудование',
        'visual_theme': 'Тема',
        'system_default': 'Системная',
        'light_mode': 'Светлая',
        'dark_mode': 'Темная',
        'ui_scaling': 'Масштаб интерфейса',
        'scale_factor': 'Масштаб:',
        'temp_dir': 'Временная папка',
        'temp_dir_placeholder': 'Системная временная',
        'browse_folder': 'Обзор',
        'models_dir': 'Папка моделей',
        'models_dir_placeholder': 'Данные приложения',
        'auto_features': 'Автоматические функции',
        'auto_enhance': 'Автоулучшение',
        'default_language': 'Язык по умолчанию:',
        'default_wpl': 'Слов в строке по умолчанию',
        'words': 'Слов:',
        'default_format': 'Формат по умолчанию',
        'format': 'Формат:',
        'cancel_options': 'Параметры отмены',
        'confirm_cancel': 'Подтверждать отмену',
        'force_cancel_timeout': 'Принудительная отмена через:',
        'seconds': 'с',
        'max_retry': 'Максимум попыток:',
        'ui_options': 'Параметры интерфейса',
        'minimize_tray': 'Сворачивать в трей',
        'show_tooltips': 'Показывать подсказки',
        'ui_language': 'Язык интерфейса:',
        'apply_restart': 'Применить и перезапустить',
        
        # Hardware Detection
        'hardware_acceleration': 'Аппаратное ускорение',
        'cuda_available': 'CUDA доступно',
        'cuda_not_available': 'CUDA недоступно',
        'gpu_info': 'GPU: {}',
        'cpu_info': 'CPU: {}',
        'memory_info': 'RAM: {:.1f} ГБ',
        'using_gpu': 'Режим GPU',
        'using_cpu': 'Режим CPU',
        'gpu_temp': 'Температура GPU: {}°C',
        'gpu_usage': 'Использование GPU: {}%',
        'cpu_usage': 'Использование CPU: {}%',
        'gpu_memory': 'Память GPU: {:.1f}/{:.1f} ГБ',
        'ram_usage': 'Использование RAM: {:.1f}/{:.1f} ГБ ({:.0f}%)',
        'disk_usage': 'Использование диска: {:.1f}/{:.1f} ГБ ({:.0f}%)',
        
        # Hardware Monitor
        'hardware_monitor': 'Монитор оборудования',
        'cpu_tab': 'ЦП',
        'gpu_tab': 'ГП',
        'ram_tab': 'ОЗУ',
        'disk_tab': 'Диск',
        'network_tab': 'Сеть',
        'performance_tab': 'Производительность',
        'start_monitoring': 'Начать мониторинг',
        'stop_monitoring': 'Остановить мониторинг',
        'export_data': 'Экспорт данных',
        'import_data': 'Импорт данных',
        'clear_history': 'Очистить историю',
        'refresh_rate': 'Частота обновления:',
        
        # Multi-monitor
        'monitor_manager': 'Управление мониторами',
        'detect_monitors': 'Обнаружить мониторы',
        'move_to_monitor': 'Переместить на монитор',
        'create_window': 'Создать окно',
        'close_window': 'Закрыть окно',
        'monitor': 'Монитор {}',
        'primary': 'Основной',
        'resolution': 'Разрешение: {}x{}',
        'refresh_rate': 'Частота: {} Гц',
        
        # Workspace customization
        'workspace_customize': 'Настройка рабочего пространства',
        'accent_color': 'Акцентный цвет',
        'glow_intensity': 'Интенсивность свечения',
        'animation_speed': 'Скорость анимации',
        'card_opacity': 'Прозрачность карточек',
        'font_family': 'Шрифт',
        'font_size': 'Размер шрифта',
        'reset_defaults': 'Сбросить',
        'preview': 'Предпросмотр',
        'save_layout': 'Сохранить макет',
        'load_layout': 'Загрузить макет',
        'layout_name': 'Имя макета:',
        'select_layout': 'Выберите макет:',
        'preset_name': 'Имя пресета:',
        'apply_preset': 'Применить пресет',
        'save_preset': 'Сохранить пресет',
        'delete_preset': 'Удалить пресет',
        
        # Animation control
        'animation_control': 'Управление анимацией',
        'enable_animations': 'Включить анимацию',
        'animation_speed_slow': 'Медленно',
        'animation_speed_normal': 'Нормально',
        'animation_speed_fast': 'Быстро',
    },
    
    'de': {
        # Window Title
        'window_title': 'NotyCaption Pro - Professioneller KI-Untertitelgenerator',
        
        # App Name
        'app_name': 'NotyCaption Pro',
        'app_subtitle': 'KI-gestützter Untertitelgenerator',
        
        # Menu and Status
        'ready': 'Bereit',
        'processing': 'Verarbeitung...',
        'canceled': 'Abgebrochen',
        'completed': 'Abgeschlossen',
        'failed': 'Fehlgeschlagen',
        
        # Buttons
        'edit_captions': '✏️ Untertitel bearbeiten',
        'save_exit_edit': '💾 Speichern & Beenden',
        'settings': '⚙️ Einstellungen',
        'download_model': '📥 Modell herunterladen',
        'login_google': '🔐 Google-Anmeldung',
        'import_media': '📁 Medien importieren',
        'browse_output': '📂 Ausgabeordner',
        'enhance_audio': '🎤 Audio verbessern',
        'play_pause': '▶️ Abspielen / ⏸️ Pause',
        'playing': '⏸️ Wiedergabe...',
        'paused': '▶️ Abspielen / ⏸️ Pause',
        'generate': '🚀 Untertitel generieren',
        'cancel': 'Abbrechen',
        'force_cancel': '⚠️ Erzwingen',
        'reopen_notebook': '🔗 Notizbuch öffnen',
        'copy_url': '📋 URL kopieren',
        'workspace': '🎨 Arbeitsbereich',
        'save_layout': '💾 Layout speichern',
        'load_layout': '📂 Layout laden',
        'presets': '🎨 Voreinstellungen',
        'hardware': '🖥️ Hardware',
        'monitor': '📊 Monitor',
        'performance': '📈 Leistung',
        'export': '📤 Exportieren',
        'import': '📥 Importieren',
        'preview': '👁️ Vorschau',
        'refresh': '🔄 Aktualisieren',
        
        # Labels
        'ai_caption_editor': 'KI-Untertitel-Editor',
        'processing_mode': 'Modus:',
        'language': 'Sprache:',
        'words_per_line': 'Wörter pro Zeile:',
        'output_format': 'Format:',
        'output_folder': 'Ausgabeordner:',
        'status': 'Status:',
        'notebook_url': 'Notizbuch-URL:',
        'not_available': 'Nicht verfügbar',
        'idle': 'Bereit',
        'speed': 'Geschwindigkeit:',
        'eta': 'Verbleibend:',
        'downloading': 'Herunterladen...',
        'uploading': 'Hochladen...',
        'waiting': 'Warten...',
        'colab_link': 'Colab-Link:',
        'click_to_open': 'Klicken zum Öffnen',
        
        # Modes
        'normal_mode': '🖥️ Lokal',
        'online_mode': '☁️ Online',
        
        # Languages for transcription
        'english_transcribe': '🇺🇸 Englisch',
        'japanese_translate': '🇯🇵 Japanisch → Englisch',
        'chinese_transcribe': '🇨🇳 Chinesisch',
        'french_transcribe': '🇫🇷 Französisch',
        'german_transcribe': '🇩🇪 Deutsch',
        'spanish_transcribe': '🇪🇸 Spanisch',
        'russian_transcribe': '🇷🇺 Russisch',
        'arabic_transcribe': '🇸🇦 Arabisch',
        'hindi_transcribe': '🇮🇳 Hindi',
        'bengali_transcribe': '🇧🇩 Bengalisch',
        'urdu_transcribe': '🇵🇰 Urdu',
        'portuguese_transcribe': '🇵🇹 Portugiesisch',
        'italian_transcribe': '🇮🇹 Italienisch',
        'dutch_transcribe': '🇳🇱 Niederländisch',
        'polish_transcribe': '🇵🇱 Polnisch',
        'turkish_transcribe': '🇹🇷 Türkisch',
        'vietnamese_transcribe': '🇻🇳 Vietnamesisch',
        'thai_transcribe': '🇹🇭 Thailändisch',
        'korean_transcribe': '🇰🇷 Koreanisch',
        
        # Formats
        'srt_format': '📄 SRT',
        'ass_format': '🎨 ASS',
        
        # Messages
        'import_complete': 'Import abgeschlossen',
        'import_success': 'Medien erfolgreich importiert.',
        'enhancement_complete': 'Verbesserung abgeschlossen',
        'enhancement_success': 'Gesang extrahiert:',
        'generation_complete': 'Generierung abgeschlossen',
        'generation_success': 'Untertitel gespeichert:',
        'download_complete': 'Download abgeschlossen',
        'download_success': 'Modell heruntergeladen!',
        'download_failed': 'Download fehlgeschlagen',
        'cancel_confirm': 'Abbruch bestätigen',
        'cancel_confirm_msg': 'Aktuellen Vorgang abbrechen?',
        'force_cancel_confirm': '⚠️ Erzwingen? Dies kann zu Instabilität führen.',
        'no_audio': 'Kein Audio',
        'no_audio_msg': 'Keine Audiodatei geladen.',
        'no_media': 'Keine Medien',
        'no_media_msg': 'Medien zuerst importieren.',
        'overwrite': 'Datei überschreiben?',
        'overwrite_msg': 'Datei existiert:\n{}\nÜberschreiben?',
        'login_required': 'Bitte zuerst bei Google anmelden.',
        'conversion_warning': 'Konvertierungswarnung',
        'conversion_warning_msg': 'Originaldatei wird verwendet.',
        'playback_error': 'Wiedergabefehler',
        'colab_timeout': 'Colab-Zeitüberschreitung',
        'colab_timeout_msg': 'Ergebnisdatei nicht gefunden.',
        'network_error': 'Netzwerkfehler',
        'model_load_error': 'Modell-Ladefehler',
        
        # Settings Dialog
        'settings_title': 'Einstellungen - Professionell',
        'general_tab': 'Allgemein',
        'paths_tab': 'Pfade',
        'features_tab': 'Funktionen',
        'advanced_tab': 'Erweitert',
        'workspace_tab': 'Arbeitsbereich',
        'presets_tab': 'Voreinstellungen',
        'hardware_tab': 'Hardware',
        'visual_theme': 'Design',
        'system_default': 'System',
        'light_mode': 'Hell',
        'dark_mode': 'Dunkel',
        'ui_scaling': 'UI-Skalierung',
        'scale_factor': 'Skalierung:',
        'temp_dir': 'Temporärverzeichnis',
        'temp_dir_placeholder': 'System-Temp',
        'browse_folder': 'Durchsuchen',
        'models_dir': 'Modellverzeichnis',
        'models_dir_placeholder': 'App-Daten',
        'auto_features': 'Automatische Funktionen',
        'auto_enhance': 'Automatisch verbessern',
        'default_language': 'Standardsprache:',
        'default_wpl': 'Standard Wörter/Zeile',
        'words': 'Wörter:',
        'default_format': 'Standardformat',
        'format': 'Format:',
        'cancel_options': 'Abbruchoptionen',
        'confirm_cancel': 'Abbruch bestätigen',
        'force_cancel_timeout': 'Erzwingen nach:',
        'seconds': 's',
        'max_retry': 'Max. Wiederholungen:',
        'ui_options': 'UI-Optionen',
        'minimize_tray': 'In Tray minimieren',
        'show_tooltips': 'Tooltips anzeigen',
        'ui_language': 'Sprache:',
        'apply_restart': 'Übernehmen & Neustarten',
        
        # Hardware Detection
        'hardware_acceleration': 'Hardwarebeschleunigung',
        'cuda_available': 'CUDA verfügbar',
        'cuda_not_available': 'CUDA nicht verfügbar',
        'gpu_info': 'GPU: {}',
        'cpu_info': 'CPU: {}',
        'memory_info': 'RAM: {:.1f} GB',
        'using_gpu': 'GPU-Modus',
        'using_cpu': 'CPU-Modus',
        'gpu_temp': 'GPU-Temperatur: {}°C',
        'gpu_usage': 'GPU-Auslastung: {}%',
        'cpu_usage': 'CPU-Auslastung: {}%',
        'gpu_memory': 'GPU-Speicher: {:.1f}/{:.1f} GB',
        'ram_usage': 'RAM-Auslastung: {:.1f}/{:.1f} GB ({:.0f}%)',
        'disk_usage': 'Festplattenauslastung: {:.1f}/{:.1f} GB ({:.0f}%)',
        
        # Hardware Monitor
        'hardware_monitor': 'Hardware-Monitor',
        'cpu_tab': 'CPU',
        'gpu_tab': 'GPU',
        'ram_tab': 'RAM',
        'disk_tab': 'Festplatte',
        'network_tab': 'Netzwerk',
        'performance_tab': 'Leistung',
        'start_monitoring': 'Überwachung starten',
        'stop_monitoring': 'Überwachung stoppen',
        'export_data': 'Daten exportieren',
        'import_data': 'Daten importieren',
        'clear_history': 'Verlauf löschen',
        'refresh_rate': 'Aktualisierungsrate:',
        
        # Multi-monitor
        'monitor_manager': 'Monitorverwaltung',
        'detect_monitors': 'Monitore erkennen',
        'move_to_monitor': 'Auf Monitor verschieben',
        'create_window': 'Fenster erstellen',
        'close_window': 'Fenster schließen',
        'monitor': 'Monitor {}',
        'primary': 'Primär',
        'resolution': 'Auflösung: {}x{}',
        'refresh_rate': 'Bildwiederholrate: {} Hz',
        
        # Workspace customization
        'workspace_customize': 'Arbeitsbereich anpassen',
        'accent_color': 'Akzentfarbe',
        'glow_intensity': 'Leuchtintensität',
        'animation_speed': 'Animationsgeschwindigkeit',
        'card_opacity': 'Kartentransparenz',
        'font_family': 'Schriftart',
        'font_size': 'Schriftgröße',
        'reset_defaults': 'Zurücksetzen',
        'preview': 'Vorschau',
        'save_layout': 'Layout speichern',
        'load_layout': 'Layout laden',
        'layout_name': 'Layout-Name:',
        'select_layout': 'Layout auswählen:',
        'preset_name': 'Voreinstellungsname:',
        'apply_preset': 'Voreinstellung anwenden',
        'save_preset': 'Voreinstellung speichern',
        'delete_preset': 'Voreinstellung löschen',
        
        # Animation control
        'animation_control': 'Animationssteuerung',
        'enable_animations': 'Animationen aktivieren',
        'animation_speed_slow': 'Langsam',
        'animation_speed_normal': 'Normal',
        'animation_speed_fast': 'Schnell',
    },
    
    'hi': {
        # Window Title
        'window_title': 'NotyCaption Pro - पेशेवर AI कैप्शन जनरेटर',
        
        # App Name
        'app_name': 'NotyCaption Pro',
        'app_subtitle': 'AI-संचालित कैप्शन जनरेटर',
        
        # Menu and Status
        'ready': 'तैयार',
        'processing': 'प्रक्रियाधीन...',
        'canceled': 'रद्द',
        'completed': 'पूर्ण',
        'failed': 'विफल',
        
        # Buttons
        'edit_captions': '✏️ कैप्शन संपादित करें',
        'save_exit_edit': '💾 सहेजें और बाहर निकलें',
        'settings': '⚙️ सेटिंग्स',
        'download_model': '📥 मॉडल डाउनलोड करें',
        'login_google': '🔐 Google लॉगिन',
        'import_media': '📁 मीडिया आयात करें',
        'browse_output': '📂 आउटपुट फ़ोल्डर',
        'enhance_audio': '🎤 ऑडियो बढ़ाएं',
        'play_pause': '▶️ चलाएं / ⏸️ रोकें',
        'playing': '⏸️ चल रहा है...',
        'paused': '▶️ चलाएं / ⏸️ रोकें',
        'generate': '🚀 कैप्शन जनरेट करें',
        'cancel': 'रद्द करें',
        'force_cancel': '⚠️ जबरन रद्द करें',
        'reopen_notebook': '🔗 नोटबुक खोलें',
        'copy_url': '📋 URL कॉपी करें',
        'workspace': '🎨 कार्यक्षेत्र',
        'save_layout': '💾 लेआउट सहेजें',
        'load_layout': '📂 लेआउट लोड करें',
        'presets': '🎨 प्रीसेट',
        'hardware': '🖥️ हार्डवेयर',
        'monitor': '📊 मॉनिटर',
        'performance': '📈 प्रदर्शन',
        'export': '📤 निर्यात',
        'import': '📥 आयात',
        'preview': '👁️ पूर्वावलोकन',
        'refresh': '🔄 ताज़ा करें',
        
        # Labels
        'ai_caption_editor': 'AI कैप्शन संपादक',
        'processing_mode': 'मोड:',
        'language': 'भाषा:',
        'words_per_line': 'प्रति पंक्ति शब्द:',
        'output_format': 'फॉर्मेट:',
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
        'colab_link': 'Colab लिंक:',
        'click_to_open': 'खोलने के लिए क्लिक करें',
        
        # Modes
        'normal_mode': '🖥️ स्थानीय',
        'online_mode': '☁️ ऑनलाइन',
        
        # Languages for transcription
        'english_transcribe': '🇺🇸 अंग्रेजी',
        'japanese_translate': '🇯🇵 जापानी → अंग्रेजी',
        'chinese_transcribe': '🇨🇳 चीनी',
        'french_transcribe': '🇫🇷 फ्रेंच',
        'german_transcribe': '🇩🇪 जर्मन',
        'spanish_transcribe': '🇪🇸 स्पेनिश',
        'russian_transcribe': '🇷🇺 रूसी',
        'arabic_transcribe': '🇸🇦 अरबी',
        'hindi_transcribe': '🇮🇳 हिंदी',
        'bengali_transcribe': '🇧🇩 बंगाली',
        'urdu_transcribe': '🇵🇰 उर्दू',
        'portuguese_transcribe': '🇵🇹 पुर्तगाली',
        'italian_transcribe': '🇮🇹 इतालवी',
        'dutch_transcribe': '🇳🇱 डच',
        'polish_transcribe': '🇵🇱 पोलिश',
        'turkish_transcribe': '🇹🇷 तुर्की',
        'vietnamese_transcribe': '🇻🇳 वियतनामी',
        'thai_transcribe': '🇹🇭 थाई',
        'korean_transcribe': '🇰🇷 कोरियाई',
        
        # Formats
        'srt_format': '📄 SRT',
        'ass_format': '🎨 ASS',
        
        # Messages
        'import_complete': 'आयात पूर्ण',
        'import_success': 'मीडिया सफलतापूर्वक आयात हुआ।',
        'enhancement_complete': 'ऑडियो सुधार पूर्ण',
        'enhancement_success': 'वोकल्स निकाले गए:',
        'generation_complete': 'कैप्शन जनरेशन पूर्ण',
        'generation_success': 'कैप्शन सहेजे गए:',
        'download_complete': 'डाउनलोड पूर्ण',
        'download_success': 'मॉडल डाउनलोड हुआ!',
        'download_failed': 'डाउनलोड विफल',
        'cancel_confirm': 'रद्द करने की पुष्टि करें',
        'cancel_confirm_msg': 'वर्तमान कार्य रद्द करें?',
        'force_cancel_confirm': '⚠️ जबरन रद्द करें? इससे अस्थिरता हो सकती है।',
        'no_audio': 'कोई ऑडियो नहीं',
        'no_audio_msg': 'कोई ऑडियो फ़ाइल लोड नहीं है।',
        'no_media': 'कोई मीडिया नहीं',
        'no_media_msg': 'पहले मीडिया आयात करें।',
        'overwrite': 'फ़ाइल ओवरराइट करें?',
        'overwrite_msg': 'फ़ाइल मौजूद है:\n{}\nओवरराइट करें?',
        'login_required': 'कृपया पहले Google से लॉगिन करें।',
        'conversion_warning': 'रूपांतरण चेतावनी',
        'conversion_warning_msg': 'मूल फ़ाइल का उपयोग कर रहे हैं।',
        'playback_error': 'प्लेबैक त्रुटि',
        'colab_timeout': 'Colab टाइमआउट',
        'colab_timeout_msg': 'परिणाम फ़ाइल नहीं मिली।',
        'network_error': 'नेटवर्क त्रुटि',
        'model_load_error': 'मॉडल लोड त्रुटि',
        
        # Settings Dialog
        'settings_title': 'सेटिंग्स - पेशेवर',
        'general_tab': 'सामान्य',
        'paths_tab': 'पथ',
        'features_tab': 'सुविधाएं',
        'advanced_tab': 'उन्नत',
        'workspace_tab': 'कार्यक्षेत्र',
        'presets_tab': 'प्रीसेट',
        'hardware_tab': 'हार्डवेयर',
        'visual_theme': 'थीम',
        'system_default': 'सिस्टम',
        'light_mode': 'लाइट',
        'dark_mode': 'डार्क',
        'ui_scaling': 'UI स्केलिंग',
        'scale_factor': 'स्केल:',
        'temp_dir': 'अस्थायी निर्देशिका',
        'temp_dir_placeholder': 'सिस्टम अस्थायी',
        'browse_folder': 'ब्राउज़ करें',
        'models_dir': 'मॉडल निर्देशिका',
        'models_dir_placeholder': 'ऐप डेटा',
        'auto_features': 'स्वचालित सुविधाएं',
        'auto_enhance': 'स्वतः सुधार',
        'default_language': 'डिफ़ॉल्ट भाषा:',
        'default_wpl': 'डिफ़ॉल्ट शब्द/पंक्ति',
        'words': 'शब्द:',
        'default_format': 'डिफ़ॉल्ट फॉर्मेट',
        'format': 'फॉर्मेट:',
        'cancel_options': 'रद्द करने के विकल्प',
        'confirm_cancel': 'रद्द करने से पहले पुष्टि करें',
        'force_cancel_timeout': 'जबरन रद्द करने का समय:',
        'seconds': 'सेकंड',
        'max_retry': 'अधिकतम प्रयास:',
        'ui_options': 'UI विकल्प',
        'minimize_tray': 'ट्रे में छोटा करें',
        'show_tooltips': 'टूलटिप दिखाएं',
        'ui_language': 'भाषा:',
        'apply_restart': 'लागू करें और पुनरारंभ करें',
        
        # Hardware Detection
        'hardware_acceleration': 'हार्डवेयर त्वरण',
        'cuda_available': 'CUDA उपलब्ध',
        'cuda_not_available': 'CUDA उपलब्ध नहीं',
        'gpu_info': 'GPU: {}',
        'cpu_info': 'CPU: {}',
        'memory_info': 'RAM: {:.1f} GB',
        'using_gpu': 'GPU मोड',
        'using_cpu': 'CPU मोड',
        'gpu_temp': 'GPU तापमान: {}°C',
        'gpu_usage': 'GPU उपयोग: {}%',
        'cpu_usage': 'CPU उपयोग: {}%',
        'gpu_memory': 'GPU मेमोरी: {:.1f}/{:.1f} GB',
        'ram_usage': 'RAM उपयोग: {:.1f}/{:.1f} GB ({:.0f}%)',
        'disk_usage': 'डिस्क उपयोग: {:.1f}/{:.1f} GB ({:.0f}%)',
        
        # Hardware Monitor
        'hardware_monitor': 'हार्डवेयर मॉनिटर',
        'cpu_tab': 'CPU',
        'gpu_tab': 'GPU',
        'ram_tab': 'RAM',
        'disk_tab': 'डिस्क',
        'network_tab': 'नेटवर्क',
        'performance_tab': 'प्रदर्शन',
        'start_monitoring': 'मॉनिटरिंग शुरू करें',
        'stop_monitoring': 'मॉनिटरिंग बंद करें',
        'export_data': 'डेटा निर्यात',
        'import_data': 'डेटा आयात',
        'clear_history': 'इतिहास साफ़ करें',
        'refresh_rate': 'रिफ्रेश दर:',
        
        # Multi-monitor
        'monitor_manager': 'मॉनिटर प्रबंधक',
        'detect_monitors': 'मॉनिटर खोजें',
        'move_to_monitor': 'मॉनिटर पर ले जाएं',
        'create_window': 'विंडो बनाएं',
        'close_window': 'विंडो बंद करें',
        'monitor': 'मॉनिटर {}',
        'primary': 'प्राथमिक',
        'resolution': 'रिज़ॉल्यूशन: {}x{}',
        'refresh_rate': 'रिफ्रेश दर: {} Hz',
        
        # Workspace customization
        'workspace_customize': 'कार्यक्षेत्र अनुकूलित करें',
        'accent_color': 'एक्सेंट रंग',
        'glow_intensity': 'चमक तीव्रता',
        'animation_speed': 'एनिमेशन गति',
        'card_opacity': 'कार्ड अपारदर्शिता',
        'font_family': 'फ़ॉन्ट परिवार',
        'font_size': 'फ़ॉन्ट आकार',
        'reset_defaults': 'डिफ़ॉल्ट पर रीसेट',
        'preview': 'पूर्वावलोकन',
        'save_layout': 'लेआउट सहेजें',
        'load_layout': 'लेआउट लोड करें',
        'layout_name': 'लेआउट नाम:',
        'select_layout': 'लेआउट चुनें:',
        'preset_name': 'प्रीसेट नाम:',
        'apply_preset': 'प्रीसेट लागू करें',
        'save_preset': 'प्रीसेट सहेजें',
        'delete_preset': 'प्रीसेट हटाएं',
        
        # Animation control
        'animation_control': 'एनिमेशन नियंत्रण',
        'enable_animations': 'एनिमेशन सक्षम करें',
        'animation_speed_slow': 'धीमा',
        'animation_speed_normal': 'सामान्य',
        'animation_speed_fast': 'तेज़',
    },
    
    'ur': {
        # Window Title
        'window_title': 'NotyCaption Pro - پیشہ ور AI کیپشن جنریٹر',
        
        # App Name
        'app_name': 'NotyCaption Pro',
        'app_subtitle': 'AI سے چلنے والا کیپشن جنریٹر',
        
        # Menu and Status
        'ready': 'تیار',
        'processing': 'پروسیسنگ...',
        'canceled': 'منسوخ',
        'completed': 'مکمل',
        'failed': 'ناکام',
        
        # Buttons
        'edit_captions': '✏️ کیپشن میں ترمیم',
        'save_exit_edit': '💾 محفوظ کریں اور باہر نکلیں',
        'settings': '⚙️ ترتیبات',
        'download_model': '📥 ماڈل ڈاؤن لوڈ',
        'login_google': '🔐 Google لاگ ان',
        'import_media': '📁 میڈیا درآمد',
        'browse_output': '📂 آؤٹ پٹ فولڈر',
        'enhance_audio': '🎤 آڈیو بہتر کریں',
        'play_pause': '▶️ چلائیں / ⏸️ روکیں',
        'playing': '⏸️ چل رہا ہے...',
        'paused': '▶️ چلائیں / ⏸️ روکیں',
        'generate': '🚀 کیپشن تیار کریں',
        'cancel': 'منسوخ کریں',
        'force_cancel': '⚠️ زبردستی منسوخ کریں',
        'reopen_notebook': '🔗 نوٹ بک کھولیں',
        'copy_url': '📋 URL کاپی کریں',
        'workspace': '🎨 کام کی جگہ',
        'save_layout': '💾 لے آؤٹ محفوظ کریں',
        'load_layout': '📂 لے آؤٹ لوڈ کریں',
        'presets': '🎨 پری سیٹس',
        'hardware': '🖥️ ہارڈویئر',
        'monitor': '📊 مانیٹر',
        'performance': '📈 کارکردگی',
        'export': '📤 برآمد',
        'import': '📥 درآمد',
        'preview': '👁️ پیش نظارہ',
        'refresh': '🔄 تازہ کریں',
        
        # Labels
        'ai_caption_editor': 'AI کیپشن ایڈیٹر',
        'processing_mode': 'موڈ:',
        'language': 'زبان:',
        'words_per_line': 'الفاظ فی سطر:',
        'output_format': 'فارمیٹ:',
        'output_folder': 'آؤٹ پٹ فولڈر:',
        'status': 'حالت:',
        'notebook_url': 'نوٹ بک URL:',
        'not_available': 'دستیاب نہیں',
        'idle': 'غیر فعال',
        'speed': 'رفتار:',
        'eta': 'باقی وقت:',
        'downloading': 'ڈاؤن لوڈ ہو رہا ہے...',
        'uploading': 'اپ لوڈ ہو رہا ہے...',
        'waiting': 'انتظار...',
        'colab_link': 'Colab لنک:',
        'click_to_open': 'کھولنے کے لیے کلک کریں',
        
        # Modes
        'normal_mode': '🖥️ مقامی',
        'online_mode': '☁️ آن لائن',
        
        # Languages for transcription
        'english_transcribe': '🇺🇸 انگریزی',
        'japanese_translate': '🇯🇵 جاپانی → انگریزی',
        'chinese_transcribe': '🇨🇳 چینی',
        'french_transcribe': '🇫🇷 فرانسیسی',
        'german_transcribe': '🇩🇪 جرمن',
        'spanish_transcribe': '🇪🇸 ہسپانوی',
        'russian_transcribe': '🇷🇺 روسی',
        'arabic_transcribe': '🇸🇦 عربی',
        'hindi_transcribe': '🇮🇳 ہندی',
        'bengali_transcribe': '🇧🇩 بنگالی',
        'urdu_transcribe': '🇵🇰 اردو',
        'portuguese_transcribe': '🇵🇹 پرتگالی',
        'italian_transcribe': '🇮🇹 اطالوی',
        'dutch_transcribe': '🇳🇱 ڈچ',
        'polish_transcribe': '🇵🇱 پولش',
        'turkish_transcribe': '🇹🇷 ترکی',
        'vietnamese_transcribe': '🇻🇳 ویتنامی',
        'thai_transcribe': '🇹🇭 تھائی',
        'korean_transcribe': '🇰🇷 کورین',
        
        # Formats
        'srt_format': '📄 SRT',
        'ass_format': '🎨 ASS',
        
        # Messages
        'import_complete': 'درآمد مکمل',
        'import_success': 'میڈیا کامیابی سے درآمد ہوا۔',
        'enhancement_complete': 'بہتری مکمل',
        'enhancement_success': 'آوازیں نکالی گئیں:',
        'generation_complete': 'کیپشن جنریشن مکمل',
        'generation_success': 'کیپشن محفوظ ہو گئے:',
        'download_complete': 'ڈاؤن لوڈ مکمل',
        'download_success': 'ماڈل ڈاؤن لوڈ ہو گیا!',
        'download_failed': 'ڈاؤن لوڈ ناکام',
        'cancel_confirm': 'منسوخی کی تصدیق',
        'cancel_confirm_msg': 'موجودہ کارروائی منسوخ کریں؟',
        'force_cancel_confirm': '⚠️ زبردستی منسوخ کریں؟ یہ عدم استحکام کا سبب بن سکتا ہے۔',
        'no_audio': 'کوئی آڈیو نہیں',
        'no_audio_msg': 'کوئی آڈیو فائل لوڈ نہیں ہے۔',
        'no_media': 'کوئی میڈیا نہیں',
        'no_media_msg': 'پہلے میڈیا درآمد کریں۔',
        'overwrite': 'فائل اوور رائٹ کریں؟',
        'overwrite_msg': 'فائل موجود ہے:\n{}\nاوور رائٹ کریں؟',
        'login_required': 'براہ کرم پہلے Google سے لاگ ان کریں۔',
        'conversion_warning': 'تبدیلی کا انتباہ',
        'conversion_warning_msg': 'اصل فائل استعمال کر رہے ہیں۔',
        'playback_error': 'پلے بیک میں خرابی',
        'colab_timeout': 'Colab ٹائم آؤٹ',
        'colab_timeout_msg': 'نتیجہ فائل نہیں ملی۔',
        'network_error': 'نیٹ ورک کی خرابی',
        'model_load_error': 'ماڈل لوڈ کرنے میں خرابی',
        
        # Settings Dialog
        'settings_title': 'ترتیبات - پیشہ ور',
        'general_tab': 'عام',
        'paths_tab': 'راستے',
        'features_tab': 'خصوصیات',
        'advanced_tab': 'جدید',
        'workspace_tab': 'کام کی جگہ',
        'presets_tab': 'پری سیٹس',
        'hardware_tab': 'ہارڈویئر',
        'visual_theme': 'تھیم',
        'system_default': 'سسٹم',
        'light_mode': 'لائٹ',
        'dark_mode': 'ڈارک',
        'ui_scaling': 'UI اسکیلنگ',
        'scale_factor': 'اسکیل:',
        'temp_dir': 'عارضی ڈائریکٹری',
        'temp_dir_placeholder': 'سسٹم عارضی',
        'browse_folder': 'براؤز کریں',
        'models_dir': 'ماڈلز ڈائریکٹری',
        'models_dir_placeholder': 'ایپ ڈیٹا',
        'auto_features': 'خودکار خصوصیات',
        'auto_enhance': 'خودکار بہتری',
        'default_language': 'پہلے سے طے شدہ زبان:',
        'default_wpl': 'پہلے سے طے شدہ الفاظ/سطر',
        'words': 'الفاظ:',
        'default_format': 'پہلے سے طے شدہ فارمیٹ',
        'format': 'فارمیٹ:',
        'cancel_options': 'منسوخی کے اختیارات',
        'confirm_cancel': 'منسوخی سے پہلے تصدیق کریں',
        'force_cancel_timeout': 'زبردستی منسوخی کا وقت:',
        'seconds': 'سیکنڈ',
        'max_retry': 'زیادہ سے زیادہ کوششیں:',
        'ui_options': 'UI اختیارات',
        'minimize_tray': 'ٹرے میں چھوٹا کریں',
        'show_tooltips': 'ٹول ٹپس دکھائیں',
        'ui_language': 'زبان:',
        'apply_restart': 'لاگو کریں اور دوبارہ شروع کریں',
        
        # Hardware Detection
        'hardware_acceleration': 'ہارڈویئر ایکسلریشن',
        'cuda_available': 'CUDA دستیاب',
        'cuda_not_available': 'CUDA دستیاب نہیں',
        'gpu_info': 'GPU: {}',
        'cpu_info': 'CPU: {}',
        'memory_info': 'RAM: {:.1f} GB',
        'using_gpu': 'GPU موڈ',
        'using_cpu': 'CPU موڈ',
        'gpu_temp': 'GPU درجہ حرارت: {}°C',
        'gpu_usage': 'GPU استعمال: {}%',
        'cpu_usage': 'CPU استعمال: {}%',
        'gpu_memory': 'GPU میموری: {:.1f}/{:.1f} GB',
        'ram_usage': 'RAM استعمال: {:.1f}/{:.1f} GB ({:.0f}%)',
        'disk_usage': 'ڈسک استعمال: {:.1f}/{:.1f} GB ({:.0f}%)',
        
        # Hardware Monitor
        'hardware_monitor': 'ہارڈویئر مانیٹر',
        'cpu_tab': 'CPU',
        'gpu_tab': 'GPU',
        'ram_tab': 'RAM',
        'disk_tab': 'ڈسک',
        'network_tab': 'نیٹ ورک',
        'performance_tab': 'کارکردگی',
        'start_monitoring': 'مانیٹرنگ شروع کریں',
        'stop_monitoring': 'مانیٹرنگ بند کریں',
        'export_data': 'ڈیٹا برآمد کریں',
        'import_data': 'ڈیٹا درآمد کریں',
        'clear_history': 'تاریخ صاف کریں',
        'refresh_rate': 'ریفریش ریٹ:',
        
        # Multi-monitor
        'monitor_manager': 'مانیٹر مینیجر',
        'detect_monitors': 'مانیٹرز کا پتہ لگائیں',
        'move_to_monitor': 'مانیٹر پر منتقل کریں',
        'create_window': 'ونڈو بنائیں',
        'close_window': 'ونڈو بند کریں',
        'monitor': 'مانیٹر {}',
        'primary': 'بنیادی',
        'resolution': 'ریزولوشن: {}x{}',
        'refresh_rate': 'ریفریش ریٹ: {} Hz',
        
        # Workspace customization
        'workspace_customize': 'کام کی جگہ کو حسب ضرورت بنائیں',
        'accent_color': 'ایکسینٹ رنگ',
        'glow_intensity': 'چمک کی شدت',
        'animation_speed': 'اینیمیشن کی رفتار',
        'card_opacity': 'کارڈ کی دھندلاپن',
        'font_family': 'فونٹ فیملی',
        'font_size': 'فونٹ سائز',
        'reset_defaults': 'ڈیفالٹ پر ری سیٹ',
        'preview': 'پیش نظارہ',
        'save_layout': 'لے آؤٹ محفوظ کریں',
        'load_layout': 'لے آؤٹ لوڈ کریں',
        'layout_name': 'لے آؤٹ کا نام:',
        'select_layout': 'لے آؤٹ منتخب کریں:',
        'preset_name': 'پری سیٹ کا نام:',
        'apply_preset': 'پری سیٹ لاگو کریں',
        'save_preset': 'پری سیٹ محفوظ کریں',
        'delete_preset': 'پری سیٹ حذف کریں',
        
        # Animation control
        'animation_control': 'اینیمیشن کنٹرول',
        'enable_animations': 'اینیمیشن فعال کریں',
        'animation_speed_slow': 'آہستہ',
        'animation_speed_normal': 'عام',
        'animation_speed_fast': 'تیز',
    },
    
    'ar': {
        # Window Title
        'window_title': 'NotyCaption Pro - مولد التسميات التوضيحية بالذكاء الاصطناعي المحترف',
        
        # App Name
        'app_name': 'NotyCaption Pro',
        'app_subtitle': 'مولد التسميات التوضيحية بالذكاء الاصطناعي',
        
        # Menu and Status
        'ready': 'جاهز',
        'processing': 'جاري المعالجة...',
        'canceled': 'ملغي',
        'completed': 'مكتمل',
        'failed': 'فشل',
        
        # Buttons
        'edit_captions': '✏️ تحرير التسميات',
        'save_exit_edit': '💾 حفظ وخروج',
        'settings': '⚙️ الإعدادات',
        'download_model': '📥 تحميل النموذج',
        'login_google': '🔐 تسجيل الدخول Google',
        'import_media': '📁 استيراد وسائط',
        'browse_output': '📂 مجلد الإخراج',
        'enhance_audio': '🎤 تحسين الصوت',
        'play_pause': '▶️ تشغيل / ⏸️ إيقاف مؤقت',
        'playing': '⏸️ جار التشغيل...',
        'paused': '▶️ تشغيل / ⏸️ إيقاف مؤقت',
        'generate': '🚀 إنشاء التسميات',
        'cancel': 'إلغاء',
        'force_cancel': '⚠️ إلغاء强制',
        'reopen_notebook': '🔗 فتح الدفتر',
        'copy_url': '📋 نسخ الرابط',
        'workspace': '🎨 مساحة العمل',
        'save_layout': '💾 حفظ التخطيط',
        'load_layout': '📂 تحميل التخطيط',
        'presets': '🎨 الإعدادات المسبقة',
        'hardware': '🖥️ الأجهزة',
        'monitor': '📊 مراقب',
        'performance': '📈 الأداء',
        'export': '📤 تصدير',
        'import': '📥 استيراد',
        'preview': '👁️ معاينة',
        'refresh': '🔄 تحديث',
        
        # Labels
        'ai_caption_editor': 'محرر التسميات بالذكاء الاصطناعي',
        'processing_mode': 'الوضع:',
        'language': 'اللغة:',
        'words_per_line': 'الكلمات في السطر:',
        'output_format': 'التنسيق:',
        'output_folder': 'مجلد الإخراج:',
        'status': 'الحالة:',
        'notebook_url': 'رابط الدفتر:',
        'not_available': 'غير متاح',
        'idle': 'خامل',
        'speed': 'السرعة:',
        'eta': 'الوقت المتبقي:',
        'downloading': 'جاري التحميل...',
        'uploading': 'جاري الرفع...',
        'waiting': 'انتظار...',
        'colab_link': 'رابط Colab:',
        'click_to_open': 'انقر للفتح',
        
        # Modes
        'normal_mode': '🖥️ محلي',
        'online_mode': '☁️ عبر الإنترنت',
        
        # Languages for transcription
        'english_transcribe': '🇺🇸 الإنجليزية',
        'japanese_translate': '🇯🇵 اليابانية → الإنجليزية',
        'chinese_transcribe': '🇨🇳 الصينية',
        'french_transcribe': '🇫🇷 الفرنسية',
        'german_transcribe': '🇩🇪 الألمانية',
        'spanish_transcribe': '🇪🇸 الإسبانية',
        'russian_transcribe': '🇷🇺 الروسية',
        'arabic_transcribe': '🇸🇦 العربية',
        'hindi_transcribe': '🇮🇳 الهندية',
        'bengali_transcribe': '🇧🇩 البنغالية',
        'urdu_transcribe': '🇵🇰 الأردية',
        'portuguese_transcribe': '🇵🇹 البرتغالية',
        'italian_transcribe': '🇮🇹 الإيطالية',
        'dutch_transcribe': '🇳🇱 الهولندية',
        'polish_transcribe': '🇵🇱 البولندية',
        'turkish_transcribe': '🇹🇷 التركية',
        'vietnamese_transcribe': '🇻🇳 الفيتنامية',
        'thai_transcribe': '🇹🇭 التايلاندية',
        'korean_transcribe': '🇰🇷 الكورية',
        
        # Formats
        'srt_format': '📄 SRT',
        'ass_format': '🎨 ASS',
        
        # Messages
        'import_complete': 'اكتمل الاستيراد',
        'import_success': 'تم استيراد الوسائط بنجاح.',
        'enhancement_complete': 'اكتمل التحسين',
        'enhancement_success': 'تم استخراج الصوت:',
        'generation_complete': 'اكتمل إنشاء التسميات',
        'generation_success': 'تم حفظ التسميات:',
        'download_complete': 'اكتمل التحميل',
        'download_success': 'تم تحميل النموذج!',
        'download_failed': 'فشل التحميل',
        'cancel_confirm': 'تأكيد الإلغاء',
        'cancel_confirm_msg': 'إلغاء العملية الحالية؟',
        'force_cancel_confirm': '⚠️ إلغاء强制؟ قد يسبب عدم استقرار.',
        'no_audio': 'لا يوجد صوت',
        'no_audio_msg': 'لم يتم تحميل ملف صوتي.',
        'no_media': 'لا توجد وسائط',
        'no_media_msg': 'قم باستيراد الوسائط أولاً.',
        'overwrite': 'استبدال الملف؟',
        'overwrite_msg': 'الملف موجود:\n{}\nهل تريد الاستبدال؟',
        'login_required': 'يرجى تسجيل الدخول عبر Google أولاً.',
        'conversion_warning': 'تحذير التحويل',
        'conversion_warning_msg': 'استخدام الملف الأصلي.',
        'playback_error': 'خطأ في التشغيل',
        'colab_timeout': 'انتهاء مهلة Colab',
        'colab_timeout_msg': 'لم يتم العثور على ملف النتيجة.',
        'network_error': 'خطأ في الشبكة',
        'model_load_error': 'خطأ في تحميل النموذج',
        
        # Settings Dialog
        'settings_title': 'الإعدادات - محترف',
        'general_tab': 'عام',
        'paths_tab': 'المسارات',
        'features_tab': 'الميزات',
        'advanced_tab': 'متقدم',
        'workspace_tab': 'مساحة العمل',
        'presets_tab': 'الإعدادات المسبقة',
        'hardware_tab': 'الأجهزة',
        'visual_theme': 'المظهر',
        'system_default': 'النظام',
        'light_mode': 'فاتح',
        'dark_mode': 'داكن',
        'ui_scaling': 'تحجيم الواجهة',
        'scale_factor': 'التحجيم:',
        'temp_dir': 'المجلد المؤقت',
        'temp_dir_placeholder': 'مؤقت النظام',
        'browse_folder': 'استعراض',
        'models_dir': 'مجلد النماذج',
        'models_dir_placeholder': 'بيانات التطبيق',
        'auto_features': 'الميزات التلقائية',
        'auto_enhance': 'تحسين تلقائي',
        'default_language': 'اللغة الافتراضية:',
        'default_wpl': 'الكلمات الافتراضية/السطر',
        'words': 'الكلمات:',
        'default_format': 'التنسيق الافتراضي',
        'format': 'التنسيق:',
        'cancel_options': 'خيارات الإلغاء',
        'confirm_cancel': 'تأكيد قبل الإلغاء',
        'force_cancel_timeout': 'الإلغاء القسري بعد:',
        'seconds': 'ثانية',
        'max_retry': 'الحد الأقصى للمحاولات:',
        'ui_options': 'خيارات الواجهة',
        'minimize_tray': 'تصغير إلى الدرج',
        'show_tooltips': 'إظهار التلميحات',
        'ui_language': 'اللغة:',
        'apply_restart': 'تطبيق وإعادة التشغيل',
        
        # Hardware Detection
        'hardware_acceleration': 'تسريع الأجهزة',
        'cuda_available': 'CUDA متاح',
        'cuda_not_available': 'CUDA غير متاح',
        'gpu_info': 'GPU: {}',
        'cpu_info': 'CPU: {}',
        'memory_info': 'RAM: {:.1f} جيجابايت',
        'using_gpu': 'وضع GPU',
        'using_cpu': 'وضع CPU',
        'gpu_temp': 'درجة حرارة GPU: {}°C',
        'gpu_usage': 'استخدام GPU: {}%',
        'cpu_usage': 'استخدام CPU: {}%',
        'gpu_memory': 'ذاكرة GPU: {:.1f}/{:.1f} جيجابايت',
        'ram_usage': 'استخدام RAM: {:.1f}/{:.1f} جيجابايت ({:.0f}%)',
        'disk_usage': 'استخدام القرص: {:.1f}/{:.1f} جيجابايت ({:.0f}%)',
        
        # Hardware Monitor
        'hardware_monitor': 'مراقب الأجهزة',
        'cpu_tab': 'المعالج',
        'gpu_tab': 'بطاقة الرسوم',
        'ram_tab': 'الذاكرة',
        'disk_tab': 'القرص',
        'network_tab': 'الشبكة',
        'performance_tab': 'الأداء',
        'start_monitoring': 'بدء المراقبة',
        'stop_monitoring': 'إيقاف المراقبة',
        'export_data': 'تصدير البيانات',
        'import_data': 'استيراد البيانات',
        'clear_history': 'مسح السجل',
        'refresh_rate': 'معدل التحديث:',
        
        # Multi-monitor
        'monitor_manager': 'مدير الشاشات',
        'detect_monitors': 'اكتشاف الشاشات',
        'move_to_monitor': 'نقل إلى الشاشة',
        'create_window': 'إنشاء نافذة',
        'close_window': 'إغلاق النافذة',
        'monitor': 'شاشة {}',
        'primary': 'أساسي',
        'resolution': 'الدقة: {}x{}',
        'refresh_rate': 'معدل التحديث: {} هرتز',
        
        # Workspace customization
        'workspace_customize': 'تخصيص مساحة العمل',
        'accent_color': 'لون التمييز',
        'glow_intensity': 'شدة التوهج',
        'animation_speed': 'سرعة الحركة',
        'card_opacity': 'شفافية البطاقات',
        'font_family': 'نوع الخط',
        'font_size': 'حجم الخط',
        'reset_defaults': 'إعادة تعيين',
        'preview': 'معاينة',
        'save_layout': 'حفظ التخطيط',
        'load_layout': 'تحميل التخطيط',
        'layout_name': 'اسم التخطيط:',
        'select_layout': 'اختر التخطيط:',
        'preset_name': 'اسم الإعداد المسبق:',
        'apply_preset': 'تطبيق الإعداد',
        'save_preset': 'حفظ الإعداد',
        'delete_preset': 'حذف الإعداد',
        
        # Animation control
        'animation_control': 'التحكم في الحركة',
        'enable_animations': 'تفعيل الحركة',
        'animation_speed_slow': 'بطيء',
        'animation_speed_normal': 'عادي',
        'animation_speed_fast': 'سريع',
    },
}

# ========================================
# TRANSLATION HELPER
# ========================================
class Translator:
    """Handle UI translations"""
    
    def __init__(self, language='en'):
        self.language = language
        self.translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])
        
    def tr(self, key: str) -> str:
        """Translate a key"""
        return self.translations.get(key, TRANSLATIONS['en'].get(key, key))
        
    def set_language(self, language: str):
        """Change language"""
        self.language = language
        self.translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])

# Global translator instance
_translator = Translator()

def tr(key: str) -> str:
    """Global translate function"""
    return _translator.tr(key)

# ========================================
# RESOURCE PATH HELPER
# ========================================
def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
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
# CUSTOM DARK THEME WITH GLOWING EFFECTS
# ========================================
DARK_THEME = {
    # Base colors - Professional dark theme
    'background_dark': '#0a0a0a',           # Almost black
    'background_medium': '#1a1a1a',          # Dark gray
    'background_light': '#2a2a2a',            # Medium dark gray
    
    # Accent colors - Glowing blue/purple gradient
    'accent_primary': '#4a6fa5',              # Muted blue
    'accent_secondary': '#6b4a9c',            # Purple
    'accent_tertiary': '#3b8ea5',             # Teal blue
    
    # Glowing effects
    'glow_blue': '#4a90e2',                    # Bright blue glow
    'glow_purple': '#9b59b6',                   # Purple glow
    'glow_cyan': '#00d4ff',                      # Cyan glow
    
    # Text colors
    'text_primary': '#ffffff',                  # Pure white
    'text_secondary': '#b0b0b0',                 # Light gray
    'text_accent': '#4a90e2',                     # Blue accent text
    
    # Status colors
    'success': '#2ecc71',                        # Green
    'warning': '#f39c12',                         # Orange
    'error': '#e74c3c',                            # Red
    'info': '#3498db',                              # Blue info
    
    # Borders and overlays
    'border': '#333333',                            # Dark border
    'hover': '#3a3a3a',                              # Hover background
    'overlay': 'rgba(10, 10, 10, 0.95)'              # Overlay background
}

# Light theme
LIGHT_THEME = {
    'background_dark': '#f0f0f0',
    'background_medium': '#ffffff',
    'background_light': '#e0e0e0',
    'accent_primary': '#0078d4',
    'accent_secondary': '#8661c5',
    'accent_tertiary': '#00b7c3',
    'glow_blue': '#0078d4',
    'glow_purple': '#8661c5',
    'glow_cyan': '#00b7c3',
    'text_primary': '#000000',
    'text_secondary': '#333333',
    'text_accent': '#0078d4',
    'success': '#107c10',
    'warning': '#ff8c00',
    'error': '#d13438',
    'info': '#0078d4',
    'border': '#cccccc',
    'hover': '#e5e5e5',
    'overlay': 'rgba(255, 255, 255, 0.95)'
}

# Color presets
COLOR_PRESETS = [
    {
        'name': 'Professional Blue',
        'colors': {
            'accent_primary': '#0078d4',
            'accent_secondary': '#8661c5',
            'glow_blue': '#0078d4',
            'glow_purple': '#8661c5',
            'glow_cyan': '#00b7c3'
        }
    },
    {
        'name': 'Cyber Purple',
        'colors': {
            'accent_primary': '#9b59b6',
            'accent_secondary': '#3498db',
            'glow_blue': '#9b59b6',
            'glow_purple': '#e74c3c',
            'glow_cyan': '#3498db'
        }
    },
    {
        'name': 'Teal Dream',
        'colors': {
            'accent_primary': '#1abc9c',
            'accent_secondary': '#3498db',
            'glow_blue': '#1abc9c',
            'glow_purple': '#9b59b6',
            'glow_cyan': '#3498db'
        }
    },
    {
        'name': 'Sunset Orange',
        'colors': {
            'accent_primary': '#e67e22',
            'accent_secondary': '#e74c3c',
            'glow_blue': '#e67e22',
            'glow_purple': '#e74c3c',
            'glow_cyan': '#f39c12'
        }
    },
    {
        'name': 'Forest Green',
        'colors': {
            'accent_primary': '#27ae60',
            'accent_secondary': '#2980b9',
            'glow_blue': '#27ae60',
            'glow_purple': '#8e44ad',
            'glow_cyan': '#2980b9'
        }
    },
    {
        'name': 'Ruby Red',
        'colors': {
            'accent_primary': '#e74c3c',
            'accent_secondary': '#c0392b',
            'glow_blue': '#e74c3c',
            'glow_purple': '#8e44ad',
            'glow_cyan': '#3498db'
        }
    },
    {
        'name': 'Amber Gold',
        'colors': {
            'accent_primary': '#f39c12',
            'accent_secondary': '#e67e22',
            'glow_blue': '#f39c12',
            'glow_purple': '#e67e22',
            'glow_cyan': '#27ae60'
        }
    },
    {
        'name': 'Deep Space',
        'colors': {
            'accent_primary': '#34495e',
            'accent_secondary': '#2c3e50',
            'glow_blue': '#34495e',
            'glow_purple': '#7f8c8d',
            'glow_cyan': '#95a5a6'
        }
    }
]

# ========================================
# CSS STYLESHEET WITH GLOWING EFFECTS
# ========================================
def get_stylesheet(theme: str, accent_color: Optional[str] = None, glow_intensity: int = 50) -> str:
    """Generate QT-compatible stylesheet"""
    
    if theme == 'Light':
        colors = LIGHT_THEME
    else:
        colors = DARK_THEME.copy()
        if accent_color:
            colors['accent_primary'] = accent_color
    
    glow_factor = glow_intensity / 50.0
    
    return f"""
/* Global Styles */
QMainWindow, QDialog {{
    background: {colors['background_dark']};
}}

QWidget {{
    color: {colors['text_primary']};
    font-family: 'Segoe UI', 'Arial', sans-serif;
}}

/* Glowing Labels */
QLabel {{
    color: {colors['text_primary']};
    background: transparent;
}}

QLabel[glow="true"] {{
    color: {colors['accent_primary']};
    font-weight: bold;
}}

/* Main Title Glowing Effect */
#appTitle {{
    font-size: 36px;
    font-weight: 800;
    color: {colors['text_primary']};
}}

/* Buttons with Hover Effects */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['background_light']},
        stop:1 {colors['background_medium']});
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
    min-height: 30px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['background_light']},
        stop:1 {colors['background_dark']});
    border: 2px solid {colors['accent_primary']};
}}

QPushButton:pressed {{
    background: {colors['background_dark']};
    border: 2px solid {colors['accent_secondary']};
}}

QPushButton:disabled {{
    background: {colors['background_medium']};
    color: {colors['text_secondary']};
    border-color: {colors['border']};
}}

/* Primary Action Button */
QPushButton[type="primary"] {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['accent_primary']},
        stop:1 {colors['accent_secondary']});
    color: white;
    font-weight: bold;
    border: none;
}}

QPushButton[type="primary"]:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['accent_secondary']},
        stop:1 {colors['accent_primary']});
}}

/* Success Button */
QPushButton[type="success"] {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['success']},
        stop:1 #27ae60);
    color: white;
    border: none;
}}

QPushButton[type="success"]:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #27ae60,
        stop:1 {colors['success']});
}}

/* Warning Button */
QPushButton[type="warning"] {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['warning']},
        stop:1 #e67e22);
    color: white;
    border: none;
}}

QPushButton[type="warning"]:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #e67e22,
        stop:1 {colors['warning']});
}}

/* Danger Button */
QPushButton[type="danger"] {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['error']},
        stop:1 #c0392b);
    color: white;
    border: none;
}}

QPushButton[type="danger"]:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #c0392b,
        stop:1 {colors['error']});
}}

/* ComboBox */
QComboBox {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 6px 12px;
    min-height: 30px;
}}

QComboBox:hover {{
    border: 2px solid {colors['accent_primary']};
}}

QComboBox::drop-down {{
    border: none;
    background: transparent;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {colors['text_primary']};
    margin-right: 5px;
}}

QComboBox QAbstractItemView {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    selection-background-color: {colors['accent_primary']};
}}

/* LineEdit, TextEdit, SpinBox */
QLineEdit, QTextEdit, QSpinBox {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: {colors['accent_primary']};
}}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {{
    border: 2px solid {colors['accent_primary']};
}}

/* Progress Bar */
QProgressBar {{
    background: {colors['background_medium']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    text-align: center;
    color: {colors['text_primary']};
    font-weight: bold;
    height: 25px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors['accent_primary']},
        stop:0.5 {colors['accent_secondary']},
        stop:1 {colors['accent_tertiary']});
    border-radius: 7px;
}}

/* GroupBox */
QGroupBox {{
    font-weight: bold;
    border: 2px solid {colors['border']};
    border-radius: 10px;
    margin-top: 15px;
    padding-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 5px;
    color: {colors['accent_primary']};
}}

/* ScrollArea */
QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: {colors['background_medium']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors['accent_primary']},
        stop:1 {colors['accent_secondary']});
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors['accent_secondary']},
        stop:1 {colors['accent_primary']});
}}

QScrollBar:horizontal {{
    background: {colors['background_medium']};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors['accent_primary']},
        stop:1 {colors['accent_secondary']});
    border-radius: 6px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors['accent_secondary']},
        stop:1 {colors['accent_primary']});
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    border: none;
    background: none;
}}

/* Slider */
QSlider::groove:horizontal {{
    background: {colors['background_medium']};
    height: 8px;
    border-radius: 4px;
}}

QSlider::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors['accent_primary']},
        stop:1 {colors['accent_secondary']});
    width: 20px;
    height: 20px;
    margin: -6px 0;
    border-radius: 10px;
    border: 2px solid {colors['text_primary']};
}}

QSlider::handle:horizontal:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors['accent_secondary']},
        stop:1 {colors['accent_primary']});
    transform: scale(1.2);
}}

QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors['accent_primary']},
        stop:1 {colors['accent_secondary']});
    border-radius: 4px;
}}

/* Tab Widget */
QTabWidget::pane {{
    background: transparent;
    border: 1px solid {colors['border']};
    border-radius: 8px;
}}

QTabBar::tab {{
    background: {colors['background_medium']};
    color: {colors['text_secondary']};
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}

QTabBar::tab:selected {{
    background: {colors['background_light']};
    color: {colors['accent_primary']};
    border-bottom: 2px solid {colors['accent_primary']};
    font-weight: bold;
}}

QTabBar::tab:hover {{
    background: {colors['hover']};
    color: {colors['text_primary']};
}}

/* Menu */
QMenu {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
}}

QMenu::item {{
    padding: 6px 25px;
    border-radius: 3px;
}}

QMenu::item:selected {{
    background: {colors['accent_primary']};
    color: white;
}}

QMenu::separator {{
    height: 1px;
    background: {colors['border']};
    margin: 5px 10px;
}}

/* ToolTip */
QToolTip {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['accent_primary']};
    border-radius: 4px;
    padding: 4px 8px;
}}

/* Status Bar */
QStatusBar {{
    background: {colors['background_dark']};
    color: {colors['text_secondary']};
    border-top: 1px solid {colors['border']};
}}

QStatusBar::item {{
    border: none;
}}

/* Message Box */
QMessageBox {{
    background: {colors['background_medium']};
}}

QMessageBox QLabel {{
    color: {colors['text_primary']};
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}

/* CheckBox */
QCheckBox {{
    color: {colors['text_primary']};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    background: {colors['background_medium']};
    border: 1px solid {colors['border']};
    border-radius: 3px;
}}

QCheckBox::indicator:checked {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['accent_primary']},
        stop:1 {colors['accent_secondary']});
    border-color: {colors['accent_primary']};
}}

QCheckBox::indicator:hover {{
    border: 2px solid {colors['accent_primary']};
}}

/* RadioButton */
QRadioButton {{
    color: {colors['text_primary']};
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    background: {colors['background_medium']};
    border: 1px solid {colors['border']};
    border-radius: 9px;
}}

QRadioButton::indicator:checked {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['accent_primary']},
        stop:1 {colors['accent_secondary']});
    border: 1px solid {colors['accent_primary']};
}}

QRadioButton::indicator:checked::after {{
    content: "";
    display: block;
    width: 8px;
    height: 8px;
    background: white;
    border-radius: 4px;
    margin: 4px;
}}

QRadioButton::indicator:hover {{
    border: 2px solid {colors['accent_primary']};
}}

/* Frame */
QFrame {{
    background: transparent;
}}

QFrame[frameShape="4"] {{
    border: 1px solid {colors['border']};
    border-radius: 8px;
    background: {colors['background_medium']};
}}

/* List Widget */
QListWidget {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 5px;
}}

QListWidget::item {{
    padding: 8px;
    border-radius: 4px;
}}

QListWidget::item:selected {{
    background: {colors['accent_primary']};
}}

QListWidget::item:hover {{
    background: {colors['hover']};
}}

/* Table Widget */
QTableWidget {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    gridline-color: {colors['border']};
}}

QTableWidget::item {{
    padding: 5px;
}}

QTableWidget::item:selected {{
    background: {colors['accent_primary']};
}}

QHeaderView::section {{
    background: {colors['background_light']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    padding: 5px;
}}

/* Tree Widget */
QTreeWidget {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
}}

QTreeWidget::item {{
    padding: 5px;
}}

QTreeWidget::item:selected {{
    background: {colors['accent_primary']};
}}

QTreeWidget::item:hover {{
    background: {colors['hover']};
}}

QTreeWidget::branch {{
    background: transparent;
}}

QTreeWidget::branch:selected {{
    background: {colors['accent_primary']};
}}

/* Splitter */
QSplitter::handle {{
    background: {colors['border']};
    height: 2px;
}}

QSplitter::handle:horizontal {{
    width: 2px;
}}

QSplitter::handle:vertical {{
    height: 2px;
}}

QSplitter::handle:hover {{
    background: {colors['accent_primary']};
}}

/* Dock Widget */
QDockWidget {{
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
}}

QDockWidget::title {{
    background: {colors['background_light']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    padding: 5px;
}}

QDockWidget::close-button, QDockWidget::float-button {{
    background: transparent;
    border: none;
}}

QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
    background: {colors['hover']};
}}

/* Toolbar */
QToolBar {{
    background: {colors['background_light']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    spacing: 5px;
}}

QToolBar QToolButton {{
    background: transparent;
    border: none;
    border-radius: 4px;
    padding: 5px;
}}

QToolBar QToolButton:hover {{
    background: {colors['hover']};
}}

QToolBar QToolButton:pressed {{
    background: {colors['accent_primary']};
}}

/* Menu Bar */
QMenuBar {{
    background: {colors['background_dark']};
    color: {colors['text_primary']};
    border-bottom: 1px solid {colors['border']};
}}

QMenuBar::item {{
    padding: 5px 10px;
    border-radius: 4px;
}}

QMenuBar::item:selected {{
    background: {colors['hover']};
}}

QMenuBar::item:pressed {{
    background: {colors['accent_primary']};
}}

/* Scroll Area */
QScrollArea {{
    border: none;
    background: transparent;
}}

/* Graphics View */
QGraphicsView {{
    background: {colors['background_dark']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
}}

/* Calendar */
QCalendarWidget QWidget {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
}}

QCalendarWidget QTableView {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
}}

QCalendarWidget QTableView::item:selected {{
    background: {colors['accent_primary']};
}}

QCalendarWidget QAbstractItemView:enabled {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
}}

/* Spin Box */
QSpinBox {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 4px;
}}

QSpinBox:hover {{
    border: 2px solid {colors['accent_primary']};
}}

QSpinBox::up-button, QSpinBox::down-button {{
    background: {colors['background_light']};
    border: 1px solid {colors['border']};
    border-radius: 3px;
    width: 16px;
}}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background: {colors['hover']};
}}

QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {{
    background: {colors['accent_primary']};
}}

/* DateTime Edit */
QDateTimeEdit {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 4px;
}}

QDateTimeEdit:hover {{
    border: 2px solid {colors['accent_primary']};
}}

QDateTimeEdit::up-button, QDateTimeEdit::down-button {{
    background: {colors['background_light']};
    border: 1px solid {colors['border']};
    border-radius: 3px;
    width: 16px;
}}

QDateTimeEdit::up-button:hover, QDateTimeEdit::down-button:hover {{
    background: {colors['hover']};
}}

QDateTimeEdit::up-button:pressed, QDateTimeEdit::down-button:pressed {{
    background: {colors['accent_primary']};
}}

/* Dial */
QDial {{
    background: {colors['background_medium']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 50%;
}}

QDial::handle {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['accent_primary']},
        stop:1 {colors['accent_secondary']});
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: 2px solid {colors['text_primary']};
}}

QDial::handle:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors['accent_secondary']},
        stop:1 {colors['accent_primary']});
}}

/* LCD Number */
QLCDNumber {{
    color: {colors['accent_primary']};
    background: {colors['background_dark']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
}}

/* Rubber Band */
QRubberBand {{
    border: 2px solid {colors['accent_primary']};
    background: rgba(74, 144, 226, 0.2);
}}

/* Print Dialog */
QPrintDialog {{
    background: {colors['background_medium']};
}}

QPrintDialog QPushButton {{
    min-width: 80px;
}}

/* Wizard */
QWizard {{
    background: {colors['background_dark']};
}}

QWizard QWizardPage {{
    background: {colors['background_medium']};
}}

QWizard QPushButton {{
    min-width: 80px;
}}

/* Error Message */
QErrorMessage {{
    background: {colors['background_medium']};
}}

QErrorMessage QTextEdit {{
    background: {colors['background_light']};
    color: {colors['text_primary']};
    border: 1px solid {colors['error']};
    border-radius: 4px;
}}

/* Progress Dialog */
QProgressDialog {{
    background: {colors['background_medium']};
}}

QProgressDialog QLabel {{
    color: {colors['text_primary']};
}}

QProgressDialog QPushButton {{
    min-width: 80px;
}}

/* Input Dialog */
QInputDialog {{
    background: {colors['background_medium']};
}}

QInputDialog QLabel {{
    color: {colors['text_primary']};
}}

QInputDialog QLineEdit {{
    background: {colors['background_light']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 4px;
    padding: 4px;
}}

QInputDialog QPushButton {{
    min-width: 80px;
}}

/* Font Dialog */
QFontDialog {{
    background: {colors['background_medium']};
}}

QFontDialog QListView {{
    background: {colors['background_light']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 4px;
}}

QFontDialog QPushButton {{
    min-width: 80px;
}}

/* Color Dialog */
QColorDialog {{
    background: {colors['background_medium']};
}}

QColorDialog QPushButton {{
    min-width: 80px;
}}

/* File Dialog */
QFileDialog {{
    background: {colors['background_medium']};
}}

QFileDialog QListView {{
    background: {colors['background_light']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 4px;
}}

QFileDialog QTreeView {{
    background: {colors['background_light']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 4px;
}}

QFileDialog QPushButton {{
    min-width: 80px;
}}

/* Animation for widgets */
QPushButton, QComboBox, QSpinBox, QCheckBox, QRadioButton {{
    transition: all 0.2s ease-in-out;
}}

QPushButton:hover, QComboBox:hover, QSpinBox:hover {{
    transform: scale(1.02);
}}

QPushButton:pressed {{
    transform: scale(0.98);
}}

/* Custom scrollbar for all widgets */
QWidget {{
    scrollbar-width: thin;
    scrollbar-color: {colors['accent_primary']} {colors['background_medium']};
}}

QWidget::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

QWidget::-webkit-scrollbar-track {{
    background: {colors['background_medium']};
    border-radius: 4px;
}}

QWidget::-webkit-scrollbar-thumb {{
    background: {colors['accent_primary']};
    border-radius: 4px;
}}

QWidget::-webkit-scrollbar-thumb:hover {{
    background: {colors['accent_secondary']};
}}

QWidget::-webkit-scrollbar-corner {{
    background: {colors['background_dark']};
}}
"""

# ========================================
# ANIMATED BUTTON CLASS
# ========================================
class GlowButton(QPushButton):
    """Custom animated button with glow effects"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self._glow_animation = QPropertyAnimation(self, b"windowOpacity")
        self._glow_animation.setDuration(1000)
        self._glow_animation.setKeyValueAt(0, 1.0)
        self._glow_animation.setKeyValueAt(0.5, 0.9)
        self._glow_animation.setKeyValueAt(1, 1.0)
        self._glow_animation.setLoopCount(-1)
        
        self._scale_animation = QPropertyAnimation(self, b"geometry")
        self._scale_animation.setDuration(300)
        self._scale_animation.setEasingCurve(QEasingCurve.OutBack)
        
        self.installEventFilter(self)
        
        # Shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 2)
        self.setGraphicsEffect(self.shadow)
        
    def eventFilter(self, obj, event):
        if event.type() == event.Enter:
            self.animate_hover(True)
            self._glow_animation.start()
            self.shadow.setBlurRadius(20)
            self.shadow.setColor(QColor(74, 144, 226, 120))
        elif event.type() == event.Leave:
            self.animate_hover(False)
            self._glow_animation.stop()
            self.setWindowOpacity(1.0)
            self.shadow.setBlurRadius(10)
            self.shadow.setColor(QColor(0, 0, 0, 80))
        return super().eventFilter(obj, event)
    
    def animate_hover(self, entering: bool):
        """Animate button on hover"""
        if entering:
            geom = self.geometry()
            self._animation.setStartValue(geom)
            self._animation.setEndValue(geom.adjusted(-2, -2, 2, 2))
            self._animation.start()
        else:
            geom = self.geometry()
            self._animation.setStartValue(geom)
            self._animation.setEndValue(geom.adjusted(2, 2, -2, -2))
            self._animation.start()
            
    def animate_press(self):
        """Animate button on press"""
        geom = self.geometry()
        self._scale_animation.setStartValue(geom)
        self._scale_animation.setEndValue(geom.adjusted(4, 4, -4, -4))
        self._scale_animation.start()
        
    def mousePressEvent(self, event):
        self.animate_press()
        super().mousePressEvent(event)

# ========================================
# GLOWING LABEL CLASS
# ========================================
class GlowLabel(QLabel):
    """Label with glowing text effect using painter"""
    
    def __init__(self, text: str = "", parent=None, glow_color: Optional[str] = None):
        super().__init__(text, parent)
        self.glow_color = glow_color or DARK_THEME['accent_primary']
        self.glow_intensity = 50
        self._glow_animation = QPropertyAnimation(self, b"windowOpacity")
        self._glow_animation.setDuration(2000)
        self._glow_animation.setKeyValueAt(0, 1.0)
        self._glow_animation.setKeyValueAt(0.5, 0.9)
        self._glow_animation.setKeyValueAt(1, 1.0)
        self._glow_animation.setLoopCount(-1)
        
        # Shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor(self.glow_color))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
    def setGlowIntensity(self, intensity: int):
        """Set glow intensity (0-100)"""
        self.glow_intensity = intensity
        self.shadow.setBlurRadius(intensity / 5)
        self.update()
        
    def setGlowColor(self, color: str):
        """Set glow color"""
        self.glow_color = color
        self.shadow.setColor(QColor(color))
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient for text
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(DARK_THEME['accent_primary']))
        gradient.setColorAt(0.5, QColor(DARK_THEME['accent_secondary']))
        gradient.setColorAt(1, QColor(DARK_THEME['accent_tertiary']))
        
        # Set font
        font = self.font()
        font.setPointSize(font.pointSize() + 4)
        font.setBold(True)
        painter.setFont(font)
        
        # Draw glow effect (multiple layers for glow)
        glow_alpha = int(100 * (self.glow_intensity / 100.0))
        for i in range(3):
            painter.setPen(QPen(QColor(self.glow_color).lighter(150 - i*20), 1))
            painter.drawText(self.rect().translated(i+1, i+1), self.alignment(), self.text())
        
        # Draw main text with gradient
        painter.setPen(QPen(gradient, 2))
        painter.drawText(self.rect(), self.alignment(), self.text())

# ========================================
# GLASS CARD WIDGET
# ========================================
class GlassCardWidget(QFrame):
    """Modern glass-morphism card widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(f"""
            GlassCardWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(30, 30, 30, 0.8),
                    stop:1 rgba(20, 20, 20, 0.9));
                border: 1px solid {DARK_THEME['border']};
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        
        self._hover_animation = QPropertyAnimation(self, b"geometry")
        self._hover_animation.setDuration(300)
        self._hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 50))
        self.shadow.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow)
        
    def enterEvent(self, event):
        geom = self.geometry()
        self._hover_animation.setStartValue(geom)
        self._hover_animation.setEndValue(geom.adjusted(-5, -5, 5, 5))
        self._hover_animation.start()
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(QColor(74, 144, 226, 30))
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        geom = self.geometry()
        self._hover_animation.setStartValue(geom)
        self._hover_animation.setEndValue(geom.adjusted(5, 5, -5, -5))
        self._hover_animation.start()
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 50))
        super().leaveEvent(event)

# ========================================
# PREVIEW WIDGET
# ========================================
class PreviewWidget(QFrame):
    """Comprehensive preview widget for media and subtitles"""
    
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
        
        # Video display area
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
        
        # Video widget (if available)
        self.video_widget = QVideoWidget()
        self.video_widget.hide()
        video_layout.addWidget(self.video_widget)
        
        layout.addWidget(self.video_container, stretch=1)
        
        # Subtitle preview
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
        
        # Control bar
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
        
        # Media player
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.stateChanged.connect(self.update_play_state)
        
        self.duration = 0
        self.muted = False
        
    def set_media(self, file_path: str):
        """Set media file for playback"""
        if os.path.exists(file_path):
            url = QUrl.fromLocalFile(file_path)
            self.player.setMedia(QMediaContent(url))
            
            # Check if video
            if file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                self.video_widget.show()
                self.video_label.hide()
            else:
                self.video_widget.hide()
                self.video_label.show()
                self.video_label.setText(f"Audio: {os.path.basename(file_path)}")
                
            self.player.play()
            
    def set_subtitles(self, subtitles: List[dict]):
        """Set subtitles for preview"""
        self.subtitles = subtitles
        
    def update_position(self, position: int):
        """Update position slider and subtitle display"""
        self.position_slider.setValue(position)
        
        # Update time label
        current = self.format_time(position)
        total = self.format_time(self.duration)
        self.time_label.setText(f"{current}/{total}")
        self.preview_timer.setText(f"{current} / {total}")
        
        # Update subtitle display
        if hasattr(self, 'subtitles') and self.subtitles:
            sec = position / 1000.0
            for sub in self.subtitles:
                start = sub["start"].total_seconds() if isinstance(sub["start"], timedelta) else sub["start"]
                end = sub["end"].total_seconds() if isinstance(sub["end"], timedelta) else sub["end"]
                if start <= sec <= end:
                    self.subtitle_display.setText(sub["text"])
                    break
                    
    def update_duration(self, duration: int):
        """Update duration slider"""
        self.duration = duration
        self.position_slider.setRange(0, duration)
        
    def update_play_state(self, state):
        """Update play button based on state"""
        if state == QMediaPlayer.PlayingState:
            self.play_btn.setText("⏸")
        else:
            self.play_btn.setText("▶")
            
    def toggle_playback(self):
        """Toggle play/pause"""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
            
    def seek_position(self, position: int):
        """Seek to position"""
        self.player.setPosition(position)
        
    def toggle_mute(self):
        """Toggle mute"""
        self.muted = not self.muted
        self.player.setMuted(self.muted)
        self.volume_btn.setText("🔇" if self.muted else "🔊")
        
    def change_volume(self, value: int):
        """Change volume"""
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
        """Format time in milliseconds to MM:SS"""
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

# ========================================
# MAIN APPLICATION WINDOW
# ========================================
class NotyCaptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load settings
        self.settings = load_settings()

        # Set language
        _translator.set_language(self.settings.get('language', 'en'))

        # Setup animation controller
        animation_controller.set_enabled(self.settings.get('enable_animations', True))
        animation_controller.set_speed(self.settings.get('animation_speed', 'normal'))

        # Basic window setup
        self.setWindowTitle(tr('window_title'))
        self.setMinimumSize(1024, 768)

        # Restore saved size
        saved_width = self.settings.get("window_width", 1280)
        saved_height = self.settings.get("window_height", 800)
        self.resize(saved_width, saved_height)

        if self.settings.get("window_maximized", False):
            self.showMaximized()

        # Apply appearance
        self.apply_ui_scale()
        self.apply_theme()

        self.center_window()

        if self.settings.get("window_geometry"):
            self.restoreGeometry(QByteArray.fromHex(self.settings["window_geometry"].encode()))
        if self.settings.get("window_state"):
            self.restoreState(QByteArray.fromHex(self.settings["window_state"].encode()))

        # Window icon
        icon_path = resource_path('App.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            logger.info("App icon set")

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Status bar
        self.statusBar().showMessage(tr('ready'))

        # System tray
        self.create_tray_icon()

        # Monitor manager
        self.monitor_manager = MonitorManager()

        # Hardware monitor
        self.hardware_monitor = hardware_monitor
        self.hardware_monitor.start_monitoring(self.settings.get('monitoring_interval', 1000))

        # Initialize state
        self.initialize_state()

        # Create menu bar
        self.create_menu_bar()

        # Create tool bar
        self.create_tool_bar()

        # Create main splitter
        self.create_main_splitter()

        # Create dock widgets
        self.create_dock_widgets()

        # Online handler
        self.online_handler = OnlineHandler(self)

        # Threads
        self.enhancer_thread = None
        self.model_download_thread = None
        self.progress_whisper = None

        # Player timer
        self.player_timer = QTimer(self)
        self.player_timer.timeout.connect(self.update_timeline)
        self.player_timer.start(50)

        # Flags
        self._closing = False
        self._cancel_lock = threading.Lock()
        self._operation_in_progress = False
        self._current_notebook_url = None
        self._monitor_windows = []

        # Force cancel timer
        self._force_cancel_timer = QTimer(self)
        self._force_cancel_timer.setSingleShot(True)
        self._force_cancel_timer.timeout.connect(self.show_force_cancel_option)

        # Load Google credentials
        self.load_existing_credentials()

        # Keyboard shortcuts
        self.setup_shortcuts()

        # Tooltips
        self.setup_tooltips()

        # Overlays
        self.create_overlays()

        # Restore session
        self.restore_session()

        # Start auto-save timer
        if self.settings.get('auto_save', True):
            self.auto_save_timer = QTimer()
            self.auto_save_timer.timeout.connect(self.auto_save)
            self.auto_save_timer.start(self.settings.get('auto_save_interval', 300) * 1000)

        logger.info("Main window fully initialized")

    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()

        # File menu
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
        
        save_session_action = QAction('💾 &Save Session', self)
        save_session_action.setShortcut('Ctrl+S')
        save_session_action.triggered.connect(self.save_session)
        file_menu.addAction(save_session_action)
        
        load_session_action = QAction('📂 &Load Session', self)
        load_session_action.setShortcut('Ctrl+L')
        load_session_action.triggered.connect(self.load_session)
        file_menu.addAction(load_session_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('🚪 E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        
        undo_action = QAction('↩ &Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('↪ &Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
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
        
        edit_menu.addSeparator()
        
        select_all_action = QAction('🔍 Select &All', self)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.triggered.connect(self.select_all)
        edit_menu.addAction(select_all_action)

        # View menu
        view_menu = menubar.addMenu('&View')
        
        hardware_monitor_action = QAction('🖥️ &Hardware Monitor', self)
        hardware_monitor_action.setCheckable(True)
        hardware_monitor_action.setChecked(True)
        hardware_monitor_action.triggered.connect(self.toggle_hardware_monitor)
        view_menu.addAction(hardware_monitor_action)
        
        performance_graph_action = QAction('📈 &Performance Graph', self)
        performance_graph_action.setCheckable(True)
        performance_graph_action.setChecked(True)
        performance_graph_action.triggered.connect(self.toggle_performance_graph)
        view_menu.addAction(performance_graph_action)
        
        preview_widget_action = QAction('👁️ &Preview Widget', self)
        preview_widget_action.setCheckable(True)
        preview_widget_action.setChecked(True)
        preview_widget_action.triggered.connect(self.toggle_preview_widget)
        view_menu.addAction(preview_widget_action)
        
        view_menu.addSeparator()
        
        fullscreen_action = QAction('🖥️ &Full Screen', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        # Monitor menu
        monitor_menu = menubar.addMenu('🖥️ &Monitors')
        
        for i, monitor in enumerate(self.monitor_manager.monitors):
            monitor_action = QAction(f"Monitor {i+1}", self)
            monitor_action.triggered.connect(lambda checked, idx=i: self.move_to_monitor(idx))
            monitor_menu.addAction(monitor_action)
            
        monitor_menu.addSeparator()
        
        new_window_action = QAction('🆕 &New Window', self)
        new_window_action.triggered.connect(self.create_monitor_window)
        monitor_menu.addAction(new_window_action)

        # Tools menu
        tools_menu = menubar.addMenu('🛠️ &Tools')
        
        settings_action = QAction('⚙️ &Settings', self)
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.open_settings_dialog)
        tools_menu.addAction(settings_action)
        
        workspace_action = QAction('🎨 &Workspace Customizer', self)
        workspace_action.setShortcut('Ctrl+W')
        workspace_action.triggered.connect(self.open_workspace_dialog)
        tools_menu.addAction(workspace_action)
        
        tools_menu.addSeparator()
        
        download_model_action = QAction('📥 &Download Model', self)
        download_model_action.triggered.connect(self.open_model_download_dialog)
        tools_menu.addAction(download_model_action)
        
        google_login_action = QAction('🔐 &Google Login', self)
        google_login_action.setShortcut('Ctrl+G')
        google_login_action.triggered.connect(self.initiate_google_login)
        tools_menu.addAction(google_login_action)

        # Help menu
        help_menu = menubar.addMenu('❓ &Help')
        
        documentation_action = QAction('📚 &Documentation', self)
        documentation_action.triggered.connect(self.open_documentation)
        help_menu.addAction(documentation_action)
        
        about_action = QAction('ℹ️ &About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def create_tool_bar(self):
        """Create main toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)

        # Import
        import_action = QAction(QIcon(resource_path('icons/import.png')), 'Import', self)
        import_action.triggered.connect(self.import_media_file)
        toolbar.addAction(import_action)

        # Generate
        generate_action = QAction(QIcon(resource_path('icons/generate.png')), 'Generate', self)
        generate_action.triggered.connect(self.start_caption_generation)
        toolbar.addAction(generate_action)

        # Enhance
        enhance_action = QAction(QIcon(resource_path('icons/enhance.png')), 'Enhance', self)
        enhance_action.triggered.connect(self.enhance_audio_vocals)
        toolbar.addAction(enhance_action)

        toolbar.addSeparator()

        # Play
        play_action = QAction(QIcon(resource_path('icons/play.png')), 'Play', self)
        play_action.triggered.connect(self.toggle_media_playback)
        toolbar.addAction(play_action)

        # Stop
        stop_action = QAction(QIcon(resource_path('icons/stop.png')), 'Stop', self)
        stop_action.triggered.connect(self.stop_playback)
        toolbar.addAction(stop_action)

        toolbar.addSeparator()

        # Settings
        settings_action = QAction(QIcon(resource_path('icons/settings.png')), 'Settings', self)
        settings_action.triggered.connect(self.open_settings_dialog)
        toolbar.addAction(settings_action)

        # Hardware
        hardware_action = QAction(QIcon(resource_path('icons/hardware.png')), 'Hardware', self)
        hardware_action.triggered.connect(self.toggle_hardware_monitor)
        toolbar.addAction(hardware_action)

    def create_main_splitter(self):
        """Create main splitter with left and right panels"""
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.main_splitter)

        # Left panel - Caption editor
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        self.main_splitter.addWidget(self.left_panel)

        # App title
        title_container = QFrame()
        title_layout = QVBoxLayout(title_container)
        
        app_title = QLabel(tr('app_name'))
        app_title.setObjectName("appTitle")
        app_title.setAlignment(Qt.AlignCenter)
        app_title.setStyleSheet(f"""
            QLabel {{
                color: {DARK_THEME['text_primary']};
                font-size: 36px;
                font-weight: 800;
                font-family: '{self.settings.get('font_family', 'Segoe UI')}';
            }}
        """)
        title_layout.addWidget(app_title)
        
        app_subtitle = QLabel(tr('app_subtitle'))
        app_subtitle.setAlignment(Qt.AlignCenter)
        app_subtitle.setStyleSheet(f"color: {DARK_THEME['text_secondary']}; font-size: 14px; margin-top: -10px;")
        title_layout.addWidget(app_subtitle)
        
        self.left_layout.addWidget(title_container)

        # Caption editor
        self.caption_edit = QTextEdit()
        self.caption_edit.setReadOnly(True)
        self.caption_edit.setFont(QFont(self.settings.get('font_family', 'Consolas'), 12))
        self.caption_edit.setPlaceholderText("Captions will appear here after generation...")
        self.left_layout.addWidget(self.caption_edit, stretch=1)

        # Button row
        btn_row = QHBoxLayout()
        
        self.edit_btn = GlowButton(tr('edit_captions'))
        self.edit_btn.setMinimumHeight(50)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.edit_btn.setEnabled(False)
        btn_row.addWidget(self.edit_btn)

        self.workspace_btn = GlowButton(tr('workspace'))
        self.workspace_btn.setMinimumHeight(50)
        self.workspace_btn.clicked.connect(self.open_workspace_dialog)
        btn_row.addWidget(self.workspace_btn)

        self.settings_btn = GlowButton(tr('settings'))
        self.settings_btn.setMinimumHeight(50)
        self.settings_btn.clicked.connect(self.open_settings_dialog)
        btn_row.addWidget(self.settings_btn)

        self.download_btn = GlowButton(tr('download_model'))
        self.download_btn.setMinimumHeight(50)
        self.download_btn.clicked.connect(self.open_model_download_dialog)
        btn_row.addWidget(self.download_btn)

        self.left_layout.addLayout(btn_row)

        # Right panel - Controls
        self.right_scroll = QScrollArea()
        self.right_scroll.setWidgetResizable(True)
        self.right_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.main_splitter.addWidget(self.right_scroll)

        self.right_panel = QWidget()
        self.right_panel.setStyleSheet("background: transparent;")
        self.right_layout = QVBoxLayout()
        self.right_panel.setLayout(self.right_layout)
        self.right_scroll.setWidget(self.right_panel)

        # Google Login
        self.login_button = GlowButton(tr('login_google'))
        self.login_button.setMinimumHeight(60)
        self.login_button.clicked.connect(self.initiate_google_login)
        self.right_layout.addWidget(self.login_button)

        # Processing Mode
        mode_card = GlassCardWidget()
        mode_layout = QVBoxLayout(mode_card)
        
        mode_label = QLabel(tr('processing_mode'))
        mode_label.setStyleSheet(f"color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])}; font-size: 14px; font-weight: bold;")
        mode_layout.addWidget(mode_label)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([tr('normal_mode'), tr('online_mode')])
        self.mode_combo.setMinimumHeight(40)
        self.mode_combo.currentTextChanged.connect(self.on_mode_change)
        mode_layout.addWidget(self.mode_combo)
        
        self.right_layout.addWidget(mode_card)

        # Language Selection
        lang_card = GlassCardWidget()
        lang_layout = QVBoxLayout(lang_card)
        
        lang_label = QLabel(tr('language'))
        lang_label.setStyleSheet(f"color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])}; font-size: 14px; font-weight: bold;")
        lang_layout.addWidget(lang_label)
        
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
        self.lang_combo.setMinimumHeight(40)
        self.lang_combo.setCurrentText(self.settings.get("default_lang", tr('english_transcribe')))
        lang_layout.addWidget(self.lang_combo)
        
        self.right_layout.addWidget(lang_card)

        # Words per Line
        wpl_card = GlassCardWidget()
        wpl_layout = QVBoxLayout(wpl_card)
        
        wpl_label = QLabel(tr('words_per_line'))
        wpl_label.setStyleSheet(f"color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])}; font-size: 14px; font-weight: bold;")
        wpl_layout.addWidget(wpl_label)
        
        self.words_spin = QSpinBox()
        self.words_spin.setRange(1, 20)
        self.words_spin.setValue(self.settings.get("words_per_line", 5))
        self.words_spin.setMinimumHeight(40)
        wpl_layout.addWidget(self.words_spin)
        
        self.right_layout.addWidget(wpl_card)

        # Import Button
        self.import_btn = GlowButton(tr('import_media'))
        self.import_btn.setMinimumHeight(60)
        self.import_btn.clicked.connect(self.import_media_file)
        self.right_layout.addWidget(self.import_btn)

        # Output Format
        fmt_card = GlassCardWidget()
        fmt_layout = QVBoxLayout(fmt_card)
        
        fmt_label = QLabel(tr('output_format'))
        fmt_label.setStyleSheet(f"color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])}; font-size: 14px; font-weight: bold;")
        fmt_layout.addWidget(fmt_label)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems([tr('srt_format'), tr('ass_format')])
        self.format_combo.setMinimumHeight(40)
        self.format_combo.setCurrentText(self.settings.get("output_format", tr('srt_format')))
        fmt_layout.addWidget(self.format_combo)
        
        self.right_layout.addWidget(fmt_card)

        # Output Folder
        folder_card = GlassCardWidget()
        folder_layout = QVBoxLayout(folder_card)
        
        out_label = QLabel(tr('output_folder'))
        out_label.setStyleSheet(f"color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])}; font-size: 14px; font-weight: bold;")
        folder_layout.addWidget(out_label)
        
        self.out_folder_edit = QLineEdit()
        self.out_folder_edit.setReadOnly(True)
        self.out_folder_edit.setMinimumHeight(40)
        self.out_folder_edit.setPlaceholderText("Default: Source Folder")
        self.out_folder_edit.setText(self.settings.get("last_output_folder", ""))
        folder_layout.addWidget(self.out_folder_edit)
        
        browse_btn = GlowButton(tr('browse_output'))
        browse_btn.setMinimumHeight(40)
        browse_btn.clicked.connect(self.browse_output_folder)
        folder_layout.addWidget(browse_btn)
        
        self.right_layout.addWidget(folder_card)

        # Enhance Button
        self.enhance_btn = GlowButton(tr('enhance_audio'))
        self.enhance_btn.setMinimumHeight(60)
        self.enhance_btn.clicked.connect(self.enhance_audio_vocals)
        self.enhance_btn.setEnabled(False)
        self.right_layout.addWidget(self.enhance_btn)

        # Status display
        status_card = GlassCardWidget()
        status_layout = QVBoxLayout(status_card)
        
        status_row = QHBoxLayout()
        status_label = QLabel(tr('status'))
        status_label.setStyleSheet(f"color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])}; font-size: 13px; font-weight: bold;")
        status_row.addWidget(status_label)
        
        self.status_value = QLabel(tr('idle'))
        self.status_value.setStyleSheet(f"color: {DARK_THEME['success']}; font-size: 13px; font-weight: bold;")
        status_row.addWidget(self.status_value)
        status_row.addStretch()
        status_layout.addLayout(status_row)
        
        self.right_layout.addWidget(status_card)
        
        self.right_layout.addStretch()
        
        logger.info("Main panels setup complete")

    def create_dock_widgets(self):
        """Create dockable widgets"""
        # Hardware Monitor Dock
        self.hardware_dock = QDockWidget(tr('hardware_monitor'), self)
        self.hardware_dock.setObjectName("HardwareMonitor")
        self.hardware_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.hardware_monitor_widget = HardwareMonitorWidget()
        self.hardware_dock.setWidget(self.hardware_monitor_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.hardware_dock)

        # Performance Graph Dock
        self.performance_dock = QDockWidget(tr('performance'), self)
        self.performance_dock.setObjectName("PerformanceGraph")
        self.performance_dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
        
        self.performance_graph = PerformanceGraphWidget()
        self.performance_dock.setWidget(self.performance_graph)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.performance_dock)

        # Preview Widget Dock
        self.preview_dock = QDockWidget(tr('preview'), self)
        self.preview_dock.setObjectName("PreviewWidget")
        self.preview_dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
        
        self.preview_widget = PreviewWidget()
        self.preview_dock.setWidget(self.preview_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.preview_dock)

        # Tabify docks
        self.tabifyDockWidget(self.performance_dock, self.preview_dock)

        # View menu actions
        self.hardware_dock.toggleViewAction().setText(tr('hardware_monitor'))
        self.hardware_dock.toggleViewAction().setIcon(QIcon(resource_path('icons/hardware.png')))
        self.menuBar().actions()[2].menu().addAction(self.hardware_dock.toggleViewAction())

        self.performance_dock.toggleViewAction().setText(tr('performance'))
        self.performance_dock.toggleViewAction().setIcon(QIcon(resource_path('icons/performance.png')))
        self.menuBar().actions()[2].menu().addAction(self.performance_dock.toggleViewAction())

        self.preview_dock.toggleViewAction().setText(tr('preview'))
        self.preview_dock.toggleViewAction().setIcon(QIcon(resource_path('icons/preview.png')))
        self.menuBar().actions()[2].menu().addAction(self.preview_dock.toggleViewAction())

    def create_tray_icon(self):
        """Create system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = resource_path('App.ico')
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        
        tray_menu = QMenu()
        show_action = tray_menu.addAction(tr('show_window'))
        show_action.triggered.connect(self.show_window)
        
        hardware_action = tray_menu.addAction(tr('hardware_monitor'))
        hardware_action.triggered.connect(self.toggle_hardware_monitor)
        
        performance_action = tray_menu.addAction(tr('performance'))
        performance_action.triggered.connect(self.toggle_performance_graph)
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction(tr('quit'))
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()

    def show_window(self):
        self.show()
        self.activateWindow()
        self.raise_()

    def quit_app(self):
        self.close()

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+O"), self, self.import_media_file)
        QShortcut(QKeySequence("Ctrl+G"), self, self.start_caption_generation)
        QShortcut(QKeySequence("Ctrl+E"), self, self.enhance_audio_vocals)
        QShortcut(QKeySequence("Ctrl+S"), self, self.toggle_edit_mode)
        QShortcut(QKeySequence("Space"), self, self.toggle_media_playback)
        QShortcut(QKeySequence("Ctrl+P"), self, self.toggle_media_playback)
        QShortcut(QKeySequence("Ctrl+,"), self, self.open_settings_dialog)
        QShortcut(QKeySequence("Esc"), self, lambda: self.cancel_current_operation(with_confirmation=True))
        QShortcut(QKeySequence("Ctrl+L"), self, self.initiate_google_login)
        QShortcut(QKeySequence("F5"), self, self.refresh_hardware)
        QShortcut(QKeySequence("Ctrl+M"), self, self.toggle_hardware_monitor)
        QShortcut(QKeySequence("Ctrl+Shift+P"), self, self.toggle_performance_graph)
        QShortcut(QKeySequence("Ctrl+Shift+V"), self, self.toggle_preview_widget)
        QShortcut(QKeySequence("Ctrl+Tab"), self, self.cycle_dock_widgets)

    def setup_tooltips(self):
        if not self.settings.get("show_tooltips", True):
            return
            
        self.import_btn.setToolTip(tr('import_media') + " (Ctrl+O)")
        self.enhance_btn.setToolTip(tr('enhance_audio') + " (Ctrl+E)")
        self.gen_btn.setToolTip(tr('generate') + " (Ctrl+G)")
        self.play_btn.setToolTip(tr('play_pause') + " (Space)")
        self.edit_btn.setToolTip(tr('edit_captions') + " (Ctrl+S)")
        self.download_btn.setToolTip(tr('download_model'))
        self.login_button.setToolTip(tr('login_google') + " (Ctrl+L)")
        
        self.mode_combo.setToolTip(tr('processing_mode'))
        self.lang_combo.setToolTip(tr('language'))
        self.words_spin.setToolTip(tr('words_per_line'))
        self.format_combo.setToolTip(tr('output_format'))
        self.out_folder_edit.setToolTip(tr('output_folder'))

    def create_overlays(self):
        """Create overlay widgets"""
        # Main operation overlay
        self.overlay = QFrame(self.central_widget)
        self.overlay.setStyleSheet(f"""
            QFrame {{
                background: rgba(10, 10, 10, 0.95);
                border: none;
            }}
        """)
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.overlay.hide()

        self.overlay_layout = QVBoxLayout(self.overlay)
        self.overlay_layout.setAlignment(Qt.AlignCenter)

        self.progress_container = QFrame()
        self.progress_container.setStyleSheet(f"""
            QFrame {{
                background: {DARK_THEME['background_medium']};
                border: 2px solid {self.settings.get('accent_color', DARK_THEME['accent_primary'])};
                border-radius: 15px;
                padding: 30px;
                max-width: 500px;
            }}
        """)
        prog_lay = QVBoxLayout(self.progress_container)

        self.prog_title = QLabel(tr('processing'))
        self.prog_title.setAlignment(Qt.AlignCenter)
        self.prog_title.setStyleSheet(f"""
            QLabel {{
                color: {DARK_THEME['text_primary']};
                font-size: 24px;
                font-weight: bold;
                font-family: '{self.settings.get('font_family', 'Segoe UI')}';
                margin-bottom: 20px;
            }}
        """)
        prog_lay.addWidget(self.prog_title)

        self.prog_info = QLabel(tr('starting'))
        self.prog_info.setAlignment(Qt.AlignCenter)
        self.prog_info.setStyleSheet(f"color: {DARK_THEME['text_secondary']}; font-size: 14px; margin: 10px;")
        prog_lay.addWidget(self.prog_info)

        self.operation_progress = QProgressBar()
        self.operation_progress.setMinimum(0)
        self.operation_progress.setMaximum(100)
        prog_lay.addWidget(self.operation_progress)

        # Speed and ETA labels
        speed_layout = QHBoxLayout()
        self.speed_label = QLabel(f"{tr('speed')} --")
        self.speed_label.setStyleSheet(f"color: {DARK_THEME['text_secondary']}; font-size: 13px;")
        speed_layout.addWidget(self.speed_label)
        
        self.eta_label = QLabel(f"{tr('eta')} --")
        self.eta_label.setStyleSheet(f"color: {DARK_THEME['text_secondary']}; font-size: 13px;")
        speed_layout.addWidget(self.eta_label)
        speed_layout.addStretch()
        prog_lay.addLayout(speed_layout)

        # Colab link display (only shown during online mode)
        self.colab_link_container = QFrame()
        colab_link_layout = QHBoxLayout(self.colab_link_container)
        colab_link_layout.setContentsMargins(0, 10, 0, 0)
        
        colab_label = QLabel(tr('colab_link'))
        colab_label.setStyleSheet(f"color: {DARK_THEME['text_secondary']}; font-size: 12px;")
        colab_link_layout.addWidget(colab_label)
        
        self.colab_link = QLabel()
        self.colab_link.setOpenExternalLinks(True)
        self.colab_link.setWordWrap(True)
        self.colab_link.setStyleSheet(f"color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])}; font-size: 12px;")
        colab_link_layout.addWidget(self.colab_link, 1)
        
        prog_lay.addWidget(self.colab_link_container)
        self.colab_link_container.hide()

        # Cancel buttons
        self.overlay_cancel_btn = GlowButton(tr('cancel'))
        self.overlay_cancel_btn.setMinimumHeight(50)
        self.overlay_cancel_btn.setProperty('type', 'danger')
        self.overlay_cancel_btn.clicked.connect(lambda: self.cancel_current_operation(with_confirmation=self.settings.get("confirm_cancel", True)))
        prog_lay.addWidget(self.overlay_cancel_btn)

        self.overlay_force_cancel_btn = GlowButton(tr('force_cancel'))
        self.overlay_force_cancel_btn.setMinimumHeight(50)
        self.overlay_force_cancel_btn.setProperty('type', 'warning')
        self.overlay_force_cancel_btn.clicked.connect(self.force_cancel_operation)
        self.overlay_force_cancel_btn.hide()
        prog_lay.addWidget(self.overlay_force_cancel_btn)

        self.overlay_layout.addWidget(self.progress_container)

        # Download overlay
        self.download_overlay = QFrame(self.central_widget)
        self.download_overlay.setStyleSheet(f"""
            QFrame {{
                background: rgba(10, 10, 10, 0.95);
                border: none;
            }}
        """)
        self.download_overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.download_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
        self.download_overlay.hide()

        download_overlay_layout = QVBoxLayout(self.download_overlay)
        download_overlay_layout.setAlignment(Qt.AlignCenter)

        download_container = QFrame()
        download_container.setStyleSheet(f"""
            QFrame {{
                background: {DARK_THEME['background_medium']};
                border: 2px solid {self.settings.get('accent_color', DARK_THEME['accent_primary'])};
                border-radius: 15px;
                padding: 30px;
                max-width: 500px;
            }}
        """)
        download_lay = QVBoxLayout(download_container)

        download_title = QLabel(tr('downloading'))
        download_title.setAlignment(Qt.AlignCenter)
        download_title.setStyleSheet(f"""
            QLabel {{
                color: {DARK_THEME['text_primary']};
                font-size: 24px;
                font-weight: bold;
                font-family: '{self.settings.get('font_family', 'Segoe UI')}';
                margin-bottom: 20px;
            }}
        """)
        download_lay.addWidget(download_title)

        self.download_info = QLabel(tr('starting'))
        self.download_info.setAlignment(Qt.AlignCenter)
        self.download_info.setStyleSheet(f"color: {DARK_THEME['text_secondary']}; font-size: 14px; margin: 10px;")
        download_lay.addWidget(self.download_info)

        self.download_progress = QProgressBar()
        self.download_progress.setMinimum(0)
        self.download_progress.setMaximum(100)
        download_lay.addWidget(self.download_progress)

        # Download speed and ETA
        download_speed_layout = QHBoxLayout()
        self.download_speed_label = QLabel(f"{tr('speed')} --")
        self.download_speed_label.setStyleSheet(f"color: {DARK_THEME['text_secondary']}; font-size: 13px;")
        download_speed_layout.addWidget(self.download_speed_label)
        
        self.download_eta_label = QLabel(f"{tr('eta')} --")
        self.download_eta_label.setStyleSheet(f"color: {DARK_THEME['text_secondary']}; font-size: 13px;")
        download_speed_layout.addWidget(self.download_eta_label)
        download_speed_layout.addStretch()
        download_lay.addLayout(download_speed_layout)

        self.download_cancel_btn = GlowButton(tr('cancel'))
        self.download_cancel_btn.setMinimumHeight(50)
        self.download_cancel_btn.setProperty('type', 'danger')
        self.download_cancel_btn.clicked.connect(lambda: self.cancel_current_operation(with_confirmation=self.settings.get("confirm_cancel", True)))
        download_lay.addWidget(self.download_cancel_btn)
        
        self.download_force_cancel_btn = GlowButton(tr('force_cancel'))
        self.download_force_cancel_btn.setMinimumHeight(50)
        self.download_force_cancel_btn.setProperty('type', 'warning')
        self.download_force_cancel_btn.clicked.connect(self.force_cancel_operation)
        self.download_force_cancel_btn.hide()
        download_lay.addWidget(self.download_force_cancel_btn)

        download_overlay_layout.addWidget(download_container)

    def resizeEvent(self, event):
        if hasattr(self, 'overlay') and self.overlay.isVisible():
            self.overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
            self.overlay.raise_()
        if hasattr(self, 'download_overlay') and self.download_overlay.isVisible():
            self.download_overlay.setGeometry(0, 0, self.central_widget.width(), self.central_widget.height())
            self.download_overlay.raise_()
        super().resizeEvent(event)

    def closeEvent(self, event: QCloseEvent):
        if not self.isMaximized():
            self.settings["window_width"] = self.width()
            self.settings["window_height"] = self.height()
        self.settings["window_maximized"] = self.isMaximized()
        self.settings["window_geometry"] = self.saveGeometry().toHex().data().decode()
        self.settings["window_state"] = self.saveState().toHex().data().decode()
        save_settings(self.settings)

        if self.settings.get("minimize_to_tray", False) and not self._closing:
            self.hide()
            self.tray_icon.show()
            self.tray_icon.showMessage(
                APP_NAME,
                "Application minimized to system tray",
                QSystemTrayIcon.Information,
                2000
            )
            event.ignore()
            return

        if self._operation_in_progress or self.is_generating:
            reply = QMessageBox.question(
                self,
                "Operation in Progress",
                "An operation is currently in progress.\n\nAre you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return

        logger.info("App close event triggered")
        self._closing = True
        
        # Stop monitoring
        self.hardware_monitor.stop_monitoring()
        
        # Save monitoring history
        history_file = os.path.join(MONITORING_DIR, f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl")
        self.hardware_monitor.save_history(history_file)
        
        self.cleanup_before_exit()
        
        logger.info("=" * 80)
        logger.info("NotyCaption Pro Secure Shutdown")
        logger.info("=" * 80)
        event.accept()

    def cleanup_before_exit(self):
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

        if self.audio_file and self.audio_file.endswith(".temp.wav") and os.path.exists(self.audio_file):
            try:
                os.remove(self.audio_file)
                logger.info(f"Temp audio removed")
            except Exception as rm_err:
                logger.warning(f"Temp audio removal failed")

        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
                logger.info(f"Last temp WAV removed")
            except Exception as rm_err:
                logger.warning(f"Last temp removal failed")

        if hasattr(self, 'online_handler') and self.online_handler.service:
            self.online_handler.cleanup_drive()

        try:
            cleanup_corrupt_models(self.settings.get("models_dir", APP_DATA_DIR))
        except Exception as e:
            logger.warning(f"Failed to clean up models on exit: {e}")

    def restore_session(self):
        session = self.session_manager.load_session()
        if session and session.get('last_input_file'):
            last_file = session['last_input_file']
            if os.path.exists(last_file):
                self.import_media_file(last_file)
                logger.info(f"Restored last session with file")

    def initialize_state(self):
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
        
        if self.output_folder and os.path.exists(self.output_folder):
            self.out_folder_edit.setText(self.output_folder)
            
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
            logger.info(f"UI scaled to {scale*100}%")
        except Exception as scale_err:
            logger.warning(f"UI scale apply failed: {scale_err}")

    def apply_theme(self):
        theme = self.settings.get("theme", "Dark")
        
        if theme == "Light":
            self.setStyleSheet(get_stylesheet('Light', self.settings.get('accent_color'), self.settings.get('glow_intensity', 50)))
            logger.info("Light theme applied")
        elif theme == "System":
            self.setStyleSheet("")
            QApplication.setStyle(QStyleFactory.create('windows'))
            logger.info("System theme applied")
        else:
            self.setStyleSheet(get_stylesheet('Dark', self.settings.get('accent_color'), self.settings.get('glow_intensity', 50)))
            logger.info("Dark theme applied")

    def freeze_ui(self, freeze=True, message=tr('processing')):
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
            self.timeline,
            self.workspace_btn,
            self.settings_btn
        ]

        for w in widgets_to_disable:
            if hasattr(w, 'setEnabled'):
                w.setEnabled(not freeze)

        if freeze:
            self._operation_in_progress = True
            self.overlay.show()
            self.overlay.raise_()
            self.overlay_cancel_btn.setEnabled(True)
            self.overlay_cancel_btn.setFocus()
            self.overlay_force_cancel_btn.hide()
            self.prog_title.setText(message)
            self.prog_info.setText(tr('processing'))
            self.operation_progress.setValue(0)
            self.statusBar().showMessage(message, 0)
            self.show_cancel_only(True)
            
            # Show colab link if in online mode
            if self.mode == "online" and self._current_notebook_url:
                self.colab_link.setText(f"<a href='{self._current_notebook_url}' style='color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])};'>{tr('click_to_open')}</a>")
                self.colab_link_container.show()
            else:
                self.colab_link_container.hide()
            
            timeout = self.settings.get("force_cancel_timeout", 30)
            self._force_cancel_timer.start(timeout * 1000)
        else:
            self._operation_in_progress = False
            self.overlay.hide()
            self.overlay_force_cancel_btn.hide()
            self.colab_link_container.hide()
            self._force_cancel_timer.stop()
            self.statusBar().clearMessage()
            self.show_cancel_only(False)

    def show_cancel_only(self, show=True):
        self.overlay_cancel_btn.setEnabled(show)
        if show:
            self.overlay_cancel_btn.raise_()
            self.overlay_cancel_btn.setFocus()

    def show_force_cancel_option(self):
        if self._operation_in_progress and self.overlay.isVisible():
            self.overlay_force_cancel_btn.show()
            self.overlay_force_cancel_btn.raise_()
            self.overlay_force_cancel_btn.setEnabled(True)

    def reset_progress_bars(self):
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
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(error)
        msg_box.setDetailedText(details)
        msg_box.exec_()

    def update_notebook_url_display(self, url):
        self._current_notebook_url = url
        # Update overlay if visible
        if self.overlay.isVisible() and url:
            self.colab_link.setText(f"<a href='{url}' style='color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])};'>{tr('click_to_open')}</a>")
            self.colab_link_container.show()

    def update_online_status_display(self, status):
        status_colors = {
            "idle": DARK_THEME['text_secondary'],
            "uploading": DARK_THEME['warning'],
            "waiting": DARK_THEME['info'],
            "processing": "#9c27b0",
            "downloading": DARK_THEME['success'],
            "completed": DARK_THEME['success'],
            "failed": DARK_THEME['error'],
            "canceled": DARK_THEME['warning'],
            "force_canceled": DARK_THEME['error'],
            "canceling": DARK_THEME['warning'],
            "timeout": DARK_THEME['error'],
            "network_error": DARK_THEME['warning'],
            "starting": DARK_THEME['info'],
            "initializing": DARK_THEME['info']
        }
        color = status_colors.get(status, DARK_THEME['text_secondary'])
        status_text = status.replace("_", " ").title()
        self.status_value.setText(status_text)
        self.status_value.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: bold;")

    def copy_notebook_url(self):
        if self._current_notebook_url:
            clipboard = QApplication.clipboard()
            clipboard.setText(self._current_notebook_url)
            self.statusBar().showMessage("Notebook URL copied to clipboard", 3000)
        else:
            QMessageBox.information(self, "No URL", "No notebook URL to copy.")

    def open_settings_dialog(self):
        logger.info("Opening settings dialog")
        dlg = SettingsDialog(self.settings, self)
        dlg.settingsChanged.connect(self.update_from_settings)
        if dlg.exec_() == QDialog.Accepted:
            logger.info("Settings dialog accepted")
            self.apply_theme()
        else:
            logger.info("Settings dialog canceled")

    def update_from_settings(self, new_settings):
        self.settings = new_settings
        self.apply_ui_scale()
        self.apply_theme()
        self.lang_combo.setCurrentText(new_settings.get("default_lang", tr('english_transcribe')))
        self.words_spin.setValue(new_settings.get("words_per_line", 5))
        self.format_combo.setCurrentText(new_settings.get("output_format", tr('srt_format')))
        self.update_download_button_visibility()
        
        # Update animation controller
        animation_controller.set_enabled(new_settings.get('enable_animations', True))
        animation_controller.set_speed(new_settings.get('animation_speed', 'normal'))
        
        # Update language
        _translator.set_language(new_settings.get('language', 'en'))
        
        if hasattr(self, 'online_handler'):
            self.online_handler.max_retry_attempts = new_settings.get("max_retry_attempts", 5)
            
        self.setup_tooltips()
        
        logger.info("Settings updated")

    def update_download_button_visibility(self):
        if self.mode == "online":
            self.download_btn.setVisible(False)
            logger.info("Download button hidden in online mode")
            return

        model_dir = self.settings.get("models_dir", APP_DATA_DIR)
        model_path_v1 = os.path.join(model_dir, "large-v1.pt")
        model_path = os.path.join(model_dir, "large.pt")
        
        exists = validate_model_file(model_path_v1) or validate_model_file(model_path)
        self.download_btn.setVisible(not exists)
        logger.info(f"Valid model exists: {exists}")

    def initiate_google_login(self):
        client_secrets = load_client_secrets()
        if not client_secrets:
            msg = "Google client secrets not found."
            logger.warning(msg)
            QMessageBox.warning(self, "Missing Credentials", msg)
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
            QMessageBox.information(self, "Login Success", "Google Drive connected.")
        except Exception as login_err:
            logger.error(f"Google login failed: {traceback.format_exc()}")
            QMessageBox.critical(self, "Login Error", f"Authentication failed:\n{str(login_err)}")
        finally:
            if os.path.exists(client_path):
                os.remove(client_path)
                logger.info("Temp client file removed")

    def load_existing_credentials(self):
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
        self.mode = "online" if text == tr('online_mode') else "normal"
        self.settings["last_mode"] = self.mode
        save_settings(self.settings)
        self.update_download_button_visibility()
        logger.info(f"Mode switched to: {self.mode}")

    def load_whisper_model(self):
        try:
            model_dir = self.settings.get("models_dir", APP_DATA_DIR)
            logger.info(f"Loading Whisper large-v1 from: {model_dir}")
            
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
            self.play_btn.setText(tr('play_pause'))
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
            QMessageBox.warning(self, tr('no_audio'), tr('no_audio_msg'))
            logger.warning("Play clicked → no audio_file")
            return

        logger.info(f"Play/Pause clicked")

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
            QMessageBox.critical(self, "Critical Playback Error",
                                f"Qt could not prepare audio:\n{str(play_err)}\n\n"
                                "Try:\n1. Play the .temp.wav file in VLC/Media Player\n"
                                "2. If it plays → issue is QtMultimedia\n"
                                "3. Re-import or restart app")

    def stop_playback(self):
        self.player.stop()
        self.play_btn.setText(tr('play_pause'))

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
                                "• Shorten filename\n"
                                "• Re-extract audio\n"
                                "• Install K-Lite Codec Pack")

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

    def import_media_file(self, file_path=None):
        logger.info("Media import dialog opened")
        if not file_path:
            filter_str = "Media Files (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv *.mp3 *.wav *.m4a *.aac *.flac *.ogg *.wma *.amr *.opus)"
            file_path, _ = QFileDialog.getOpenFileName(self, tr('import_media'), self.settings.get("last_input_file", ""), filter_str)
            
        if not file_path:
            logger.info("Import cancelled by user")
            return

        logger.info(f"Importing: {file_path}")
        self.input_file = file_path
        self.output_folder = self.output_folder or os.path.dirname(file_path)
        self.out_folder_edit.setText(self.output_folder)
        self.enhance_btn.setEnabled(True)
        
        self.settings["last_input_file"] = file_path
        self.settings["last_output_folder"] = self.output_folder
        save_settings(self.settings)
        
        self.session_manager.save_operation_state("import", {
            "file": file_path,
            "timestamp": datetime.now().isoformat()
        })

        temp_dir = self.settings.get("temp_dir", tempfile.gettempdir())
        temp_name = os.path.splitext(os.path.basename(file_path))[0] + ".temp.wav"
        new_temp = os.path.join(temp_dir, temp_name)

        if self.last_temp_wav and os.path.exists(self.last_temp_wav):
            try:
                os.remove(self.last_temp_wav)
                logger.info(f"Previous temp removed")
            except Exception as rm_err:
                logger.warning(f"Previous temp removal failed")

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
        
        # Update preview widget
        self.preview_widget.set_media(self.audio_file)
        
        logger.info(f"Audio prepared")
        QMessageBox.information(self, tr('import_complete'), tr('import_success'))

    def debug_audio_file(self):
        if not self.audio_file:
            logger.info("No audio file set")
            return
        logger.info(f"Audio file exists: {os.path.exists(self.audio_file)}")
        logger.info(f"Size: {os.path.getsize(self.audio_file) / 1024 / 1024:.2f} MB")

    def browse_output_folder(self):
        d = QFileDialog.getExistingDirectory(self, tr('browse_output'), self.output_folder or "")
        if d:
            self.output_folder = d
            self.out_folder_edit.setText(d)
            self.settings["last_output_folder"] = d
            save_settings(self.settings)
            logger.info(f"Output folder set")

    def enhance_audio_vocals(self):
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
        self.progress_update(value)

    def on_enhance_finished(self, vocals_path, success):
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
                self.preview_widget.set_media(final_path)
                logger.info(f"Enhanced audio saved")
                QMessageBox.information(self, tr('enhancement_complete'), f"{tr('enhancement_success')}\n{final_path}")
            except Exception as move_err:
                logger.error(f"Move enhanced file failed: {move_err}")
                QMessageBox.warning(self, tr('save_error'), str(move_err))
        self.enhancer_thread = None
        logger.info("Enhancer thread finished")

    def on_enhance_error(self, error_msg):
        self.freeze_ui(False)
        logger.error(f"Enhancement error: {error_msg}")
        QMessageBox.critical(self, tr('enhancement_failed'), error_msg)
        self.enhancer_thread = None

    def open_model_download_dialog(self):
        if self._closing:
            return
            
        logger.info("Opening model download dialog")
        dlg = QDialog(self)
        dlg.setWindowTitle(tr('download_model'))
        dlg.setFixedSize(520, 340)
        lay = QVBoxLayout()
        dlg.setLayout(lay)

        title = QLabel("Download Whisper large-v1 Model (~2.9 GB)")
        title.setFont(QFont(self.settings.get('font_family', 'Segoe UI'), 14, QFont.Bold))
        title.setStyleSheet(f"color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])};")
        title.setAlignment(Qt.AlignCenter)
        lay.addWidget(title)

        desc = QLabel("large-v1 is the most accurate model.\nRequires ~3 GB disk space.\nDownload may take 5-30 minutes.")
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
        ok_btn = GlowButton(tr('start_download'))
        ok_btn.clicked.connect(dlg.accept)
        
        cancel_btn = GlowButton(tr('cancel'))
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
                    logger.info(f"Valid model linked")
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

        logger.info(f"Model download started")

    def on_download_progress(self, value, speed, eta):
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
        if success:
            enhanced_path = vocals_path
            base = os.path.splitext(os.path.basename(self.input_file or "audio"))[0]
            final_name = f"{base}_auto_enhanced.wav"
            final_path = os.path.join(self.output_folder or APP_DATA_DIR, final_name)
            shutil.move(vocals_path, final_path)
            self.audio_file = final_path
            self.play_btn.setEnabled(True)
            logger.info(f"Auto-enhanced")
            self.proceed_to_transcription(final_path)
        else:
            logger.warning("Auto-enhance failed, using original audio")
            self.proceed_to_transcription(self.audio_file)

        self.enhancer_thread = None

    def on_auto_enhance_error(self, error):
        logger.error(f"Auto-enhance error: {error}")
        QMessageBox.warning(self, tr('enhancement_failed'), error)
        self.enhancer_thread = None
        self.proceed_to_transcription(self.audio_file)

    def proceed_to_transcription(self, audio_to_use):
        lang_text = self.lang_combo.currentText()
        
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
        task = "translate" if "Translate" in lang_text else "transcribe"

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

        logger.info(f"Transcription params: lang={lang_code}, task={task}, wpl={wpl}, fmt={fmt}")

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
        try:
            self.progress_update(10)
            model = self.load_whisper_model()
            
            self.progress_whisper = ProgressWhisper(lambda p, msg: self.update_transcription_progress(p, msg))
            
            logger.info("Starting local transcription with progress tracking...")
            
            result = model.transcribe(
                audio_path,
                language=lang_code,
                task=task,
                word_timestamps=True,
                verbose=False
            )
            
            total_segments = len(result.get("segments", []))
            for i, seg in enumerate(result.get("segments", [])):
                if self.progress_whisper and self.progress_whisper.is_canceled():
                    raise Exception(tr('canceled'))
                    
                progress = 20 + int((i / max(1, total_segments)) * 60)
                self.update_transcription_progress(progress, f"{tr('processing_segment')} {i+1}/{total_segments}")
                
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
            
            # Update preview widget
            self.preview_widget.set_subtitles(self.subtitles)

            logger.info(f"Local generation saved")
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
        self.progress_update(progress)
        self.prog_info.setText(message)
        QApplication.processEvents()

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
                logger.info(f"SRT saved")
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
                logger.info(f"ASS saved")
            logger.info(f"Subtitles saved")
        except Exception as save_err:
            logger.error(f"Save failed: {save_err}")
            raise

    def load_downloaded_subtitles(self, file_path):
        logger.info(f"Loading online subtitles")
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
            
            # Update preview widget
            self.preview_widget.set_subtitles(self.subtitles)
            
            logger.info("Online subtitles loaded successfully")
        except Exception as load_err:
            logger.error(f"Online load failed: {traceback.format_exc()}")
            QMessageBox.warning(self, tr('load_error'), f"{tr('preview_failed')}\n{str(load_err)}")

    def toggle_edit_mode(self):
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
        
        # Update preview widget
        self.preview_widget.set_subtitles(self.subtitles)
        
        logger.info("Edits applied to subtitles")
        QMessageBox.information(self, tr('saved'), tr('edits_applied'))

    def refresh_caption_preview(self):
        preview = "\n\n".join(self.display_lines)
        self.caption_edit.setText(preview)
        logger.debug("Caption preview refreshed")

    def cancel_current_operation(self, with_confirmation=False):
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

    def export_subtitles(self):
        """Export subtitles to file"""
        if not self.generated or not self.subtitles:
            QMessageBox.warning(self, "No Subtitles", "No subtitles to export.")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Subtitles",
            os.path.join(EXPORTS_DIR, f"subtitles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.srt"),
            "Subtitle Files (*.srt *.ass *.ssa *.vtt)"
        )
        if filename:
            fmt = os.path.splitext(filename)[1]
            self.save_subtitles_to_file(self.subtitles, fmt, filename)
            QMessageBox.information(self, "Export Complete", f"Subtitles exported to:\n{filename}")

    def save_session(self):
        """Save current session"""
        session_data = {
            'last_input_file': self.input_file,
            'last_output_folder': self.output_folder,
            'subtitles': self.subtitles,
            'display_lines': self.display_lines,
            'generated': self.generated,
            'mode': self.mode,
            'timestamp': datetime.now().isoformat()
        }
        self.session_manager.save_session(session_data)
        QMessageBox.information(self, "Session Saved", "Current session has been saved.")

    def load_session(self):
        """Load saved session"""
        session_data = self.session_manager.load_session()
        if session_data:
            if session_data.get('last_input_file') and os.path.exists(session_data['last_input_file']):
                self.input_file = session_data['last_input_file']
                self.output_folder = session_data.get('last_output_folder')
                self.subtitles = session_data.get('subtitles', [])
                self.display_lines = session_data.get('display_lines', [])
                self.generated = session_data.get('generated', False)
                
                if self.generated:
                    preview = "\n\n".join(self.display_lines)
                    self.caption_edit.setText(preview)
                    self.edit_btn.setEnabled(True)
                    
                QMessageBox.information(self, "Session Loaded", "Session loaded successfully.")
            else:
                QMessageBox.warning(self, "Session Error", "Session file not found.")
        else:
            QMessageBox.warning(self, "Session Error", "No saved session found.")

    def undo(self):
        """Undo last action"""
        # Implement undo functionality
        pass

    def redo(self):
        """Redo last undone action"""
        # Implement redo functionality
        pass

    def cut(self):
        """Cut selected text"""
        self.caption_edit.cut()

    def copy(self):
        """Copy selected text"""
        self.caption_edit.copy()

    def paste(self):
        """Paste text"""
        self.caption_edit.paste()

    def select_all(self):
        """Select all text"""
        self.caption_edit.selectAll()

    def toggle_hardware_monitor(self):
        """Toggle hardware monitor visibility"""
        self.hardware_dock.setVisible(not self.hardware_dock.isVisible())

    def toggle_performance_graph(self):
        """Toggle performance graph visibility"""
        self.performance_dock.setVisible(not self.performance_dock.isVisible())

    def toggle_preview_widget(self):
        """Toggle preview widget visibility"""
        self.preview_dock.setVisible(not self.preview_dock.isVisible())

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def refresh_hardware(self):
        """Refresh hardware information"""
        self.hardware_monitor.detect_all()
        self.statusBar().showMessage("Hardware information refreshed", 3000)

    def move_to_monitor(self, monitor_index: int):
        """Move window to specified monitor"""
        self.monitor_manager.move_window_to_monitor(self, monitor_index)

    def create_monitor_window(self):
        """Create a new window on another monitor"""
        current_index = 0
        for i, monitor in enumerate(self.monitor_manager.monitors):
            if monitor['geometry']['x'] == self.x() and monitor['geometry']['y'] == self.y():
                current_index = i
                break
                
        next_index = (current_index + 1) % self.monitor_manager.get_monitor_count()
        new_window = self.monitor_manager.create_monitor_window(self, next_index)
        if new_window:
            self._monitor_windows.append(new_window)
            new_window.show()

    def cycle_dock_widgets(self):
        """Cycle through dock widgets"""
        docks = [self.hardware_dock, self.performance_dock, self.preview_dock]
        for dock in docks:
            if dock.isVisible():
                dock.hide()
                next_index = (docks.index(dock) + 1) % len(docks)
                docks[next_index].show()
                break

    def open_documentation(self):
        """Open documentation in web browser"""
        QDesktopServices.openUrl(QUrl("https://github.com/NotY215/NotyCaption"))

    def show_about_dialog(self):
        """Show about dialog"""
        about_text = f"""
        <h1>{APP_NAME}</h1>
        <h3>Version {APP_VERSION}</h3>
        <p>Professional AI-Powered Caption Generator</p>
        <p>Build: {APP_BUILD}</p>
        <p>{APP_COPYRIGHT}</p>
        <hr>
        <p><b>Features:</b></p>
        <ul>
            <li>AI transcription using OpenAI Whisper</li>
            <li>Hardware acceleration (NVIDIA CUDA, AMD ROCm, Intel, Apple Metal)</li>
            <li>Real-time hardware monitoring</li>
            <li>Performance graphs</li>
            <li>Multi-monitor support</li>
            <li>Multiple language support</li>
            <li>Google Drive integration</li>
            <li>Vocal enhancement with Spleeter</li>
            <li>Advanced subtitle editing</li>
        </ul>
        <hr>
        <p><b>Author:</b> NotY215</p>
        <p><b>Website:</b> <a href="https://github.com/NotY215">GitHub</a></p>
        """
        
        QMessageBox.about(self, "About NotyCaption Pro", about_text)

    def auto_save(self):
        """Auto-save current session"""
        if self.input_file:
            self.save_session()
            logger.info("Auto-save completed")

    def open_workspace_dialog(self):
        """Open workspace customization dialog"""
        dlg = WorkspaceCustomizeDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            settings = dlg.get_current_settings()
            self.settings.update(settings)
            save_settings(self.settings)
            self.apply_theme()
            # Update colab link if visible
            if hasattr(self, 'overlay') and self.overlay.isVisible():
                self.update_colab_link_style()
            QMessageBox.information(self, "Workspace Updated", "Workspace settings have been updated.")

    def update_colab_link_style(self):
        if hasattr(self, 'colab_link'):
            self.colab_link.setStyleSheet(f"color: {self.settings.get('accent_color', DARK_THEME['accent_primary'])}; font-size: 12px;")

# ========================================
# MAIN ENTRY
# ========================================
if __name__ == "__main__":
    # Check for single instance
    instance = SingleInstance()
    if instance.is_already_running():
        logger.warning("Duplicate instance detected")
        QMessageBox.warning(None, "Already Running", "NotyCaption is already open in another window.")
        sys.exit(1)

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_AUTHOR)
    app.setStyle('Fusion')

    # Set application icon
    icon_path = resource_path('App.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        logger.info("Global app icon set")

    # Show splash screen
    splash_path = resource_path('splash.png')
    splash_pixmap = QPixmap(splash_path) if os.path.exists(splash_path) else QPixmap(800, 600)
    if not os.path.exists(splash_path):
        splash_pixmap.fill(QColor(26, 26, 26))
        painter = QPainter(splash_pixmap)
        painter.setPen(QColor(74, 111, 165))
        painter.setFont(QFont("Segoe UI", 24, QFont.Bold))
        painter.drawText(splash_pixmap.rect(), Qt.AlignCenter, APP_NAME)
        painter.end()
        
    splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    logger.info("Launching secure NotyCaption...")
    
    # Create and show main window
    window = NotyCaptionWindow()
    
    # Finish splash
    splash.finish(window)
    
    window.show()
    logger.info("Main loop started")
    
    sys.exit(app.exec_())