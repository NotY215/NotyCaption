# online.py
# Handles online mode for NotyCaption (Colab Whisper generator)

import os
import json
from datetime import timedelta
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
import webbrowser
import pysrt
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ==============================
# MAIN ONLINE HANDLER
# ==============================
def handle_online(self, audio_to_use, lang_code, task, wpl, fmt, base, out_path):

    if not self.service:
        QMessageBox.warning(self, "Error", "Please login with Google first.")
        return False

    try:
        # Check for existing output and prompt to overwrite
        self.poll_output_name = f"{base}_captions{fmt}"
        query = f"name='{self.poll_output_name}' and trashed=false"
        results = self.service.files().list(q=query, fields="files(id,name)").execute()
        files = results.get("files", [])
        if files:
            reply = QMessageBox.question(self, "File Exists", f"{self.poll_output_name} already exists in Drive.\nOverwrite?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return False
            for f in files:
                self.service.files().delete(fileId=f["id"]).execute()

        # Delete old notebooks to avoid clutter
        query = "name='NotyCaption_Generator.ipynb' and trashed=false"
        results = self.service.files().list(q=query, fields="files(id)").execute()
        for f in results.get("files", []):
            self.service.files().delete(fileId=f["id"]).execute()

        # Upload audio
        uploads_id = get_or_create_folder(self.service, "uploads")
        audio_filename = os.path.basename(audio_to_use)
        audio_id = upload_file(self.service, audio_to_use, audio_filename, uploads_id)

        query = f"name='{audio_filename}' and '{uploads_id}' in parents and trashed=false"
        results = self.service.files().list(q=query).execute()
        if not results.get("files", []):
            raise Exception("Audio upload failed - file not found in Drive.")

        # Generate notebook
        notebook_content = generate_notebook_content(
            audio_filename,
            wpl,
            fmt,
            self.poll_output_name,
            lang_code,
            task
        )

        temp_ipynb = "NotyCaption_Generator.ipynb"
        with open(temp_ipynb, "w", encoding="utf-8") as f:
            json.dump(notebook_content, f, indent=2)

        notebook_id = upload_file(self.service, temp_ipynb, temp_ipynb)
        os.remove(temp_ipynb)

        colab_url = f"https://colab.research.google.com/drive/{notebook_id}"
        webbrowser.open(colab_url)

        QMessageBox.information(
            self,
            "Colab Opened",
            "Notebook opened in browser.\n\n"
            "Wait 60 seconds → then Runtime → Run All.\n"
            "After completion, app auto-downloads result."
        )

        self.poll_audio_id = audio_id
        self.poll_notebook_id = notebook_id
        self.poll_local_out = out_path

        self.poll_timer.stop()
        try:
            self.poll_timer.timeout.disconnect()
        except TypeError:
            pass
        self.poll_timer.timeout.connect(lambda: poll_for_output(self))
        self.poll_timer.start(8000)

    except Exception as e:
        QMessageBox.critical(self, "Online Mode Failed", str(e))
        return False

    return True


# ==============================
# DRIVE HELPERS
# ==============================
def get_or_create_folder(service, name):
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]

    metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder.get("id")


def upload_file(service, filepath, filename, parent_id=None):
    metadata = {"name": filename}
    if parent_id:
        metadata["parents"] = [parent_id]

    media = MediaFileUpload(filepath, resumable=True)
    file = service.files().create(body=metadata, media_body=media, fields="id").execute()
    return file.get("id")


