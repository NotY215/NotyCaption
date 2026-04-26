// ========================================
// NotyCaption Pro - Notebook Builder
// ========================================

const NOTEBOOK_TEMPLATES = {
    captionGeneration: `{
 "nbformat": 4,
 "nbformat_minor": 0,
 "metadata": {
  "colab": {
   "provenance": [],
   "toc_visible": true,
   "gpuType": "T4"
  },
  "kernelspec": {
   "display_name": "Python 3",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "header_cell"
   },
   "source": [
    "# 🎬 NotyCaption Pro - AI Caption Generator\\n",
    "\\n",
    "This notebook will generate professional subtitles for your media file using OpenAI's Whisper AI.\\n",
    "\\n",
    "**Features:**\\n",
    "- 🎯 High accuracy transcription\\n",
    "- ⏱️ Word-level timestamps\\n",
    "- 📝 Smart line breaking\\n",
    "- 🌍 Multi-language support\\n"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "install_deps"
   },
   "source": [
    "# Install required packages\\n",
    "!apt-get update -qq && apt-get install -y ffmpeg -qq\\n",
    "!pip install -q openai-whisper pysrt pysubs2 google-auth google-auth-oauthlib google-api-python-client\\n",
    "\\n",
    "print(\"✅ Dependencies installed successfully\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "mount_drive"
   },
   "source": [
    "# Mount Google Drive\\n",
    "from google.colab import drive\\n",
    "drive.mount('/content/drive', force_remount=True)\\n",
    "print(\"✅ Drive mounted successfully\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "setup_drive_api"
   },
   "source": [
    "# Setup Drive API\\n",
    "from google.auth import default\\n",
    "from googleapiclient.discovery import build\\n",
    "from googleapiclient.http import MediaIoBaseDownload\\n",
    "import io\\n",
    "\\n",
    "creds, _ = default()\\n",
    "drive_service = build('drive', 'v3', credentials=creds)\\n",
    "print(\"✅ Drive API initialized\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "download_audio"
   },
   "source": [
    "# Configuration\\n",
    "AUDIO_ID = \"{{AUDIO_ID}}\"\\n",
    "LANGUAGE = \"{{LANGUAGE}}\\n",
    "WORDS_PER_LINE = {{WORDS_PER_LINE}}\\n",
    "OUTPUT_FORMAT = \"{{OUTPUT_FORMAT}}\\n",
    "OPERATION_ID = \"{{OPERATION_ID}}\\n",
    "\\n",
    "print(f\"📁 Audio ID: {AUDIO_ID}\")\\n",
    "print(f\"🌍 Language: {LANGUAGE if LANGUAGE != 'auto' else 'Auto Detect'}\")\\n",
    "print(f\"📝 Words per line: {WORDS_PER_LINE}\")\\n",
    "print(f\"📄 Output format: {OUTPUT_FORMAT}\")\\n",
    "\\n",
    "# Download audio file from Drive\\n",
    "def download_file(file_id, destination):\\n",
    "    request = drive_service.files().get_media(fileId=file_id)\\n",
    "    fh = io.FileIO(destination, 'wb')\\n",
    "    downloader = MediaIoBaseDownload(fh, request)\\n",
    "    done = False\\n",
    "    while not done:\\n",
    "        status, done = downloader.next_chunk()\\n",
    "        if status:\\n",
    "            print(f\"⬇️ Downloaded: {int(status.progress() * 100)}%\")\\n",
    "    print(f\"✅ Audio downloaded to {destination}\")\\n",
    "\\n",
    "audio_path = f\"/content/audio_{OPERATION_ID}.wav\"\\n",
    "download_file(AUDIO_ID, audio_path)\\n",
    "print(f\"🎵 Audio file ready: {audio_path}\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "whisper_transcribe"
   },
   "source": [
    "# Transcribe with Whisper AI\\n",
    "import whisper\\n",
    "\\n",
    "print(\"🎤 Loading Whisper model...\")\\n",
    "model = whisper.load_model(\"large-v3-turbo\")\\n",
    "\\n",
    "print(\"🎙️ Transcribing audio...\")\\n",
    "if LANGUAGE == 'auto':\\n",
    "    result = model.transcribe(audio_path, word_timestamps=True)\\n",
    "else:\\n",
    "    result = model.transcribe(audio_path, language=LANGUAGE, word_timestamps=True)\\n",
    "\\n",
    "print(f\"✅ Transcription complete! Found {len(result['segments'])} segments\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "generate_subtitles"
   },
   "source": [
    "# Generate subtitles with word-level timing\\n",
    "subtitles = []\\n",
    "idx = 1\\n",
    "\\n",
    "for seg in result['segments']:\\n",
    "    words = seg.get('words', [])\\n",
    "    for i in range(0, len(words), WORDS_PER_LINE):\\n",
    "        chunk = words[i:i+WORDS_PER_LINE]\\n",
    "        if not chunk:\\n",
    "            continue\\n",
    "        text = ' '.join([w['word'].strip() for w in chunk])\\n",
    "        start = chunk[0]['start']\\n",
    "        end = chunk[-1]['end']\\n",
    "        subtitles.append((idx, start, end, text))\\n",
    "        idx += 1\\n",
    "\\n",
    "print(f\"📝 Generated {len(subtitles)} subtitle lines\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "save_subtitles"
   },
   "source": [
    "# Save subtitles to file\\n",
    "output_path = f\"/content/captions_{OPERATION_ID}.{OUTPUT_FORMAT}\"\\n",
    "\\n",
    "if OUTPUT_FORMAT == \"srt\":\\n",
    "    import pysrt\\n",
    "    srt = pysrt.SubRipFile()\\n",
    "    for i, s, e, t in subtitles:\\n",
    "        srt.append(pysrt.SubRipItem(\\n",
    "            index=i,\\n",
    "            start=pysrt.SubRipTime(milliseconds=int(s*1000)),\\n",
    "            end=pysrt.SubRipTime(milliseconds=int(e*1000)),\\n",
    "            text=t\\n",
    "        ))\\n",
    "    srt.save(output_path)\\n",
    "else:\\n",
    "    import pysubs2\\n",
    "    ass = pysubs2.SSAFile()\\n",
    "    for i, s, e, t in subtitles:\\n",
    "        ass.events.append(pysubs2.SSAEvent(\\n",
    "            start=int(s*1000),\\n",
    "            end=int(e*1000),\\n",
    "            text=t\\n",
    "        ))\\n",
    "    ass.save(output_path)\\n",
    "\\n",
    "print(f\"💾 Subtitles saved to {output_path}\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "upload_results"
   },
   "source": [
    "# Upload results back to Google Drive\\n",
    "from googleapiclient.http import MediaFileUpload\\n",
    "\\n",
    "# Create output folder\\n",
    "folder_name = \"NotyCaption_Output\"\\n",
    "query = f\"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false\"\\n",
    "response = drive_service.files().list(q=query, fields=\"files(id, name)\").execute()\\n",
    "\\n",
    "if response.get('files'):\\n",
    "    folder_id = response['files'][0]['id']\\n",
    "else:\\n",
    "    folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}\\n",
    "    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()\\n",
    "    folder_id = folder['id']\\n",
    "\\n",
    "# Upload subtitle file\\n",
    "file_metadata = {'name': f'captions_{OPERATION_ID}.{OUTPUT_FORMAT}', 'parents': [folder_id]}\\n",
    "media = MediaFileUpload(output_path, mimetype='text/plain', resumable=True)\\n",
    "uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()\\n",
    "\\n",
    "print(f\"✅ Subtitle file uploaded: https://drive.google.com/file/d/{uploaded_file['id']}\")\\n",
    "\\n",
    "# Store result for callback\\n",
    "result = {\\n",
    "    'success': True,\\n",
    "    'file_id': uploaded_file['id'],\\n",
    "    'file_name': f'captions_{OPERATION_ID}.{OUTPUT_FORMAT}',\\n",
    "    'operation_id': OPERATION_ID\\n",
    "}\\n",
    "\\n",
    "import json\\n",
    "from IPython.display import display, Javascript\\n",
    "\\n",
    "# Send result back to web app\\n",
    "js_code = f'''\\n",
    "sessionStorage.setItem('colab_result_{OPERATION_ID}', '{json.dumps(result)}');\\n",
    "console.log('✅ Result saved to sessionStorage');\\n",
    "'''\\n",
    "display(Javascript(js_code))\\n",
    "\\n",
    "print(\"🎉 All done! You can close this tab.\")"
   ],
   "execution_count": null,
   "outputs": []
  }
 ]
}`,

    vocalEnhancement: `{
 "nbformat": 4,
 "nbformat_minor": 0,
 "metadata": {
  "colab": {
   "provenance": [],
   "toc_visible": true,
   "gpuType": "T4"
  },
  "kernelspec": {
   "display_name": "Python 3",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "header_cell"
   },
   "source": [
    "# 🎤 NotyCaption Pro - Vocal Enhancement\\n",
    "\\n",
    "This notebook extracts vocals from your audio file using Spleeter AI.\\n",
    "\\n",
    "**Features:**\\n",
    "- 🎵 Remove background music\\n",
    "- 🎙️ Extract clean vocals\\n",
    "- 📊 2-stem separation (vocals + accompaniment)\\n"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "install_deps"
   },
   "source": [
    "# Install required packages\\n",
    "!apt-get update -qq && apt-get install -y ffmpeg -qq\\n",
    "!pip install -q spleeter google-auth google-api-python-client\\n",
    "\\n",
    "print(\"✅ Dependencies installed\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "mount_drive"
   },
   "source": [
    "# Mount Google Drive\\n",
    "from google.colab import drive\\n",
    "drive.mount('/content/drive', force_remount=True)\\n",
    "print(\"✅ Drive mounted\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "setup_drive_api"
   },
   "source": [
    "# Setup Drive API\\n",
    "from google.auth import default\\n",
    "from googleapiclient.discovery import build\\n",
    "from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload\\n",
    "import io\\n",
    "\\n",
    "creds, _ = default()\\n",
    "drive_service = build('drive', 'v3', credentials=creds)\\n",
    "print(\"✅ Drive API ready\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "download_audio"
   },
   "source": [
    "# Download audio file\\n",
    "AUDIO_ID = \"{{AUDIO_ID}}\\n",
    "OPERATION_ID = \"{{OPERATION_ID}}\\n",
    "\\n",
    "def download_file(file_id, destination):\\n",
    "    request = drive_service.files().get_media(fileId=file_id)\\n",
    "    fh = io.FileIO(destination, 'wb')\\n",
    "    downloader = MediaIoBaseDownload(fh, request)\\n",
    "    done = False\\n",
    "    while not done:\\n",
    "        status, done = downloader.next_chunk()\\n",
    "    print(f\"✅ Downloaded to {destination}\")\\n",
    "\\n",
    "audio_path = f\"/content/audio_{OPERATION_ID}.wav\"\\n",
    "download_file(AUDIO_ID, audio_path)\\n",
    "print(f\"🎵 Audio ready: {audio_path}\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "spleeter_separate"
   },
   "source": [
    "# Extract vocals with Spleeter\\n",
    "from spleeter.separator import Separator\\n",
    "\\n",
    "print(\"🎤 Loading Spleeter model...\")\\n",
    "separator = Separator('spleeter:2stems')\\n",
    "\\n",
    "print(\"🎵 Separating vocals from accompaniment...\")\\n",
    "separator.separate_to_file(audio_path, \"/content/output\")\\n",
    "\\n",
    "print(\"✅ Vocal extraction complete!\")"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "id": "upload_results"
   },
   "source": [
    "# Upload enhanced vocals to Drive\\n",
    "vocals_path = f\"/content/output/audio_{OPERATION_ID}/vocals.wav\"\\n",
    "\\n",
    "# Create folder\\n",
    "folder_name = \"NotyCaption_Enhanced\"\\n",
    "query = f\"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false\"\\n",
    "response = drive_service.files().list(q=query, fields=\"files(id, name)\").execute()\\n",
    "\\n",
    "if response.get('files'):\\n",
    "    folder_id = response['files'][0]['id']\\n",
    "else:\\n",
    "    folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}\\n",
    "    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()\\n",
    "    folder_id = folder['id']\\n",
    "\\n",
    "# Upload file\\n",
    "file_metadata = {'name': f'vocals_{OPERATION_ID}.wav', 'parents': [folder_id]}\\n",
    "media = MediaFileUpload(vocals_path, mimetype='audio/wav', resumable=True)\\n",
    "uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()\\n",
    "\\n",
    "print(f\"✅ Enhanced vocals uploaded: https://drive.google.com/file/d/{uploaded_file['id']}\")\\n",
    "\\n",
    "# Store result\\n",
    "import json\\n",
    "from IPython.display import display, Javascript\\n",
    "\\n",
    "result = {\\n",
    "    'success': True,\\n",
    "    'file_id': uploaded_file['id'],\\n",
    "    'file_name': f'vocals_{OPERATION_ID}.wav',\\n",
    "    'operation_id': OPERATION_ID\\n",
    "}\\n",
    "\\n",
    "js_code = f'''\\n",
    "sessionStorage.setItem('colab_result_{OPERATION_ID}', '{json.dumps(result)}');\\n",
    "console.log('✅ Result saved');\\n",
    "'''\\n",
    "display(Javascript(js_code))\\n",
    "\\n",
    "print(\"🎉 All done! You can close this tab.\")"
   ],
   "execution_count": null,
   "outputs": []
  }
 ]
}`
};

function createNotebookFromTemplate(templateType, params) {
    let template = NOTEBOOK_TEMPLATES[templateType];
    if (!template) {
        throw new Error(`Unknown template type: ${templateType}`);
    }
    
    // Replace placeholders
    let notebookJson = template
        .replace(/\{\{AUDIO_ID\}\}/g, params.audioId)
        .replace(/\{\{LANGUAGE\}\}/g, params.language || 'en')
        .replace(/\{\{WORDS_PER_LINE\}\}/g, params.wordsPerLine || '5')
        .replace(/\{\{OUTPUT_FORMAT\}\}/g, params.outputFormat || 'srt')
        .replace(/\{\{OPERATION_ID\}\}/g, params.operationId);
    
    return JSON.parse(notebookJson);
}

function getNotebookContent(operationType, params) {
    const templateType = operationType === 'enhance' ? 'vocalEnhancement' : 'captionGeneration';
    const notebook = createNotebookFromTemplate(templateType, params);
    return JSON.stringify(notebook);
}

// Export functions
window.getNotebookContent = getNotebookContent;
window.createNotebookFromTemplate = createNotebookFromTemplate;