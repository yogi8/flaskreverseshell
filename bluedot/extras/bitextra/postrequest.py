#!/usr/bin/python3
import requests
import base64

'''
#mac = 'abcd'
url = 'http://192.168.1.5:5000/wheel/status'  #gets all online nodes

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
        
'''


def if_logged_in(func):
    def retrowrapper(self, *args, **kwargs):
        if not self.access_token:
            print('Please Log In to Execute a command')
            return None
        return func(self, *args, **kwargs)
    return retrowrapper


class Retro:
    def __init__(self, username, password, access_token=None):
        self.username = username
        self.password = password
        self.access_token = access_token
        self.logged_in = self.login()

    def login(self):
        url = 'http://192.168.1.5:5000/user/login'
        data = {'username': self.username, 'password': self.password}
        response = self.requeste(url, data=data, post=True)
        a = response.json()
        if 'access_token' in a:
            self.access_token = a['access_token']
            return True
        print(a)

    @if_logged_in
    def logout(self):
        url = 'http://192.168.1.5:5000/user/logout'
        response = self.requeste(url, post=True)
        print(response.json())
        self.logged_in = False
        return True

    def requeste(self, url, data=None, get=None, post=None):
        head = {'Authorization': 'Bearer ' + self.access_token}
        if get:
            response = requests.get(url, json=data, headers=head)
        if post:
            response = requests.post(url, json=data, headers=head)
        return response

    @if_logged_in
    def file_output(self, data, mac):
        url = 'http://192.168.1.5:5000/store/' + mac
        response = self.requeste(url, data=data, post=True)
        print(type(response.content))
        try:
            with open(data['command'].split('/')[-1], "wb") as fp:
                fp.write(base64.b64decode(response.content))
        except base64.binascii.Error as err:
            print(err)
            a = response.json()
            print(a)

    @if_logged_in
    def command_output(self, data, mac):
        url = 'http://192.168.1.5:5000/store/' + mac
        response = self.requeste(url, data=data, post=True)
        a = response.json()       # error needed if server is not running or something else
        print(a, end='')

    @if_logged_in
    def retro(self):
        pass

    @if_logged_in
    def grouplist(self):
        url = 'http://192.168.1.5:5000/user/listbyuser'
        response = self.requeste(url, get=True)
        a = response.json()
        return a['message']

    @if_logged_in
    def nodelist(self, gname):
        url = 'http://192.168.1.5:5000/user/online/nodelist/' + gname
        response = self.requeste(url, get=True)
        # a = response.json()
        # return a['message']
        return response
