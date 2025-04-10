import streamlit as st
import PyPDF2
import google.generativeai as genai
import os

# ✅ Gemini API key (REQUIRED for Hugging Face secret setting)
GEMINI_API_KEY = ("AIzaSyDIndYyJczNWDb1Gih8_PYk5A0s3X0taLc")
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="📋 Meeting Transcript Analyzer", layout="wide")

# Styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2E86C1;
        text-shadow: 1px 1px 3px rgba(46, 134, 193, 0.3);
    }
    .result-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 8px rgba(0,0,0,0.1);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📋 Meeting Transcript Analyzer</h1>', unsafe_allow_html=True)
st.write("Upload a `.pdf` meeting transcript or paste text to get summaries, decisions, action items, and sentiment.")

# Upload and Text Input
uploaded_file = st.file_uploader("📂 Upload PDF", type=["pdf"])
text_input = st.text_area("📝 Or paste transcript text here", height=250)

# PDF Extractor
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

# LLM Analyzer
def analyze_transcript(text):
    try:
        model = genai.GenerativeModel("learnlm-1.5-pro-experimental")  # ✅ Correct model name for public Gemini API
        prompt = f"""
        Given the following meeting transcript, summarize the main points, list key decisions and action items, 
        and analyze the overall sentiment.

        Transcript:
        {text}

        Return the output in a clean structured format with headers:
        1. Summary
        2. Key Decisions
        3. Action Items
        4. Sentiment Analysis
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Main Logic
if uploaded_file or text_input.strip():
    with st.spinner("🔍 Analyzing..."):
        if uploaded_file:
            transcript = extract_text_from_pdf(uploaded_file)
        else:
            transcript = text_input.strip()

        if transcript:
            result = analyze_transcript(transcript)
            st.markdown("### 🧾 Analysis Result")
            st.markdown(f'<div class="result-card">{result}</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Empty transcript.")
else:
    st.info("📌 Please upload or paste your transcript to begin.")
