import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_downloader import *
from lyrics_api import *
from wav_from_mp3 import *
from spotify_api import *

DATA_CSV_FILE = "data.csv"

playlists = {"sad": ["6kIofAY27hecJAuDln8t53", "6nxPNnmSE0d5WlplUsa5L3", "3p0pyQmJi6h3xUn25403WH"],
             "happy": ["37i9dQZF1DX84kJlLdo9vT", "0RH319xCjeU8VyTSqCF6M4", "37i9dQZF1EIgG2NEOhqsD7"],
             "in-love": ["6oNsYDhN95gkENsdFcAwTh", "37i9dQZF1DX4pAtJteyweQ"],
             "angry": ["0jbaEzUwLTOlIOp42B5pXV", "32jdsAx2HOE3I8cDKXynlK", "4Tdgj7NprP4Ou3qzul2WLX"]}

# Initialize a set to track unique song ID-emotion pairs
unique_song_emotion_pairs = set()

# Initialize a list to track conflicting songs
conflicting_songs = []


def process_single_song(song_name, emotion):
    try:
        print(f"Processing song name: {song_name}")
        song_id = get_song_id(song_name)
        song_path = download_song(song_name)
        wav_files_paths = create_short_wav_clips_ffmpeg(song_name, song_path)
        features = get_song_features(song_id)
        artist = features['artist']
        length = features['length']
        lyrics = get_lyrics(song_name, artist)
        lyrics_scores = classify_lyrics(song_name, lyrics)
        for wav_file in wav_files_paths:
            writer.writerow([
                song_id, song_name, artist, length,
                features['danceability'], features['energy'], features['key'], features['loudness'],
                features['mode'], features['speechiness'], features['acousticness'],
                features['instrumentalness'], features['liveness'], features['valence'], features['tempo'],
                features['time_signature'], wav_file, lyrics, lyrics_scores['sadness'],
                lyrics_scores['neutral'],
                lyrics_scores['disappointment'], lyrics_scores['annoyance'], lyrics_scores['realization'],
                lyrics_scores['disapproval'], lyrics_scores['curiosity'], lyrics_scores['nervousness'],
                lyrics_scores['anger'], lyrics_scores['confusion'], lyrics_scores['approval'],
                lyrics_scores['grief'], lyrics_scores['amusement'], lyrics_scores['caring'],
                lyrics_scores['remorse'], lyrics_scores['embarrassment'], lyrics_scores['joy'],
                lyrics_scores['disgust'], lyrics_scores['optimism'], lyrics_scores['desire'],
                lyrics_scores['fear'], lyrics_scores['surprise'], lyrics_scores['relief'],
                lyrics_scores['love'], lyrics_scores['admiration'], lyrics_scores['excitement'],
                lyrics_scores['pride'], lyrics_scores['gratitude'], emotion
            ])
        unique_song_emotion_pairs.add((song_id, emotion))
        print(f"Done processing {song_name}")
    except Exception as e:
        print(f"Error processing {song_name}: {e}")
        return


if os.path.exists(DATA_CSV_FILE):
    with open(DATA_CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            song_id = row[0]
            emotion = row[-1]
            unique_song_emotion_pairs.add((song_id, emotion))

# Create the CSV file
with open(DATA_CSV_FILE, mode='a', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow([
        'Song ID', 'Song Name', 'Artist', 'Length', 'Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness',
        'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Time Signature', 'wav Path', 'Lyrics',
        'sadness', 'neutral', 'disappointment', 'annoyance', 'realization', 'disapproval', 'curiosity', 'nervousness',
        'anger', 'confusion', 'approval', 'grief', 'amusement', 'caring', 'remorse', 'embarrassment', 'joy', 'disgust',
        'optimism', 'desire', 'fear', 'surprise', 'relief', 'love', 'admiration', 'excitement', 'pride', 'gratitude',
        'Emotion'
    ])

    # Iterate through the playlists
    for emotion, playlist_ids in playlists.items():
        for playlist_id in playlist_ids:
            name, _ = fetch_playlist_details
            print(f"Processing playlist {name} with emotion {emotion}")
            songs_ids, songs_list = get_playlist_song_names(playlist_id)
            for song_id, song_name in zip(songs_ids, songs_list):
                try:
                    if (song_id, emotion) in unique_song_emotion_pairs:
                        print(f"Skipping duplicate song: {song_name} with emotion {emotion}")
                        continue
                    elif song_id in [pair[0] for pair in unique_song_emotion_pairs]:
                        conflicting_songs.append(song_name)
                    process_song(song_name, emotion)
                except Exception as e:
                    print(f"Error processing {song_name}: {e}")
                    continue

    print(
        f"Done processing songs. Conflicting songs: {conflicting_songs} Total processed songs: {len(unique_song_emotion_pairs)}")
