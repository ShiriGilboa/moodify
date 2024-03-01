import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_downloader import *

DATA_CSV_FILE = "data.csv"

# Set up Spotify client
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get audio features for a list of track IDs
def get_audio_features(track_ids):
    features = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        features.extend(sp.audio_features(batch))
    return features

# Function to get track metadata for a list of track IDs
def get_track_metadata(track_ids):
    metadata = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        metadata.extend(sp.tracks(batch)['tracks'])
    return metadata

# Example: Fetch audio features and metadata for a set of tracks
track_ids = ['3n3Ppam7vgaVa1iaRUc9Lp', '7dS5EaCoMnN7DzlpT6aRn2', '4VqPOruhp5EdPBeR92t6lQ']
audio_features = get_audio_features(track_ids)
track_metadata = get_track_metadata(track_ids)


def get_playlist_song_names(playlist_id):
    song_names = []
    song_ids = []
    results = sp.playlist_items(playlist_id, limit=100)
    for item in results['items']:
        track = item['track']
        song_names.append(track['name'])
        song_ids.append(track['id'])
    return song_ids, song_names

songs_ids, songs_list  = get_playlist_song_names("6nxPNnmSE0d5WlplUsa5L3") # sad songs


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

# Create the CSV file
with open(DATA_CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Define the header with individual feature columns
    writer.writerow(['Song ID', 'Song Name', 'Artist', 'Length', 'Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Time Signature', 'Spectrogram Path', 'Emotion'])

    for song_id, song_name in zip(songs_ids, songs_list):
        try:
            print(f"Downloading {song_name}")
            song_path = download_song(song_name)
            print(f"Creating spectrogram for {song_name}")
            spec_path = create_spectrogram(song_name=song_name, song_file_path=song_path)

            print(f"Extracting features for {song_name}")
            features = get_song_features(song_id)

            # Extract additional information from the features
            artist = features['artist']
            length = features['length']

            # Write the data to the CSV file, including individual features
            writer.writerow([
                song_id, song_name, artist, length,
                features['danceability'], features['energy'], features['key'], features['loudness'],
                features['mode'], features['speechiness'], features['acousticness'], features['instrumentalness'],
                features['liveness'], features['valence'], features['tempo'], features['time_signature'],
                spec_path, 'SAD'
            ])
        except Exception as e:
            print(f"Error processing {song_name}: {e}")
            continue
