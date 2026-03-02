import streamlit as st
import asyncio
from database import display_stored_user_data
from login import is_authenticated, show_login_page
st.markdown("""
<style>
.stApp {
    background: 
        radial-gradient(ellipse at 30% 20%, rgba(88, 28, 135, 0.4) 0%, transparent 50%),
        radial-gradient(ellipse at 70% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(15, 23, 42, 1) 0%, rgba(0, 0, 0, 1) 100%);
}

[data-testid="stSlider"] div[data-baseweb="slider"] > div > div > div:first-child {
    background-color: #22D3EE !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background-image: none !important;
}


[data-testid="stSlider"] div[role="slider"] {
    background-color: #22D3EE !important;
    border: 2px solid white !important;
    box-shadow: 0 0 10px rgba(34, 211, 238, 0.5);
}


[data-testid="stSlider"] div[role="slider"] > div {
    color: white !important; /* Makes the number readable */
    background-color: transparent !important; /* Removes the cyan box behind the number */
    font-weight: bold;
}

/* 5. The Tick Marks / Unfilled Track */
[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
    background-color: transparent;
}



div.stButton > button {
    background-color: #22D3EE !important;
    color: #000000 !important; /* Dark text for readability */
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: bold !important;
    transition: all 0.2s ease-in-out !important;
}

div.stButton > button:hover {
    background-color: #64E9FA !important;
    color: #000000 !important; /* Dark text for readability */
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.6) !important;
}


div.stFormSubmitButton > button {
    background-color: #22D3EE !important;
    color: #000000 !important; /* Black text for better contrast on Cyan */
    border: none !important;
    width: 100%; /* Optional: makes button full width of the form */
    font-weight: bold !important;
    padding: 0.6rem 2rem !important;
    border-radius: 8px !important;
}


div.stFormSubmitButton > button:hover {
    background-color: #64E9FA !important;
    color: #000000 !important; /* Dark text for readability */
    border: 1px solid #64E9FA !important;
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.6) !important;
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
        st.info("**Want to update your current mood or analyze music preferences?** Navigate to 'Current Mood' page to track your emotional state and get personalized music recommendations.")

    # Get user data from session state
    if 'user_profile' in st.session_state and 'model' in st.session_state:
        asyncio.run(profile_page(st.session_state.user_profile, st.session_state.model))
    else:
        st.error("Please go to main page first to load your profile.")
