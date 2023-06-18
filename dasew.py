import os
import requests
import time

# Set up authentication credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAAC61oAEAAAAATv3V%2Bw%2BDdSmQVzAvpezr44IMGNI%3DD1Vpa8eaAG2r0C2Z0lrzXYUKD7MeLiwWbfPVQAwK9bh7PhqCP5"

# Set up the API endpoint and headers
base_url = "https://api.twitter.com/2/"
headers = {"Authorization": f"Bearer {bearer_token}"}

# Define a function to search for users based on keywords
def search_users(keywords, min_followers=1000):
    # Set up the search parameters
    query = f"{keywords}"
    params = {
        "query": query,
        "max_results": 10,
        "expansions": "author_id",
        "user.fields": "public_metrics"
    }
    
    # Make the API call
    response = requests.get(f"{base_url}tweets/search/recent", headers=headers, params=params)
    
    # Parse the response
    data = response.json()
    print(data)

    # Extract the user information from the tweets
    for user in data["data"]:
        user1 = user["author_id"]
        print(user1)
        users = requests.get(f"{base_url}users/", headers=headers, params={"ids" : user1, "user.fields": "public_metrics"})
        print(users.json())
    
    return users

# Define a function to get a user's tweets
def get_user_tweets(user_id, max_results=10):
    # Set up the API endpoint and parameters
    url = f"{base_url}users/{user_id}/tweets"
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at"
    }
    
    # Make the API call
    response = requests.get(url, headers=headers, params=params)
    
    # Parse the response
    data = response.json()
    
    return data["data"]

# Define a function to follow a user
def follow_user(user_id):
    # Set up the API endpoint and payload
    url = f"{base_url}users/{user_id}/following"
    payload = {"target_user_id": user_id}
    
    # Make the API call
    response = requests.post(url, headers=headers, json=payload)
    
    return response.status_code

# Define a function to like a tweet
def like_tweet(tweet_id):
    # Set up the API endpoint and payload
    url = f"{base_url}users/{tweet_id}/liking"
    payload = {"tweet_id": tweet_id}
    
    # Make the API call
    response = requests.post(url, headers=headers, json=payload)
    
    return response.status_code

# Define a function to comment on a tweet
def comment_on_tweet(tweet_id, text):
    # Set up the API endpoint and payload
    url = f"{base_url}tweets"
    payload = {
        "status": text,
        "in_reply_to_status_id": tweet_id,
        "auto_populate_reply_metadata": True
    }
    
    # Make the API call
    response = requests.post(url, headers=headers, json=payload)
    
    return response.status_code

# Define a function to interact with users based on keywords
def interact_with_users(keywords, min_followers=100000, comment_text="Great post!"):
    # Search for users based on keywords
    users = search_users(keywords, min_followers)
    
    # Iterate over each user
    for user in users:
        # Follow the user
        follow_user(user["id"])
        
        # Get the user's 10 most recent tweets
        tweets = get_user_tweets(user["id"], 10)
        
        # Iterate over each tweet
        for tweet in tweets:
            # Like the tweet
            like_tweet(tweet["id"])
            
            # Comment on the tweet
            comment_on_tweet(tweet["id"], comment_text)

# Example usage: interact with users based on the keyword "python"
interact_with_users("python")