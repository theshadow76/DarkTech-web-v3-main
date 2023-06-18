import os
import requests
import time
import tweepy

class TwitterAPI:


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
