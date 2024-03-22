import os

import soundfile as sf
import openl3

# def extract_features(audio_path: str):
#
#     audio, sr = sf.read('/Users/shirigilboa/audio_ai/moodify/moodify/wav_clips/7_Years_0.wav')
#
#     # get embedding using librosa frontend
#     input_repr, content_type, embedding_size = 'mel128', 'music', 6144
#     model = openl3.models.load_audio_embedding_model(
#         input_repr=input_repr, content_type=content_type, embedding_size=embedding_size, frontend='librosa')
#     # print(model.summary())
#     emb, ts = openl3.get_audio_embedding(audio, sr, model=model, frontend='librosa', input_repr=input_repr, content_type=content_type, embedding_size=embedding_size, center=True, hop_size=0.1, batch_size=32, verbose=True)
#     # print(emb.shape)
#     # print(ts.shape)
#     return emb, ts

def extract_features(audio_path: str):
    if os.path.exists(audio_path):
        audio, sr = sf.read(audio_path)
        embedding, ts = openl3.get_audio_embedding(audio, sr, input_repr="mel256", embedding_size=512)
        return embedding
    else:
        raise FileNotFoundError(f"File {audio_path} not found")

wav_file = '/Users/shirigilboa/audio_ai/moodify/moodify/wav_clips/7_Years_0.wav'
# embedding, _ = extract_features(wav_file)
extract_features(wav_file)
# print(embedding.shape)