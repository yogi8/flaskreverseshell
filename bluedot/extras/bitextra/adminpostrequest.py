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

    def login(self):                                     # extra decorator needed
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

# user

    @if_logged_in
    def register_user(self, username, password, is_admin=False):            # extra decorator needed
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
    def change_username(self, new_username):            # extra decorator needed
        url = 'http://192.168.1.5:5000/user/change_username/' + new_username
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def change_password(self, new_password):           # extra decorator needed
        url = 'http://192.168.1.5:5000/user/change_password/' + new_password
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def change_users_username(self, username, new_username):        # extra decorator needed
        url = 'http://192.168.1.5:5000/user/admin/change_username/' + username + '/' + new_username
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def change_users_password(self, username, new_password):          # extra decorator needed
        url = 'http://192.168.1.5:5000/user/admin/change_password/' + username + '/' + new_password
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)


# group


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

# nodes

    @if_logged_in
    def add_node(self, node):
        url = 'http://192.168.1.5:5000/node/add/' + node
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def del_node(self, node):
        url = 'http://192.168.1.5:5000/node/delete/' + node
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def make_node_active(self, node):
        url = 'http://192.168.1.5:5000/node/active/' + node
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

    @if_logged_in
    def make_node_inactive(self, node):
        url = 'http://192.168.1.5:5000/node/inactive/' + node
        response = self.requeste(url, post=True)
        a = response.json()
        print(a)

# untruce

    @if_logged_in
    def untruce_list(self):
        url = 'http://192.168.1.5:5000/untruce'
        response = self.requeste(url, get=True)
        a = response.json()
        print(a)
