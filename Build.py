# build.py
"""
FINAL Build script - bundles both encrypted secrets AND the fixed key
"""

import os
import sys
import json
import base64
import shutil
import subprocess
import datetime
from cryptography.fernet import Fernet

# CONFIG
EXE_NAME        = "NotyCaption"
MAIN_SCRIPT     = "main.py"
ICON_FILE       = "App.ico"
CLIENT_JSON_SRC = "client.json"
ENCRYPTED_FILE  = "client.notycapz"
KEY_FILE_NAME   = "key.notcapz"   # Must match load_or_create_key()

REQUIRED_FILES = [MAIN_SCRIPT, ICON_FILE, CLIENT_JSON_SRC]

RELEASE_FOLDER = f"release_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

TEMP_FOLDERS = ["build", "dist", "__pycache__"]

PYINSTALLER_CMD = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--clean",
    "--noupx",
    "--log-level=INFO",
    f"--icon={ICON_FILE}",
    f"--name={EXE_NAME}",

    # Bundle everything needed
    "--add-data", f"{ICON_FILE};.",
    "--add-data", f"{ENCRYPTED_FILE};.",
    "--add-data", f"{KEY_FILE_NAME};.",   # ← Bundles the key too

    "--collect-all", "imageio",
    "--collect-all", "imageio_ffmpeg",
    "--collect-all", "moviepy",
    "--collect-all", "whisper",
    "--collect-all", "tqdm",

    "--hidden-import", "imageio",
    "--hidden-import", "imageio_ffmpeg",
    "--hidden-import", "moviepy.editor",
    "--hidden-import", "tqdm",
    "--hidden-import", "whisper",
    "--hidden-import", "googleapiclient.discovery",
    "--hidden-import", "googleapiclient.http",
    "--hidden-import", "google.auth.transport.requests",
    "--hidden-import", "google.oauth2.credentials",
    "--hidden-import", "google_auth_oauthlib.flow",

    MAIN_SCRIPT
]

# ────────────────────────────────────────────────
# ENCRYPTION - using FIXED key name
# ────────────────────────────────────────────────

def encrypt_client():
    if not os.path.isfile(CLIENT_JSON_SRC):
        print(f"[ERROR] Missing {CLIENT_JSON_SRC}")
        sys.exit(1)

    # Use FIXED key file name
    key_path = KEY_FILE_NAME
    if os.path.exists(key_path):
        print(f"[KEY] Using existing key: {key_path}")
        with open(key_path, "rb") as f:
            key = f.read()
    else:
        print(f"[KEY] Generating new fixed key → {key_path}")
        key = Fernet.generate_key()
        with open(key_path, "wb") as f:
            f.write(key)

    fernet = Fernet(key)

    with open(CLIENT_JSON_SRC, "r", encoding="utf-8") as f:
        data = json.load(f)

    json_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    encrypted = fernet.encrypt(json_bytes)
    encoded = base64.b64encode(encrypted).decode("utf-8")

    with open(ENCRYPTED_FILE, "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"[OK] Encrypted → {ENCRYPTED_FILE} (using key: {key_path})")


# ────────────────────────────────────────────────
# BUILD FLOW
# ────────────────────────────────────────────────

def check_files():
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(f)]
    if missing:
        print("Missing files:")
        for m in missing:
            print(f"  • {m}")
        sys.exit(1)


def clean_old():
    for d in TEMP_FOLDERS:
        if os.path.exists(d):
            print(f"[CLEAN] {d}/")
            try:
                shutil.rmtree(d, ignore_errors=True)
            except:
                pass


def run_build():
    print("\n" + "═"*80)
    print(f" BUILDING {EXE_NAME}.exe (with key & secrets bundled) ".center(80))
    print("═"*80 + "\n")

    print("Command:")
    print(" ".join(PYINSTALLER_CMD))
    print()

    try:
        subprocess.run(PYINSTALLER_CMD, check=True)
    except subprocess.CalledProcessError as e:
        print("\nPyInstaller FAILED!")
        print(e)
        sys.exit(1)


def copy_release():
    os.makedirs(RELEASE_FOLDER, exist_ok=True)
    files = [
        (f"dist/{EXE_NAME}.exe",    f"{RELEASE_FOLDER}/{EXE_NAME}.exe"),
        (ENCRYPTED_FILE,            f"{RELEASE_FOLDER}/{ENCRYPTED_FILE}"),
        (KEY_FILE_NAME,             f"{RELEASE_FOLDER}/{KEY_FILE_NAME}"),
        (ICON_FILE,                 f"{RELEASE_FOLDER}/{ICON_FILE}"),
    ]
    for src, dst in files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"[COPY] {dst}")
        else:
            print(f"[WARN] {src} missing")


def cleanup():
    print("\nCleaning...")
    for d in TEMP_FOLDERS:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"[RM] {d}/")
            except:
                pass


def summary():
    print("\n" + "═"*100)
    print(" BUILD FINISHED - Key & Secrets BUNDLED INSIDE EXE ".center(100, "═"))
    print("═"*100)
    print(f"Folder: {RELEASE_FOLDER}")
    print(f"EXE   : {RELEASE_FOLDER}/{EXE_NAME}.exe")
    print("\nRun it → decryption should now succeed with the same key.\n")


def main():
    print("NotyCaption Build - Fixed Key Bundling\n")
    check_files()
    encrypt_client()
    clean_old()
    run_build()
    copy_release()
    cleanup()
    summary()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)