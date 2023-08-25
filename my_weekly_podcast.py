import spotipy
import spotipy.util as util

username= ''
client_id = ''
client_secret = ''
redirect_uri = 'https://localhost:8080'
# scope= 'playlist-modify-private,playlist-modify-public'

scope = "user-library-read,playlist-modify-private,playlist-modify-public"
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id, 
                                   client_secret, 
                                   redirect_uri)
sp = spotipy.Spotify(auth=token)

playlist_id = '' 

results = sp.current_user_saved_shows()
show_ids = []
for idx, item in enumerate(results['items']):
    show = item['show']
    show_ids.append(show['id'])

uris =  []
for show_id in show_ids:
    episodes = sp.show_episodes(show_id)
    last_episode = episodes['items'][0]
    print(last_episode['name'])
    uris.append(last_episode['uri'])

sp.playlist_add_items(playlist_id, uris)