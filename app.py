import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import requests

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Lazy QA | AI Bug Reporter",
    page_icon="🐞",
    layout="wide"
)

st.markdown("## 🐞 The Lazy QA Agent")
st.caption("Automated bug reporting powered by local AI reasoning")

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

        try:
            with st.status("🚀 Agent working locally...", expanded=True) as status:

                # Save video
                status.write("📥 Saving video...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(uploaded_video.read())
                    video_path = tmp.name

                # Analyze frame differences
                status.write("🎞️ Detecting UI behavior...")
                cap = cv2.VideoCapture(video_path)

                prev_gray = None
                events = []
                frame_no = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    if prev_gray is not None:
                        diff = cv2.absdiff(prev_gray, gray)
                        score = np.mean(diff)

                        if score > 12:
                            events.append(
                                f"Significant UI change detected around frame {frame_no}"
                            )

                    prev_gray = gray
                    frame_no += 1

                    if len(events) >= 6:
                        break

                cap.release()
                os.remove(video_path)

                if not events:
                    events.append(
                        "User interacts with the UI, but no visible response occurs."
                    )

                # Local LLM reasoning via Ollama
                status.write("🧠 Writing JIRA ticket (local LLM)...")

                prompt = f"""
You are a Senior QA Automation Engineer.

Based on the following UI behavior observations from a screen recording,
write a PROFESSIONAL JIRA BUG REPORT.

UI Observations:
{chr(10).join(events)}

Structure:

## 🐛 Bug Report
**Title:** Concise technical summary
**Severity:** Critical / High / Medium / Low

### 📝 Description
### 👣 Steps to Reproduce
### 🔍 Technical Analysis
- Observed Behavior
- Expected Behavior
- Potential Root Cause
"""

                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen3:8b",
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=120
                )

                result = response.json()["response"]

                status.update(
                    label="✅ Analysis complete",
                    state="complete",
                    expanded=False
                )

            st.markdown("### 📄 Generated JIRA Ticket")
            st.markdown(result)
            st.code(result, language="markdown")

        except Exception as e:
            st.error("Unexpected error occurred")
            st.exception(e)
