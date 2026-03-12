# build.py
"""
NotyCaption Pro - Complete Build System
Builds: Main App, Uninstaller, and Creates Professional Installer Package
"""

import os
import sys
import json
import base64
import shutil
import subprocess
import datetime
import struct
import zlib
from pathlib import Path
from cryptography.fernet import Fernet

# ────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────

APP_NAME        = "NotyCaption"
PUBLISHER       = "NotY215"
MAIN_SCRIPT     = "main.py"
INSTALLER_SCRIPT = "installer.py"
UNINSTALLER_SCRIPT = "uninstaller.py"
ICON_FILE       = "App.ico"
UNINSTALLER_ICON = "Uninstaller.ico"
CLIENT_JSON_SRC = "client.json"
ENCRYPTED_FILE  = "client.notycapz"
KEY_FILE_NAME   = "key.notcapz"

# Documentation files
README_FILE     = "Readme.html"
TOC_FILE        = "T&C.html"

REQUIRED_FILES = [
    MAIN_SCRIPT,
    INSTALLER_SCRIPT,
    UNINSTALLER_SCRIPT,
    ICON_FILE,
    UNINSTALLER_ICON,
    CLIENT_JSON_SRC,
]

# Output directories
BUILD_DIR       = "build_temp"
DIST_DIR        = "dist"
PACKAGE_DIR     = "package"
INSTALLER_OUTPUT = f"{APP_NAME}_Setup.exe"
RELEASE_FOLDER  = f"release_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

# PyInstaller common args
PYINSTALLER_ARGS = [
    "--onefile",
    "--windowed",
    "--clean",
    "--noupx",
    "--log-level=INFO",
]

# ────────────────────────────────────────────────
# ENCRYPTION UTILS
# ────────────────────────────────────────────────

def generate_or_load_key(key_path=KEY_FILE_NAME):
    """Generate or load encryption key"""
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
    print(f"✓ Created new key: {key_path}")
    return key

