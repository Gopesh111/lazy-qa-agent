import streamlit as st
import google.generativeai as genai
import cv2
import tempfile
import os
from PIL import Image
import pytesseract

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Lazy QA | AI Bug Reporter",
    page_icon="🐞",
    layout="wide"
)

st.markdown("## 🐞 The Lazy QA Agent")
st.caption("Automated bug reporting powered by AI reasoning")

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.secrets.get("GOOGLE_API_KEY") or st.text_input(
        "Google Gemini API Key", type="password"
    )

# -------------------------------------------------
# UI
# -------------------------------------------------
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
            st.error("API key required")
            st.stop()

        genai.configure(api_key=api_key)

        try:
            with st.status("🚀 Agent working...", expanded=True) as status:

                # Save video
                status.write("📥 Saving video...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(uploaded_video.read())
                    video_path = tmp.name

                # Extract frames
                status.write("🎞️ Extracting frames...")
                cap = cv2.VideoCapture(video_path)
                fps = int(cap.get(cv2.CAP_PROP_FPS)) or 1

                ui_observations = []
                frame_index = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    if frame_index % fps == 0:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        text = pytesseract.image_to_string(gray)
                        if text.strip():
                            ui_observations.append(text.strip())

                    frame_index += 1
                    if len(ui_observations) >= 6:
                        break

                cap.release()
                os.remove(video_path)

                if not ui_observations:
                    ui_observations.append(
                        "User interacts with UI but unexpected behavior occurs."
                    )

                # Gemini TEXT model (always available)
                status.write("🧠 Reasoning about bug...")
                model = genai.GenerativeModel("gemini-pro")

                prompt = f"""
You are a Senior QA Automation Engineer.

Based on the following UI observations extracted from a screen recording,
generate a PROFESSIONAL JIRA BUG REPORT.

UI Observations:
{chr(10).join(ui_observations)}

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

                response = model.generate_content(prompt)

                status.update(
                    label="✅ Analysis complete",
                    state="complete",
                    expanded=False
                )

            st.markdown("### 📄 Generated JIRA Ticket")
            st.markdown(response.text)
            st.code(response.text, language="markdown")

        except Exception as e:
            st.error("Unexpected error")
            st.exception(e)
