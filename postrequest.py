#!/usr/bin/python3
import requests
data = {'command': 'pwd'}
url = 'http://192.168.1.5:5000/store/abcd'
response = requests.post(url, json=data)
#print(response.content)
a=response.json()
print(a)
#print('one')
