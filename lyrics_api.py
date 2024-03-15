import pandas as pd
import requests

LYRICS_NOT_FOUND = "Lyrics not found"
LYRICS_API_URL = "https://api.lyrics.ovh/v1/"

# Function to get the lyrics for a song
def get_lyrics(song_name, artist_name):
    try:
        base_url = LYRICS_API_URL
        full_url = f"{base_url}{artist_name}/{song_name}"

        response = requests.get(full_url)
        if response.status_code == 200:
            data = response.json()
            lyrics = data.get('lyrics', LYRICS_NOT_FOUND)
            print("Lyrics found")
            return lyrics
        else:
            return LYRICS_NOT_FOUND
    except Exception as e:
        print(f"Error getting lyrics: {e}")
        return LYRICS_NOT_FOUND
