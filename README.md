# MeloMatch AI

Personalized music recommendations from self-reported listening preferences,
using a machine-learning genre model and generative audio — a research prototype.

## Description

This is the GitHub repository for a research prototype exploring personalized
music recommendation. The app gathers self-reported user data — age, music
listening habits, and a set of self-rated survey scales — and uses this data
with a trained machine-learning model to predict a music genre preference.
It then either generates an original track for that genre using generative
AI, or surfaces a matching Spotify playlist.

**MeloMatch AI is a research prototype only.** It is not a medical device,
does not provide therapy, diagnosis, or treatment, and should not be used as
a substitute for professional mental health care. The self-rated scales in
the profile form are survey inputs to the recommendation model, not a
clinical assessment.

## Project Structure

```
MeloMatch-AI/
│
├── Home.py            # single Streamlit entry point
├── login.py
├── music.py
├── database.py
├── best_xgb
├── requirements.txt
├── pages/
└── README.md
```

## File Descriptions

### Home.py

Single entry point for the Streamlit application. Handles login state,
loads the machine-learning model, initializes the Spotify client, and
renders both the landing page and the recommendations UI.

### login.py

Handles authentication login, logout, session management, and retrieving
the current user.

### music.py

Predicts a favorite genre using the trained ML model, generates music using
Google Lyria, retrieves Spotify playlists, and maps genres to generation
prompts.

### database.py

Manages user data in Firestore, including:

- creating user profiles
- retrieving stored user information
- updating self-reported listening-context data
- displaying stored profile information

### best_xgb

Trained **XGBoost model** used to predict a user's favorite music genre.
Unchanged in this pass — same features, artifact, and output mapping.

### requirements.txt

Python dependencies required to run the project.

### pages/

Additional Streamlit pages used for navigation within the app.

---

## How the System Works

1. User opens the application.
2. User logs in or creates an account.
3. User profile and self-reported listening-context data are retrieved from
   the database.
4. The **XGBoost model predicts the user's preferred genre**.
5. The system either:
   - generates a new track using **Google Lyria**, or
   - retrieves a **Spotify playlist** matching the genre.
6. The recommendation is displayed to the user.

---

## Installation

### 1. Clone the Repository

```
git clone https://github.com/yourusername/MeloMatch-AI.git
cd MeloMatch-AI
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

## Environment Setup

Create a **Streamlit secrets file**:

```
.streamlit/secrets.toml
```

Add the following:

```
SPOTIFY_CLIENT_ID="your_spotify_client_id"
SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
LYRIA_API_KEY="your_lyria_api_key"
```

Never commit `secrets.toml` or any real credentials to the repository.

---

## Running the Application

Start the Streamlit app:

```
streamlit run Home.py
```

The application will launch in your browser.

---

## Technologies Used

- Python
- Streamlit
- XGBoost
- Spotify API (Spotipy)
- Google Lyria API
- NumPy
- Asyncio

---

## Author

Suhani Sharma, @<suha.shar2000@gmail.com>
