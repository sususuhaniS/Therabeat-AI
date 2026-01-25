# app.py

import streamlit as st
import asyncio
from login import show_login_page, is_authenticated, get_current_user, logout
from music import predict_favorite_genre, create_and_compose
# from music import get_spotify_playlist   # ❌ Spotify disabled
from database import (
    get_user_profile,
    create_initial_user_profile,
    display_stored_user_data,
    update_user_mood
)

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials  # ❌ Spotify disabled

import nest_asyncio
from datetime import datetime
import pickle
from pathlib import Path

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()


def load_model():
    """Load the trained XGBoost model."""
    try:
        model_path = Path("best_xgb")
        if not model_path.exists():
            raise FileNotFoundError("Model file not found.")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        raise


# ❌ Spotify initialization disabled
# def initialize_spotify():
#     try:
#         if not all(key in st.secrets for key in ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"]):
#             st.error("Spotify API credentials missing.")
#             return None
#         return spotipy.Spotify(
#             auth_manager=SpotifyClientCredentials(
#                 client_id=st.secrets["SPOTIFY_CLIENT_ID"],
#                 client_secret=st.secrets["SPOTIFY_CLIENT_SECRET"]
#             )
#         )
#     except Exception as e:
#         st.error(f"Failed to initialize Spotify: {str(e)}")
#         return None


async def show_music_recommendations(user_profile, model):
    st.title("Music for Mental Health")

    display_stored_user_data(user_profile)

    col1, col2 = st.columns(2)

    with col1:
        st.header("🎵 AI-Generated Music")
        if st.button("Generate AI Music"):
            with st.spinner("Composing your personalized music..."):
                try:
                    genre = predict_favorite_genre(user_profile, model)
                    await create_and_compose(genre)
                except Exception as e:
                    st.error(f"❌ Error generating music: {str(e)}")

    with col2:
        st.header("🚫 Spotify Disabled")
        st.info("Spotify features are currently turned off.")


async def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    try:
        st.set_page_config(
            page_title="Music for Mental Health",
            page_icon="🎵",
            layout="wide"
        )

        if not is_authenticated():
            show_login_page()
            return

        user = get_current_user()
        if not user:
            st.error("Failed to get user information.")
            show_login_page()
            return

        # ❌ Spotify client disabled
        # sp_client = initialize_spotify()

        model = load_model()

        st.image(
            "https://cdn.punchng.com/wp-content/uploads/2022/03/28122921/Brain-Train-Blog-Image-2.jpg",
            use_column_width=True
        )

        if st.sidebar.button("Logout"):
            logout()
            st.rerun()

        user_email = user["email"]
        user_profile = get_user_profile(user_email)

        if user_profile is None:
            user_profile = create_initial_user_profile(user_email)
            if user_profile is None:
                st.warning("Please complete your profile.")
                return

        await show_music_recommendations(user_profile, model)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()


if __name__ == "__main__":
    asyncio.run(main())
