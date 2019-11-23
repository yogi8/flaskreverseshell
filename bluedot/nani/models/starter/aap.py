#!/home/yogi/bluedot/randie/bin/python

from flask import request, jsonify, url_for, redirect
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt_claims
)
from nani import app
from datetime import datetime, timedelta
import random
from nani.src.database import Database
from .pretty import Pretty, statuss
from .commands import Commands
from . import appy
from nani.models.groups.group import Group
from .errors import NodeNotExistsError

collection = app.config['COLLECTION']
timeout = app.config['TIMEOUT']
lastreach = app.config['LASTREACH']

print(type(collection))
print(type(timeout))
print(type(lastreach))



@appy.route('/store', methods=['POST'])
def hello():
    print(Database.DATABASE)
    request_data = request.get_json()
    data = Database.find_one(collection, {'mac': request_data['mac']})

    if data is not None:
        Database.update(collection, query={'mac': request_data['mac']}, data={"$set": {'reporte': datetime.now()}})
        if 'token' in request_data:
            base = Database.find_one(collection, {'mac': request_data['mac'], 'commands.token': request_data['token']})
            if base is not None:
                Database.update(collection,
                    query= {'mac': request_data['mac'], 'commands.token': request_data['token']},
                    data= {"$set": {"commands.$.response": request_data['response']}})
                Database.update(collection,
                    query= {'mac': request_data['mac'], 'commands.token': request_data['token']},
                    data= {"$set": {"commands.$.tag": 'true'}})

        requeste = {'mac': request_data['mac']}
        print(request_data['mac'])
        rev = Database.find_one(collection, {'mac': request_data['mac'], 'commands.serve': 'true'})

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
                    Database.update(collection,
                        query= {'mac': rev['mac'], 'commands.token': i['token']},
                        data= {"$set": {"commands.$.serve": 'mild'}})
                    break
        print(requeste)
        return jsonify(requeste)


@appy.route('/store/<string:mac>', methods=['POST'])  # { 'command': "ls -l" }
@jwt_required
def exec(mac):
    request_data = request.get_json()
    try:
        if Pretty.is_mac_valid(mac):
            pass
    except NodeNotExistsError as e:
        return jsonify(message=e.message), 400
    user = get_jwt_identity()
    auth = Group.find_user_and_node_in_same_group(mac, user)
    claims = get_jwt_claims()
    if claims['is_admin'] is not True:
        if auth is not True:
            return jsonify(message='You are not Authorised to access this system'), 401

    data = Database.find_one(collection, {'mac': mac})
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
        b = timedelta(seconds=timeout)
        c = a + b
        while datetime.now() < c:
            r = Database.find_one(collection, {'mac': mac, 'commands.token': rand, 'commands.tag': 'true'})
            randie = r['commands']
            for i in randie:
                if i['token'] == rand and i['tag'] == 'true':
                    response = i['response']
                    print('horrible')
                    print(response)
                    Database.update(collection, query={'mac': mac},
                                    data={'$pull': {'commands': {'token': rand}}})
                    return jsonify(response)
        Database.update(collection,query= {'mac': mac}, data= {'$pull': {'commands': {'token': rand}}})
        print('server timeout for' + str(rand))
        return jsonify({'output': 'server time out or server busy'})
    return jsonify({'output': 'unable to find with that mac'})


@appy.route('/wheel/add/<string:mac>', methods=['POST'])  # adding new mac if doesn't exists
def registerpost(mac):
    data = Database.find_one(collection, {'mac': mac})
    if data is not None:
        return {"message": "Already exists"}
    doc = Pretty(mac=mac)
    doc.save_to_mongo()
    return {"message": "success"}


@appy.route('/wheel/add/<string:mac>', methods=['GET'])  # checks for a mac if exists or not
def registerget(mac):
    data = Database.find_one(collection, {'mac': mac})
    if data is not None:
        print(data['mac'])
        #randie = data['commands']
        # for i in randie:
        #     print(i)
        return {"message": "Exists"}
    return {"message": "MAC Doesn't Exists or not registered"}


@appy.route('/wheel/status/<string:mac>', methods=['GET'])    # checks against mac for offline or online
def status(mac):
    data = Database.find_one(collection, {'mac': mac})
    if data is not None:
        print(data['mac'])
        print(data['reporte'])
        d = data['reporte']
        e = datetime.now()
        f = e-d
        g = int(f.total_seconds())
        if g<=lastreach:
            return {"message": "Online"}
        else:
            return {"message": "Offline"}
    return {"message": "MAC Doesn't Exists or not registered"}


@appy.route('/wheel/status', methods=['GET'])    #checks for no of devices online against mac
def statuslist():
    s=[]
    data = Database.find(collection, {})
    if data is not None:
        for i in data:
            print(i['mac'])
            if i['reporte']:
                d = i['reporte']
                e = datetime.now()
                f = e-d
                g = int(f.total_seconds())
                print(g)
                print(lastreach)
                if g <= lastreach:
                    s.append(i['mac'])
        return jsonify({'message': s })
    return {'message': 'None'}
