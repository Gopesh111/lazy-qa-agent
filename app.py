import streamlit as st
import google.generativeai as genai
import cv2
import numpy as np
import tempfile
import os

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
    st.subheader("📹 Input Source")
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
            st.error("Please provide a Google API key.")
            st.stop()

        genai.configure(api_key=api_key)

        try:
            with st.status("🚀 Agent working...", expanded=True) as status:

                # -----------------------------
                # Save video temporarily
                # -----------------------------
                status.write("📥 Saving video...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(uploaded_video.read())
                    video_path = tmp.name

                # -----------------------------
                # Analyze frame changes
                # -----------------------------
                status.write("🎞️ Detecting UI behavior patterns...")
                cap = cv2.VideoCapture(video_path)

                prev_gray = None
                significant_events = []
                frame_count = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    if prev_gray is not None:
                        diff = cv2.absdiff(prev_gray, gray)
                        change_score = np.mean(diff)

                        if change_score > 12:
                            significant_events.append(
                                f"UI change detected around frame {frame_count}"
                            )

                    prev_gray = gray
                    frame_count += 1

                    if len(significant_events) >= 6:
                        break

                cap.release()
                os.remove(video_path)

                if not significant_events:
                    significant_events.append(
                        "User interacts with the UI, but the screen shows no meaningful response."
                    )

                # -----------------------------
                # Gemini TEXT model (always available)
                # -----------------------------
                status.write("🧠 Generating engineering-grade bug report...")
                model = genai.GenerativeModel("gemini-pro")

                prompt = f"""
You are a Senior QA Automation Engineer.

Based on the following UI behavior observations extracted
from a screen recording, generate a PROFESSIONAL JIRA BUG REPORT.

UI Observations:
{chr(10).join(significant_events)}

Structure:

## 🐛 Bug Report
**Title:** Clear and concise technical summary
**Severity:** Critical / High / Medium / Low

### 📝 Description
Summarize the issue based on UI behavior.

### 👣 Steps to Reproduce
Write realistic, user-action-based steps.

### 🔍 Technical Analysis
- **Observed Behavior**
- **Expected Behavior**
- **Potential Root Cause** (educated guess)
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
            st.error("Unexpected error occurred")
            st.exception(e)
