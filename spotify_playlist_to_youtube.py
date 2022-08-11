# this is still such a mess please do not look at this code

from __future__ import print_function
import sys
import spotipy
import spotipy.util as util

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Checks .py is run with two arguments: Spotify username and the link to Spotify playlist
if len(sys.argv) > 2:
    username = sys.argv[1]
    playlist = sys.argv[2]
else:
    print("Usage: %s username playlist" % (sys.argv[0]))
    sys.exit()

# Spotify API
scope = 'user-library-read'
token = util.prompt_for_user_token(username, scope)

# Creates list of song titles and artist names
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

# YouTube API
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret_file.json"
scopes = 'https://www.googleapis.com/auth/youtube'
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

# Creates a YouTube playlist
request = youtube.playlists().insert(
    part="snippet,status",
    body={
        "snippet": {
        "title": "Spotify Playlist to YouTube",
        "defaultLanguage": "en"
        },
        "status": {
        "privacyStatus": "private"
        }
    }
)
response = request.execute()
iDresponse = response['id']

# For each song, searches YouTube, then adds to the playlist
j = 0
for song in songs:
    request = youtube.search().list(q=song,part='snippet',type='video', maxResults=1)
    response = request.execute()
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": iDresponse,
                "position": j,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": response['items'][0]['id']['videoId']
                }
            }
        }
    )
    response = request.execute()
    j += 1