import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from music import predict_favorite_genre, get_spotify_playlist, embed_spotify_playlist
from datetime import datetime
from login import is_authenticated, show_login_page

if "sp_client" not in st.session_state:
    try:
        st.session_state.sp_client = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=st.secrets["SPOTIFY_CLIENT_ID"],
                client_secret=st.secrets["SPOTIFY_CLIENT_SECRET"]
            )
        )
    except:
        st.session_state.sp_client = None

if not is_authenticated():
    show_login_page()
    st.stop()

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 30% 20%, rgba(88, 28, 135, 0.4) 0%, transparent 50%),
        radial-gradient(ellipse at 70% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(15, 23, 42, 1) 0%, rgba(0, 0, 0, 1) 100%);
}
div.stButton > button {
    background-color: #22D3EE;
    color: #000000;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #64E9FA;
    box-shadow: 0 0 15px rgba(34,211,238,0.6);
}
</style>
""", unsafe_allow_html=True)

st.title("🎧 Spotify Playlists")

try:
    predicted_genre = predict_favorite_genre(
        st.session_state.user_profile,
        st.session_state.model
    )
except:
    predicted_genre = "pop"

st.info(f"Your predicted favorite genre: **{predicted_genre}**")

st.header("Get Personalized Playlists")

if not st.session_state.sp_client:
    st.error("Spotify client failed to initialize.")
    st.stop()

col1, col2 = st.columns([2,1])

with col1:

    st.write("Get curated Spotify playlists based on your music preferences and current mood.")

    if st.button("🎧 Get Spotify Playlist"):

        with st.spinner("Finding playlist..."):

            playlist_url = None

            try:
                playlist_url = get_spotify_playlist(
                    st.session_state.sp_client,
                    predicted_genre
                )
            except:
                playlist_url = None

            if playlist_url:

                if "playlist_history" not in st.session_state:
                    st.session_state.playlist_history = []

                st.session_state.playlist_history.append(
                    (
                        predicted_genre,
                        playlist_url,
                        datetime.now().strftime("%Y-%m-%d %H:%M")
                    )
                )

                st.success("Playlist found!")

                st.subheader(f"{predicted_genre.title()} Playlist")

                embed_spotify_playlist(playlist_url)

                st.markdown(
                    f'<a href="{playlist_url}" target="_blank">Open in Spotify</a>',
                    unsafe_allow_html=True
                )

            else:
                st.error("No playlist found.")

with col2:

    st.subheader("Playlist History")

    if "playlist_history" not in st.session_state:
        st.session_state.playlist_history = []

    if len(st.session_state.playlist_history) == 0:
        st.write("No playlists generated yet.")
    else:
        for i, (genre, url, timestamp) in enumerate(st.session_state.playlist_history[-5:], 1):
            st.write(f"{i}. [{genre}]({url}) - {timestamp}")
