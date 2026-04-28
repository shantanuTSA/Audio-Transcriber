import streamlit as st
import requests
import time
from audio_recorder_streamlit import audio_recorder

BACKEND_URL = "http://127.0.0.1:8000/transcribe/"

st.set_page_config(page_title="Audio Transcriber", layout="wide")

# =========================
#  CUSTOM STYLING
# =========================
st.markdown("""
<style>
/* Accent colors */
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

/* Card effect */
.block-container {
    padding-top: 1.5rem;
}

/* Headers */
h1, h2, h3 {
    font-weight: 700;
}

/* Code block */
code {
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
#  HEADER
# =========================
st.title(" Audio Transcription Studio")
st.caption(" Convert speech to text with intelligent processing")

st.divider()

# =========================
#  INPUT SECTION
# =========================
tab1, tab2 = st.tabs([" Upload Audio", " Record Audio"])

file_data = None
file_name = None
file_type = None

# 🔹 Upload
with tab1:
    uploaded_file = st.file_uploader(
        "Upload audio file",
        type=["wav", "mp3", "mp4"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.audio(uploaded_file)
        file_data = uploaded_file.getvalue()
        file_name = uploaded_file.name
        file_type = uploaded_file.type

# 🔹 Record
with tab2:
    audio_bytes = audio_recorder()

    if audio_bytes:
        st.audio(audio_bytes)
        file_data = audio_bytes
        file_name = "recording.wav"
        file_type = "audio/wav"

# =========================
# 🚀 TRANSCRIBE
# =========================
if file_data:
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run = st.button(" Transcribe", use_container_width=True)

    if run:
        start_time = time.time()

        # 🔥 Fancy loader
        with st.spinner("🔄 Processing your audio..."):
            time.sleep(0.5)

            try:
                response = requests.post(
                    BACKEND_URL,
                    files={
                        "file": (
                            file_name,
                            file_data,
                            file_type
                        )
                    }
                )

                end_time = time.time()
                processing_time = round(end_time - start_time, 2)

                if response.status_code == 200:
                    result = response.json()

                    st.divider()

                    # =========================
                    # ⚠️ WARNING
                    # =========================
                    if result.get("warning"):
                        st.warning(f"⚠️ {result.get('warning')}")

                    # =========================
                    # 📊 METRICS
                    # =========================
                    st.subheader("📊 Audio Insights")

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric("Type", result.get("audio_type"))
                    col2.metric("Quality", result.get("quality"))
                    col3.metric("Duration (s)", result.get("duration"))
                    col4.metric("⏱ Time (s)", processing_time)

                    st.divider()

                    # =========================
                    # 📝 TRANSCRIPTS
                    # =========================
                    st.subheader("📝 Transcription Results")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 📝 Raw Output")
                        st.write(result.get("raw_transcript"))

                    with col2:
                        st.markdown("### ✨ Clean Output")
                        st.write(result.get("clean_transcript"))

                    st.divider()

                    # =========================
                    # 📋 FINAL TEXT
                    # =========================
                    final_text = result.get("clean_transcript") or result.get("raw_transcript")

                    st.subheader("📋 Final Transcript")
                    st.code(final_text)

                    # =========================
                    # 📥 DOWNLOAD
                    # =========================
                    st.download_button(
                        " Download Transcript",
                        final_text,
                        file_name="transcript.txt",
                        use_container_width=True
                    )

                else:
                    st.error(f"Backend Error: {response.text}")

            except Exception as e:
                st.error(f"Request failed: {e}")

# =========================
# 🔻 FOOTER
# =========================
st.divider()
# st.caption(" Built with Whisper + FastAPI + Streamlit")