import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '6dad214ac6f249049d2ea16396e95533'
client_secret = '2754466718b944c299de88ccad4ffb41'

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

def get_track_id(artist_name, track_name):
    query = f"artist:{artist_name} track:{track_name}"
    results = sp.search(q=query, type='track')
    if results['tracks']['items']:
        return results['tracks']['items'][0]['id']
    else:
        return None

def get_audio_features(track_id):
    audio_features = sp.audio_features([track_id])
    if audio_features:
        energy = audio_features[0]['energy']
        valence = audio_features[0]['valence']
        tempo = audio_features[0]['tempo']
        danceability = audio_features[0]['danceability']
        return {
            'energy': energy,
            'valence': valence,
            'tempo': tempo,
            'danceability': danceability
        }
    else:
        return None
def get_track_release_year(track_id):
    track_info = sp.track(track_id)
    release_year = track_info['album']['release_date'][:4]
    return release_year

if __name__ == '__main__':
    print('spotify feature')