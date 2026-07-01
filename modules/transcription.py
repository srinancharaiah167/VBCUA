import os
import ssl
import whisper
import imageio_ffmpeg

# Fix SSL issue if Whisper model download is needed
ssl._create_default_https_context = ssl._create_unverified_context

# Make ffmpeg available to Whisper
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_path)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

_model = None

def load_whisper_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model

def transcribe_audio(audio_path):
    model = load_whisper_model()
    result = model.transcribe(audio_path)
    return result["text"]