import whisper

model = whisper.load_model("tiny")  # use tiny for deployment


def transcribe_audio(file_path):
    result = model.transcribe(file_path)

    segments = result.get("segments", [])

    processed_segments = []

    for seg in segments:
        text = seg["text"]
        confidence = seg.get("avg_logprob", -1)

        processed_segments.append({
            "text": text,
            "confidence": confidence
        })

    return processed_segments