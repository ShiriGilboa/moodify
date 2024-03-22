# Moodify: Emotion Detection in Music

Moodify is a project aimed at classifying songs into four emotions: Happy, Sad, Angry, and In-Love. The project utilizes a unique dataset comprising Spotify audio features, emotional tags from a language model based on Roberta using the song lyrics, and feature embeddings extracted from the OpenL3 model.

## Getting Started

### Prerequisites

- Python 3.9
- Libraries: `spotipy`, `youtube_dl`, `requests`, `ffmpeg`, `scikit-learn`, `xgboost`
- Spotify API credentials: Client ID and Client Secret

### Installation


Install the required libraries
1. spotipy 
2. youtube_dl 
3. requests 
4. ffmpeg 
5. scikit-learn 
6. xgboost
7. openl3
8. tensorflow


The script will:

Fetch songs from predefined Spotify playlists.
Download the audio files and lyrics.
Extract audio features and embeddings.
Classify the songs into emotions and save the results in data.csv.



