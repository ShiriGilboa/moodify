import os
import subprocess

from pydub import AudioSegment
WAV_CLIPS_PATH = "./wav_clips"

def create_short_wav_clips_ffmpeg(song_name, mp3_path, clip_duration=20, num_clips=3):
    """
    Creates short WAV clips from an MP3 file using FFmpeg.

    Parameters:
        mp3_path (str): Path to the MP3 file.
        output_dir (str): Directory to save the WAV clips.
        clip_duration (int): Duration of each clip in seconds (default is 20 seconds).
        num_clips (int): Number of clips to create (default is 3).
    """
    # Get the duration of the MP3 file in seconds
    total_duration_cmd = ['ffprobe', '-v', 'error', '-show_entries',
                          'format=duration', '-of',
                          'default=noprint_wrappers=1:nokey=1', mp3_path]
    total_duration = float(subprocess.check_output(total_duration_cmd).decode('utf-8').strip())
    print(total_duration)
    # Calculate the start times for each clip
    interval = (total_duration - clip_duration) / (num_clips + 1)
    start_times = [interval * (i + 1) for i in range(num_clips)]
    output_paths = []
    for i, start_time in enumerate(start_times):
        file_name = song_name.replace(" ", "_")
        wav_path = os.path.join(WAV_CLIPS_PATH, f"{file_name}_{i}.wav")
        ffmpeg_cmd = ['ffmpeg', '-ss', str(start_time), '-t', str(clip_duration), '-y',
                      '-i', mp3_path, '-acodec', 'pcm_s16le', '-ac', '2', wav_path]
        subprocess.run(ffmpeg_cmd)
        output_paths.append(wav_path)
    return output_paths



# song_path = '/Users/shirigilboa/audio_ai/moodify/moodify/full_songs_files/7_Years.mp3'
# output_dir = '/Users/shirigilboa/audio_ai/moodify/moodify/wav_clips'
# create_short_wav_clips_ffmpeg(song_path, output_dir)
