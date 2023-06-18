import tkinter as tk
from tkinter import Label, Button, StringVar, Text, Image, Checkbutton, messagebox

import os
import requests
import time
import tweepy

class TwitterAPI:
    def __init__(self):


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



def test(usernames, likes = "", retweets = "", content = ""):
    users = str(usernames).split(",")
    print(type(users))
    print(users)
    try:
        for username in users:
            username2 = username.replace(" ", "")
            username3 = username2.replace("'", "")
            username4 = username3.replace("[", "")
            print(f"Username: {username4}")
            user_id = client.get_user(username=username4, user_auth=True)
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
                            client.create_tweet(text=content, in_reply_to_tweet_id=id)
                            if likes and retweets in "True":
                                client.like(id)
                                client.retweet(id)
        time.sleep(1)
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"status": "failure", "error": f"Error: {e}"}

class Form1(tk.Tk):
    def __init__(self):
        super().__init__()

        self.label1 = Label(self)
        self.pictureBox1 = tk.PhotoImage(file="logo.png")
        self.img1 = tk.PhotoImage(file="logo.png")
        self.label2 = Label(self)
        self.button1 = Button(self, text="submit", command=self.button1_Click)
        self.label3 = Label(self, text="Usernames", font=("MV Boli", 13))
        self.label4 = Label(self, text="Content", font=("MV Boli", 13))
        self.richTextBox1 = Text(self)
        self.richTextBox2 = Text(self)
        self.vlike = StringVar()
        self.vretweet = StringVar()
        self.checklikes = Checkbutton(self, text="Likes", font=("MV Boli", 13), variable=self.vlike)
        self.checkretweets = Checkbutton(self, text="Retweets", font=("MV Boli", 13), variable=self.vretweet)

        self.initialize_ui()

    def initialize_ui(self):
        self.title("Form1")
        self.geometry("800x450")
        self.configure(background="white")

        self.label1.place(x=80, y=46)
        self.label2.place(x=678, y=46)
        self.button1.place(x=707, y=12)
        self.label3.place(x=12, y=97)
        self.label4.place(x=343, y=97)
        self.richTextBox1.place(x=12, y=123, width=325, height=315)
        self.richTextBox2.place(x=353, y=123, width=435, height=315)
        self.checklikes.place(x=12, y=12)
        self.checkretweets.place(x=12, y=46)

    def button1_Click(self):
        # TODO: Implement button click logic
        test(usernames=self.richTextBox1.get("1.0", "end-1c").split(","), likes=self.vlike.get(), retweets=self.vretweet.get(), content=self.richTextBox2.get("1.0", "end-1c"))
        if test(usernames=self.richTextBox1.get("1.0", "end-1c").split(","), likes=self.vlike.get(), retweets=self.vretweet.get(), content=self.richTextBox2.get("1.0", "end-1c"))["status"] == "success":
            messagebox.showinfo("Status", "Success, check your twitter account!")
        messagebox.showinfo("Status", "Success, check your twitter account!")

if __name__ == "__main__":
    form = Form1()
    form.mainloop()
