import asyncio
import kin


def get_keypair(seed=None):
    if seed is None:
        return kin.Keypair()
    try:
        return kin.Keypair(seed=seed)
    except kin.KinErrors.StellarSecretInvalidError:
        return -1


# returns public address of current server waller
async def get_cwpa():
    pass


async def create_account(client, keypair=None):
    if keypair is None:
        keypair = get_keypair()
    if not await client.does_account_exists(keypair.public_address):
        await client.friendbot(keypair.public_address)
    return client.kin_account(keypair.secret_seed)


async def send_kin(account, destination, count):
    tx_hash = await account.send_kin(destination, count, fee=100, memo_text='test')
    print(tx_hash)
    return tx_hash


async def info(client, accounts: list):
    for acc in accounts:
        print('')
        print(acc.keypair)
        print(await acc.get_balance())
        print(acc.get_public_address())
        print('')


async def main():
    client = get_client()
    pair1 = get_keypair('SBIJHIEY4OR4LOMYWH4YQLDEQWUJHCFMIZDJZOOGOMEPTURM3KVZNZWT')
    account1 = await create_account(client, pair1)

    pair2 = get_keypair('SBI7YGTN4SVFJHIKKPTP3GAXD7WOERDPV7544JL6WAGZURIRBKY7OFEY')
    account2 = await create_account(client, pair2)

    print(client.does_account_exists(account1.get_public_address()))
    print('1 acc before ', await account1.get_balance())
    print('2 acc before ', await account2.get_balance())

    # await send_kin(account1, account2.get_public_address(), 1000)

    print('1 acc after ', await account1.get_balance())
    print('2 acc after ', await account2.get_balance())

    print('1 status ', await account1.get_status(verbose=True))
    print('2 status ', await account2.get_status(verbose=True))
    await client.close()


def get_client():
    return kin.KinClient(kin.TEST_ENVIRONMENT)


async def cclient():
    async with kin.KinClient(kin.TEST_ENVIRONMENT) as client:
        return client


#asyncio.run(main())
