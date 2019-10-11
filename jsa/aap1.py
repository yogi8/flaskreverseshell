#!/home/yogi/flaskk/yogi/bin/python

from flask import Flask, request, jsonify
import random
from datetime import datetime, timedelta
app = Flask(__name__)
ro = [
    {'mac': 'abcd',
    'commands': [{'token': 1234, 'serve': 'true', 'command': 'ls', 'response': ''},{'token': 12345, 'serve': 'true', 'command': 'ls -l', 'response': ''}]
    },
    {'mac': 'efgh',
    'commands': [{'token': 1234, 'serve': 'true', 'command': 'ls', 'response': ''},{'token': 12345, 'serve': 'true', 'command': 'ls -l', 'response': ''}]
    }
    ]


@app.route('/store/<string:mac>', methods=['POST'])    #{ 'command': "ls -l" }
def exec(mac):
    request_data = request.get_json()

    for i in ro:
        if i['mac'] == mac:
            rand = random.randint(1000, 9999)
            print(rand)
            josn = {'token': rand, 'serve': 'true', 'command': request_data['command'], 'tag': 'false', 'response': ''}
            i['commands'].append(josn)

    for i in ro:
        if i['mac'] == mac:
            for j in i['commands']:
                if j['token'] == rand:
                    a = datetime.now()
                    b = timedelta(seconds=30)
                    c = a + b
                    while datetime.now() < c:
                        while not j['tag'] == 'false':
                            response = j['response']
                            i['commands'].remove(j)
                            return jsonify({'output': response})
                    i['commands'].remove(j)
                    return jsonify({'output': 'server time out or server busy'})


@app.route('/wheel/<string:mac>', methods=['POST'])
def registerpost(mac):
    doc = Pretty(mac=mac)
    doc.save_to_mongo
    return {"message": "success"}
