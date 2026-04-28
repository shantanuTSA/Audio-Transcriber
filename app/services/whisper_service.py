import whisper
from app.services.chunking_service import split_audio

model = whisper.load_model("base")

def transcribe_audio(file_path):
    chunks = split_audio(file_path)

    full_text = ""

    for chunk in chunks:
        result = model.transcribe(chunk)
        full_text += result["text"] + " "

    return full_text.strip()