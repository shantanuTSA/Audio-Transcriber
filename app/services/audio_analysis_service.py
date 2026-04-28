import librosa
import numpy as np


def analyze_audio(file_path):
    y, sr = librosa.load(file_path, sr=16000)

    duration = librosa.get_duration(y=y, sr=sr)

    # Simple energy-based quality
    energy = np.mean(np.abs(y))

    if energy < 0.01:
        quality = "low"
    elif energy < 0.03:
        quality = "medium"
    else:
        quality = "high"

    # Simple assumption: speech (we drop music detection)
    audio_type = "speech"

    warning = None
    if quality == "low":
        warning = "Low audio volume — results may be inaccurate"

    return {
        "duration": round(duration, 2),
        "audio_type": audio_type,
        "quality": quality,
        "warning": warning
    }