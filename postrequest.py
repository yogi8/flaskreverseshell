#!/usr/bin/python3
import requests, base64
data = {'command': 'download /home/yogi/jsa/flasky.csv'}
url = 'http://192.168.1.5:5000/store/abcd'
response = requests.post(url, json=data)
print(response.content)
a=response.json()
print(a)
b=response.text
print(b)
with open('/home/yogi/jsa/yogi.csv', "wb") as fp:
        fp.write(base64.b64decode(response.content))
