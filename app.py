import streamlit as st
import yt_dlp
import os

# 1. Page Configuration
st.set_page_config(
    page_title="SnapLoader Pro - Global Video Downloader",
    page_icon="🎬",
    layout="centered"
)

# Har dafa naya version check karne ke liye
os.system("pip install -U yt-dlp")

# 2. Premium Dark UI
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: white;
        margin-bottom: 0px;
    }
    .sub-text {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .supported-platforms {
        font-size: 1.4rem;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        background-color: #1a1c24;
        padding: 20px;
        border: 1px solid #333;
        border-radius: 15px;
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
    input {
        border-radius: 12px !important;
        background-color: #262730 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("<h1 class='main-title'>🎬 SnapLoader Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>The Ultimate All-in-One Video Downloader</p>", unsafe_allow_html=True)

st.markdown("""
<div class='supported-platforms'>
    📥 Supported Platforms:<br>
    YouTube (4K/1080p), Instagram, TikTok,<br>
    Twitter (X), Facebook, and 1000+ more!
</div>
""", unsafe_allow_html=True)

# 4. Input Section
url = st.text_input("🔗 Paste link here:", placeholder="https://...")

col1, col2 = st.columns(2)
with col1:
    format_type = st.selectbox("Type:", ["Video", "Audio (MP3)"])
with col2:
    quality = st.selectbox("Quality:", ["Best Available", "1080p", "720p", "480p", "360p"])

# 5. Enhanced Download Logic (To Fix 403 Forbidden)
if url:
    try:
        with st.spinner('🚀 Processing... Please wait.'):
            q_map = {
                "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                "Best Available": "best"
            }
            
            final_format = q_map[quality] if format_type == "Video" else "bestaudio/best"

            ydl_opts = {
                'format': final_format,
                'outtmpl': 'download_%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'source_address': '0.0.0.0', # Force IPv4
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                },
            }

            if format_type == "Audio (MP3)":
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if format_type == "Audio (MP3)":
                    filename = filename.rsplit('.', 1)[0] + ".mp3"

            st.balloons()
            st.success(f"Ready: {info.get('title', 'Video')[:50]}...")
            
            with open(filename, "rb") as file:
                st.download_button(
                    label=f"✅ CLICK TO DOWNLOAD {format_type}",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="video/mp4" if format_type == "Video" else "audio/mpeg"
                )
            os.remove(filename)

    except Exception as e:
        st.error("Error: The platform is blocking the request. Try 'Best Available' or refresh.")
        st.warning(f"Details: {e}")

st.divider()
st.markdown("<div style='text-align: center; color: #555;'>SnapLoader Pro © 2026 | Safe • Fast • Free</div>", unsafe_allow_html=True)