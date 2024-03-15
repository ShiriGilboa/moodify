import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Playlists to fetch
playlists = {
    "sad": ["6kIofAY27hecJAuDln8t53", "6nxPNnmSE0d5WlplUsa5L3", "3p0pyQmJi6h3xUn25403WH"],
    "happy": ["37i9dQZF1DX84kJlLdo9vT", "0RH319xCjeU8VyTSqCF6M4", "37i9dQZF1EIgG2NEOhqsD7"],
    "in-love": ["6oNsYDhN95gkENsdFcAwTh", "37i9dQZF1DX4pAtJteyweQ"],
    "angry": ["0jbaEzUwLTOlIOp42B5pXV", "32jdsAx2HOE3I8cDKXynlK", "4Tdgj7NprP4Ou3qzul2WLX"]
}

# Function to fetch playlist details
def fetch_playlist_details(playlist_id):
    playlist = sp.playlist(playlist_id)
    name = playlist['name']
    owner = playlist['owner']['display_name']
    return name, owner

# Generate LaTeX table
latex_table = """
\\begin{table}[h]
\\centering
\\begin{tabular}{|l|l|l|l|}
\\hline
Emotion & Playlist ID & Playlist Name & Author \\\\ \\hline
"""

for emotion, playlist_ids in playlists.items():
    for playlist_id in playlist_ids:
        name, owner = fetch_playlist_details(playlist_id)
        latex_table += f"{emotion} & \\href{{https://open.spotify.com/playlist/{playlist_id}}}{{{playlist_id}}} & {name} & {owner} \\\\ \\hline\n"

latex_table += """
\\end{tabular}
\\caption{Spotify Playlists Used for Dataset Creation}
\\label{tab:playlists}
\\end{table}
"""

print(latex_table)
