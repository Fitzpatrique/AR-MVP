import json


def updatePasskey(email):
    with open('passkey.json','r') as file:
        file_data = json.load(file)
        print(file_data)

    for v,i in enumerate(file_data['passcode']):
        if i['email'] == email:
            file_data['passcode'].pop(v)
                
    with open('passkey.json','w') as file:
        json.dump(file_data,file)


PUBLIC_KEY = '' #some public key
PRIVATE_KEY = '' #some private key

SECRET_KEY = '' #some secret key

ACCESS_KEY_ID='' #some access key id
ACCESS_SECRET_KEY='' #some access secret key
AWS_SESSION_TOKEN= '' #some aws session token


import random

def generate():
    word = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = 9

    password = ''.join(random.sample(word,length))

    final =  password
    return final