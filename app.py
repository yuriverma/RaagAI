import streamlit as st
import os
from backend.music_pipeline import generate_music

# Set page config
st.set_page_config(page_title="RAAG.AI", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(to bottom right, #0f0f0f, #1c1c1c);
            color: white;
            font-family: 'Georgia', serif;
        }
        .title {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
            letter-spacing: 2px;
            color: #68a0f6;
            text-shadow: 1px 1px 2px #000;
        }
        .button-row {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }
        .genre-btn button {
            background-color: #2e3a59 !important;
            color: #ffffff !important;
            border: none;
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            border-radius: 8px;
            font-family: 'Georgia', serif;
        }
        .section-title {
            font-size: 1.5rem;
            margin-top: 2rem;
            color: #7db4ff;
            font-weight: 600;
        }
        .lyrics-box {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 1rem;
            border-radius: 8px;
            font-family: 'Georgia', serif;
            white-space: pre-wrap;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">RAAG.AI</div>', unsafe_allow_html=True)

# Genre selection
st.markdown('<div class="button-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    classical = st.button("🎻 Classical", key="classical")
with col2:
    qawwali = st.button("🕌 Qawwali", key="qawwali")
with col3:
    dhh = st.button("🎤 DHH", key="dhh")
st.markdown('</div>', unsafe_allow_html=True)

# Load API key
API_KEY = st.secrets.get("API_KEY", "")

# Music Generation Logic
if classical:
    st.markdown("Generating Classical Raag...")
    result = generate_music("classical", API_KEY)
elif qawwali:
    st.markdown("Generating Qawwali...")
    result = generate_music("qawwali", API_KEY)
elif dhh:
    st.markdown("Generating DHH...")
    result = generate_music("dhh", API_KEY)
else:
    result = None

# Show result
if result:
    st.markdown('<div class="section-title">🎧 Track Preview</div>', unsafe_allow_html=True)
    audio_file = result["track"]
    if os.path.exists(audio_file):
        with open(audio_file, "rb") as audio:
            audio_bytes = audio.read()
            st.audio(audio_bytes, format="audio/mp3")
    
    st.markdown('<div class="section-title">📝 Lyrics</div>', unsafe_allow_html=True)
    lyrics_file = result["lyrics"]
    if os.path.exists(lyrics_file):
        with open(lyrics_file, "r", encoding="utf-8") as file:
            lyrics = file.read()
            st.markdown(f'<div class="lyrics-box">{lyrics}</div>', unsafe_allow_html=True)

