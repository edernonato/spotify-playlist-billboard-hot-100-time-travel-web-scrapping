import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "8122d25ed2784d47b49c399195e438e6"
CLIENT_SECRET = "078d74616cfb4745aaf6d60d6357cc4e"
REDIRECT_URI = "http://example.com"
USERNAME = "31dv3yv2rnz7g7it6jx3wzh4o3zy"
scope = "playlist-modify-public"
partial_url = "https://www.billboard.com/charts/hot-100/"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                    redirect_uri=REDIRECT_URI, scope=scope))

year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

url = partial_url + year

response = requests.get(url)
website = response.text
soup = BeautifulSoup(website, "html.parser")

songs_tag = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
songs = [song.text.replace("\t", "").replace("\n", "") for song in songs_tag]
artists_tag = soup.find_all(name="span", class_="a-no-trucate")
artists = [artist.text.replace("\t", "").replace("\n", "") for artist in artists_tag]

USER_ID = spotify.current_user()["id"]
playlist_description = "Playlist of Top 100 songs played in " + year
new_playlist_name = f"Billboard TOP 100 {year}"

user_playlists = spotify.current_user_playlists()
playlists_name = []

if user_playlists["items"]:
    for item in user_playlists.keys():
        playlists_name.append(user_playlists["items"][0]["name"])

tracks_uri = []

for index in range(len(songs)):
    print(f"{index + 1}: {songs[index]}, {artists[index]}")
    results = spotify.search(q=f"'track': {songs[index]} 'artist': {artists[index]}", limit=1, type='track')
    if results["tracks"]["items"][0]:
        tracks_uri.append(results["tracks"]["items"][0]["uri"])

for track in tracks_uri:
    print(track)

if new_playlist_name in playlists_name:
    print("PLAYLIST ALREADY CREATED")
else:
    new_playlist = spotify.user_playlist_create(user=USER_ID, name=new_playlist_name, description=playlist_description)
    print(new_playlist["id"])
    spotify.playlist_add_items(new_playlist["id"], tracks_uri)
    print(f"{new_playlist_name} Created!")
