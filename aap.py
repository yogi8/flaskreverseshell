#!/home/yogi/flaskk/yogi/bin/python

from flask import Flask,request,jsonify
app = Flask(__name__)
ro = [
    {'mac': 'abcd',
    'commands': [{'token': 1234, 'serve': 'true', 'command': 'ls', 'response': ''},{'token': 12345, 'serve': 'true', 'command': 'ls -l', 'response': ''}]
    },
    {'mac': 'efgh',
    'commands': [{'token': 1234, 'serve': 'true', 'command': 'ls', 'response': ''},{'token': 12345, 'serve': 'true', 'command': 'ls -l', 'response': ''}]
    }
    ]
print(ro)
@app.route('/store', methods=['POST'])
def hello():
    request_data = request.get_json()

    if 'token' in request_data:
        for i in ro:
            if i['mac'] == request_data['mac']:
                for j in i['commands']:
                    if j['token'] == request_data['token']:
                        j['response'] = request_data['response']
        request_data = {'mac': request_data['mac']}


    for i in ro:
        print("start")
        print (request_data['mac'])
        if i['mac'] == request_data['mac']:
            print('finish')
            for j in i['commands']:
                if j['serve'] == 'true':
                    rrr = j['token']
                    jjj = j['command']
                    print(rrr)
                    print(jjj)
                    request_data = {'mac': i['mac'], 'token': rrr, 'command': jjj}
                    j['serve'] = 'mild'
                    break
            break


    print(request_data)
    print(ro)
    return jsonify(request_data)

   # return {"ip": "192.168.1.1", "up": "25","down": "30"}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
