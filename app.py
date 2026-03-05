import streamlit as st
import yt_dlp
import os

# 1. Page Configuration
st.set_page_config(
    page_title="SnapLoader Pro - Global Video Downloader",
    page_icon="🎬",
    layout="centered"
)

# 2. Advanced UI with Fixed Button Colors
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
    /* Fixed Download Button Visibility */
    .stDownloadButton > button {
        width: 100%;
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 12px;
        padding: 15px;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 15px rgba(40, 167, 69, 0.3);
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
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header & Features List
st.markdown("<h1 class='main-title'>🎬 SnapLoader Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>The Ultimate All-in-One Video Downloader</p>", unsafe_allow_html=True)

# List of supported features for your users
with st.expander("✨ See What You Can Download"):
    st.write("""
    - **YouTube:** 4K, 1080p, 720p & MP3 Audio
    - **TikTok:** High Quality (No Watermark)
    - **Instagram:** Reels, IGTV & Stories
    - **Facebook:** HD Video Downloads
    - **Twitter (X):** Fast Video Saving
    - **1000+ Other Sites Supported!**
    """)

# 4. Input Section
url = st.text_input("🔗 Paste link here:", placeholder="https://...")

col1, col2 = st.columns(2)
with col1:
    format_type = st.selectbox("Type:", ["Video", "Audio (MP3)"])
with col2:
    quality = st.selectbox("Quality:", ["Best Available", "1080p", "720p", "360p"])

# 5. Download Logic
if url:
    try:
        with st.spinner('🚀 Preparing your download...'):
            q_map = {
                "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                "Best Available": "best"
            }
            
            final_format = q_map[quality] if format_type == "Video" else "bestaudio/best"

            ydl_opts = {
                'format': final_format,
                'outtmpl': 'download_%(title)s.%(ext)s',
                'quiet': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
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

            # 6. Success & Visible Download Button
            st.balloons()
            st.success(f"Ready: {info.get('title', 'Video')[:50]}...")
            
            with open(filename, "rb") as file:
                st.download_button(
                    label=f"✅ CLICK HERE TO DOWNLOAD {format_type}",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="video/mp4" if format_type == "Video" else "audio/mpeg"
                )
            
            os.remove(filename)

    except Exception as e:
        st.error("Error: Please check the link or try a public video.")

# 7. Global Footer
st.divider()
st.markdown("<div style='text-align: center; color: #555;'>SnapLoader Pro © 2026 | Safe • Fast • Free</div>", unsafe_allow_html=True)