def encrypt_client():
    """Encrypt client secrets file"""
    if not os.path.isfile(CLIENT_JSON_SRC):
        print(f"⚠ Creating placeholder {CLIENT_JSON_SRC}")
        placeholder = {
            "installed": {
                "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
                "project_id": "your-project-id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "YOUR_CLIENT_SECRET",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
            }
        }
        with open(CLIENT_JSON_SRC, "w", encoding="utf-8") as f:
            json.dump(placeholder, f, indent=2)

    key = generate_or_load_key()
    fernet = Fernet(key)

    with open(CLIENT_JSON_SRC, "r", encoding="utf-8") as f:
        data = json.load(f)

    encrypted = fernet.encrypt(json.dumps(data).encode())
    encoded = base64.b64encode(encrypted).decode()

    with open(ENCRYPTED_FILE, "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"✓ Encrypted client secrets → {ENCRYPTED_FILE}")

# ────────────────────────────────────────────────
# DOCUMENTATION FILES
# ────────────────────────────────────────────────

def create_documentation():
    """Create HTML documentation files if they don't exist"""
    
    # Readme.html
    if not os.path.exists(README_FILE):
        readme_content = """<!DOCTYPE html>
<html>
<head>
    <title>NotyCaption Pro - Welcome</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #e0e0ff; line-height: 1.6; padding: 20px; }
        h1 { color: #89b4fa; border-bottom: 2px solid #45475a; padding-bottom: 10px; }
        h2 { color: #b4befe; margin-top: 25px; }
        ul { list-style-type: none; padding-left: 0; }
        li { margin: 10px 0; padding: 10px; background: #242436; border-radius: 8px; }
        li:before { content: "✓ "; color: #a6e3a1; font-weight: bold; }
        .feature-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .note { background: #2a2a3a; border-left: 4px solid #f38ba8; padding: 15px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>🎬 Welcome to NotyCaption Pro</h1>
    <p><strong>Secure AI Caption Generator by NotY215 & Team</strong></p>
    
    <div class="feature-grid">
        <div>
            <h2>✨ Key Features</h2>
            <ul>
                <li>AI-Powered Caption Generation (Whisper)</li>
                <li>Vocal Enhancement with Spleeter</li>
                <li>Google Drive Integration</li>
                <li>8 Language Support</li>
                <li>Hardware Acceleration Detection</li>
                <li>Real-time Progress Tracking</li>
            </ul>
        </div>
        <div>
            <h2>🖥️ System Requirements</h2>
            <ul>
                <li>Windows 10/11 (64-bit)</li>
                <li>4GB RAM minimum (8GB recommended)</li>
                <li>3GB free disk space</li>
                <li>Internet connection for online mode</li>
                <li>Optional: NVIDIA GPU for acceleration</li>
            </ul>
        </div>
    </div>
    
    <h2>📦 What's Included</h2>
    <ul>
        <li>NotyCaption Pro Application</li>
        <li>Uninstaller Tool</li>
        <li>Documentation & Help Files</li>
        <li>Encrypted Client Secrets</li>
    </ul>
    
    <div class="note">
        <strong>⚠️ Important:</strong> This software uses AI models that may require 
        initial download (~2.9GB). Ensure stable internet connection for first run.
    </div>
    
    <p style="text-align: center; margin-top: 30px; color: #89b4fa;">
        Click Next to continue with installation →
    </p>
</body>
</html>"""
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"✓ Created {README_FILE}")

    # T&C.html
    if not os.path.exists(TOC_FILE):
        toc_content = """<!DOCTYPE html>
<html>
<head>
    <title>Terms & Conditions - NotyCaption Pro</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #e0e0ff; line-height: 1.6; padding: 20px; }
        h1 { color: #f38ba8; border-bottom: 2px solid #45475a; padding-bottom: 10px; }
        h2 { color: #fab387; margin-top: 25px; }
        .section { background: #242436; padding: 15px; border-radius: 8px; margin: 15px 0; }
        .highlight { color: #a6e3a1; font-weight: bold; }
    </style>
</head>
<body>
    <h1>📜 Terms and Conditions</h1>
    <p><strong>Last Updated: March 2026</strong></p>
    
    <div class="section">
        <h2>1. License Agreement</h2>
        <p>This software is licensed, not sold. NotY215 grants you a non-exclusive, 
        non-transferable license to use this software on your personal computer.</p>
    </div>
    
    <div class="section">
        <h2>2. Open Source Components</h2>
        <p>This software uses the following open-source libraries:</p>
        <ul>
            <li>Whisper AI (MIT License)</li>
            <li>Spleeter (MIT License)</li>
            <li>PyQt5 (GPL v3)</li>
            <li>TensorFlow (Apache 2.0)</li>
            <li>And others - see documentation</li>
        </ul>
    </div>
    
    <div class="section">
        <h2>3. Data Privacy</h2>
        <p>NotyCaption Pro processes all media locally by default. When using online mode,
        audio files are temporarily uploaded to Google Drive and automatically deleted 
        after processing. No personal data is collected or stored by NotY215.</p>
    </div>
    
    <div class="section">
        <h2>4. Disclaimer of Warranty</h2>
        <p>This software is provided "AS IS" without warranty of any kind. The authors
        are not liable for any damages arising from its use.</p>
    </div>
    
    <div class="section">
        <h2>5. AI Model Usage</h2>
        <p>The Whisper and Spleeter models are downloaded separately and subject to their
        respective licenses. You are responsible for complying with those licenses.</p>
    </div>
    
    <p style="text-align: center; margin-top: 30px;">
        <span class="highlight">By installing, you agree to these terms.</span>
    </p>
</body>
</html>"""
        with open(TOC_FILE, "w", encoding="utf-8") as f:
            f.write(toc_content)
        print(f"✓ Created {TOC_FILE}")

# ────────────────────────────────────────────────
# BUILD FUNCTIONS
# ────────────────────────────────────────────────

def clean_directories():
    """Clean build directories"""
    dirs = [BUILD_DIR, DIST_DIR, PACKAGE_DIR]
    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d, ignore_errors=True)
            print(f"✓ Cleaned {d}/")
    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(PACKAGE_DIR, exist_ok=True)

