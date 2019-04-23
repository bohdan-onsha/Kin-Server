import asyncio
import re

import pyrebase
import validate_email as validator

import configuration
import kin_service
import errors

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
        account = await kin_service.create_account(client)
        data = {
            'public_address': account.keypair.public_address,
            'seed': account.keypair.secret_seed,
            'balance': await account.get_balance(),
            'email': user['email'],
            'uid': user['localId'],
        }

    db.child('users').push(data)
    return data


def authenticate(uid: str) -> dict:
    """
            Returns public wallet address and secret seed of the account with the given uid

            :param uid: uid of the account

            :return: Dictionary with keypair data (public address, seed)

            :raises: :class: errors.AccountNotFoundError if account with the given uid does not exist

    """
    query = db.child("users").child().order_by_child("uid").equal_to(uid).get()
    try:
        user_data = query.each()[0].val()
    except IndexError:
        raise errors.ItemNotFoundError()
    data = {
        'public_address': user_data['email'],
        'seed': user_data['email'],
    }
    return data


async def get_kins(uid, count, description):
    user_query = db.child("users").child().order_by_child("uid").equal_to(uid).get()
    server_query = db.child("server_wallet").child().get()
    try:
        user_data = user_query.each()[0].val()
        recipient_address = user_data['public_address']

        server_wallet_data = server_query.each()[0].val()
        server_wallet_keypair = kin_service.get_keypair(seed=server_wallet_data['seed'])
    except IndexError:
        raise errors.ItemNotFoundError()

    async with kin_service.get_client() as client:
        account = await kin_service.create_account(client, server_wallet_keypair)
        transaction = await kin_service.send_kin(client, account, recipient_address, count, description)

        tx_data = {
            'id': transaction['id'],
            'memo': transaction['memo'],
            'amount': transaction['operation']['amount'],
            'recipient_address': transaction['operation']['destination'],
            'sender_address': transaction['source']
        }
        db.child('transactions').push(tx_data)
    await update_server_wallet_balance()
    await update_wallet_balance(uid)


'''

'''


async def create_server_wallet():
    db.child("server_wallet").remove()
    async with kin_service.get_client() as client:
        account = await kin_service.create_account(client, kin_service.get_keypair())

        data = {
            'public_address': account.keypair.public_address,
            'seed': account.keypair.secret_seed,
            'balance': await account.get_balance(),
        }
    db.child('server_wallet').push(data)


def get_server_wallet_address(uid):
    try:
        authenticate(uid)
        wallet_data = get_server_wallet()
        return wallet_data['public_address']
    except errors.ItemNotFoundError:
        raise


def get_server_wallet():
    query = db.child("server_wallet").child().get()

    try:
        wallet_data = query.each()[0].val()
        return wallet_data
    except IndexError:
        raise errors.ItemNotFoundError()


def history(uid):
    pass

    '''
    -> transactions list (descr, count, status(bool))
    '''


async def update_server_wallet_balance():
    wallet_data = get_server_wallet()
    public_address = wallet_data['public_address']
    wallet_data['balance'] = await kin_service.get_wallet_balance(public_address)

    db.child('server_wallet').update(wallet_data)


async def update_wallet_balance(uid):
    user_query = db.child("users").child().order_by_child("uid").equal_to(uid).get()
    user_data = user_query.each()[0].val()
    current_balance = await kin_service.get_wallet_balance(user_data['public_address'])

    user_data['balance'] = current_balance
    db.child("users").child().order_by_child("uid").equal_to(uid).update(user_data)


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
    # await register('testemail@google.com', '1A345asfsa')
    # await register('onsha.bogdan@gmail.com', 'ASsgnale32r')
    # await register('nure.forum@gmail.com', '3jrnsod8an')
    # print(authenticate('nHZ1IXDUaXemjgLpIbgeM3BbtNk2'))
    # await create_server_wallet()
    # print(get_server_wallet_address('1VUeQgrTBbSltSEtm89gP8DMxmC3'))
    await get_kins('Cul7y6e6mWah1EWfkJAEPC1rOho1', 1000, 'othertest')
    # await create_server_wallet()
    #await update_server_wallet_balance()
    #await update_wallet_balance('Cul7y6e6mWah1EWfkJAEPC1rOho1')


asyncio.run(main())
