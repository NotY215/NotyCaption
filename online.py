# online.py
# Handles online mode for NotyCaption: Drive upload, notebook generation, polling

import os
import json
import shutil
from datetime import timedelta
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from io import FileIO
import pysrt
import pysubs2
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
import webbrowser

def handle_online(self, audio_to_use, lang_code, task, wpl, fmt, base, out_path):
    if not self.service:
        QMessageBox.warning(self, "Error", "Please login with Google first.")
        return False

    try:
        uploads_id = get_or_create_folder(self.service, "uploads")
        audio_filename = os.path.basename(audio_to_use)
        audio_id = upload_file(self.service, audio_to_use, audio_filename, uploads_id)

        notebook_content = generate_notebook_content(audio_filename, wpl, fmt, f"{base}_captions{fmt}")

        temp_dir = self.settings.get("temp_dir", os.path.join(os.path.dirname(__file__), "temp"))
        os.makedirs(temp_dir, exist_ok=True)
        temp_ipynb = os.path.join(temp_dir, "notycaption_generator.ipynb")
        with open(temp_ipynb, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, ensure_ascii=False, indent=2)

        notebook_id = upload_file(self.service, temp_ipynb, "NotyCaption_Generator.ipynb")
        os.remove(temp_ipynb)

        colab_url = f"https://colab.research.google.com/drive/{notebook_id}?authuser=0"
        webbrowser.open(colab_url)

        QMessageBox.information(self, "Colab Started",
                                "Colab notebook opened in browser.\n"
                                "1. Wait 30–60 seconds after opening\n"
                                "2. Click Runtime → Run all (or Ctrl+F9)\n"
                                "3. App will automatically download result when ready.\n\n"
                                "If you see loading error, refresh page or restart runtime.")

        self.poll_audio_id = audio_id
        self.poll_notebook_id = notebook_id
        self.poll_output_name = f"{base}_captions{fmt}"
        self.poll_local_out = out_path

        self.poll_timer.timeout.connect(lambda: poll_for_output(self))
        self.poll_timer.start(8000)  # Poll every 8 seconds

    except Exception as e:
        QMessageBox.critical(self, "Online Mode Failed", f"Setup error:\n{str(e)}")
        return False

    return True


def get_or_create_folder(service, name):
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    if files:
        return files[0]['id']
    metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
    file = service.files().create(body=metadata, fields='id').execute()
    return file.get('id')


def upload_file(service, filepath, filename, parent_id=None):
    metadata = {'name': filename}
    if parent_id:
        metadata['parents'] = [parent_id]
    media = MediaFileUpload(filepath, resumable=True)
    file = service.files().create(body=metadata, media_body=media, fields='id').execute()
    return file.get('id')


