#!/usr/bin/python3

import subprocess,os
def yogi():
    val = input("Enter your value: ")
    print(len(val[0:8]))
    if val[0:8] == 'download':
        path = val[9:]
        print(path)
        with open(path,"rb") as file:
            return file.read()

rr=yogi()
print(rr)

with open('/home/yogi/jsa/yogi.csv', "wb") as fp:
        fp.write(rr)


#cwd = os.getcwd()
#print(cwd)
#cmd = subprocess.Popen('pwd',shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
#output_byte = cmd.stdout.read() + cmd.stderr.read()
#output_str = str(output_byte,"utf-8")
#print(output_str)
#print('hi')
#print(output_str.strip())
