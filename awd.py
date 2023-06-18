import requests

v1 = requests.get("https://api.twitter.com/2/users/by/username/elonmusk", headers={"Authorization" : ""})
print(v1.json())
