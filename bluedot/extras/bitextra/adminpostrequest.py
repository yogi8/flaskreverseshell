#!/usr/bin/python3
import requests
import time

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
    def register_user(self, username, password, is_admin=False):
        url = 'http://192.168.1.5:5000/user/register'
        data = {'username': username, 'password': password, 'is_admin': is_admin}
        response = self.requeste(url, data=data, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def make_user_active(self, username):
        url = 'http://192.168.1.5:5000/user/active/' + username
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def make_user_inactive(self, username):
        url = 'http://192.168.1.5:5000/user/inactive/' + username
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def delete_user(self, username):
        url = 'http://192.168.1.5:5000/user/delete/' + username
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def change_username(self):
        pass

    @if_logged_in
    def change_password(self):
        pass

    @if_logged_in
    def add_group(self, gname):
        url = 'http://192.168.1.5:5000/group/add/' + gname
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def delete_group(self, gname):
        url = 'http://192.168.1.5:5000/group/delete/' + gname
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def make_group_active(self, gname):
        url = 'http://192.168.1.5:5000/group/active/' + gname
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def make_group_inactive(self, gname):
        url = 'http://192.168.1.5:5000/group/inactive/' + gname
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def add_node_to_group(self, gname, node):
        url = 'http://192.168.1.5:5000/group/addnode/' + gname + '/' + node
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def del_node_from_group(self, gname, node):
        url = 'http://192.168.1.5:5000/group/delnode/' + gname + '/' + node
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def add_user_to_group(self, gname, user):
        url = 'http://192.168.1.5:5000/group/adduser/' + gname + '/' + user
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def del_user_from_group(self, gname, user):
        url = 'http://192.168.1.5:5000/group/deluser/' + gname + '/' + user
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def add_node(self,node):
        pass

    @if_logged_in
    def del_node(self, node):   # deleting a node should be also deleted from all groups
        pass

    @if_logged_in
    def make_node_active(self, node):
        pass

    @if_logged_in
    def make_group_inactive(self, node):
        pass
