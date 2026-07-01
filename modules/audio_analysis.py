import os
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


def load_audio_safely(audio_path):
    try:
        y, sr = sf.read(audio_path)

        if len(y.shape) > 1:
            y = np.mean(y, axis=1)

        y = np.asarray(y, dtype=np.float32)

        if len(y) == 0:
            y, sr = librosa.load(audio_path, sr=None, mono=True)

    except Exception:
        y, sr = librosa.load(audio_path, sr=None, mono=True)

    return y, sr


def extract_audio_features(audio_path):
    y, sr = load_audio_safely(audio_path)

    if y is None or len(y) == 0:
        return {
            "duration": 0,
            "avg_rms": 0,
            "pause_ratio": 0,
            "confidence_level": "Audio not detected properly"
        }

    duration = librosa.get_duration(y=y, sr=sr)

    if duration <= 0:
        return {
            "duration": 0,
            "avg_rms": 0,
            "pause_ratio": 0,
            "confidence_level": "Audio not detected properly"
        }

    rms_values = librosa.feature.rms(y=y)[0]

    if len(rms_values) == 0:
        avg_rms = 0
        pause_ratio = 0
    else:
        avg_rms = float(np.mean(rms_values))
        silence_threshold = avg_rms * 0.5
        silent_frames = rms_values < silence_threshold
        pause_ratio = float(np.sum(silent_frames) / len(rms_values))

    if avg_rms >= 0.05:
        confidence_level = "High Voice Energy"
    elif avg_rms >= 0.02:
        confidence_level = "Moderate Voice Energy"
    elif avg_rms > 0:
        confidence_level = "Low Voice Energy"
    else:
        confidence_level = "Audio not detected properly"

    return {
        "duration": round(duration, 2),
        "avg_rms": round(avg_rms, 4),
        "pause_ratio": round(pause_ratio * 100, 2),
        "confidence_level": confidence_level
    }


def generate_waveform(audio_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    y, sr = load_audio_safely(audio_path)

    if y is None or len(y) == 0:
        return None

    duration = librosa.get_duration(y=y, sr=sr)

    if duration <= 0:
        return None

    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title("Audio Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path