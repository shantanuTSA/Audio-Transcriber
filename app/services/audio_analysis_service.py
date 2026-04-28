import librosa
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf

# Load model once
model = hub.load("https://tfhub.dev/google/yamnet/1")

# Load class names properly
class_map_path = model.class_map_path().numpy().decode("utf-8")
with open(class_map_path) as f:
    class_names = [line.strip() for line in f.readlines()]


def analyze_audio(file_path):
    # 🔹 Load audio (YAMNet expects float32 mono 16k)
    y, sr = librosa.load(file_path, sr=16000)
    y = y.astype(np.float32)

    duration = librosa.get_duration(y=y, sr=sr)

    # 🔹 Run model
    scores, embeddings, spectrogram = model(y)
    scores = scores.numpy()

    # 🔹 Average predictions over time
    mean_scores = np.mean(scores, axis=0)

    # 🔹 Top-K predictions
    top_indices = np.argsort(mean_scores)[-5:][::-1]

    top_classes = [class_names[i] for i in top_indices]
    top_scores = [float(mean_scores[i]) for i in top_indices]

    # 🧠 Smarter classification
    music_keywords = ["music", "song", "instrument", "band", "melody"]

    music_score = 0
    for cls, score in zip(top_classes, top_scores):
        if any(keyword in cls.lower() for keyword in music_keywords):
            music_score += score

    if music_score > 0.3:
        audio_type = "music"
    else:
        audio_type = "speech"

    # For logging/debugging
    top_class = top_classes[0]
    confidence = top_scores[0]

    # 🧠 Classification (robust)
    if any(keyword in top_class.lower() for keyword in ["music", "song", "instrument"]):
        audio_type = "music"
    else:
        audio_type = "speech"

    # 🔹 Quality estimation (simple energy-based)
    energy = np.mean(np.abs(y))
    if energy < 0.01:
        quality = "low"
    elif energy < 0.03:
        quality = "medium"
    else:
        quality = "high"

    # ⚠️ Warning
    warning = None
    if audio_type == "music":
        warning = f"Music detected ({top_class}) — transcription may be inaccurate"
    elif quality == "low":
        warning = "Low audio volume — results may be inaccurate"

    return {
        "duration": round(duration, 2),
        "audio_type": audio_type,
        "quality": quality,
        "warning": warning,
        "detected_class": top_class,
        "confidence": confidence
    }