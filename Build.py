# build.py
"""
Build script for NotyCaption Pro
Creates encrypted client.notycapz from client.json
Builds single-file EXE using PyInstaller
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
#  CONFIGURATION
# ────────────────────────────────────────────────

APP_NAME = "NotyCaption"
MAIN_SCRIPT = "main.py"
ICON_FILE = "App.ico"

# Expected input files in the same folder as build.py
REQUIRED_FILES = [
    MAIN_SCRIPT,
    ICON_FILE,
    "client.json",           # ← your Google API credentials
]

# Output directories
DIST_DIR = "dist"
BUILD_DIR = "build"
OUTPUT_VERSION_FOLDER = f"release_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"

# PyInstaller command base (will be extended)
PYINSTALLER_CMD = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--clean",
    "--noupx",
    f"--icon={ICON_FILE}",
    f"--name={APP_NAME}",
    "--add-data", f"{ICON_FILE};.",
    "--hidden-import", "pkg_resources.py2_warn",  # sometimes needed
    "--hidden-import", "google.auth.transport.requests",
    "--hidden-import", "google.oauth2.credentials",
    "--hidden-import", "google_auth_oauthlib.flow",
    "--hidden-import", "googleapiclient.discovery",
    "--hidden-import", "googleapiclient.http",
    "--hidden-import", "pysrt",
    "--hidden-import", "pysubs2",
    "--hidden-import", "spleeter",
    "--hidden-import", "whisper",
    # You can add more hidden-imports if you get import errors
]

# ────────────────────────────────────────────────
#  ENCRYPTION FUNCTIONS
# ────────────────────────────────────────────────

def generate_or_load_key(key_path="build_key.key"):
    """Generate or load Fernet key for encryption"""
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            key = f.read()
        print(f"→ Using existing encryption key: {key_path}")
        return key

    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
    print(f"→ Generated new encryption key → {key_path}")
    print("   !! KEEP THIS KEY SAFE !! You will need it to decrypt later.")
    return key


def encrypt_client_json(key: bytes, input_json="client.json", output_enc="client.notycapz"):
    """Encrypt client.json → client.notycapz"""
    if not os.path.exists(input_json):
        print(f"ERROR: {input_json} not found!")
        print("You must place your Google API client.json in the same folder.")
        sys.exit(1)

    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    fernet = Fernet(key)
    json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
    encrypted = fernet.encrypt(json_bytes)
    encoded = base64.b85encode(encrypted).decode("ascii")   # more compact than b64

    with open(output_enc, "w", encoding="ascii") as f:
        f.write(encoded)

    print(f"→ Successfully encrypted → {output_enc}")
    print(f"   Size: {os.path.getsize(output_enc):,} bytes")


# ────────────────────────────────────────────────
#  MAIN BUILD LOGIC
# ────────────────────────────────────────────────

def check_requirements():
    """Basic sanity check"""
    missing = []
    for f in REQUIRED_FILES:
        if not os.path.isfile(f):
            missing.append(f)

    if missing:
        print("Missing required files:")
        for m in missing:
            print(f"  • {m}")
        print("\nPlace all required files in the same directory as build.py")
        sys.exit(1)


def prepare_build():
    """Create clean build environment"""
    for d in [BUILD_DIR, DIST_DIR]:
        if os.path.exists(d):
            print(f"→ Removing old {d}/ ...")
            shutil.rmtree(d, ignore_errors=True)

    os.makedirs(DIST_DIR, exist_ok=True)


def build_exe():
    """Run PyInstaller"""
    print("\n" + "="*70)
    print(" Starting PyInstaller build...")
    print("="*70 + "\n")

    cmd = PYINSTALLER_CMD + [MAIN_SCRIPT]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("PyInstaller failed!")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)


def post_build_actions():
    """Copy important files to versioned output folder"""
    version_folder = OUTPUT_VERSION_FOLDER
    os.makedirs(version_folder, exist_ok=True)

    # Main executable
    exe_name = f"{APP_NAME}.exe"
    src_exe = os.path.join(DIST_DIR, exe_name)
    if os.path.exists(src_exe):
        shutil.copy2(src_exe, version_folder)
        print(f"→ Copied {exe_name} → {version_folder}/")

    # Encrypted client secrets
    if os.path.exists("client.notycapz"):
        shutil.copy2("client.notycapz", version_folder)
        print(f"→ Copied client.notycapz → {version_folder}/")

    # Icon (for reference)
    if os.path.exists(ICON_FILE):
        shutil.copy2(ICON_FILE, version_folder)

    # Copy encryption key (VERY IMPORTANT!)
    key_file = "build_key.key"
    if os.path.exists(key_file):
        shutil.copy2(key_file, version_folder)
        print(f"→ Copied encryption key {key_file} → {version_folder}/")
        print("   !! SAVE THIS KEY SOMEWHERE SAFE !!")
    else:
        print("\nWARNING: build_key.key not found in output folder!")

    print(f"\nBuild artifacts saved in: {version_folder}/")


def main():
    print("NotyCaption Pro - Build Tool\n")
    print(f"Date: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n")

    check_requirements()

    # Step 1: Encrypt client secrets
    key = generate_or_load_key()
    encrypt_client_json(key)

    # Step 2: Prepare clean build
    prepare_build()

    # Step 3: Build EXE
    build_exe()

    # Step 4: Organize output
    post_build_actions()

    print("\n" + "="*70)
    print(" BUILD FINISHED ".center(70, "="))
    print("="*70)
    print(f"Output folder : {OUTPUT_VERSION_FOLDER}")
    print(f"Executable    : {OUTPUT_VERSION_FOLDER}/{APP_NAME}.exe")
    print(f"Encrypted auth: {OUTPUT_VERSION_FOLDER}/client.notycapz")
    print(f"Encryption key: {OUTPUT_VERSION_FOLDER}/build_key.key  ← VERY IMPORTANT!")
    print("\nDone.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBuild aborted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during build:\n{e}")
        sys.exit(1)