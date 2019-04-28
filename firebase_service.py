import asyncio
import re
import requests

import kin
import pyrebase
import validate_email as validator

import configuration
import kin_service
import errors

app_id = 'NM8e'
"""
user - firebase uid,  email, password hash, public wallet address,  recovery string

transactions - from uid, to uid, count, description, date etc.

"""

firebase = pyrebase.initialize_app(configuration.config)
auth = firebase.auth()
db = firebase.database()


async def register(email: str, password: str) -> dict:
    """
            Creates new account, associates new kin account with it
            and save users data to db

            :param email: Email address that will be linked to account
            :param password: Password of the account

            :return: Dictionary with account data (public address, seed, balance, email, uid)

            :raises: :class: errors.InvalidEmailError if email is wrong or does not exist
            :raises: :class: errors.InvalidPasswordError`: if the password is too weak (more than 8 symbols)

    """
    try:
        validate_email(email)
        validate_password(password)
    except (errors.InvalidEmailError, errors.InvalidPasswordError):
        raise

    user = auth.create_user_with_email_and_password(email, password)
    async with kin_service.get_client() as client:
        server_account = await get_server_account(client)
        account = await kin_service.create_account(client, server_account)
        data = {
            'public_address': account.keypair.public_address,
            'seed': account.keypair.secret_seed,
            'balance': await account.get_balance(),
            'email': user['email'],
            'uid': user['localId'],
        }

    db.child('users').push(data)
    return data


