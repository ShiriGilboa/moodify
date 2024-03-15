import os

import pandas as pd
from transformers import pipeline
from lyrics_api import LYRICS_NOT_FOUND
# Load the data
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
df = pd.read_csv('data.csv')

# Initialize the classifier
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

# Define the emotion labels
emotion_labels = ['sadness', 'neutral', 'disappointment', 'annoyance', 'realization', 'disapproval', 'curiosity', 'nervousness', 'anger', 'confusion', 'approval', 'grief', 'amusement', 'caring', 'remorse', 'embarrassment', 'joy', 'disgust', 'optimism', 'desire', 'fear', 'surprise', 'relief', 'love', 'admiration', 'excitement', 'pride', 'gratitude']

MAX_LYRICS_LENGTH = 00

def classify_lyrics(song_name, lyrics):
    scores = {label: "null" for label in emotion_labels}  # Initialize scores with "null"

    if lyrics == LYRICS_NOT_FOUND:
        print(f"Lyrics not found for {song_name}")
        return scores

    try:
        print(f"Classifying lyrics for {song_name}")

        # Truncate lyrics to 400 words if necessary
        words = lyrics.split()
        if len(words) > 400:
            print(f"Truncating lyrics for {song_name}")
            words = words[:400]
        truncated_lyrics = ' '.join(words)

        # Apply the model to the lyrics
        model_outputs = classifier([truncated_lyrics])
        for output in model_outputs[0]:
            label = output['label']
            score = output['score']
            scores[label] = score

        return scores
    except Exception as e:
        print(f"Error classifying lyrics for {song_name}: {e}")
        return scores

# Save the updated DataFrame to a new CSV file
# df.to_csv('data_with_lyrics_class.csv', index=False)
