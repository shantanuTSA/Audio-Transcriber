import os
import uuid
import subprocess
from pydub import AudioSegment
import noisereduce as nr
import numpy as np

PROCESSED_DIR = "data/processed/"

os.makedirs(PROCESSED_DIR, exist_ok=True)


# 🔹 Step 1: Convert to WAV
def convert_to_wav(input_path):
    output_path = os.path.join(PROCESSED_DIR, f"{uuid.uuid4()}.wav")

    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ])

    return output_path


# 🔹 Step 2: Normalize audio
def normalize_audio(input_path):
    audio = AudioSegment.from_file(input_path)
    normalized_audio = audio.normalize()

    output_path = os.path.join(PROCESSED_DIR, f"{uuid.uuid4()}.wav")
    normalized_audio.export(output_path, format="wav")

    return output_path


# 🔹 Step 3: Reduce noise
def reduce_noise(input_path):
    audio = AudioSegment.from_file(input_path)
    samples = np.array(audio.get_array_of_samples())

    reduced_noise = nr.reduce_noise(y=samples, sr=16000)

    cleaned_audio = AudioSegment(
        reduced_noise.tobytes(),
        frame_rate=16000,
        sample_width=audio.sample_width,
        channels=1
    )

    output_path = os.path.join(PROCESSED_DIR, f"{uuid.uuid4()}.wav")
    cleaned_audio.export(output_path, format="wav")

    return output_path


# 🔹 Step 4: Trim silence
def trim_audio(input_path, silence_thresh=-40, min_silence_len=500):
    audio = AudioSegment.from_file(input_path)

    trimmed_audio = audio.strip_silence(
        silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )

    output_path = os.path.join(PROCESSED_DIR, f"{uuid.uuid4()}.wav")
    trimmed_audio.export(output_path, format="wav")

    return output_path


# 🔹 Full pipeline
def preprocess_audio(input_path):
    wav_path = convert_to_wav(input_path)
    normalized_path = normalize_audio(wav_path)

    return normalized_path