import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



# Set up Spotify client
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_audio_features(track_ids):
    features = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i + 50]
        features.extend(sp.audio_features(batch))
    return features

def get_track_metadata(track_ids):
    metadata = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i + 50]
        metadata.extend(sp.tracks(batch)['tracks'])
    return metadata

def get_playlist_song_names(playlist_id):
    song_names = []
    song_ids = []
    results = sp.playlist_items(playlist_id, limit=100)
    for item in results['items']:
        track = item['track']
        song_names.append(track['name'])
        song_ids.append(track['id'])
    return song_ids, song_names

def get_song_features(song_id):
    # Get the audio features
    audio_features = sp.audio_features(song_id)[0]

    # Get the track information
    track_info = sp.track(song_id)

    # Extract the artist's name and song's length
    artist = track_info['artists'][0]['name']
    length = track_info['duration_ms']

    # Combine the audio features with the additional information
    features = audio_features.copy()
    features['artist'] = artist
    features['length'] = length

    return features

def fetch_playlist_details(playlist_id):
    playlist = sp.playlist(playlist_id)
    name = playlist['name']
    owner = playlist['owner']['display_name']
    return name, owner
