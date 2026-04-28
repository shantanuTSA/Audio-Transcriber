import os
import uuid
from pydub import AudioSegment

CHUNK_DIR = "data/processed/chunks/"

def split_audio(file_path, chunk_length_ms=30000):
    os.makedirs(CHUNK_DIR, exist_ok=True)

    audio = AudioSegment.from_file(file_path)
    chunks = []

    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]

        chunk_name = f"{uuid.uuid4()}.wav"
        chunk_path = os.path.join(CHUNK_DIR, chunk_name)

        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks