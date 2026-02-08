import streamlit as st
import google.generativeai as genai
import time
from tempfile import NamedTemporaryFile
import os

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Lazy QA | AI Bug Reporter",
    page_icon="🐞",
    layout="wide",  # This enables the cool split-screen view
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for "Wow" Factor
st.markdown("""
<style>
    /* Gradient Title */
    .title-text {
        background: -webkit-linear-gradient(45deg, #00FF94, #00B8FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 3em;
        padding-bottom: 20px;
    }
    
    /* Custom Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: black;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: bold;
        transition: transform 0.2s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        color: black;
    }

    /* Card Styling for Output */
    .report-container {
        background-color: #262730;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #41444C;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar (API Key & Instructions)
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Try to get key from secrets, otherwise ask user (fallback for local dev)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ API Key Loaded from Secrets")
    else:
        api_key = st.text_input("Enter Google Gemini API Key", type="password")

    st.markdown("---")
    st.info("💡 **How it works:**\n1. Upload a video of a bug.\n2. AI watches the video frame-by-frame.\n3. It writes a JIRA ticket for you.")

# 4. Main UI
st.markdown('<p class="title-text">🐞 The Lazy QA Agent</p>', unsafe_allow_html=True)
st.caption("🚀 automated Bug Reporting System powered by Multimodal AI")

# Layout: 2 Columns
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📹 Input Source")
    uploaded_file = st.file_uploader("Upload Screen Recording", type=['mp4', 'mov', 'avi'])
    
    if uploaded_file is not None:
        st.video(uploaded_file)

with col2:
    st.subheader("🤖 AI Analysis")
    
    # Placeholder for the result
    result_container = st.empty()

    if uploaded_file is not None:
        if st.button("Generate JIRA Ticket ✨", key="analyze_btn"):
            if not api_key:
                st.error("Please provide an API Key in the sidebar.")
            else:
                genai.configure(api_key=api_key)
                
                # THE AGENT WORKFLOW
                try:
                    # Create a status container (Looks very "Agentic")
                    with st.status("🚀 Agent starting...", expanded=True) as status:
                        
                        # Step 1: Processing Video
                        status.write("📥 Uploading video to AI vision engine...")
                        with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
                            temp_video.write(uploaded_file.getvalue())
                            temp_video_path = temp_video.name

                        video_file = genai.upload_file(path=temp_video_path)
                        
                        # Wait for processing
                        status.write("👀 Analyzing video frames & timestamping events...")
                        while video_file.state.name == "PROCESSING":
                            time.sleep(2)
                            video_file = genai.get_file(video_file.name)

                        if video_file.state.name == "FAILED":
                            status.update(label="Video processing failed!", state="error")
                            st.stop()

                        # Step 2: Reasoning
                        status.write("🧠 Identifying UI elements and error patterns...")
                        
                        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
                        
                        prompt = """
                        You are an expert QA Automation Engineer.
                        Analyze this video. It shows a software bug/glitch.
                        
                        Create a PROFESSIONAL JIRA TICKET.
                        Format it nicely in Markdown.
                        
                        Structure:
                        ## 🐛 Bug Report
                        **Title:** [Write a concise, technical title]
                        **Severity:** [Critical/High/Medium/Low]
                        
                        ### 📝 Description
                        [Brief summary of what went wrong]
                        
                        ### 👣 Steps to Reproduce
                        1. [Step 1 based on video]
                        2. [Step 2 based on video]
                        3. [Step 3...]
                        
                        ### 🔍 Technical Analysis
                        - **Observed Behavior:** [What actually happened]
                        - **Expected Behavior:** [What should have happened]
                        - **Potential Root Cause:** [Make an educated guess based on the visual evidence, e.g., API 500 error, CSS overflow, Timeout]
                        
                        ---
                        *Generated by Lazy QA AI*
                        """
                        
                        status.write("✍️ Drafting professional bug report...")
                        response = model.generate_content([video_file, prompt])
                        
                        # Step 3: Cleanup
                        genai.delete_file(video_file.name)
                        os.remove(temp_video_path)
                        
                        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

                    # Display Result in a nice card
                    with result_container.container():
                        st.markdown('<div class="report-container">', unsafe_allow_html=True)
                        st.markdown(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Add a copy button logic (Streamlit native)
                        st.code(response.text, language="markdown") # Backup for easy copying

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        # Empty state graphic
        st.info("👈 Upload a video to see the magic happen.")
