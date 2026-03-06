# build.py
"""
Build script for NotyCaption Pro - aggressive imageio / moviepy fix attempt
"""

import os
import sys
import json
import base64
import shutil
import subprocess
import datetime
from pathlib import Path
from cryptography.fernet import Fernet

# ────────────────────────────────────────────────
#  CONFIG
# ────────────────────────────────────────────────

APP_NAME    = "NotyCaption"
MAIN_SCRIPT = "main.py"
ICON_FILE   = "App.ico"

REQUIRED_FILES = [
    MAIN_SCRIPT,
    ICON_FILE,
    "client.json",
]

RELEASE_FOLDER = f"release_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

TEMP_FOLDERS = ["build", "dist", "__pycache__"]

# ────────────────────────────────────────────────
#  MOST AGGRESSIVE PYINSTALLER COMMAND WE CAN WRITE
#  for moviepy → imageio → importlib.metadata crash
# ────────────────────────────────────────────────

PYINSTALLER_CMD = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--clean",
    "--noupx",
    "--log-level=DEBUG",

    f"--icon={ICON_FILE}",
    f"--name={APP_NAME}",

    # Icon
    "--add-data", f"{ICON_FILE};.",

    # === CRITICAL FOR IMAGEIO METADATA CRASH ===
    "--collect-all", "imageio",
    "--collect-all", "imageio_ffmpeg",
    "--collect-data", "imageio",
    "--collect-data", "imageio_ffmpeg",

    "--hidden-import", "imageio",
    "--hidden-import", "imageio.plugins",
    "--hidden-import", "imageio.core",
    "--hidden-import", "imageio_ffmpeg",
    "--hidden-import", "imageio_ffmpeg.binaries",
    "--hidden-import", "moviepy",
    "--hidden-import", "moviepy.editor",
    "--hidden-import", "moviepy.video.io.ffmpeg_tools",
    "--hidden-import", "moviepy.audio.io.ffmpeg_audiowriter",
    "--hidden-import", "pkg_resources.py2_warn",

    # Your other modules
    "--hidden-import", "google.auth.transport.requests",
    "--hidden-import", "google.oauth2.credentials",
    "--hidden-import", "google_auth_oauthlib.flow",
    "--hidden-import", "googleapiclient.discovery",
    "--hidden-import", "googleapiclient.http",
    "--hidden-import", "pysrt",
    "--hidden-import", "pysubs2",
    "--hidden-import", "spleeter",
    "--hidden-import", "whisper",

    # Sometimes helps with metadata / importlib issues
    "--hidden-import", "importlib.metadata",
    "--hidden-import", "importlib_metadata",

    MAIN_SCRIPT
]

# ────────────────────────────────────────────────
#  ENCRYPTION
# ────────────────────────────────────────────────

def generate_or_load_key(key_path="secret-build-key.key"):
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
    print(f"[KEY] Created new key → {key_path}")
    print("     KEEP THIS FILE SAFE!\n")
    return key


def encrypt_client_secrets(key: bytes):
    src = "client.json"
    dst = "client.notycapz"

    if not os.path.isfile(src):
        print(f"ERROR: {src} missing!")
        sys.exit(1)

    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)

    fernet = Fernet(key)
    encrypted = fernet.encrypt(json.dumps(data, indent=2).encode("utf-8"))
    encoded = base64.b85encode(encrypted).decode("ascii")

    with open(dst, "w", encoding="ascii") as f:
        f.write(encoded)

    print(f"[OK] Encrypted → {dst}")

# ────────────────────────────────────────────────
#  BUILD FLOW
# ────────────────────────────────────────────────

def check_files():
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(f)]
    if missing:
        print("Missing files:")
        for f in missing:
            print(f"  • {f}")
        sys.exit(1)


def clean_old_folders():
    for d in TEMP_FOLDERS:
        if os.path.exists(d):
            print(f"[CLEAN] Removing {d}/")
            try:
                shutil.rmtree(d, ignore_errors=True)
            except:
                pass


def run_build():
    print("\n" + "═"*80)
    print(" STARTING PYINSTALLER BUILD ".center(80))
    print("═"*80 + "\n")

    print("Command:")
    print(" ".join(PYINSTALLER_CMD))
    print()

    try:
        subprocess.run(PYINSTALLER_CMD, check=True)
    except subprocess.CalledProcessError as e:
        print("\nPyInstaller FAILED!")
        if e.stderr:
            print(e.stderr.decode("utf-8", errors="replace"))
        sys.exit(1)


def copy_artifacts():
    os.makedirs(RELEASE_FOLDER, exist_ok=True)

    copies = [
        (f"dist/{APP_NAME}.exe",          f"{RELEASE_FOLDER}/{APP_NAME}.exe"),
        ("client.notycapz",               f"{RELEASE_FOLDER}/client.notycapz"),
        (ICON_FILE,                       f"{RELEASE_FOLDER}/{ICON_FILE}"),
        ("secret-build-key.key",          f"{RELEASE_FOLDER}/secret-build-key.key"),
    ]

    for src, dst in copies:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"[COPY] {dst}")
        else:
            print(f"[WARN] Not found → {src}")


def final_cleanup():
    print("\nFinal cleanup...")
    for d in TEMP_FOLDERS:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"[RM] {d}/")
            except:
                print(f"[FAIL] Could not remove {d}")


def print_result():
    print("\n" + "═"*90)
    print(" BUILD SHOULD BE FINISHED ".center(90, "═"))
    print("═"*90)
    print(f"Folder:          {RELEASE_FOLDER}")
    print(f"EXE:             {RELEASE_FOLDER}/{APP_NAME}.exe")
    print(f"Secrets:         {RELEASE_FOLDER}/client.notycapz")
    print(f"Key (important): {RELEASE_FOLDER}/secret-build-key.key")
    print("\n")


def main():
    print("NotyCaption build - last desperate attempt\n")

    check_files()
    clean_old_folders()

    key = generate_or_load_key()
    encrypt_client_secrets(key)

    run_build()
    copy_artifacts()
    final_cleanup()
    print_result()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
    except Exception as ex:
        print(f"\nCRASH:\n{type(ex).__name__}: {ex}")
        sys.exit(1)