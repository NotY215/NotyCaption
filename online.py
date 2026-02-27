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

        colab_url = f"https://colab.research.google.com/drive/{notebook_id}"
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
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"}
        },
        "cells": [
            {
                "cell_type": "code",
                "source": [
                    "# Install packages\n",
                    "!pip install --quiet openai-whisper==20231117\n",
                    "!pip install --quiet pysrt pysubs2\n",
                    "print(\"Packages installed\")"
                ]
            },
            {
                "cell_type": "code",
                "source": [
                    "# Mount Drive\n",
                    "from google.colab import drive\n",
                    "drive.mount('/content/drive', force_remount=True)"
                ]
            },
            {
                "cell_type": "code",
                "source": [
                    "import whisper\n",
                    "import pysrt\n",
                    "import pysubs2\n",
                    "from datetime import timedelta\n",
                    "import os\n",
                    "import shutil\n",
                    "print(\"Imports done\")"
                ]
            },
            {
                "cell_type": "code",
                "source": [
                    "# ---------------- SETTINGS ----------------\n",
                    "model_name = \"medium\"\n",  # Changed to medium for faster/safer loading
                    f"audio_path = \"/content/drive/My Drive/uploads/{audio_filename}\"\n",
                    f"output_path = \"/content/drive/My Drive/{output_name}\"\n",
                    f"words_per_line = {words_per_line}  # change this to control subtitle chunk size\n",
                    "# ------------------------------------------"
                ]
            },
            {
                "cell_type": "code",
                "source": [
                    "# Model storage paths\n",
                    "drive_model_folder = \"/content/drive/My Drive/SrtModels\"\n",
                    "os.makedirs(drive_model_folder, exist_ok=True)\n",
                    "drive_model_path = os.path.join(drive_model_folder, f\"{model_name}.pt\")\n",
                    "local_model_path = f\"/content/{model_name}.pt\"\n",
                    "# Download model only once\n",
                    "if os.path.exists(drive_model_path):\n",
                    "    print(\"Found model in Drive → copying to Colab...\")\n",
                    "    shutil.copyfile(drive_model_path, local_model_path)\n",
                    "else:\n",
                    "    print(\"Model not found in Drive → downloading...\")\n",
                    "    model_temp = whisper.load_model(model_name)\n",
                    "    shutil.copyfile(\n",
                    "        f\"/root/.cache/whisper/{model_name}.pt\",\n",
                    "        drive_model_path\n",
                    "    )\n",
                    "    shutil.copyfile(\n",
                    "        f\"/root/.cache/whisper/{model_name}.pt\",\n",
                    "        local_model_path\n",
                    "    )\n",
                    "    del model_temp\n",
                    "print(\"Loading model...\")\n",
                    "model = whisper.load_model(local_model_path)\n",
                    "print(\"Model ready!\")"
                ]
            },
            {
                "cell_type": "code",
                "source": [
                    "# Transcribe\n",
                    "print(f\"Transcribing: {audio_path}\")\n",
                    "result = model.transcribe(\n",
                    "    audio_path,\n",
                    "    language=\"en\",\n",
                    "    task=\"transcribe\",\n",
                    "    verbose=True,\n",
                    "    word_timestamps=True\n",
                    ")\n",
                    "print(\"Transcription finished\")"
                ]
            },
            {
                "cell_type": "code",
                "source": [
                    "# Generate subtitles\n",
                    "subtitles = []\n",
                    "idx = 1\n",
                    "for seg in result.get(\"segments\", []):\n",
                    "    text = seg.get(\"text\", \"\").strip()\n",
                    "    if not text:\n",
                    "        continue\n",
                    "    start = seg.get(\"start\", 0)\n",
                    "    end = seg.get(\"end\", start + 1)\n",
                    "    words = seg.get(\"words\", [])\n",
                    "    if words:\n",
                    "        word_texts = [w[\"word\"].strip() for w in words]\n",
                    "        word_starts = [w.get(\"start\", start) for w in words]\n",
                    "        word_ends = [w.get(\"end\", end) for w in words]\n",
                    "    else:\n",
                    "        word_texts = text.split()\n",
                    "        duration = end - start\n",
                    "        word_starts = [\n",
                    "            start + i * duration / max(1, len(word_texts))\n",
                    "            for i in range(len(word_texts))\n",
                    "        ]\n",
                    "        word_ends = word_starts[1:] + [end]\n",
                    "    for i in range(0, len(word_texts), words_per_line):\n",
                    "        chunk = word_texts[i:i + words_per_line]\n",
                    "        line = \" \".join(chunk).strip()\n",
                    "        if not line:\n",
                    "            continue\n",
                    "        st = word_starts[i]\n",
                    "        en = word_ends[min(i + words_per_line - 1, len(word_ends) - 1)]\n",
                    "        subtitles.append({\n",
                    "            \"index\": idx,\n",
                    "            \"start\": timedelta(seconds=st),\n",
                    "            \"end\": timedelta(seconds=en),\n",
                    "            \"text\": line\n",
                    "        })\n",
                    "        idx += 1\n",
                    "print(f\"Generated {len(subtitles)} subtitle lines\")"
                ]
            },
            {
                "cell_type": "code",
                "source": [
                    "# Save SRT\n",
                    "srt = pysrt.SubRipFile()\n",
                    "for s in subtitles:\n",
                    "    item = pysrt.SubRipItem(\n",
                    "        index=s[\"index\"],\n",
                    "        start=pysrt.SubRipTime(milliseconds=int(s[\"start\"].total_seconds()*1000)),\n",
                    "        end=pysrt.SubRipTime(milliseconds=int(s[\"end\"].total_seconds()*1000)),\n",
                    "        text=s[\"text\"]\n",
                    "    )\n",
                    "    srt.append(item)\n",
                    "srt.save(output_path, encoding=\"utf-8\")\n",
                    "print(f\"SRT saved → {output_path}\")\n",
                    "print(\"\\nDone! You can close this tab now.\")"
                ]
            }
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