from fastapi import APIRouter, UploadFile, File

from app.utils.file_handler import save_file
from app.services.preprocess_service import preprocess_audio
from app.services.whisper_service import transcribe_audio
from app.services.audio_analysis_service import analyze_audio

router = APIRouter()


@router.post("/transcribe/")
async def transcribe(file: UploadFile = File(...), clean: bool = True):
    # 🔹 Step 1: Save file
    input_path = save_file(file)

    # 🔹 Step 2: Analyze
    analysis = analyze_audio(input_path)

    # 🔹 Step 3: ALWAYS do raw transcription
    raw_text = transcribe_audio(input_path)

    # 🔥 SMART DECISION
    if analysis["audio_type"] == "music":
        return {
            "raw_transcript": raw_text,
            "clean_transcript": None,
            "audio_type": analysis["audio_type"],
            "quality": analysis["quality"],
            "duration": analysis["duration"],
            "warning": analysis["warning"] or "Music detected — skipping preprocessing"
        }

    # 🔹 Step 4: Only preprocess if speech
    if clean:
        processed_path = preprocess_audio(input_path)
        clean_text = transcribe_audio(processed_path)
    else:
        clean_text = None

    # 🔹 Step 5: Return full response
    return {
        "raw_transcript": raw_text,
        "clean_transcript": clean_text,
        "audio_type": analysis["audio_type"],
        "quality": analysis["quality"],
        "duration": analysis["duration"],
        "warning": analysis["warning"]
    }