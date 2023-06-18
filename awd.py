import requests

v1 = requests.get("https://api.twitter.com/2/users/by/username/elonmusk", headers={"Authorization" : "Bearer AAAAAAAAAAAAAAAAAAAAAC61oAEAAAAATv3V%2Bw%2BDdSmQVzAvpezr44IMGNI%3DD1Vpa8eaAG2r0C2Z0lrzXYUKD7MeLiwWbfPVQAwK9bh7PhqCP5"})
print(v1.json())