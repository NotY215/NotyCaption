# build.py
"""
Build script for NotyCaption Pro - FINAL FIXED VERSION (March 2026)
Handles encryption + PyInstaller one-file build + cleanup
"""

import os
import sys
import json
import base64
import shutil
import subprocess
import datetime
from cryptography.fernet import Fernet

# ────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────

APP_NAME      = "NotyCaption"
MAIN_SCRIPT   = "main.py"
ICON_FILE     = "App.ico"

REQUIRED_FILES = [
    MAIN_SCRIPT,
    ICON_FILE,
    "client.json",              # Google API credentials
]

RELEASE_FOLDER = f"release_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

TEMP_FOLDERS_TO_DELETE = ["build", "dist", "__pycache__"]

# PyInstaller command - optimized for Whisper + moviepy + imageio + google-api issues
PYINSTALLER_CMD = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--clean",
    "--noupx",
    "--log-level=DEBUG",               # Helps debug missing modules
    f"--icon={ICON_FILE}",
    f"--name={APP_NAME}",

    # Resources
    "--add-data", f"{ICON_FILE};.",

    # ─── CRITICAL: Collect ALL submodules and data for problematic libs ───
    "--collect-all", "imageio",
    "--collect-all", "imageio_ffmpeg",
    "--collect-all", "moviepy",
    "--collect-all", "whisper",
    "--collect-all", "tqdm",
    "--collect-all", "googleapiclient",
    "--collect-all", "google_auth_oauthlib",
    "--collect-all", "google.auth",

    # Hidden imports (prevents runtime AttributeError / ModuleNotFound)
    "--hidden-import", "imageio",
    "--hidden-import", "imageio_ffmpeg",
    "--hidden-import", "imageio.plugins.ffmpeg",
    "--hidden-import", "moviepy.editor",
    "--hidden-import", "moviepy.video.io.ffmpeg_tools",
    "--hidden-import", "tqdm",
    "--hidden-import", "tqdm.std",
    "--hidden-import", "whisper",
    "--hidden-import", "torch",
    "--hidden-import", "pkg_resources.py2_warn",
    "--hidden-import", "importlib.metadata",
    "--hidden-import", "importlib_metadata",
    "--hidden-import", "googleapiclient.discovery",
    "--hidden-import", "googleapiclient.http",
    "--hidden-import", "google.auth.transport.requests",
    "--hidden-import", "google.oauth2.credentials",
    "--hidden-import", "google_auth_oauthlib.flow",

    # Exclude unused heavy modules to reduce size
    "--exclude-module", "tkinter",
    "--exclude-module", "matplotlib",
    "--exclude-module", "PIL",
    "--exclude-module", "pygame",

    MAIN_SCRIPT
]

# ────────────────────────────────────────────────
# ENCRYPTION
# ────────────────────────────────────────────────

def generate_or_load_key(key_path="secret-build-key.key"):
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
    print(f"[KEY] Created new encryption key → {key_path}")
    print("     !! KEEP THIS FILE SAFE !!")
    return key


def encrypt_client_json(key: bytes, input_file="client.json", output_file="client.notycapz"):
    if not os.path.isfile(input_file):
        print(f"[ERROR] {input_file} not found!")
        print("Place your Google client.json in this folder.")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    fernet = Fernet(key)
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    encrypted = fernet.encrypt(json_str.encode("utf-8"))
    encoded = base64.b85encode(encrypted).decode("ascii")

    with open(output_file, "w", encoding="ascii") as f:
        f.write(encoded)

    print(f"[OK] Encrypted client secrets → {output_file}")


# ────────────────────────────────────────────────
# BUILD LOGIC
# ────────────────────────────────────────────────

def check_requirements():
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(f)]
    if missing:
        print("Missing required files:")
        for m in missing:
            print(f"  • {m}")
        sys.exit(1)


def clean_old_builds():
    for folder in TEMP_FOLDERS_TO_DELETE:
        if os.path.exists(folder):
            print(f"[CLEAN] Removing {folder}/")
            try:
                shutil.rmtree(folder, ignore_errors=True)
            except Exception as e:
                print(f"  Could not remove {folder} → {e}")


def run_pyinstaller():
    print("\n" + "═"*90)
    print(" STARTING PYINSTALLER BUILD (DEBUG MODE) ".center(90))
    print("═"*90 + "\n")

    print("Command being executed:")
    print(" ".join(PYINSTALLER_CMD))
    print()

    try:
        subprocess.run(PYINSTALLER_CMD, check=True)
        print("\nPyInstaller finished successfully.")
    except subprocess.CalledProcessError as e:
        print("\nPyInstaller FAILED!")
        print(e.stdout.decode("utf-8", errors="replace"))
        if e.stderr:
            print(e.stderr.decode("utf-8", errors="replace"))
        sys.exit(1)


def copy_release_files():
    os.makedirs(RELEASE_FOLDER, exist_ok=True)

    files_to_copy = [
        (f"dist/{APP_NAME}.exe",          f"{RELEASE_FOLDER}/{APP_NAME}.exe"),
        ("client.notycapz",               f"{RELEASE_FOLDER}/client.notycapz"),
        (ICON_FILE,                       f"{RELEASE_FOLDER}/{ICON_FILE}"),
        ("secret-build-key.key",          f"{RELEASE_FOLDER}/secret-build-key.key"),
    ]

    copied_ok = False
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"[COPY] → {dst}")
            if ".exe" in dst:
                copied_ok = True
        else:
            print(f"[WARN] Source not found: {src}")

    if not copied_ok:
        print("\n[ERROR] Executable was not created or not found in dist/")
        sys.exit(1)


def final_cleanup():
    print("\nCleaning temporary folders...")
    for folder in TEMP_FOLDERS_TO_DELETE:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"[RM] {folder}/ removed")
            except Exception as e:
                print(f"[FAIL] Could not delete {folder} → {e}")


def print_summary():
    print("\n" + "═"*100)
    print(" BUILD COMPLETED SUCCESSFULLY ".center(100, "═"))
    print("═"*100)
    print(f"Release folder : {RELEASE_FOLDER}")
    print(f"Executable     : {RELEASE_FOLDER}/{APP_NAME}.exe")
    print(f"Encrypted auth : {RELEASE_FOLDER}/client.notycapz")
    print(f"Encryption key : {RELEASE_FOLDER}/secret-build-key.key   ← KEEP SAFE!")
    print("\nRun the EXE and test model download again.\n")


def main():
    print("NotyCaption Pro - FINAL Build Tool\n")
    print(f"Started: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n")

    check_requirements()
    clean_old_builds()

    key = generate_or_load_key()
    encrypt_client_json(key)

    run_pyinstaller()
    copy_release_files()
    final_cleanup()

    print_summary()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBuild aborted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nBuild crashed:\n{type(e).__name__}: {e}")
        sys.exit(1)