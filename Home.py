import streamlit as st
import asyncio
from login import show_login_page, is_authenticated, get_current_user, logout
from music import predict_favorite_genre, create_and_compose, get_spotify_playlist
from database import get_user_profile, create_initial_user_profile, display_stored_user_data, update_user_mood
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
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
            raise FileNotFoundError("Model file not found. Please ensure best_xgb.pkl is in the project root.")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        raise

def initialize_spotify():
    """Initialize Spotify client with error handling."""
    try:
        if not all(key in st.secrets for key in ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"]):
            st.error("❌ Spotify API credentials are missing. Please check your secrets.toml")
            return None
            
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["SPOTIFY_CLIENT_ID"],
            client_secret=st.secrets["SPOTIFY_CLIENT_SECRET"]
        ))
    except Exception as e:
        st.error(f"❌ Failed to initialize Spotify client: {str(e)}")
        return None

async def home_page():
    """Display home page with welcome message."""
    
    # Set background color
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');

    /* 1. Global App Background */
    .stApp {
        background:
            radial-gradient(ellipse at 30% 20%, rgba(88, 28, 135, 0.4) 0%, transparent 50%),
            radial-gradient(ellipse at 70% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(15, 23, 42, 1) 0%, rgba(0, 0, 0, 1) 100%);
    }

    /* 2. Welcome Container */
    .welcome-container {
        font-family: 'Inter', sans-serif;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
        text-align: center;
        color: white;
        padding: 20px;
    }

    /* 3. Typography */
    .top-eyebrow {
        font-size: 14px;
        letter-spacing: 8px;
        text-transform: uppercase;
        color: #22D3EE;
        font-weight: 700;
        margin-bottom: 25px;
    }

    .main-hero-title {
        font-size: 5.5rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 25px;
        letter-spacing: -2px;
    }

    .gradient-text {
        background: linear-gradient(135deg, #ffffff 30%, #22D3EE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-left: 10px;
    }

    .subtitle-desc {
        font-size: 1.2rem;
        max-width: 700px;
        margin: 0 auto 3rem auto;
        opacity: 0.8;
        font-weight: 400;
        line-height: 1.6;
    }

    /* 4. Feature Cards - THE FIX */
    .feature-cards {
        display: flex;
        flex-direction: row; /* Forces horizontal layout */
        gap: 2rem;
        margin-top: 1rem;
        justify-content: center;
        flex-wrap: wrap; /* Allows wrapping on small screens */
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 40px 30px;
        width: 300px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .feature-card:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(34, 211, 238, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 20px;
    }

    .feature-title {
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 12px;
        color: white;
    }

    .feature-desc {
        opacity: 0.6;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    </style>

    <div class="welcome-container">
        <div class="top-eyebrow">Reimagining Music Therapy</div>
        <div class="main-hero-title">
            TheraBeat<span class="gradient-text">AI</span>
        </div>
        <div class="subtitle-desc">
            Your personalized journey to mental wellness through the power of generative audio landscapes.
        </div>
        
        <div class="feature-cards">
            <div class="feature-card">
                <div class="feature-icon">🎵</div>
                <div class="feature-title">AI Music</div>
                <div class="feature-desc">Generate personalized music tracks based on your unique mood and emotional state.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎧</div>
                <div class="feature-title">Spotify Playlists</div>
                <div class="feature-desc">Get curated Spotify collections tailored to help you navigate your emotional journey.</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
    
async def main():
    # Initialize session state
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'music_history' not in st.session_state:
        st.session_state.music_history = []
    if 'playlist_history' not in st.session_state:
        st.session_state.playlist_history = []

   
    try:
        # Set page config
        st.set_page_config(
            page_title="TheraBeat AI - Home",
            page_icon="🎵",
            layout="wide"
        )
        
        # Show login page if not authenticated
        if not is_authenticated():
            show_login_page()
            return

        # Get current user
        user = get_current_user()
        if not user:
            st.error("Failed to get user information. Please try logging in again.")
            show_login_page()
            return

        # Initialize Spotify client
        sp_client = initialize_spotify()
        if not sp_client:
            st.error("Failed to initialize Spotify client. Please check your credentials.")
            return

        # Load the trained model
        model = load_model()
        if not model:
            st.error("Failed to load the prediction model.")
            return
        
        # Get user profile
        user_email = user['email']
        user_profile = get_user_profile(user_email)
        
        if user_profile is None:
            # First-time user - show profile creation
            user_profile = create_initial_user_profile(user_email)
            
            if user_profile is None:
                # User didn't complete profile
                st.warning("Please complete your profile to continue.")
                return
        
        # Store data in session state for other pages
        st.session_state.user_profile = user_profile
        st.session_state.model = model
        st.session_state.sp_client = sp_client
        st.session_state.user = user
        
        # Add logout button in sidebar with gradient background
        st.sidebar.markdown("""
        <style>
        [data-testid="stSidebar"] {
             
            padding: 20px;
            background-color: black
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("Logout", type="secondary"):
            logout()
            st.rerun()
        
        # Show welcome message in sidebar
        st.sidebar.write(f"Welcome, {user.get('name', 'User')}!")
        
        # Show the main home page content
        await home_page()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

if __name__ == "__main__":
    asyncio.run(main())
