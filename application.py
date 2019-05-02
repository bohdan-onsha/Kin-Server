import json
import requests
import os

from quart import Quart, render_template, session, flash
from quart import request
from quart import jsonify
from kin import KinErrors

import firebase_service
import limits  # runs limit resetting thread
import errors

application = app = Quart(__name__)


@app.route('/api/v1/user/register', methods=['POST'])
async def register():
    try:
        data = json.loads(await request.data)
        if 'email' not in data or 'password' not in data:
            return jsonify(["There is no 'email' or/and 'password' field in the request"]), 400

        data = await firebase_service.register(data['email'], data['password'])
        return jsonify(data), 200
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
        return jsonify(token), 200
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


# get current wallet public address
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


@app.route('/admin/')
def admin_panel():
    if not session.get('logged_in'):
        return render_template('admin_auth.html')
    else:
        data = firebase_service.get_admin_data()
        return render_template('admin-panel.html', data=data)


@app.route('/admin-auth', methods=['POST'])
async def admin_auth():
    form = await request.form
    try:
        token = firebase_service.authenticate(form['email'], form['password'])
        if len(token) > 1 and token[1] is True:
            session['logged_in'] = True
        else:
            await flash("You don't have admin access")
    except requests.exceptions.HTTPError:
        await flash('Wrong email/password!')
    return await admin_panel()


@app.route('/reset-limits', methods=['POST'])
async def reset_limits():
    form = await request.form
    firebase_service.set_limits(dict(form))
    return await admin_panel()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=8000)
