"""
Created by Bogdan Onsha
15.04.19 - 02.05.19

https://t.me/onsha_bogdan
"""

import json
import requests

from quart import Quart, render_template, session, flash
from quart import request
from quart import jsonify
from kin import KinErrors

import firebase_service
import errors

application = app = Quart(__name__)


# app.secret_key = 'appSecretKey'


@app.route('/api/v1/user/register', methods=['POST'])
async def register():
    try:
        data = json.loads(await request.data)

        data = await firebase_service.register(data['email'], data['password'])
        return jsonify(data), 200
    except (errors.InvalidEmailError, errors.InvalidPasswordError) as e:
        return jsonify(e.args), 400
    except requests.exceptions.HTTPError:
        return jsonify(["User with that email already exists"]), 400
    except (ValueError, TypeError, KeyError, json.decoder.JSONDecodeError):
        return jsonify(['Invalid parameters']), 400
    except:
        return jsonify(["Something's wrong with the server"]), 400


@app.route('/api/v1/user/auth', methods=['POST'])
async def auth():
    try:
        data = json.loads(await request.data)
        auth_data = firebase_service.authenticate(data['email'], data['password'])
        return jsonify({'token': auth_data['token'], 'is_admin': auth_data['is_admin'], 'uid': auth_data['uid']}), 200
    except requests.exceptions.HTTPError:
        return jsonify(['Invalid email or password']), 400
    except (ValueError, TypeError, KeyError, json.decoder.JSONDecodeError):
        return jsonify(['Invalid parameters']), 400
    except:
        return jsonify(["Something's wrong with the server"])


@app.route('/api/v1/user/earn', methods=['POST'])
async def earn():
    data = json.loads(await request.data)
    fields = ['token', 'amount', 'description']
    if not all(field in data for field in fields):
        return jsonify(['Some of required fields missing or wrong: uid, token, amount, description']), 400
    try:
        uid = request.headers['uid']

        data = await firebase_service.replenish(uid, data['token'], data['amount'], data['description'])
        return jsonify(data), 200
    except errors.ItemNotFoundError:
        return jsonify(["User with the given uid does not exist"]), 400
    except requests.exceptions.HTTPError:
        return jsonify(['Invalid or outdated token']), 400
    except KinErrors.LowBalanceError:
        return jsonify(['Insufficient funds on server wallet']), 400
    except (KinErrors.NotValidParamError, ValueError, TypeError, KeyError):
        return jsonify(['Invalid parameters']), 400
    except:
        return jsonify(["Something's wrong with the server"]), 400


@app.route('/api/v1/user/pay', methods=['POST'])
async def pay():
    try:
        data = json.loads(await request.data)
        fields = ['token', 'amount', 'description']
        if not all(field in data for field in fields):
            return jsonify(['Some of required fields missing or wrong: token, amount, description']), 400
        uid = request.headers['uid']

        data = await firebase_service.pay(uid, data['token'], data['amount'], data['description'])
        return jsonify(data), 200
    except (IndexError, ValueError, KeyError, KinErrors.NotValidParamError):
        return jsonify(['Invalid parameters']), 400
    except KinErrors.LowBalanceError:
        return jsonify(['Insufficient funds on user wallet']), 400
    except:
        return jsonify(["Something's wrong with the server"]), 400


@app.route('/api/v1/user/balance', methods=['POST'])
async def balance():
    try:
        data = json.loads(await request.data)
        uid = request.headers['uid']
        token = data['token']

        current_balance = firebase_service.get_balance(uid, token)
        return jsonify({'balance': current_balance}), 200
    except requests.exceptions.HTTPError:
        return jsonify(['Invalid or outdated token']), 400
    except (KinErrors.NotValidParamError, ValueError, TypeError, KeyError, IndexError):
        return jsonify(['Invalid parameters']), 400
    except:
        return jsonify(["Something's wrong with the server"]), 400


# get current wallet public address
@app.route('/api/v1/server-wallet', methods=['POST'])
async def get_cwpa():
    try:
        data = json.loads(await request.data)
        if 'token' not in data:
            return jsonify("Missing 'token' field in the request")
        uid = request.headers['uid']
        address = firebase_service.get_server_wallet_address(uid, data['token'])
        return jsonify({'public_address': address}), 200
    except errors.ItemNotFoundError:
        return jsonify(["User with the given uid does not exist"])
    except requests.exceptions.HTTPError:
        return jsonify(['Invalid or outdated token']), 400
    except (ValueError, TypeError, json.decoder.JSONDecodeError):
        return jsonify(['Invalid parameters']), 400
    except KeyError:
        return jsonify(["Missing 'uid' field in headers"]), 400
    except:
        return jsonify(["Something's wrong with the server"]), 400


@app.route('/api/v1/user/history', methods=['POST'])
async def history():
    try:
        data = json.loads(await request.data)
        if 'token' not in data:
            return jsonify("Missing 'token' field in the request"), 400
        uid = request.headers['uid']
        return jsonify(firebase_service.history(uid, data['token'])), 200
    except errors.ItemNotFoundError:
        return jsonify(["User with the given uid is not exist"]), 400
    except requests.exceptions.HTTPError:
        return jsonify(['Invalid or outdated token']), 400
    except (ValueError, TypeError, json.decoder.JSONDecodeError):
        return jsonify(['Invalid parameters']), 400
    except KeyError:
        return jsonify(["Missing 'uid' field in headers"]), 400
    except:
        return jsonify(["Something's wrong with the server"]), 400


@app.route('/api/v1/user/logout', methods=['POST'])
async def logout():
    try:
        uid = request.headers['uid']

        firebase_service.log_out(uid)
        return jsonify({'status': True})
    except (KeyError, IndexError):
        return jsonify('Wrong parameters'), 400
    except:
        return jsonify(["Something's wrong with the server"]), 400


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
        if token['is_admin']:
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
    app.run(debug=True, port=8000)
    # app.run(debug=False, host='0.0.0.0')
