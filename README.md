# NotyCaption - Summary

**NotyCaption** is a simple, dark-themed desktop application for automatically generating synchronized subtitle/caption files from video or audio files.

## Core Features

- **Supported Input Formats**  
  Video: .mp4, .avi, .mkv, .mov  
  Audio: .mp3, .wav

- **AI-Powered Transcription**  
  Uses OpenAI's Whisper model with five size options:  
  tiny · base · small · medium · large  
  (larger models are more accurate but slower)

- **Language Support**  
  - English  
  - Hindi (including Hinglish)

- **Caption Customization**  
  - Words per line: 1–14  
    → Values below 5 are only allowed when using the **large** model  
  - Output formats: .srt (default) or .ass (advanced subtitles)

- **User Interface Layout**  
  - **Left side** — Caption editor & timeline view  
    Shows numbered captions (timestamps hidden in preview)  
    Yellow highlight shows active line during audio playback  
    Clicking/selecting a line jumps playback to that timestamp

  - **Right side** — Controls panel  
    AI model selection  
    Language choice  
    Words-per-line setting  
    Import file button  
    Output format selector  
    Output folder browser

  - **Bottom bar**  
    Play/Pause button (also triggered by Spacebar)  
    Timeline seek slider  
    Generate & Export button  
    Two progress bars:  
      - Main progress (blue)  
      - Frames processed (orange)

## How the App Works – Step by Step

1. **Import a file**  
   Click "Import Video / Audio"  
   → If it's a video, audio is automatically extracted to a temporary .wav file

2. **Configure settings**  
   Choose AI model, language, words per line, and output format  
   Select output folder (defaults to source file location)

3. **Generate captions**  
   Click "Generate & Export"  
   → Whisper transcribes the audio  
   → Captions are split into lines according to the words-per-line setting  
   → Timestamps are calculated per line  
   → Preview appears in the left panel (index + text only)  
   → Progress is shown in two bars (overall + frames processed)

4. **Preview & playback**  
   Use Play/Pause or Spacebar to hear audio  
   Active caption line highlights in yellow  
   Select any caption text → playback jumps to that time

5. **Edit captions (optional)**  
   After generation, click "Edit Captions"  
   Modify text directly (timestamps remain unchanged)  
   Click again to save changes

6. **Export**  
   File is automatically saved as:  
   `[original_filename]_captions.srt` or `.ass`  
   in the chosen output folder  
   Temporary audio file is deleted after completion

## Quick Tips

- For very short lines (1–4 words) → use **large** model  
- For fastest results → use **tiny** or **base** models  
- .ass format supports more styling options in compatible players  
- Spacebar works anywhere in the app to play/pause

**Developed by NotY215**  
All rights reserved
