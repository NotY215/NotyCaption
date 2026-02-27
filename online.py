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

        notebook_content = generate_notebook_content(audio_filename, lang_code, task, wpl, fmt, f"{base}_captions{fmt}")

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
                                "Colab notebook opened.\n"
                                "Run cells one by one or Runtime > Run all.\n"
                                "App will poll for result every 8 seconds.")

        self.poll_audio_id = audio_id
        self.poll_notebook_id = notebook_id
        self.poll_output_name = f"{base}_captions{fmt}"
        self.poll_local_out = out_path

        self.poll_timer.timeout.connect(lambda: poll_for_output(self))
        self.poll_timer.start(8000)

    except Exception as e:
        QMessageBox.critical(self, "Online Failed", f"Error: {str(e)}")
        return False

    return True

def get_or_create_folder(service, name):
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    if files:
        return files[0]['id']
    metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=metadata, fields='id').execute()
    return file.get('id')

def upload_file(service, filepath, filename, parent_id=None):
    metadata = {'name': filename}
    if parent_id:
        metadata['parents'] = [parent_id]
    media = MediaFileUpload(filepath, resumable=True)
    file = service.files().create(body=metadata, media_body=media, fields='id').execute()
    return file.get('id')

def generate_notebook_content(filename, lang_code, task, wpl, fmt, output_name):
    cells = []

    # Cell 1: Install packages with %%capture to reduce output
    cells.append({
        "cell_type": "code",
        "source": [
            "%%capture\n",
            "!pip install --quiet openai-whisper==20231117\n",
            "!pip install --quiet pysrt pysubs2"
        ]
    })

    # Cell 2: Mount Drive
    cells.append({
        "cell_type": "code",
        "source": [
            "from google.colab import drive\n",
            "drive.mount('/content/drive', force_remount=True)\n",
            "print('Drive mounted')"
        ]
    })

    # Cell 3: Imports
    cells.append({
        "cell_type": "code",
        "source": [
            "import whisper\n",
            "import pysrt\n",
            "import pysubs2\n",
            "from datetime import timedelta\n",
            "print('Imports complete')"
        ]
    })

    # Cell 4: Load model with try-except
    cells.append({
        "cell_type": "code",
        "source": [
            "try:\n",
            "    model = whisper.load_model('large-v3')\n",
            "    print('Model loaded successfully')\n",
            "except Exception as e:\n",
            "    print(f'Error loading model: {str(e)}')\n",
            "    raise"
        ]
    })

    # Cell 5: Transcription with try-except
    cells.append({
        "cell_type": "code",
        "source": [
            "try:\n",
            f"    audio_path = '/content/drive/My Drive/uploads/{filename}'\n",
            "    print(f'Starting transcription for {audio_path}')\n",
            f"    result = model.transcribe(audio_path, language='{lang_code}', task='{task}', verbose=True, word_timestamps=True)\n",
            "    print('Transcription complete')\n",
            "except Exception as e:\n",
            "    print(f'Transcription error: {str(e)}')\n",
            "    raise"
        ]
    })

    # Cell 6: Process subtitles
    cells.append({
        "cell_type": "code",
        "source": [
            "subtitles = []\n",
            "idx = 1\n",
            "for seg in result.get('segments', []):\n",
            "    txt = seg.get('text', '').strip()\n",
            "    if not txt: continue\n",
            "    s = seg.get('start', 0)\n",
            "    e = seg.get('end', s + 1)\n",
            "    words = seg.get('words', [])\n",
            "    if words:\n",
            "        w_txt = [w['word'].strip() for w in words]\n",
            "        w_s = [w.get('start', s) for w in words]\n",
            "        w_e = [w.get('end', e) for w in words]\n",
            "    else:\n",
            "        w_txt = txt.split()\n",
            "        dur = e - s\n",
            "        w_s = [s + i * dur / max(1, len(w_txt)) for i in range(len(w_txt))]\n",
            "        w_e = w_s[1:] + [e]\n",
            f"    for i in range(0, len(w_txt), {wpl}):\n",
            "        chunk = w_txt[i:i + {wpl}]\n",
            "        line = ' '.join(chunk).strip()\n",
            "        if not line: continue\n",
            "        st = w_s[i]\n",
            "        en = w_e[min(i + {wpl} - 1, len(w_e) - 1)]\n",
            "        subtitles.append({\n",
            "            'index': idx,\n",
            "            'start': timedelta(seconds=st),\n",
            "            'end': timedelta(seconds=en),\n",
            "            'text': line\n",
            "        })\n",
            "        idx += 1\n",
            "print(f'Processed {len(subtitles)} lines')"
        ]
    })

    # Cell 7: Save file with try-except
    cells.append({
        "cell_type": "code",
        "source": [
            "try:\n",
            f"    output_path = '/content/drive/My Drive/{output_name}'\n",
            f"    fmt = '{fmt}'\n",
            "    if fmt == '.srt':\n",
            "        srt = pysrt.SubRipFile()\n",
            "        for s in subtitles:\n",
            "            item = pysrt.SubRipItem(\n",
            "                index=s['index'],\n",
            "                start=pysrt.SubRipTime.from_ordinal(s['start'].total_seconds()*1000),\n",
            "                end=pysrt.SubRipTime.from_ordinal(s['end'].total_seconds()*1000),\n",
            "                text=s['text']\n",
            "            )\n",
            "            srt.append(item)\n",
            "        srt.save(output_path, encoding='utf-8')\n",
            "    else:\n",
            "        ass = pysubs2.SSAFile()\n",
            "        for s in subtitles:\n",
            "            ev = pysubs2.SSAEvent(\n",
            "                start=int(s['start'].total_seconds()*1000),\n",
            "                end=int(s['end'].total_seconds()*1000),\n",
            "                text=s['text']\n",
            "            )\n",
            "            ass.events.append(ev)\n",
            "        ass.save(output_path)\n",
            "    print(f'Saved to {output_name} in My Drive. Process complete!')\n",
            "except Exception as e:\n",
            "    print(f'Save error: {str(e)}')\n",
            "    raise"
        ]
    })

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"}
        },
        "cells": cells
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
        # Cleanup
        try:
            self.service.files().delete(fileId=self.poll_audio_id).execute()
            self.service.files().delete(fileId=self.poll_notebook_id).execute()
            self.service.files().delete(fileId=file_id).execute()
        except:
            pass
        self.poll_timer.stop()

        # Load subtitles
        fmt = os.path.splitext(self.poll_output_name)[1]
        if fmt == ".srt":
            srt = pysrt.open(self.poll_local_out)
            self.subtitles = [{
                "index": item.index,
                "start": timedelta(seconds=item.start.ordinal / 1000),
                "end": timedelta(seconds=item.end.ordinal / 1000),
                "text": item.text
            } for item in srt]
            self.display_lines = [item.text for item in srt]
        else:
            ass = pysubs2.load(self.poll_local_out)
            self.subtitles = [{
                "index": i+1,
                "start": timedelta(milliseconds=ev.start),
                "end": timedelta(milliseconds=ev.end),
                "text": ev.text
            } for i, ev in enumerate(ass.events)]
            self.display_lines = [ev.text for ev in ass.events]

        self.caption_edit.setText("\n".join(self.display_lines))
        self.generated = True
        self.edit_btn.setEnabled(True)
        QMessageBox.information(self, "Success", f"Captions downloaded to {self.poll_local_out}")
