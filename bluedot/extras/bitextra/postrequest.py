#!/usr/bin/python3
import requests
import time
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
        response = requests.post(url, json=data)
        a = response.json()
        print(a)
        if 'access_token' in a:
            self.access_token = a['access_token']
            print(self.username + 'Logged in succesfully')
            return True


    @if_logged_in
    def logout(self):
        url = 'http://192.168.1.5:5000/user/logout'
        response = self.requeste(url, post=True)
        print(response.json())
        self.logged_in = False
        print(self.username + 'Logged out succesfully')
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
        glist = True
        nlist = True
        while True:
            gname = ''
            time.sleep(5)
            grouplist = self.grouplist()
            print(grouplist)
            if grouplist:
                print(grouplist)
                gname = input('>>Type the GroupName')
            if glist is True and not grouplist:
                print('No groups Found')
                glist = False
            while gname:
                nodename = ''
                time.sleep(5)
                response = self.nodelist(gname)
                if response.status_code == 200 and response.json()['message']:
                    a = response.json()
                    nodelist = a['message']
                    print(nodelist)
                    while True:
                        nodename = input('>>Type any System to Login or Enter back to go back')
                        if nodename not in nodelist and nodename != 'back':
                            print('Please Enter Exact Name')
                        else:
                            break
                    if nodename == 'back':
                        glist = True
                        break
                elif response.status_code == 200:
                    if nlist is True:
                        print("No Devices Found")
                        nlist = False
                if not response.status_code == 200:
                    a = response.json()
                    nodelist = a['message']
                    print(nodelist)
                    glist = True
                    break
                while nodename:
                    vale = input('>')
                    data = {'command': vale}
                    if vale[0:8] == 'download':
                        self.file_output(data=data, mac=nodename)
                    elif vale.strip() == 'quit':
                        nlist = True
                        break
                    elif vale.strip() == 'logout':
                        self.logout()
                        return None
                    else:
                        self.command_output(data=data, mac=nodename)

    @if_logged_in
    def grouplist(self):
        url = 'http://192.168.1.5:5000/group/listbyuser'
        response = self.requeste(url, get=True)
        a = response.json()
        print(a)
        return a['message']

    @if_logged_in
    def nodelist(self, gname):
        url = 'http://192.168.1.5:5000/group/online/nodelist/' + gname
        response = self.requeste(url, get=True)
        #a = response.json()
        # return a['message']
        return response

#dad = Retro(username='yogi',password='yogi123')
#dad.retro()
