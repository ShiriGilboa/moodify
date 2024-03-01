import os.path

from googleapiclient.discovery import build
from pytube import YouTube
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Set up the YouTube Data API
api_key = os.getenv('YONI_YOUTUBE_API')
youtube = build('youtube', 'v3', developerKey=api_key)

SONGS_FILES_OUTPUT_PATH = "./full_songs_files"
SPECTOGRAM_PATH = "./spectograms"


def download_song(song_name):
    file_name = song_name.replace(" ", "_")
    file_name = f"{file_name}.mp3"
    file_path = os.path.join(SONGS_FILES_OUTPUT_PATH, f'{file_name}')
    # Search for the song on YouTube
    if not os.path.exists(file_path) :
        request = youtube.search().list(q=song_name, part='snippet', type='video', maxResults=1)
        response = request.execute()

        # Get the first video's URL
        video_id = response['items'][0]['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        # Download the audio using pytube
        yt = YouTube(video_url)
        audio_stream = yt.streams.get_audio_only()

        audio_stream.download(output_path=SONGS_FILES_OUTPUT_PATH, filename=f'{file_name}')

        print(f'Downloaded audio for "{song_name}" from {video_url}')
    else:
        print(f'File already exists for "{song_name}"')
    return file_path


def create_spectrogram(song_name, song_file_path):
    y, sr = librosa.load(song_file_path, duration=30, offset=60)

    # Generate the spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr)

    # Convert to dB
    S_dB = librosa.power_to_db(S, ref=np.max)

    # Plot the spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram of the First 30 Seconds of the Song')

    # Save the spectrogram to a file
    file_name = song_name.replace(" ", "_")
    spec_path = os.path.join(SPECTOGRAM_PATH, f"{file_name}.png")
    plt.savefig(spec_path)
    plt.close()  # Close the plot to free up memory

    print(f"Spectrogram saved to {spec_path}")
    return spec_path
