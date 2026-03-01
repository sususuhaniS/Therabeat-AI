import streamlit as st
import asyncio
from database import display_stored_user_data
from login import is_authenticated, show_login_page
st.markdown("""
<style>
/* 1. The Main App Background */
.stApp {
    background: 
        radial-gradient(ellipse at 30% 20%, rgba(88, 28, 135, 0.4) 0%, transparent 50%),
        radial-gradient(ellipse at 70% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(15, 23, 42, 1) 0%, rgba(0, 0, 0, 1) 100%);
}

/* 2. Force the filled track to Cyan (removes the red) */
[data-testid="stSlider"] div[data-baseweb="slider"] > div > div > div:first-child {
    background-color: #22D3EE !important;
}

/* 3. The Slider Thumb (The Circle) */
[data-testid="stSlider"] div[role="slider"] {
    background-color: #22D3EE !important;
    border: 2px solid white !important;
    box-shadow: 0 0 10px rgba(34, 211, 238, 0.5);
}

/* 4. Fix the labels (the numbers above the thumb) */
[data-testid="stSlider"] div[role="slider"] > div {
    color: white !important; /* Makes the number readable */
    background-color: transparent !important; /* Removes the cyan box behind the number */
    font-weight: bold;
}

/* 5. The Tick Marks / Unfilled Track */
[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
    background-color: rgba(255, 255, 255, 0.1) !important;
}

</style>
""", unsafe_allow_html=True)

# Check authentication before showing page
if not is_authenticated():
    show_login_page()
else:
    async def profile_page(user_profile, model):
        """Display user profile page."""
        st.title("👤 Your Profile")
        
        # Display user profile information (without mood section)
        display_stored_user_data(user_profile)
        
        # Quick navigation to mood page
        st.markdown("---")
        st.info("📊 **Want to update your current mood or analyze music preferences?** Navigate to 'Current Mood' page to track your emotional state and get personalized music recommendations.")

    # Get user data from session state
    if 'user_profile' in st.session_state and 'model' in st.session_state:
        asyncio.run(profile_page(st.session_state.user_profile, st.session_state.model))
    else:
        st.error("Please go to main page first to load your profile.")
