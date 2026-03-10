import asyncio
import os
import wave
import streamlit as st
import random
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from io import BytesIO
from datetime import datetime, timedelta
import time
import nest_asyncio
from google import genai
from google.genai import types

nest_asyncio.apply()

API_KEY = st.secrets.get("LYRIA_API_KEY")
SPOTIFY_ID = st.secrets.get("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = st.secrets.get("SPOTIFY_CLIENT_SECRET")

client = genai.Client(
    api_key=API_KEY,
    http_options={'api_version': 'v1alpha'}
)

@st.cache_resource
def get_sp_client():
    if SPOTIFY_ID and SPOTIFY_SECRET:
        try:
            return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                client_id=SPOTIFY_ID,
                client_secret=SPOTIFY_SECRET
            ))
        except Exception:
            return None
    return None

sp_client = get_sp_client()

GENRE_MAPPING = ["Rock", "Pop", "Metal", "EDM", "Hip hop", "Classical", "Video game music", "R&B"]

GENRE_PROMPTS = {
    "Classical": "Compose a serene classical piano piece reminiscent of a peaceful afternoon in a garden.",
    "EDM": "Create an upbeat and energetic electronic dance track suitable for a vibrant festival atmosphere.",
    "Hip hop": "Generate a laid-back hip hop beat with a smooth rhythm and catchy bassline, perfect for a chill evening.",
    "Metal": "Produce a high-intensity metal track with fast guitar riffs and powerful drum beats.",
    "Pop": "Compose a catchy pop melody with an uplifting vibe and a memorable chorus.",
    "R&B": "Create a soulful R&B track with a slow groove and emotional vocal harmonies.",
    "Rock": "Generate a classic rock anthem with strong guitar chords and a steady, driving beat.",
    "Video game music": "Compose an adventurous and dynamic theme suitable for an action-packed video game level."
}

def predict_favorite_genre(user_profile, model):
    try:
        def get_feature(key, default=0):
            value = user_profile.get(key, default)
            if value is None: return float(default)
            if not isinstance(value, str): value = str(value)
            if value.replace('.', '').isdigit(): return float(value)
            if value.lower() in ['yes', 'no']: return 1.0 if value.lower() == 'yes' else 0.0
            freq_map = {'never': 0.0, 'rarely': 1.0, 'sometimes': 2.0, 'very frequently': 3.0}
            if value.lower() in freq_map: return freq_map[value.lower()]
            try:
                return float(value)
            except (ValueError, TypeError):
                return float(default)
       
        input_features = [
            float(get_feature('Age', 25)),
            float(get_feature('Hours per day', 2)),
            float(1 if str(user_profile.get('While working', 'No')).lower() == 'yes' else 0),
            float(1 if str(user_profile.get('Instrumentalist', 'No')).lower() == 'yes' else 0),
            float(1 if str(user_profile.get('Composer', 'No')).lower() == 'yes' else 0),
            float(1 if str(user_profile.get('Exploratory', 'No')).lower() == 'yes' else 0),
            float(1 if str(user_profile.get('Foreign languages', 'No')).lower() == 'yes' else 0),
            float(get_feature('BPM', 120)),
            float(get_feature('Frequency_Classical', get_feature('Frequency [Classical]', 2))),
            float(get_feature('Frequency_EDM', get_feature('Frequency [EDM]', 2))),
            float(get_feature('Frequency_Folk', get_feature('Frequency [Folk]', 2))),
            float(get_feature('Frequency_Gospel', get_feature('Frequency [Gospel]', 2))),
            float(get_feature('Frequency_HipHop', get_feature('Frequency [Hip hop]', 2))),
            float(get_feature('Frequency_Jazz', get_feature('Frequency [Jazz]', 2))),
            float(get_feature('Frequency_KPop', get_feature('Frequency [K pop]', 2))),
            float(get_feature('Frequency_Metal', get_feature('Frequency [Metal]', 2))),
            float(get_feature('Frequency_Pop', get_feature('Frequency [Pop]', 2))),
            float(get_feature('Frequency_RnB', get_feature('Frequency [R&B]', 2))),
            float(get_feature('Frequency_Rock', get_feature('Frequency [Rock]', 2))),
            float(get_feature('Frequency_VGM', get_feature('Frequency [Video game music]', 2))),
            float(get_feature('Anxiety', 5)),
            float(get_feature('Depression', 5)),
            float(get_feature('Insomnia', 5)),
            float(get_feature('OCD', 5)),
            float(1 if str(user_profile.get('MusicEffects', 'No')).lower() == 'improve' else 0)
        ]
       
        input_array = np.array([input_features], dtype=np.float32)
        prediction = model.predict(input_array)
        index = int(prediction[0]) if len(prediction) > 0 else 0
        index = max(0, min(index, len(GENRE_MAPPING) - 1))
        return GENRE_MAPPING[index]
    except Exception:
        return "Pop"

async def generate_genre_track(genre_name, duration_seconds=10):
    prompt_text = GENRE_PROMPTS.get(genre_name)
    if not prompt_text: return None
    filename = f"{genre_name.replace(' ', '_')}_track.wav"
    try:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(48000)
            async with client.aio.live.music.connect(model='models/lyria-realtime-exp') as session:
                await session.set_weighted_prompts(prompts=[types.WeightedPrompt(text=prompt_text, weight=1.0)])
                await session.play()
                chunks_needed = duration_seconds // 2
                count = 0
                async for message in session.receive():
                    if message.server_content.audio_chunks:
                        wf.writeframes(message.server_content.audio_chunks[0].data)
                        count += 1
                    if count >= chunks_needed: break
        return filename
    except Exception:
        return None

def get_spotify_playlist(genre):
    if not sp_client:
        return "37i9dQZF1DXcBWIGoYBM3M"
    try:
        results = sp_client.search(q=f"genre:{genre}", type="playlist", limit=1)
        items = results.get("playlists", {}).get("items", [])
        if items:
            return items[0]["id"]
        
        fallback = sp_client.search(q=genre, type="playlist", limit=1)
        fallback_items = fallback.get("playlists", {}).get("items", [])
        return fallback_items[0]["id"] if fallback_items else "37i9dQZF1DXcBWIGoYBM3M"
    except Exception:
        return "37i9dQZF1DXcBWIGoYBM3M"

def embed_spotify_playlist(playlist_id):
    embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
    st.markdown(
        f"""
        <iframe src="{embed_url}" width="100%" height="380" frameBorder="0" 
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
        loading="lazy"></iframe>
        """,
        unsafe_allow_html=True
    )

async def create_and_compose(genre):
    if not API_KEY: return None
    try:
        filename = await generate_genre_track(genre, duration_seconds=10)
        return filename
    except Exception:
        return None
