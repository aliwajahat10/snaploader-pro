import streamlit as st
import yt_dlp
import os
import random
import time

# 1. Page Configuration
st.set_page_config(page_title="SnapLoader Pro", page_icon="🎬", layout="centered")

# 2. Premium Dark UI
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { font-size: 3.5rem; font-weight: 900; text-align: center; color: white; }
    .supported-platforms {
        font-size: 1.4rem; font-weight: bold; color: #FF4B4B; text-align: center;
        background-color: #1a1c24; padding: 20px; border-radius: 15px; margin-bottom: 2rem;
    }
    .stDownloadButton > button { width: 100%; background-color: #28a745 !important; color: white !important; border-radius: 12px; font-weight: bold; padding: 15px; }
    .stButton>button { width: 100%; background-color: #FF4B4B !important; color: white !important; font-weight: bold; }
    input { border-radius: 12px !important; background-color: #262730 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎬 SnapLoader Pro</h1>", unsafe_allow_html=True)
st.markdown("<div class='supported-platforms'>📥 YouTube, Instagram, TikTok, Twitter & more!</div>", unsafe_allow_html=True)

# 3. Input Section
url = st.text_input("🔗 Paste link here:", placeholder="https://...")
col1, col2 = st.columns(2)
with col1:
    format_type = st.selectbox("Type:", ["Video", "Audio (MP3)"])
with col2:
    quality = st.selectbox("Quality:", ["Best Available", "1080p", "720p", "480p", "360p"])

# 4. 📤 Cookies Upload Section
st.markdown("---")
with st.expander("🔐 Bypass 403 Error (Upload Cookies)"):
    st.markdown("""
    **Why cookies?** YouTube blocks downloads without login.  
    Upload your `cookies.txt` file to fix 403 error.
    
    1. Install Chrome extension: [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid)
    2. Go to YouTube and login
    3. Export cookies and upload below
    """)
    cookies_file = st.file_uploader("Upload cookies.txt", type=['txt'])

# Save uploaded cookies
if cookies_file is not None:
    with open("cookies.txt", "wb") as f:
        f.write(cookies_file.getbuffer())
    st.success("✅ Cookies uploaded successfully!")

# 5. Download Function
if url:
    try:
        with st.spinner('🚀 Bypassing restrictions... Please wait.'):
            
            # Random delay to avoid bot detection
            time.sleep(random.uniform(2, 5))
            
            # Quality Mapping
            q_map = {
                "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                "Best Available": "best"
            }
            
            final_format = q_map[quality] if format_type == "Video" else "bestaudio/best"

            # 🛡️ Advanced Anti-Block Options
            ydl_opts = {
                'format': final_format,
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'geo_bypass': True,
                'extract_flat': False,
                'sleep_interval': 5,  # Anti-bot delay
                'max_sleep_interval': 10,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                }
            }

            # Add cookies if uploaded
            if os.path.exists('cookies.txt'):
                ydl_opts['cookiefile'] = 'cookies.txt'
                st.info("🍪 Using cookies for authentication")
            else:
                st.warning("⚠️ No cookies found. May get 403 error for YouTube.")

            # For Audio MP3
            if format_type == "Audio (MP3)":
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                ydl_opts['format'] = 'bestaudio/best'

            # Create downloads folder
            os.makedirs("downloads", exist_ok=True)

            # Download with progress
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get filename
                if 'entries' in info:  # Playlist
                    filename = ydl.prepare_filename(info['entries'][0])
                else:
                    filename = ydl.prepare_filename(info)
                
                if format_type == "Audio (MP3)":
                    filename = filename.rsplit('.', 1)[0] + ".mp3"

            st.balloons()
            st.success(f"✅ Success! Ready to Download.")
            
            # Download button
            if os.path.exists(filename):
                with open(filename, "rb") as file:
                    st.download_button(
                        label=f"📥 CLICK TO DOWNLOAD {format_type}",
                        data=file,
                        file_name=os.path.basename(filename),
                        mime="video/mp4" if format_type == "Video" else "audio/mpeg"
                    )
                
                # Cleanup
                os.remove(filename)
                st.info("🧹 Temporary file cleaned up")
            else:
                st.error("❌ File not found after download")

    except Exception as e:
        error_msg = str(e)
        st.error("❌ Error: This video is protected or the server is temporarily blocked.")
        st.info("💡 Tip: Upload cookies.txt file above to bypass 403 error.")
        
        if "403" in error_msg:
            st.warning("🔐 YouTube 403 Forbidden - Upload cookies to fix!")
        else:
            st.warning(f"Technical Reason: {error_msg}")

st.divider()
st.markdown("<center>SnapLoader Pro © 2026 | Safe • Fast • Free</center>", unsafe_allow_html=True)