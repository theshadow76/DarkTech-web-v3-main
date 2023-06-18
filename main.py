import os
import requests
import time
import tweepy

class TwitterAPI:
    def __init__(self):
        self.CLIENT_ID_SECRET = "KmCoAZapOhXI9b-pq37Eq8jwFefAWDS1ynfXm6rTR9kQu-Qokl"
        self.CLIENT_ID = "bzRHdWNDUXZGNjIyalN0NVJDZnM6MTpjaQ"
        self.API_KEY = "0xLqPIweifAb0E6ymKeMemJF5"
        self.API_KEY_SECRET = "gF7LjynN8KRL7MOnomYVbNSYYXnZWL83W78OgF6A1cFTXS6zxi"
        self.ACCESS_TOKEN = "1668931265435713541-t6uZRhf6YigavQp2TWk3xpiRToVy9p"
        self.ACCESS_TOKEN_SECRET = "w0OqCVRNUGu5Fv8Q7uHrz63fEZq6Rfl81A5fLxXUldVet"
        self.BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAC61oAEAAAAATv3V%2Bw%2BDdSmQVzAvpezr44IMGNI%3DD1Vpa8eaAG2r0C2Z0lrzXYUKD7MeLiwWbfPVQAwK9bh7PhqCP5"
        self.base_url = "https://api.twitter.com/2/"
        self.headers = {"Authorization": f"Bearer {self.BEARER_TOKEN}"}
        self.client = self.authenticate()

    def authenticate(self):
        oauth2_user_handler = tweepy.OAuth2UserHandler(
            client_id=self.CLIENT_ID,
            redirect_uri="Callback / Redirect URI / https://theshadowtech.com",
            scope=["Scope here", "Scope here"],
            client_secret=self.CLIENT_ID_SECRET
        )

        client = tweepy.Client(
            consumer_key=self.API_KEY,
            consumer_secret=self.API_KEY_SECRET,
            access_token=self.ACCESS_TOKEN,
            access_token_secret=self.ACCESS_TOKEN_SECRET
        )
        return client

    def search_users(self, keywords, min_followers=1000):
        query = f"{keywords}"
        tweets = requests.get(f"{self.base_url}tweets/search/recent?query={query}&tweet.fields=created_at&expansions=author_id&user.fields=created_at", headers=self.headers)
        for tweet in tweets.json()["data"]:
            self.client.create_tweet(text="Nice tweet!", in_reply_to_tweet_id=tweet["id"])
            self.client.like(tweet["id"])
            self.client.retweet(tweet["id"])
            print("Done")
            time.sleep(1)
# Create an instance of the class outside the class
twitter_api = TwitterAPI()

CLIENT_ID_SECRET = "KmCoAZapOhXI9b-pq37Eq8jwFefAWDS1ynfXm6rTR9kQu-Qokl"
CLIENT_ID = "bzRHdWNDUXZGNjIyalN0NVJDZnM6MTpjaQ"
API_KEY = "0xLqPIweifAb0E6ymKeMemJF5"
API_KEY_SECRET = "gF7LjynN8KRL7MOnomYVbNSYYXnZWL83W78OgF6A1cFTXS6zxi"
ACCESS_TOKEN = "1668931265435713541-t6uZRhf6YigavQp2TWk3xpiRToVy9p"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAC61oAEAAAAATv3V%2Bw%2BDdSmQVzAvpezr44IMGNI%3DD1Vpa8eaAG2r0C2Z0lrzXYUKD7MeLiwWbfPVQAwK9bh7PhqCP5"
base_url = "https://api.twitter.com/2/"
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
client = twitter_api.authenticate()

def test(usernames, likes = False, retweets = False):
    try:
        for username in usernames:
            user_id = client.get_user(username=username, user_auth=True)
            user_id_formatted = str(user_id).split()
            for word in user_id_formatted:
                if word.startswith("id="):
                    Id = ''
                    for s in word:
                        if s.isdigit():
                            Id += s
                    print(f"User ID: {Id}")
                    tweet_ids = client.get_users_tweets(id=Id, user_auth=True)
                    data = str(tweet_ids).split()
                    for word in data:
                        if word.startswith("id="):
                            id = ''
                            for s in word:
                                if s.isdigit():
                                    id += s
                            print(f"Tweet ID: {id}")
                            client.create_tweet(text="Nice tweet!", in_reply_to_tweet_id=id)
                            if likes and retweets:
                                client.like(id)
                                client.retweet(id)
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"status": "failure", "error": f"Error: {e}"}