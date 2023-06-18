import tweepy
import requests

CLIENT_ID_SECRET = "KmCoAZapOhXI9b-pq37Eq8jwFefAWDS1ynfXm6rTR9kQu-Qokl"
CLIENT_ID = "bzRHdWNDUXZGNjIyalN0NVJDZnM6MTpjaQ"
API_KEY = "0xLqPIweifAb0E6ymKeMemJF5"
API_KEY_SECRET = "gF7LjynN8KRL7MOnomYVbNSYYXnZWL83W78OgF6A1cFTXS6zxi"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAC61oAEAAAAATv3V%2Bw%2BDdSmQVzAvpezr44IMGNI%3DD1Vpa8eaAG2r0C2Z0lrzXYUKD7MeLiwWbfPVQAwK9bh7PhqCP5"
ACCESS_TOKEN = "1668931265435713541-t6uZRhf6YigavQp2TWk3xpiRToVy9p"
ACCESS_TOKEN_SECRET = "w0OqCVRNUGu5Fv8Q7uHrz63fEZq6Rfl81A5fLxXUldVet"

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri="Callback / Redirect URI / https://theshadowtech.com",
    scope=["Scope here", "Scope here"],
    # Client Secret is only necessary if using a confidential client
    client_secret=CLIENT_ID_SECRET
)

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

keywords = ["Java", "MachineLearning", "DataScience", "Python", "OpenAI", "DeepLearning", "BigData", "IoT", "Tech", "Innovation", "Startups", "Blockchain", "Cybersecurity", "CloudComputing"]

class SearchTeet:
    def __init__(self, min_followers: int =1000):
        self.query = "Gaming"
        self.user = ""
        self.min_followers = min_followers
        # self.action = Action()
    
    def get_user(self):
        for keyword in keywords:
            try:
                print(f"Searching for {keyword}")
                tweets = requests.get(f"https://api.twitter.com/2/tweets/search/recent?query={keyword}&tweet.fields=created_at&expansions=author_id&user.fields=public_metrics", headers={"Authorization" : f"Bearer {BEARER_TOKEN}"})
                for tweet in tweets.json()['data']:
                    try:
                        # print(tweet['id'])
                        # users = requests.get(f"https://api.twitter.com/2/users/{tweet['author_id']}", headers={"Authorization" : f"Bearer {BEARER_TOKEN}"})
                        # print(f"users: {users.json()}")
                        followers = requests.get(f"https://api.twitter.com/2/users/{tweet['author_id']}?user.fields=public_metrics", headers={"Authorization" : f"Bearer {BEARER_TOKEN}"})
                        dataFLW = followers.json()['data']
                        dataFLW2 = dataFLW['public_metrics']
                        dataFLW3 = dataFLW2['followers_count']
                        if dataFLW3 > self.min_followers:
                            print(f"Found a user with more than 100000 followers: {tweet['author_id']}")
                            client.create_tweet(text=f"you should check this out!: https://theshadowtech.com", in_reply_to_tweet_id=tweet['id'])
                            # self.action.LikeTweet()
                        else:
                            print(f"this user: {tweet['author_id']} has less than 100000 followers, next...")
                        # print(f"tweeted {tweet['id']}")
                    except:
                        print("error getting user")
            except:
                print("Error with your keyword")
    def TweetToUser(self):
        pass

class Action:
    def __init__(self):
        pass
    def LikeTweet(self):
        try:
            for keyword in keywords:
                try:
                    print(f"Searching for {keyword}")
                    tweets = requests.get(f"https://api.twitter.com/2/tweets/search/recent?query={keyword}&tweet.fields=created_at&expansions=author_id&user.fields=public_metrics", headers={"Authorization" : f"Bearer {BEARER_TOKEN}"})
                    for tweet in tweets.json()['data']:
                        try:
                            client.like(tweet['id'])
                            print(f"liked {tweet['id']}")
                        except:
                            print("error liking tweet")
                except:
                    print("Error with your keyword")
        except:
            print("Something went wrong")

def main():
    search = SearchTeet()
    search.get_user()

if __name__ == "__main__":
    main()