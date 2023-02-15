import json


def updatePasskey(email):
    with open('passkey.json','r') as file:
        file_data = json.load(file)
        print(file_data)

    for v,i in enumerate(file_data["passcode"]):
        if i["email"] == email:
            file_data["passcode"].pop(v)
                
    with open('passkey.json','w') as file:
        json.dump(file_data,file)


PUBLIC_KEY = 'pk_test_e29839a674846979afdc3afe2ca1f3e404bd90c6'

SECRET_KEY = 'Oy!sWestAfr!ca03%'

ACCESS_KEY_ID='AKIA4PJD5IK4CUJRQAMI'
ACCESS_SECRET_KEY='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'
AWS_SESSION_TOKEN= ''


import random

def generate():
    word = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = 9

    password = ''.join(random.sample(word,length))

    final =  password
    return final