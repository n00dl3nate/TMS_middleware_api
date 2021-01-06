from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from cryptography.fernet import Fernet
import uuid
import hashlib
import os

app = FlaskAPI(__name__)
from flask_cors import CORS
from tms.service import *
from tms.base import Configuration
import json

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

c = Configuration()
client = SetUp()
token = None
import secrets


authkey_dict = {
    'key_1':'e9c4fe2d-8f01-4467-8ec1-bfcc34e1f98b',
}

key = Fernet.generate_key()
f = Fernet(key)

@app.route("/create/token", methods=['GET'])
def create_token():
    try:
        authkey = request.args['authkey']
        token = client.get_token()
        encrypted_token = encrypt(token.encode("utf-8"), key)
        if authkey in authkey_dict.values():
            return {
                'status_code':'200',
                'token' : encrypted_token.decode("utf-8")
                }
        else:
            return {'status_code': '401',
                    'message': 'invalid authkey'}

    except:
        return { 'status_code':'400',
                 'message': 'invalid request'}

@app.route("/notices/<int:id>/<string:token>/", methods=['GET'])
def get_notice_by_notice_id(id, token):
    print('get notice by id')
    try:
        url = f"{c.get_configuration_for('service', 'notices')}&ntid={id}"
        return api_get_request(url, token)
    except:
        return {
            'status_code': '400',
            'data': 'bad request'
        }

@app.route("/notices/<string:token>/", methods=['GET'])
def get_notices(token):
    try:
        url = c.get_configuration_for('service', 'notices')
        return api_get_request(url,token)
    except:
        return {
            'status_code':'400',
            'data':'bad request'
        }

def api_get_request(url, token):
    decrypted_token = decrypt(token.encode("utf-8"), key).decode("utf-8")
    header = client.create_header(decrypted_token)
    rest = RestRequests(header)
    resp = rest.get(url)
    return resp

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

def updateKey():
    generated_key = secrets.token_urlsafe(20)
    authkey_dict['key_2'] = generated_key
    f = open("authkey.txt", "w")
    print('updated authkey')
    f.write(generated_key)
    f.close()

if __name__ == "__main__":
    # import sched, time
    # s = sched.scheduler(time.time, time.sleep)
    # s.enter(10, 1, updateKey)
    # s.run()

    app.run(debug=True)