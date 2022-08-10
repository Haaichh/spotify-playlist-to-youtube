from __future__ import print_function
import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read'

if len(sys.argv) > 2:
    username = sys.argv[1]
    playlist = sys.argv[2]
else:
    print("Usage: %s username playlist" % (sys.argv[0]))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.playlist_tracks(playlist)
    total = results['total']
    offset = 0
    songs = []
    while total > 0:
        results = sp.playlist_tracks(playlist, offset=offset)
        for item in results['items']:
            if item['track'] == None: continue
            track = item['track']
            songs.append(track['name'] + ' - ' + track['artists'][0]['name'])
        offset += 100
        total -= 100
else:
    print("Can't get token for", username)

print(songs, len(songs))