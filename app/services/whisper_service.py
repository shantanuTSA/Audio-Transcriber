import whisper
import streamlit as st

@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

def transcribe_audio(file_path):
    model = load_model()  # lazy load

    result = model.transcribe(file_path)

    segments = result.get("segments", [])

    processed = []
    for seg in segments:
        processed.append({
            "text": seg["text"],
            "confidence": seg.get("avg_logprob", -1)
        })

    return processed