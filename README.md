# TheraBeat AI

Optimizing Music Therapy for a Person’s Music Preferences and 
Mental Health Symptoms Using Generative AI.

## Description

This is the GitHub repository for the development of a working application that aims to allow Music Therapy to become more accessible to a wide audience, including those who may not be able to afford traditional therapy. This app will offer personalized support for individuals facing mental health issues like Depression, Anxiety, OCD, and Insomnia. To do this, the app gathers user information such as age, music preferences, and self-reported mental health ratings on a scale from 1 to 10. Then the app will use this participant data to recommend music genres that may improve the user’s mental well-being using a Machine Learning model. In addition, the app uses Generative AI to create custom playlists tailored to individual needs. This approach ensures that a scientifically validated and accessible form of music therapy will be offered to a diverse range of users.

# Project Structure

```
Therabeat-AI/
│
├── app.py
├── Home.py
├── login.py
├── music.py
├── database.py
├── best_xgb
├── requirements.txt
├── pages/
└── README.md
```

## File Descriptions

### app.py
Main application logic for the Streamlit app.  
Handles model loading, Spotify initialization, and displaying music recommendations.

### Home.py
Landing page of the Streamlit application.  
Controls login state, loads the machine learning model, and manages the main user interface.

### login.py
Handles authentication login, logout, session management, and retrieving the current user

### music.py
Contains the functionalities of predicting favorite genre using the ML model, generating music using Google Lyria, retrieving Spotify playlists, and mapping genres to prompts for music generation

### database.py
Manages user data including:
- creating user profiles
- retrieving stored user information
- updating mood data
- displaying user profile information

### best_xgb
Optimized **XGBoost model** used to predict the user’s favorite music genre.

### requirements.txt
A list of Python dependencies required to run the project.

### pages/
Contains additional, stylized Streamlit pages used for navigation within the app, 

---

# How the System Works

1. User opens the application.
2. User logs in or creates an account.
3. User profile and mood data are retrieved from the database.
4. The **XGBoost model predicts the user’s preferred genre**.
5. The system either:
   - generates a new song using **Google Lyria**, or
   - retrieves a **Spotify playlist** matching the genre.
6. The recommended music is displayed to the user.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Therabeat-AI.git
cd Therabeat-AI
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```
---

# Environment Setup

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
---

# Running the Application

Start the Streamlit app:

```bash
streamlit run Home.py
```
The application will launch in your browser.

---

# Technologies Used

- Python
- Streamlit
- XGBoost
- Spotify API (Spotipy)
- Google Lyria API
- NumPy
- Asyncio

---

## Author
Suhani Sharma, @suha.shar2000@gmail.com
