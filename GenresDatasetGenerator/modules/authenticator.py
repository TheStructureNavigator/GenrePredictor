####################################################
#-----------Spotify API user credentials-----------#
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
####################################################

#----------------Client keys------------------#
client_id = 'a7058d1ff16a485fbf7b490d8737e92e'
secret = 'bce158ba00fb48718c49c44651f9aa45'
#---------------------------------------------#

#--------------------------------Authenticator-----------------------------------#
def authenticator(client_id = client_id, secret = secret):
    client_credentials_manager = SpotifyClientCredentials(client_id = client_id, 
                                                          client_secret = secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    return sp
#--------------------------------------------------------------------------------#