def build_app():
    """Build main NotyCaption application"""
    print("\n" + "="*60)
    print(" Building NotyCaption Application ".center(60))
    print("="*60)

    cmd = [
        "pyinstaller",
        *PYINSTALLER_ARGS,
        f"--icon={ICON_FILE}",
        f"--name={APP_NAME}",
        "--add-data", f"{ICON_FILE};.",
        "--add-data", f"{ENCRYPTED_FILE};.",
        "--add-data", f"{KEY_FILE_NAME};.",
        "--collect-all", "charset_normalizer",
        "--collect-all", "spleeter",
        "--collect-all", "tensorflow",
        "--collect-all", "whisper",
        "--collect-all", "torch",
        "--collect-all", "moviepy",
        "--collect-all", "PyQt5",
        "--collect-all", "cpuinfo",
        "--collect-all", "GPUtil",
        "--collect-all", "psutil",
        "--collect-all", "googleapiclient",
        "--collect-all", "cryptography",
        "--hidden-import", "charset_normalizer",
        "--hidden-import", "spleeter.separator",
        "--hidden-import", "whisper",
        "--hidden-import", "moviepy.editor",
        "--hidden-import", "pysrt",
        "--hidden-import", "pysubs2",
        "--hidden-import", "google.auth",
        "--hidden-import", "google_auth_oauthlib.flow",
        "--exclude-module", "tkinter",
        "--exclude-module", "matplotlib",
        "--exclude-module", "PIL",
        "--exclude-module", "pygame",
        "--exclude-module", "charset_normalizer.md__mypyc",
        "--exclude-module", "charset_normalizer.legacy__mypyc",
        MAIN_SCRIPT
    ]

    print("Running PyInstaller...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ App build failed!")
        print(result.stderr)
        sys.exit(1)
    
    # Copy to package folder
    shutil.copy2(f"dist/{APP_NAME}.exe", f"{PACKAGE_DIR}/{APP_NAME}.exe")
    print(f"✓ App built: {PACKAGE_DIR}/{APP_NAME}.exe")

