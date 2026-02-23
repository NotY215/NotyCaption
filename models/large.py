# models/large.py
import whisper

def transcribe_audio(audio_file):
    model = whisper.load_model("large")
    return model.transcribe(audio_file, word_timestamps=True)