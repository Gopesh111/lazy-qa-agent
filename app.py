import streamlit as st
import google.generativeai as genai
import cv2
import os
import tempfile
from PIL import Image

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Lazy QA | AI Bug Reporter",
    page_icon="🐞",
    layout="wide"
)

st.markdown("## 🐞 The Lazy QA Agent")
st.caption("Automated bug reporting powered by multimodal AI")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.secrets.get("GOOGLE_API_KEY") or st.text_input(
        "Google Gemini API Key", type="password"
    )

# ---------------- UI ----------------
col1, col2 = st.columns(2)

with col1:
    uploaded_video = st.file_uploader(
        "Upload Screen Recording",
        type=["mp4", "mov", "avi"]
    )
    if uploaded_video:
        st.video(uploaded_video)

with col2:
    st.subheader("🤖 AI Analysis")

    if uploaded_video and st.button("Generate JIRA Ticket ✨"):
        if not api_key:
            st.error("API key missing")
            st.stop()

        genai.configure(api_key=api_key)

        with st.status("🚀 Agent working...", expanded=True) as status:

            # ---------- Save video ----------
            status.write("📥 Saving video...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
                temp.write(uploaded_video.read())
                video_path = temp.name

            # ---------- Extract frames ----------
            status.write("🎞️ Extracting key frames...")
            cap = cv2.VideoCapture(video_path)
            frames = []
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Take 1 frame per second
                if frame_count % fps == 0:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(Image.fromarray(frame_rgb))

                frame_count += 1
                if len(frames) >= 6:
                    break

            cap.release()
            os.remove(video_path)

            # ---------- Gemini Vision ----------
            status.write("🧠 Analyzing UI behavior...")
            model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

            prompt = """
You are a Senior QA Automation Engineer.

The images represent key UI states from a screen recording that contains a software bug.

Generate a PROFESSIONAL JIRA BUG REPORT in Markdown.

Structure:
## 🐛 Bug Report
**Title:**
**Severity:**

### 📝 Description
### 👣 Steps to Reproduce
### 🔍 Technical Analysis
- Observed Behavior
- Expected Behavior
- Potential Root Cause
"""

            response = model.generate_content([prompt, *frames])

            status.update(label="✅ Done", state="complete")

        st.markdown("### 📄 Generated JIRA Ticket")
        st.markdown(response.text)
        st.code(response.text, language="markdown")
