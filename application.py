import json
import requests
import asyncio

from quart import Quart
from quart import request
from quart import jsonify
from kin import KinErrors

import firebase_service
import limits #runs limit resetting thread
import errors

application = app = Quart(__name__)


@app.route('/api/v1/user/register', methods=['POST'])
async def register():
    try:
        data = json.loads(await request.data)
        if 'email' not in data or 'password' not in data:
            return jsonify(["There is no 'email' or/and 'password' field in the request"]), 400

        responce_data = await firebase_service.register(data['email'], data['password'])
        return jsonify(responce_data), 200
    except (errors.InvalidEmailError, errors.InvalidPasswordError) as e:
        return jsonify(e.args), 400
    except requests.exceptions.HTTPError:
        return jsonify(["User with that email already exists"]), 400
    except (ValueError, TypeError, json.decoder.JSONDecodeError):
        return jsonify(['Invalid parameters']), 400


@app.route('/api/v1/user/auth', methods=['POST'])
async def auth():
    try:
        data = json.loads(await request.data)

        if 'email' not in data or 'password' not in data:
            return jsonify(["Missing 'email' and/or 'password' field in the request"]), 400
        token = firebase_service.authenticate(data['email'], data['password'])
        return jsonify([token]), 200
    except requests.exceptions.HTTPError:
        return jsonify(['Invalid email or password']), 400
    except (ValueError, TypeError, json.decoder.JSONDecodeError):
        return jsonify(['Invalid parameters']), 400


@app.route('/api/v1/user/get-kins', methods=['POST'])
async def get_kins():
    data = json.loads(await request.data)
    fields = ['uid', 'token', 'amount', 'description']
    if not all(field in data for field in fields):
        return jsonify(['Some of required fields missing or wrong: uid, token, amount, description']), 400
    try:
        data = await firebase_service.get_kins(data['uid'], data['token'], data['amount'], data['description'])
        return jsonify(data), 200
    except errors.ItemNotFoundError:
        return jsonify(["User with the given uid does not exist"]), 400
    except requests.exceptions.HTTPError:
        return jsonify(['Invalid or outdated token']), 400
    except KinErrors.LowBalanceError:
        return jsonify(['Insufficient funds on server wallet']), 400
    except (KinErrors.NotValidParamError, ValueError, TypeError):
        return jsonify(['Invalid parameters']), 400


@app.route('/api/v1/server-wallet', methods=['POST'])
async def get_cwpa():
    try:
        data = json.loads(await request.data)
        if 'uid' not in data or 'token' not in data:
            return jsonify("Missing 'uid' or/and 'token' fields in the request")

        address = firebase_service.get_server_wallet_address(data['uid'], data['token'])
        return jsonify([address]), 200
    except errors.ItemNotFoundError:
        return jsonify(["User with the given uid does not exist"])
    except requests.exceptions.HTTPError:
        return jsonify(['Invalid or outdated token']), 400
    except (ValueError, TypeError, json.decoder.JSONDecodeError):
        return jsonify(['Invalid parameters']), 400


@app.route('/api/v1/user/history', methods=['POST'])
async def history():
    data = json.loads(await request.data)
    if 'uid' not in data or 'token' not in data:
        return jsonify("Missing 'uid' or/and 'token' fields in the request"), 400
    try:
        return jsonify(firebase_service.history(data['uid'], data['token'])), 200
    except errors.ItemNotFoundError:
        return jsonify(["User with the given uid is not exist"]), 400
    except requests.exceptions.HTTPError:
        return jsonify(['Invalid or outdated token']), 400
    except (ValueError, TypeError):
        return jsonify(['Invalid parameters']), 400


if __name__ == '__main__':
    app.run(debug=True, port=8000)
