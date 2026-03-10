import streamlit as st
import asyncio
from music import predict_favorite_genre, get_spotify_playlist, embed_spotify_playlist
from datetime import datetime
from login import is_authenticated, show_login_page

# Set background color to match home page
st.markdown("""
<style>
.stApp {
    background:
            radial-gradient(ellipse at 30% 20%, rgba(88, 28, 135, 0.4) 0%, transparent 50%),
            radial-gradient(ellipse at 70% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(15, 23, 42, 1) 0%, rgba(0, 0, 0, 1) 100%);
    /* 5. BUTTON: Change 'Update Mood' to Cyan */
div.stButton > button {
    background-color: #22D3EE !important;
    color: #000000 !important; /* Dark text for readability */
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: bold !important;
    transition: all 0.2s ease-in-out !important;
}

/* 6. BUTTON: Hover Effect */
div.stButton > button:hover {
    background-color: #64E9FA !important;
    color: #000000 !important; /* Dark text for readability */
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.6) !important;
}

/* 5. THE BUTTON: Targets st.form_submit_button */
/* This kills the orange/red and forces Cyan */
div.stFormSubmitButton > button {
    background-color: #22D3EE !important;
    color: #000000 !important; /* Black text for better contrast on Cyan */
    border: none !important;
    width: 100%; /* Optional: makes button full width of the form */
    font-weight: bold !important;
    padding: 0.6rem 2rem !important;
    border-radius: 8px !important;
}

/* 6. BUTTON HOVER: Light up on mouseover */
div.stFormSubmitButton > button:hover {
    background-color: #64E9FA !important;
    color: #000000 !important; /* Dark text for readability */
    border: 1px solid #64E9FA !important;
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.6) !important;
}

}
</style>
""", unsafe_allow_html=True)

# Check authentication before showing page
if not is_authenticated():
    show_login_page()
else:
    st.title("🎧 Spotify Playlists")
    
    # Show user's predicted genre
    try:
        predicted_genre = predict_favorite_genre(st.session_state.user_profile, st.session_state.model)
        st.info(f"Your predicted favorite genre: **{predicted_genre}**")
    except Exception as e:
        predicted_genre = "Pop"
        st.warning(f"Could not predict genre: {str(e)}. Using default: {predicted_genre}")
    
    # Playlist generation section
    st.header("Get Personalized Playlists")
    
    if not st.session_state.sp_client:
        st.error("❌ Spotify is not available. Please check your credentials.")
    else:
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("Get curated Spotify playlists based on your music preferences and current mood.")
            
            if st.button("🎧 Get Spotify Playlist", key="get_spotify_playlist", type="primary"):
                with st.spinner('🎧 Finding your perfect playlist...'):
if st.button("🎧 Get Spotify Playlist", key="get_spotify_playlist", type="primary"):
    with st.spinner('🎧 Finding your perfect playlist...'):

        try:
            playlist_url = asyncio.run(
                get_spotify_playlist(predicted_genre, st.session_state.sp_client)
            )

            if playlist_url:

                # Store playlist history
                if 'playlist_history' not in st.session_state:
                    st.session_state.playlist_history = []

                st.session_state.playlist_history.append(
                    (predicted_genre, playlist_url, datetime.now().strftime("%Y-%m-%d %H:%M"))
                )

                st.success("✅ Playlist found!")

                st.subheader(f"🎧 Recommended {predicted_genre} Playlist")

                # Embedded Spotify player
                embed_spotify_playlist(playlist_url)

                # Optional link
                st.markdown(
                    f'<a href="{playlist_url}" target="_blank">🎵 Open Playlist in Spotify</a>',
                    unsafe_allow_html=True
                )

            else:
                st.error("❌ No playlist found. Try a different genre.")

        except Exception as e:
            st.error(f"❌ Error getting playlist: {str(e)}")
        with col2:
            st.subheader("Playlist History")
            if 'playlist_history' not in st.session_state:
                st.session_state.playlist_history = []
            
            if st.session_state.playlist_history:
                for i, (genre, url, timestamp) in enumerate(st.session_state.playlist_history[-5:], 1):
                    st.write(f"{i}. [{genre}]({url}) - {timestamp}")
            else:
                st.write("No playlists generated yet.")
    
    
