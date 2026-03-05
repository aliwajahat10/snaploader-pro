import streamlit as st
import yt_dlp
import os

# 1. Page Configuration
st.set_page_config(
    page_title="SnapLoader Pro - Global Video Downloader",
    page_icon="🎬",
    layout="centered"
)

# Har dafa server par latest version update karne ke liye
os.system("pip install -U yt-dlp")

# 2. Advanced UI with Fixed Colors
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #050505 100%);
        color: white;
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: #FF4B4B;
        margin-bottom: 0px;
    }
    .sub-text {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stDownloadButton > button {
        width: 100%;
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 12px;
        padding: 15px;
        font-weight: bold;
        border: none;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #FF4B4B !important;
        color: white !important;
        font-weight: bold;
        height: 3.5em;
        border: none;
    }
    input { border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("<h1 class='main-title'>🎬 SnapLoader Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>The Ultimate All-in-One Video Downloader</p>", unsafe_allow_html=True)

with st.expander("✨ Supported Platforms"):
    st.write("- YouTube (4K/1080p), TikTok (No Watermark), Instagram, Facebook, Twitter & more.")

# 4. Input Section
url = st.text_input("🔗 Paste link here:", placeholder="https://...")

col1, col2 = st.columns(2)
with col1:
    format_type = st.selectbox("Type:", ["Video", "Audio (MP3)"])