# ==============================
# NOTEBOOK GENERATOR
# ==============================
def generate_notebook_content(audio_filename, words_per_line, fmt, output_name, lang_code='en', task='transcribe'):

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
            "language_info": {"name": "python"}
        },
        "cells": [

            code_cell([
                "%%capture\n",
                "!apt update -qq\n",
                "!apt install -y ffmpeg -qq\n",
                "!pip install -q openai-whisper\n",
                "!pip install -q pysrt pysubs2\n",
                "print('Dependencies installed')"
            ]),

            code_cell([
                "from google.colab import drive\n",
                "drive.mount('/content/drive', force_remount=True)\n"
            ]),

            code_cell([
                "import whisper\n",
                "import pysrt\n",
                "import pysubs2\n",
                "from datetime import timedelta\n",
                "import os\n"
            ]),

            code_cell([
                "model_name = 'medium'\n",
                "print('Loading model...')\n",
                "model = whisper.load_model(model_name)\n",
                "print('Model ready')\n"
            ]),

            code_cell([
                f"audio_path = '/content/drive/My Drive/uploads/{audio_filename}'\n",
                "import os\n",
                "if not os.path.exists(audio_path):\n",
                "    raise FileNotFoundError(f'Audio file not found at {audio_path}. Ensure Drive is mounted and file is uploaded.')\n",
                "else:\n",
                "    print('Audio file found successfully')\n"
            ]),

            code_cell([
                f"result = model.transcribe(\n",
                "    audio_path,\n",
                f"    language='{lang_code}',\n",
                f"    task='{task}',\n",
                "    word_timestamps=True\n",
                ")\n"
            ]),

            code_cell([
                "subtitles = []\n",
                "idx = 1\n",
                "for seg in result['segments']:\n",
                "    words = seg.get('words', [])\n",
                "    if not words: continue\n",
                f"    for i in range(0, len(words), {words_per_line}):\n",
                f"        chunk = words[i:i+{words_per_line}]\n",
                "        text = ' '.join([w['word'].strip() for w in chunk])\n",
                "        start = chunk[0]['start']\n",
                "        end = chunk[-1]['end']\n",
                "        subtitles.append((idx, start, end, text))\n",
                "        idx += 1\n"
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
                "else:\n",
                "    ass = pysubs2.SSAFile()\n",
                "    for idx, start, end, text in subtitles:\n",
                "        event = pysubs2.SSAEvent(\n",
                "            start=int(start*1000),\n",
                "            end=int(end*1000),\n",
                "            text=text\n",
                "        )\n",
                "        ass.events.append(event)\n",
                "    ass.save(output_path)\n",
                f"print('Saved to Drive as: {output_name}')\n"
            ])
        ]
    }

    return notebook


# ==============================
# POLLING FOR OUTPUT
# ==============================
def poll_for_output(self):

    query = f"name='{self.poll_output_name}' and trashed=false"
    try:
        results = self.service.files().list(q=query, fields="files(id,name)").execute()
    except Exception as e:
        return

    files = results.get("files", [])

    if not files:
        return

    file_id = files[0]["id"]

    try:
        with open(self.poll_local_out, "wb") as f:
            request = self.service.files().get_media(fileId=file_id)
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
    except Exception as e:
        return

    # Load to preview
    self.load_downloaded_subtitles(self.poll_local_out)

    # Cleanup
    try: self.service.files().delete(fileId=self.poll_audio_id).execute()
    except: pass
    try: self.service.files().delete(fileId=self.poll_notebook_id).execute()
    except: pass
    try: self.service.files().delete(fileId=file_id).execute()
    except: pass

    self.poll_timer.stop()
    self.is_generating = False
    self.gen_btn.setEnabled(True)

    QMessageBox.information(
        self,
        "Success",
        f"Subtitles downloaded and loaded:\n{self.poll_local_out}"
    )


def empty_uploads(service):
    uploads_id = get_or_create_folder(service, "uploads")
    query = f"'{uploads_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    for f in results.get("files", []):
        try:
            service.files().delete(fileId=f["id"]).execute()
        except:
            pass

def delete_temp_notebooks(service):
    query = "name='NotyCaption_Generator.ipynb' and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    for f in results.get("files", []):
        try:
            service.files().delete(fileId=f["id"]).execute()
        except:
            pass