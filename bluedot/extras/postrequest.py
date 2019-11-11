#!/usr/bin/python3
import requests, base64
#mac = 'abcd'
url = 'http://192.168.1.5:5000/wheel/status'
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

def command_output(data,mac):
    url = 'http://192.168.1.5:5000/store/' + mac
    response = requests.post(url, json=data)
    a=response.json()
    print(a,end='')

def file_output(data,mac):
    url = 'http://192.168.1.5:5000/store/' + mac
    response = requests.post(url, json=data)
    print(type(response.content))
    try:
        with open(data['command'].split('/')[-1], "wb") as fp:
            fp.write(base64.b64decode(response.content))
    except base64.binascii.Error as err:
        a=response.json()
        print(a)

def cmdinput(mac):
    a=mac
    while True:
        vale = input(a+'>')
        data = {'command': vale}
        if vale[0:8] == 'download':
            file_output(data,mac)
        elif vale.strip() == 'quit':
            break
        else:
            command_output(data,mac)
        a=''

#while True:
#    cmdinput()


def test():
    response = requests.get(url)
    #print(response.content)
    a=response.json()    #command pretty output
    #print(a)
    if a['message'] == 'None':
        print('No devices registered')
        return None

    if a['message']:
        for i in a['message']:       #
            print(i)                 #
        d=a['message']
        print('Total '+ str(len(d)) +' online')
        for i in range(len(d)):
            print ('Enter ' + str(i) + ' for ' + d[i])
        print ('Enter ' + str(len(d)) + ' to exit')
        try:
            ad = int(input(">>"))
            print(ad)
            if ad is len(d):
                return None
            #print(len(d))
            if isinstance(ad, int) and ad < len(d):
                mac = d[ad]
                cmdinput(mac)
        except ValueError as err:
            print("Please enter number")
    else:
        print('No devices found Online')
        return None
    return True

while True:
    if test() is None:
        break
