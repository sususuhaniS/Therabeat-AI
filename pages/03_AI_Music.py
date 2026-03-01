import streamlit as st
import asyncio
from music import predict_favorite_genre, create_and_compose
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
    }
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
    st.title("🎵 AI-Generated Music")
    
    # Show user's predicted genre
    try:
        predicted_genre = predict_favorite_genre(st.session_state.user_profile, st.session_state.model)
        st.info(f"Your predicted favorite genre: **{predicted_genre}**")
    except Exception as e:
        predicted_genre = "Pop"
        st.warning(f"Could not predict genre: {str(e)}. Using default: {predicted_genre}")
        
    # Music generation section
    st.header("Generate Personalized Music")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Generate a unique AI-composed track based on your mental health ratings and preferences.")
        
        if st.button("🎼 Generate AI Music", key="generate_ai_music", type="primary"):
            with st.spinner("Generating your personalized music..."):
                filename = asyncio.run(create_and_compose(predicted_genre))
            if filename:
                # Store in history
                if 'music_history' not in st.session_state:
                    st.session_state.music_history = []
                st.session_state.music_history.append((predicted_genre, datetime.now().strftime("%Y-%m-%d %H:%M"), filename))
                
                st.success("Music generated successfully!")
                
                # Display music player
                st.subheader("🎵 Your Generated Music")
                st.audio(filename, format='audio/wav')
                
                # Provide download option
                with open(filename, 'rb') as audio_file:
                    st.download_button(
                        label="Download Music",
                        data=audio_file.read(),
                        file_name=f"{predicted_genre}_track.wav",
                        mime="audio/wav"
                    )
            else:
                st.error("Failed to generate music. Please try again.")
    
    with col2:
        st.subheader("Music History")
        if 'music_history' not in st.session_state:
            st.session_state.music_history = []
        
        if st.session_state.music_history:
            for i, (genre, timestamp, filename) in enumerate(st.session_state.music_history[-5:], 1):
                st.write(f"{i}. {genre} - {timestamp}")
        else:
            st.write("No music generated yet.")

# Get user data from session state
if 'user_profile' not in st.session_state or 'model' not in st.session_state:
    st.error("Please go to the main page first to load your profile.")