def authenticate(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user['idToken']
    except requests.exceptions.HTTPError:
        raise


def get_account_keypair(uid: str, token: str) -> dict:
    """
            Returns public wallet address and secret seed of the account with the given uid

            :param uid: uid of the account
            :param token: active firebase token

            :return: Dictionary with keypair data (public address, seed)

            :raises: :class: errors.AccountNotFoundError if account with the given uid does not exist

    """
    query = db.child("users").child().order_by_child("uid").equal_to(uid).get(token=token)
    try:
        user_data = query.each()[0].val()
    except IndexError:
        raise errors.ItemNotFoundError()
    data = {
        'public_address': user_data['email'],
        'seed': user_data['email'],
    }
    return data


async def get_kins(uid: str, token: str, amount: int, description: str) -> dict:
    """
            Send kin from current server wallet to wallet linked with the given uid
            Also push the data about transaction and wallet balances to the db

            :param uid: uid of the account
            :param token: active firebase token
            :param amount: amount of kin to be sent
            :param description: additional transaction text


            :raises: :class: errors.ItemNotFoundError if account with the given uid does not exist
            :raises: :class: errors.LowBalanceError if there is no enough money on server wallet

            :return dictionary with transaction data
    """
    user_query = db.child("users").child().order_by_child("uid").equal_to(uid).get(token=token)
    server_query = db.child("server_wallet").child().get()
    try:
        user_data = user_query.each()[0].val()
        recipient_address = user_data['public_address']
        server_wallet_data = server_query.each()[0].val()
        server_wallet_keypair = kin_service.get_keypair(seed=server_wallet_data['seed'])
    except IndexError:
        raise errors.ItemNotFoundError()

    try:
        async with kin_service.get_client() as client:
            account = client.kin_account(server_wallet_keypair.secret_seed, app_id=app_id)
            transaction = await kin_service.send_kin(client, account, recipient_address, amount, description)

            tx_data = {
                'id': transaction['id'],
                'uid': user_data['uid'],
                'memo': transaction['memo'],
                'amount': transaction['operation']['amount'],
                'recipient_address': transaction['operation']['destination'],
                'sender_address': transaction['source']
            }
            db.child('transactions').push(tx_data)
        await update_server_wallet_balance()
        await update_wallet_balance(uid)

        return tx_data
    except (kin.KinErrors.LowBalanceError, kin.KinErrors.NotValidParamError):
        raise

'''
async def create_server_wallet() -> None:
    """
            Create kin wallet that will be used like main server wallet
            Replace old server wallet with itself


    """

    async with kin_service.get_client() as client:
        account = await kin_service.create_account(client, kin_service.get_keypair())

        data = {
            'public_address': account.keypair.public_address,
            'seed': account.keypair.secret_seed,
            'balance': await account.get_balance(),
        }
    db.child('server_wallet').remove()
    db.child('server_wallet').push(data)

'''


def get_server_wallet_address(uid: str, token: str) -> str:
    """
            Returns current server wallet public address with
            Available only for registered users

            :param uid: uid of the user
            :param token: active firebase token

            :return: public address of current server wallet

            :raises: errors.ItemNotFoundError if user with given uid does not exist
    """
    try:
        get_account_keypair(uid, token)
        wallet_data = get_server_wallet()
        return wallet_data['public_address']
    except errors.ItemNotFoundError:
        raise


def get_server_wallet() -> dict:
    """
            Returns full data about current server wallet


            :return: dictionary that store current balance, public address and secret seed of current server wallet

            :raises: errors.ItemNotFoundError if user with given uid does not exist
    """
    query = db.child("server_wallet").child().get()

    try:
        wallet_data = query.each()[0].val()
        return wallet_data
    except IndexError:
        raise errors.ItemNotFoundError()


async def get_server_account(client):
    wallet_data = get_server_wallet()
    account = client.kin_account(wallet_data['seed'])
    return account


def history(uid: str, token: str) -> list:
    data = db.child('transactions').child().order_by_child('uid').equal_to(uid).get(token=token)
    if len(data.each()) == 0:
        raise errors.ItemNotFoundError
    return [i.val() for i in data.each()]


async def update_server_wallet_balance() -> None:
    """
            Updates balance of server wallet at db

    """
    wallet_data = get_server_wallet()
    public_address = wallet_data['public_address']
    wallet_data['balance'] = await kin_service.get_wallet_balance(public_address)
    data = db.child('server_wallet').get()
    key = data.each()[0].key()
    db.child('server_wallet').child(key).update(wallet_data)


async def update_wallet_balance(uid: str) -> None:
    """
            Updates balance of kin wallet linked to the given uid

            :raises: errors.ItemNotFoundError if user with given uid does not exist
    """
    try:
        user_query = db.child("users").child().order_by_child("uid").equal_to(uid).get()
        user_data = user_query.each()[0].val()
        current_balance = await kin_service.get_wallet_balance(user_data['public_address'])  # raises some shit
    except (IndexError, errors.ItemNotFoundError):
        raise errors.ItemNotFoundError
    except kin.errors.StellarAddressInvalidError:
        raise

    user_data['balance'] = current_balance

    data = db.child('users').child().order_by_child('uid').equal_to(uid).limit_to_first(1).get()
    key = data.each()[0].key()
    db.child('users').child(key).update(user_data)


def validate_email(email: str) -> bool:
    """
            Checks if email is valid and exists


            :param email: email address (who would have thought?)

            :return: True if email is correct

            :raises: :class: errors.InvalidEmailError otherwise

    """
    if validator.validate_email(email, check_mx=True, verify=True):
        return True
    else:
        raise errors.InvalidEmailError()


def validate_password(password: str) -> bool:
    """
            Checks if password:
                - Has at least 8 characters
                - Consists of letters (upper/lowercase), numbers and/or any of the special characters: @#$%^&+=

            :param password: password of the account (who would have thought?)

            :return: True if password is correct

            :raises: :class: errors.InvalidPasswordError otherwise

    """
    regexp = r'[A-Za-z0-9@#$%^&+=]{8,}'
    if re.match(regexp, password):
        return True
    else:
        raise errors.InvalidPasswordError()


async def main():
    # print('registering 3 accounts...')
    # await register('testemail@google.com', '1A345asfsa')
    # await register('onsha.bogdan@gmail.com', 'ASsgnale32r')
    # await register('nure.forum@gmail.com', '3jrnsod8an')
    # await register('trophimov.alexey@gmail.com', 'jasGJEFKJ22')
    # await register('memepunct@gmail.com', 'asdasr322cs')

    #token = authenticate('memepunct@gmail.com', 'asdasr322cs')
    #print(token)
    # await get_kins('9FHS4w9zFJNuSuhy4XfSREvcASv2', token, 300, 'again')
    pass
#asyncio.run(main())
