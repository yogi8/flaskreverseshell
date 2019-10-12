#!/usr/bin/python3
import requests, base64
mac = 'abcd'
#vale = input("pls/enter/the/command#")
#data = {'command': vale}
#url = 'http://192.168.1.5:5000/store/abcd'
#response = requests.post(url, json=data)
#print(response.content)
#a=response.json()    #command pretty output
#print(data)
#b=response.text
#print(b)
#with open('/home/yogi/jsa/yogi.csv', "wb") as fp:
        #fp.write(base64.b64decode(response.content))

def command_output(data):
    url = 'http://192.168.1.5:5000/store/' + mac
    response = requests.post(url, json=data)
    a=response.json()
    print(a)

def file_output(data):
    url = 'http://192.168.1.5:5000/store/' + mac
    response = requests.post(url, json=data)
    print(type(response.content))
    try:
        with open(data['command'].split('/')[-1], "wb") as fp:
            fp.write(base64.b64decode(response.content))
    except base64.binascii.Error as err:
        a=response.json()
        print(a)

def cmdinput():
    vale = input("pls/enter/the/command#")
    data = {'command': vale}
    if vale[0:8] == 'download':
        file_output(data)
    else:
        command_output(data)

cmdinput()
