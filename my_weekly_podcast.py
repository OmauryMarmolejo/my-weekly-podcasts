import os 
from dotenv import load_dotenv
import spotipy
import spotipy.util as util

load_dotenv()

username= os.getenv('SPOTIFY_USERNAME')
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'https://localhost:8080'

scope = "user-library-read,playlist-modify-private,playlist-modify-public"
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id, 
                                   client_secret, 
                                   redirect_uri)
sp = spotipy.Spotify(auth=token)

results = sp.current_user_saved_shows()
show_ids = []
for idx, item in enumerate(results['items']):
    show = item['show']
    show_ids.append(show['id'])

last_episodes =  []
for show_id in show_ids:
    episodes = sp.show_episodes(show_id)
    last_episode = episodes['items'][0]
    print(last_episode['name'])
    last_episodes.append(last_episode['uri'])

playlist_id = os.getenv('SPOTIFY_PLAYLIST_ID')

current_tracks = sp.playlist_tracks(playlist_id)

current_uris = [track['track']['uri'] for track in current_tracks['items']]

uris = [episode for episode in last_episodes if episode not in current_uris]

if uris:
  sp.playlist_add_items(playlist_id, uris)
