import requests


BASE = "http://127.0.0.1:5000/"
# obvious that the url is the same as the one in the app.py file
# if you call get method then it will call the get method in the class
response = requests.get(BASE + "helloworld")
resp_name =requests.get(BASE + "data/rohit/34")
video_resp = requests.put(BASE + "video/1" , {"likes" : 45})
print(response.json())
print(resp_name.json())