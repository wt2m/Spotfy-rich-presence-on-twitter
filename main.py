import requests
import dotenv
import os
import tweepy
import spotipy.util as util
import time
import threading

dotenv.load_dotenv(dotenv.find_dotenv()); ##reading env

##twitter api variables
twitter = {
    "bearer": os.getenv('TWITTER_BEARER_TOKEN'), 
    "consumer_key":os.getenv('TWITTER_KEY'), 
    "consumer_key_secret" : os.getenv('TWITTER_KEY_SECRET'),
    "access_token" : os.getenv('TWITTER_ACCESS_TOKEN'),
    "access_token_secret" : os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    "redirect": "http://localhost:7777/callback"
}

##spotify api variables
spotify = {
    "client": os.getenv("SPOTIFY_CLIENT"),
    "secret": os.getenv("SPOTIFY_SECRET"),
    "username": os.getenv("SPOTIFY_USERNAME"),
    "redirect": "http://localhost:7777/callback",
    "scope": "user-read-currently-playing"
}

print("Initializing")



def main():
    threading.Timer(60.0, main).start()
    token = get_token()
    current_track = get_current_track(token)
    if(current_track != 'Old track'):
        change_twitter_status(current_track['name'], current_track['artist'])




def get_current_track(token: str) -> str:
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer ' + token,
    }
    
    try:
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', 
                    headers = headers, timeout = 5)
        json = response.json()
        old_track = ''
        song = {
            'artist': json['item']['album']['artists'][0]['name'],
            'name': json['item']['name']
        }
        if(song['name'] == old_track):
            return 'Old track'
        else:
            old_track = song['name']
            return song
    except:
        return None

def get_token() -> str:
    token = util.prompt_for_user_token(username=spotify['username'], 
                                   scope=spotify['scope'], 
                                   client_id=spotify['client'],   
                                   client_secret=spotify['secret'],     
                                   redirect_uri=spotify['redirect'])
    return token
    




def change_twitter_status(song_name:str, artist: str) -> str:
    auth = tweepy.OAuth1UserHandler(
    twitter['consumer_key'], twitter['consumer_key_secret'], twitter['access_token'], twitter['access_token_secret']
    )
    try:
        twitterAPI = tweepy.API(auth)
        description = "based low profile guy \n\nplaying on spotfy: " + artist + ' "' + song_name+'"'
        twitterAPI.update_profile(description=description)
        print(time.ctime() + " Description changed to: \n" + description)
    except:
        return False
    


if __name__ == "__main__": #calling main function when runs the file
    main()