def generate_notebook_content(audio_filename, words_per_line, fmt, output_name):

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
        "nbformat_minor": 2,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3"
            },
            "language_info": {"name": "python"}
        },
        "cells": [

            code_cell([
                "# Install packages\n",
                "!pip install --quiet openai-whisper==20231117\n",
                "!pip install --quiet pysrt pysubs2\n",
                "print('Packages installed')"
            ]),

            code_cell([
                "from google.colab import drive\n",
                "drive.mount('/content/drive', force_remount=True)"
            ]),

            code_cell([
                "import whisper\n",
                "import pysrt\n",
                "import pysubs2\n",
                "from datetime import timedelta\n",
                "import os, shutil\n",
                "print('Imports done')"
            ]),

            code_cell([
                f"audio_path = '/content/drive/My Drive/uploads/{audio_filename}'\n",
                f"output_path = '/content/drive/My Drive/{output_name}'\n",
                f"words_per_line = {words_per_line}\n",
                "model_name = 'medium'\n"
            ]),

            code_cell([
                "drive_model_folder = '/content/drive/My Drive/SrtModels'\n",
                "os.makedirs(drive_model_folder, exist_ok=True)\n",
                "drive_model_path = os.path.join(drive_model_folder, f'{model_name}.pt')\n",
                "local_model_path = f'/content/{model_name}.pt'\n",
                "\n",
                "if os.path.exists(drive_model_path):\n",
                "    shutil.copyfile(drive_model_path, local_model_path)\n",
                "else:\n",
                "    model_temp = whisper.load_model(model_name)\n",
                "    shutil.copyfile(f'/root/.cache/whisper/{model_name}.pt', drive_model_path)\n",
                "    shutil.copyfile(f'/root/.cache/whisper/{model_name}.pt', local_model_path)\n",
                "    del model_temp\n",
                "\n",
                "model = whisper.load_model(local_model_path)\n",
                "print('Model ready!')"
            ]),

            code_cell([
                "result = model.transcribe(\n",
                "    audio_path,\n",
                "    language='en',\n",
                "    task='transcribe',\n",
                "    word_timestamps=True\n",
                ")\n",
                "print('Transcription finished')"
            ]),

            code_cell([
                "subtitles = []\n",
                "idx = 1\n",
                "for seg in result.get('segments', []):\n",
                "    txt = seg.get('text', '').strip()\n",
                "    if not txt:\n",
                "        continue\n",
                "    s = seg.get('start', 0)\n",
                "    e = seg.get('end', s + 1)\n",
                "    words = seg.get('words', [])\n",
                "\n",
                "    if words:\n",
                "        w_txt = [w['word'].strip() for w in words]\n",
                "        w_s = [w.get('start', s) for w in words]\n",
                "        w_e = [w.get('end', e) for w in words]\n",
                "    else:\n",
                "        w_txt = txt.split()\n",
                "        dur = e - s\n",
                "        w_s = [s + i * dur / max(1, len(w_txt)) for i in range(len(w_txt))]\n",
                "        w_e = w_s[1:] + [e]\n",
                "\n",
                "    for i in range(0, len(w_txt), words_per_line):\n",
                "        chunk = w_txt[i:i + words_per_line]\n",
                "        line = ' '.join(chunk).strip()\n",
                "        if not line:\n",
                "            continue\n",
                "        st = w_s[i]\n",
                "        en = w_e[min(i + words_per_line - 1, len(w_e) - 1)]\n",
                "        subtitles.append({\n",
                "            'index': idx,\n",
                "            'start': timedelta(seconds=st),\n",
                "            'end': timedelta(seconds=en),\n",
                "            'text': line\n",
                "        })\n",
                "        idx += 1\n",
                "\n",
                "print(f'Generated {len(subtitles)} lines')"
            ]),

            code_cell([
                "srt = pysrt.SubRipFile()\n",
                "for s in subtitles:\n",
                "    item = pysrt.SubRipItem(\n",
                "        index=s['index'],\n",
                "        start=pysrt.SubRipTime(milliseconds=int(s['start'].total_seconds()*1000)),\n",
                "        end=pysrt.SubRipTime(milliseconds=int(s['end'].total_seconds()*1000)),\n",
                "        text=s['text']\n",
                "    )\n",
                "    srt.append(item)\n",
                "\n",
                "srt.save(output_path, encoding='utf-8')\n",
                "print('SRT saved →', output_path)\n",
                "print('Done!')"
            ])
        ]
    }

    return notebook


def poll_for_output(self):
    if not hasattr(self, 'poll_output_name') or not self.poll_output_name:
        return

    query = f"name='{self.poll_output_name}' and trashed=false"
    results = self.service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    if files:
        file_id = files[0]['id']
        with open(self.poll_local_out, 'wb') as f:
            request = self.service.files().get_media(fileId=file_id)
            downloader = MediaIoBaseDownload(FileIO(f), request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

        # Cleanup temporary files (audio + notebook + output)
        try:
            self.service.files().delete(fileId=self.poll_audio_id).execute()
            self.service.files().delete(fileId=self.poll_notebook_id).execute()
            self.service.files().delete(fileId=file_id).execute()
        except:
            pass

        self.poll_timer.stop()

        # Load the downloaded SRT into the app for preview & editing
        srt = pysrt.open(self.poll_local_out)
        self.subtitles = []
        self.display_lines = []
        for item in srt:
            self.subtitles.append({
                "index": item.index,
                "start": timedelta(seconds=item.start.ordinal / 1000.0),
                "end": timedelta(seconds=item.end.ordinal / 1000.0),
                "text": item.text
            })
            self.display_lines.append(item.text)

        self.caption_edit.setText("\n".join(self.display_lines).strip())
        self.generated = True
        self.edit_btn.setEnabled(True)

        QMessageBox.information(self, "Success",
                                f"Subtitles generated remotely and downloaded!\nSaved to:\n{self.poll_local_out}")