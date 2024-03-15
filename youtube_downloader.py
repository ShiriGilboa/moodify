import os.path

from googleapiclient.discovery import build
from pytube import YouTube
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

os.system("source ~/.zshrc")
api_key = os.getenv('YONI_YOUTUBE_API')
youtube = build('youtube', 'v3', developerKey=api_key)

SONGS_FILES_OUTPUT_PATH = "./full_songs_files"
SPECTOGRAM_PATH = "./spectograms"


def download_song(song_name):
    file_name = song_name.replace(" ", "_")
    file_name = f"{file_name}.mp3"
    file_path = os.path.join(SONGS_FILES_OUTPUT_PATH, f'{file_name}')
    # Search for the song on YouTube
    if not os.path.exists(file_path):
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


def load_audio_segment(song_file_path, start, duration):
    """Load a segment of an audio file."""
    y, sr = librosa.load(song_file_path, offset=start, duration=duration)
    return y, sr

def generate_mel_spectrogram(y, sr, n_mels=128, target_length=1292):
    """Generate a mel-scaled spectrogram."""
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)

    # Resize or pad the spectrogram to ensure a consistent shape
    if S.shape[1] < target_length:
        S = np.pad(S, ((0, 0), (0, target_length - S.shape[1])), mode='constant')
    elif S.shape[1] > target_length:
        S = S[:, :target_length]

    return S

def save_spectrogram(S, file_path):
    """Save a spectrogram to a .npy file."""
    np.save(file_path, S)

def process_song(song_name, song_file_path, num_spectrograms=3, segment_duration=30):
    """Process a song to generate and save multiple spectrograms."""
    # Load the entire song to determine its total duration
    file_name = song_name.replace(" ", "_")
    spec_path = os.path.join(SPECTOGRAM_PATH, f"{file_name}.npy")
    y_full, sr = librosa.load(song_file_path)
    total_duration = len(y_full) / sr

    # Calculate the start times for each segment
    segment_starts = np.linspace(0, total_duration - segment_duration, num_spectrograms)

    # Initialize the list of spectrogram paths
    spectrogram_paths = []

    # Generate and save spectrograms for each segment
    for i, start in enumerate(segment_starts):
        spec_path = os.path.join(SPECTOGRAM_PATH, f"{file_name}_{i}.npy")
        if not os.path.exists(spec_path):
            y, sr = load_audio_segment(song_file_path, start, segment_duration)
            S = generate_mel_spectrogram(y, sr)
            save_spectrogram(S, spec_path)
            spectrogram_paths.append(spec_path)
    return spectrogram_paths

def create_spectrogram(song_name, song_file_path):
    file_name = song_name.replace(" ", "_")
    spec_path = os.path.join(SPECTOGRAM_PATH, f"{file_name}.npy")
    if not os.path.exists(spec_path):
        load_and_process_spectrogram(song_file_path)
    return spec_path

def load_and_process_spectrogram(song_file_path):
    # Load the song with a specific duration and offset
    y, sr = librosa.load(song_file_path, duration=30, offset=60)

    # Compute the mel-scaled spectrogram with 128 mel bands
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)

    # Ensure the spectrogram has 1292 time frames (adjust hop_length if needed)
    expected_frames = 1292
    hop_length = int(len(y) / (expected_frames - 1))

    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, hop_length=hop_length)

    # Check the shape of the spectrogram
    assert S.shape == (128, 1292), f"Unexpected spectrogram shape: {S.shape}"

    return S
