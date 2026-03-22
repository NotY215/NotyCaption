# NotyCaption Pro – AI-Powered Smart Caption Generator

<p align="center">
  <br><br>
  <strong>Generate perfectly synced, beautiful subtitles automatically with Whisper AI</strong><br>
  Local + Online (Colab) modes • SRT/ASS support • Vocal enhancement • GPU acceleration
</p>

<p align="center">
  <a href="https://github.com/NotY215/NotyCaption/releases/latest">
    <img src="https://img.shields.io/github/v/release/NotY215/NotyCaption?color=00c853&label=Latest%20Release&logo=windows&logoColor=white&style=for-the-badge" alt="Latest Release">
  </a>
  <a href="https://github.com/NotY215/NotyCaption/releases">
    <img src="https://img.shields.io/github/downloads/NotY215/NotyCaption/total?color=4285f4&style=for-the-badge&logo=google-drive&logoColor=white" alt="Downloads">
  </a>
  <img src="https://img.shields.io/badge/Java-21+-orange?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java Version">
  <img src="https://img.shields.io/badge/License-GNU%20GPLv3-red?style=for-the-badge" alt="License">
</p>

<p align="center">
  <a href="https://github.com/NotY215/NotyCaption/releases/">
    <img src="https://img.shields.io/badge/DOWNLOAD%20INSTALLER-2.9%E2%80%93GB%20Model%20Ready-00c853?style=for-the-badge&logo=windows&logoColor=white&labelColor=111111" alt="Download Windows Installer">
  </a>
</p>

---

## ✨ Features

* **AI Subtitle Generation** powered by OpenAI Whisper (local + online Colab mode)
* **Large-v1 model support** – highest accuracy (~2.9 GB download)
* **Words-per-line control** (1–20 words) with model validation
* **SRT** (standard) and **ASS** (advanced styling) export
* **Vocal-only enhancement** using Spleeter (remove background music/noise)
* **Media playback** with real-time subtitle highlighting
* **Editable captions** directly in the app
* **Google Drive / Colab integration** for GPU-accelerated processing
* **Dark & Light themes**, UI scaling, secure encrypted settings
* **Single-instance lock** – prevents multiple app launches
* **Model integrity check** + automatic corrupt file cleanup
* **Cancellation-safe model download** with progress bar

---

## 🚀 Quick Start – Windows Installer (Recommended)

1. Go to → [Latest Release Page](https://github.com/NotY215/NotyCaption/releases/latest)
2. Download **NotyCaption.exe** (~800 MB–1.20 GB)
3. Run the installer (no installation needed – portable app)
4. First launch → download **large-v1** model (~2.9 GB) when prompted
5. Import video/audio → Generate captions → Export SRT/ASS

**Direct download link (latest stable):**
[https://github.com/NotY215/NotyCaption/releases/latest/download](https://github.com/NotY215/NotyCaption/releases/latest/download)

---

## ☕ Tech Stack (Updated)

* **Java 21 (Core Application)**
* **JavaFX / Swing (UI Layer)**
* **Whisper AI (via API / local integration)**
* **FFmpeg (media processing)**
* **Spleeter (audio separation)**
* **Google Drive API + Colab integration**

---

## 🛠️ Manual Setup (Developers / Advanced Users)

### Requirements

* Java 21+
* Windows 10/11 (64-bit)
* FFmpeg installed and added to PATH

### Setup

```bash
git clone https://github.com/NotY215/NotyCaption.git
cd NotyCaption
```

### Run Application

```bash
./gradlew run
```

*or (if using Maven)*

```bash
mvn clean install
mvn javafx:run
```

---

## 🎬 FFmpeg Setup

* Download from: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
* Extract and add the `bin` folder to system PATH

---

## 📥 Download & Releases

* All pre-built binaries and model files are available here:
* → [https://github.com/NotY215/NotyCaption/releases](https://github.com/NotY215/NotyCaption/releases)
* Recommended version: Latest Stable
* File: NotyCaption.exe

---

## 🔒 Security Notes

* All settings are encrypted using modern AES-based encryption
* Google client secrets are securely bundled in EXE builds
* No telemetry or external tracking
* Model files are validated for size & integrity before use

---

## 🛠️ Building from Source (for Developers)

### Requirements

* Java 21
* Gradle or Maven

### Build

```bash
./gradlew build
```

*or*

```bash
mvn clean package
```

* Output will be generated in the `build/` or `target/` directory

---

## ⚡ Performance Tips

* Use large-v1 model for best accuracy (requires ~3 GB RAM + disk)
* Enable GPU in online Colab mode for 5–10× faster transcription
* Use vocal enhancement for videos with background music
* Set 1 word per line + large model for karaoke-style subtitles

---

## 📜 License

* GNU General Public License v3.0
* See LICENSE file for full details
* Copyright © 2026 NotY215

---

## 🙏 Acknowledgments

* OpenAI Whisper
* Spleeter
* FFmpeg
* JavaFX / Swing
* Google Colab & Google Drive API

---

# Made with ❤️ in India

* Star ⭐ the repo if you find it useful!

## [Download Latest Installer ](https://github.com/NotY215/NotyCaption/releases/latest)
