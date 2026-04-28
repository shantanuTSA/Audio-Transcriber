import streamlit as st
import time
import tempfile

# 🔹 Optional mic support (won’t crash if missing)
try:
    from audio_recorder_streamlit import audio_recorder
    mic_available = True
except:
    mic_available = False

# 🔹 Import your backend logic directly
from app.services.preprocess_service import preprocess_audio
from app.services.whisper_service import transcribe_audio
from app.services.audio_analysis_service import analyze_audio

# =========================
# 🎨 PAGE CONFIG
# =========================
st.set_page_config(page_title="Audio Transcriber", layout="wide")

# =========================
# 🎨 CUSTOM STYLING
# =========================
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🎯 HEADER
# =========================
st.title("🎤 Audio Transcription Studio")
st.caption("✨ Convert speech to text with intelligent processing")

st.divider()

# =========================
# 📂 INPUT TABS
# =========================
tab1, tab2 = st.tabs(["📁 Upload Audio", "🎙 Record Audio"])

file_data = None

# 🔹 Upload Tab
with tab1:
    uploaded_file = st.file_uploader(
        "Upload audio",
        type=["wav", "mp3", "mp4"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.audio(uploaded_file)
        file_data = uploaded_file.getvalue()

# 🔹 Record Tab
with tab2:
    if mic_available:
        audio_bytes = audio_recorder()

        if audio_bytes:
            st.audio(audio_bytes)
            file_data = audio_bytes
    else:
        st.info("🎙 Microphone not available in this deployment")

# =========================
# 🚀 TRANSCRIBE
# =========================
if file_data:
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run = st.button("🚀 Transcribe", use_container_width=True)

    if run:
        start_time = time.time()

        with st.spinner("🔄 Processing audio..."):
            try:
                # 🔥 Save temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(file_data)
                    temp_path = tmp.name

                # 🔥 ANALYSIS
                analysis = analyze_audio(temp_path)

                # 🔥 RAW TRANSCRIPTION
                raw_text = transcribe_audio(temp_path)

                # 🔥 CLEAN TRANSCRIPTION
                processed_path = preprocess_audio(temp_path)
                clean_text = transcribe_audio(processed_path)

                processing_time = round(time.time() - start_time, 2)

                st.divider()

                # ⚠️ Warning
                if analysis.get("warning"):
                    st.warning(f"⚠️ {analysis.get('warning')}")

                # 📊 Metrics
                st.subheader("📊 Audio Insights")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Type", analysis.get("audio_type"))
                col2.metric("Quality", analysis.get("quality"))
                col3.metric("Duration (s)", analysis.get("duration"))
                col4.metric("⏱ Time (s)", processing_time)

                st.divider()

                # 📝 Transcripts
                st.subheader("📝 Transcription Results")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 📝 Raw Output")
                    st.write(raw_text)

                with col2:
                    st.markdown("### ✨ Clean Output")
                    st.write(clean_text)

                st.divider()

                # 📋 Final Text
                final_text = clean_text or raw_text

                st.subheader("📋 Final Transcript")
                st.code(final_text)

                # 📥 Download
                st.download_button(
                    "📥 Download Transcript",
                    final_text,
                    file_name="transcript.txt",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Error: {e}")

# =========================
# 🔻 FOOTER
# =========================
st.divider()
st.caption("🚀 Built with Whisper + Streamlit")