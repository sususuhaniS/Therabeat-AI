import asyncio
import os
import wave
import streamlit as st
import random
import numpy as np
from io import BytesIO
from datetime import datetime, timedelta
import time
import nest_asyncio
from google import genai
from google.genai import types

nest_asyncio.apply()

API_KEY = st.secrets.get("LYRIA_API_KEY")
MODEL_ID = "models/lyria-v1"

if not API_KEY:
    st.error("❌ Lyria API key is not configured. Please check your secrets.toml file.")

client = genai.Client(
    api_key=API_KEY,
    http_options={'api_version': 'v1alpha'}
)

GENRE_MAPPING = [
    "Rock", "Pop", "Metal", "EDM", "Hip hop", "Classical", "Video game music", "R&B"
]

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
           
            if value is None:
                return float(default)
               
            if not isinstance(value, str):
                value = str(value)
               
            if value.replace('.', '').isdigit():
                return float(value)
               
            if value.lower() in ['yes', 'no']:
                return 1.0 if value.lower() == 'yes' else 0.0
               
            freq_map = {
                'never': 0.0,
                'rarely': 1.0,
                'sometimes': 2.0,
                'very frequently': 3.0
            }
            if value.lower() in freq_map:
                return freq_map[value.lower()]
               
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
            float