def build_uninstaller():
    """Build uninstaller application"""
    print("\n" + "="*60)
    print(" Building Uninstaller ".center(60))
    print("="*60)

    # Create uninstaller with its own icon
    cmd = [
        "pyinstaller",
        *PYINSTALLER_ARGS,
        f"--icon={UNINSTALLER_ICON}",
        "--name=uninstall",
        "--add-data", f"{UNINSTALLER_ICON};.",
        "--collect-all", "PySide6",
        "--hidden-import", "win32com",
        "--hidden-import", "winreg",
        UNINSTALLER_SCRIPT
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Uninstaller build failed!")
        print(result.stderr)
        sys.exit(1)
    
    # Copy to package folder
    shutil.copy2("dist/uninstall.exe", f"{PACKAGE_DIR}/uninstall.exe")
    print(f"✓ Uninstaller built: {PACKAGE_DIR}/uninstall.exe")

def build_installer():
    """Build installer as self-extracting executable"""
    print("\n" + "="*60)
    print(" Building Installer Package ".center(60))
    print("="*60)

    # Copy installer script and required files
    shutil.copy2(INSTALLER_SCRIPT, f"{PACKAGE_DIR}/installer.py")
    shutil.copy2(ICON_FILE, f"{PACKAGE_DIR}/App.ico")
    shutil.copy2(UNINSTALLER_ICON, f"{PACKAGE_DIR}/Uninstaller.ico")
    shutil.copy2(ENCRYPTED_FILE, f"{PACKAGE_DIR}/client.notycapz")
    shutil.copy2(KEY_FILE_NAME, f"{PACKAGE_DIR}/key.notcapz")
    
    # Copy documentation
    create_documentation()
    shutil.copy2(README_FILE, f"{PACKAGE_DIR}/Readme.html")
    shutil.copy2(TOC_FILE, f"{PACKAGE_DIR}/T&C.html")

    # Create the installer executable
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--clean",
        f"--icon={ICON_FILE}",
        f"--name={APP_NAME}_Setup",
        "--add-data", f"{PACKAGE_DIR};package",
        "--hidden-import", "PySide6",
        "--hidden-import", "win32com",
        "--hidden-import", "winreg",
        "--hidden-import", "psutil",
        INSTALLER_SCRIPT
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Installer build failed!")
        print(result.stderr)
        sys.exit(1)

    print(f"✓ Installer built: dist/{APP_NAME}_Setup.exe")

# ────────────────────────────────────────────────
# PACKAGE CREATION
# ────────────────────────────────────────────────

def create_installer_package():
    """Create the final installer package with embedded data"""
    print("\n" + "="*60)
    print(" Creating Final Installer Package ".center(60))
    print("="*60)

    # Create release folder
    os.makedirs(RELEASE_FOLDER, exist_ok=True)

    # Copy installer
    shutil.copy2(f"dist/{APP_NAME}_Setup.exe", f"{RELEASE_FOLDER}/{APP_NAME}_Setup.exe")

    # Create README
    readme_txt = f"""=== {APP_NAME} Pro ===
Version: 2026.1.0
Publisher: {PUBLISHER}

Installation Instructions:
1. Run {APP_NAME}_Setup.exe as Administrator
2. Follow the installation wizard
3. Launch {APP_NAME} from Desktop or Start Menu

Features:
- AI-Powered Caption Generation
- Vocal Enhancement with Spleeter
- Google Drive Integration
- Multi-language Support (8 languages)
- Hardware Acceleration Detection

System Requirements:
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 3GB free disk space

Support: Visit our documentation for help

All rights reserved © 2026 {PUBLISHER}
"""
    with open(f"{RELEASE_FOLDER}/README.txt", "w") as f:
        f.write(readme_txt)

    # Get file sizes
    installer_size = os.path.getsize(f"{RELEASE_FOLDER}/{APP_NAME}_Setup.exe") / (1024*1024)
    print(f"\n📦 Package Details:")
    print(f"   • Installer: {installer_size:.2f} MB")
    print(f"   • Location: {RELEASE_FOLDER}/")

def verify_package():
    """Verify all components are present"""
    required_in_package = [
        f"{PACKAGE_DIR}/{APP_NAME}.exe",
        f"{PACKAGE_DIR}/uninstall.exe",
        f"{PACKAGE_DIR}/installer.py",
        f"{PACKAGE_DIR}/App.ico",
        f"{PACKAGE_DIR}/Uninstaller.ico",
        f"{PACKAGE_DIR}/client.notycapz",
        f"{PACKAGE_DIR}/key.notcapz",
        f"{PACKAGE_DIR}/Readme.html",
        f"{PACKAGE_DIR}/T&C.html",
    ]

    missing = []
    for f in required_in_package:
        if not os.path.exists(f):
            missing.append(f)

    if missing:
        print("\n❌ Missing files in package:")
        for f in missing:
            print(f"   • {f}")
        return False
    
    print("\n✓ Package verification passed")
    return True

# ────────────────────────────────────────────────
# MAIN BUILD PROCESS
# ────────────────────────────────────────────────

def main():
    print("="*80)
    print(f" {APP_NAME} Pro - Complete Build System ".center(80))
    print("="*80)
    print(f"Started: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {sys.platform}\n")

    # Step 1: Encrypt client secrets
    print("📁 Step 1: Preparing secrets...")
    encrypt_client()

    # Step 2: Create documentation
    print("\n📄 Step 2: Creating documentation...")
    create_documentation()

    # Step 3: Clean directories
    print("\n🧹 Step 3: Cleaning directories...")
    clean_directories()

    # Step 4: Build main app
    print("\n🔨 Step 4: Building main application...")
    build_app()

    # Step 5: Build uninstaller
    print("\n🔨 Step 5: Building uninstaller...")
    build_uninstaller()

    # Step 6: Build installer
    print("\n🔨 Step 6: Building installer...")
    build_installer()

    # Step 7: Verify package
    print("\n✅ Step 7: Verifying package...")
    if not verify_package():
        sys.exit(1)

    # Step 8: Create final release
    print("\n📦 Step 8: Creating release package...")
    create_installer_package()

    # Final summary
    print("\n" + "="*80)
    print(" BUILD COMPLETE - SUCCESS ".center(80, "="))
    print("="*80)
    print(f"\n📂 Release folder: {RELEASE_FOLDER}/")
    print(f"   ├─ {APP_NAME}_Setup.exe")
    print(f"   └─ README.txt")
    
    installer_size = os.path.getsize(f"{RELEASE_FOLDER}/{APP_NAME}_Setup.exe") / (1024*1024)
    print(f"\n📊 Statistics:")
    print(f"   • Installer size: {installer_size:.2f} MB")
    print(f"   • Package includes: Main App, Uninstaller, Documentation")
    
    print(f"\n▶️  Run {RELEASE_FOLDER}/{APP_NAME}_Setup.exe to install")
    print(f"\n{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - Build finished\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)