# NotyCaption - Terms and Conditions

Welcome to **NotyCaption**, developed by **NotY215**.

By downloading, installing, accessing, or using NotyCaption (including any updates, modifications, or future versions), you agree to be bound by these **Terms and Conditions** ("Terms"). If you do **not** agree with any part of these Terms, you must **not** use the App.

---

## 1. Acceptance of Terms

These Terms constitute a legally binding agreement between you and NotY215.  
You must be at least **13 years old** (or the minimum age required in your country to use online services without parental consent) to use the App. If you are under the age of majority in your jurisdiction, you must have your parent or legal guardian consent to these Terms on your behalf.

---

## 2. License to Use the App

NotY215 grants you a **limited, non-exclusive, non-transferable, revocable license** to use NotyCaption for **personal, non-commercial purposes** only, subject to these Terms.

You may **not**:

- Copy, modify, adapt, translate, reverse engineer, decompile, disassemble, or create derivative works based on the App
- Rent, lease, lend, sell, sublicense, distribute, or commercially exploit the App
- Remove, obscure, or alter any copyright, trademark, or other proprietary notices
- Use the App for any illegal, fraudulent, or unauthorized purpose
- Interfere with or disrupt the App or servers/networks connected to the App

---

## 3. Google Login & Online Mode

### 3.1 Google OAuth Authentication
When you choose to log in with Google, the App uses **Google OAuth 2.0** to request access to your Google Drive (read/write permissions for specific folders only).  
We **only** use these permissions to:

- Upload temporary audio files to a private "uploads" folder
- Create and run temporary Google Colab notebooks
- Download generated caption files (.srt / .ass)
- Delete temporary files after successful download (when possible)

We **do not** store your Google credentials, access tokens (beyond what's needed during the session), or read any other files in your Drive.

### 3.2 Online Mode Limitations & Risks
- Caption generation in **Online mode** runs on **Google Colab** — a third-party service.
- We have **no control** over Google Colab availability, speed, quotas, or suspension of free accounts.
- Temporary files are deleted from Drive after download (when the process completes successfully). However, we cannot guarantee 100% deletion in all failure scenarios.
- **You are responsible** for any Google account quota usage, billing (if applicable), or policy violations caused by using Online mode.

---

## 4. Local Processing & Privacy

When using **Normal (local) mode**:

- All audio processing, transcription (using OpenAI Whisper), and subtitle generation happen **entirely on your device**.
- No audio, video, or generated subtitles are sent to any external server unless you explicitly choose Online mode.
- Temporary WAV files created during import/enhancement are stored in your chosen temp directory and should be deleted when you close the app (best-effort basis).

We **do not** collect, store, or transmit:

- Your audio files
- Your generated subtitles
- Any personally identifiable information (except what Google provides during OAuth login if you use Online mode)

---

## 5. Open-Source Components & Third-Party Services

NotyCaption uses the following third-party libraries and services:

- **OpenAI Whisper** (MIT License)
- **Spleeter** (MIT License)
- **PyQt5** (GPLv3)
- **pysrt**, **pysubs2**, **moviepy**, etc.
- **Google Drive API** & **Google Colab** (when using Online mode)

You are subject to the licenses and terms of these third-party components.

---

## 6. No Warranty – Provided "AS IS"

THE APP IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, ACCURACY OF TRANSCRIPTION, TIMELINESS, OR RELIABILITY.

We do **not** guarantee:

- 100% accurate speech-to-text transcription
- Perfect audio–subtitle sync
- That Online mode will always succeed (Colab quotas, network issues, etc.)
- That temporary files will always be perfectly cleaned from Google Drive

---

## 7. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY LAW, **NotY215** SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING LOSS OF PROFITS, DATA, GOODWILL, OR OTHER INTANGIBLE LOSSES, ARISING FROM OR RELATED TO YOUR USE OF THE APP.

Our total liability shall not exceed **₹100 INR** (one hundred Indian rupees).

---

## 8. Termination

We may terminate or suspend your access to the App (including Online mode features) at any time, without notice or liability, for any reason, including if you breach these Terms.

---

## 9. Changes to Terms

We may update these Terms from time to time.  
The updated version will be available inside the App (or on a link provided in future versions).  
Continued use of the App after changes constitutes acceptance of the revised Terms.

---

## 10. Governing Law & Jurisdiction

These Terms shall be governed by the laws of **India**.  
Any dispute arising out of or in connection with these Terms shall be subject to the exclusive jurisdiction of the courts located in **Patna, Bihar, India**.

---

## 11. Contact

For questions about these Terms, please contact:

**Developer:** NotY215

---

**By using NotyCaption you acknowledge that you have read, understood, and agree to be bound by these Terms and Conditions.**

Thank you for using NotyCaption!

© 2025–2026 NotY215. All rights reserved.