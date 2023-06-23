from modules.authenticator import authenticator
import pandas as pd

#Extractor
def extract_features(sp, info_dict, url_types):

    # Initialize Spotify user credentials
    sp = authenticator()

    track_uris = []

    for i in range(len(info_dict)):

        url_type = url_types[i]
        item = info_dict[i]

        # Extract track URI
        if url_type in ['playlist', 'track']:
            track_uri = item['track']['uri']
        elif url_type in 'album':
            track_uri = item['uri']
        elif url_type == 'artist':
            track_uri = item['track']['uri']
        else:
            track_uri = None

        track_uris.append(track_uri)

    audio_features = [list(sp.audio_features(uri)[0].values()) for uri in track_uris]

    feature_keys = list(sp.audio_features(track_uris[0])[0].keys())

    data_features_df = pd.DataFrame({'Track URI': track_uris})

    audio_features_df = pd.DataFrame(audio_features, columns=feature_keys).drop(
        ['type', 'id', 'uri', 'track_href', 'analysis_url'], axis=1)

    playlist_df = pd.concat([data_features_df, audio_features_df], axis=1, join='inner') \
        .set_index('Track URI')

    return playlist_df