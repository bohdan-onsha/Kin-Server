import asyncio
import kin

app_id = 'NM8e'


def get_keypair(seed=None):
    if seed is None:
        return kin.Keypair()
    try:
        return kin.Keypair(seed=seed)
    except kin.KinErrors.StellarSecretInvalidError:
        raise


async def create_account(client, keypair=None):
    if keypair is None:
        keypair = get_keypair()
    if not await client.does_account_exists(keypair.public_address):
        await client.friendbot(keypair.public_address)
    return client.kin_account(keypair.secret_seed, app_id=app_id)


async def send_kin(client, account, destination, count, memo_text=''):
    tx_hash = await account.send_kin(destination, count, fee=100, memo_text=memo_text)
    transaction = await client.get_transaction_data(tx_hash=tx_hash)
    transaction.operation = vars(transaction.operation)
    return vars(transaction)


async def get_wallet_balance(public_address):
    async with get_client() as client:
        return await client.get_account_balance(public_address)


async def main():
    print(await get_wallet_balance('GDMDSV7UMMQ46TYV2MKA6MQDRXKHC2HBSKNO6IFU7LPZIJ6LVNJMJKNY'))


def get_client():
    return kin.KinClient(kin.TEST_ENVIRONMENT)


#asyncio.run(main())
