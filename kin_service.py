import asyncio
import kin


def get_keypair(seed=None):
    if seed is None:
        return kin.Keypair()
    try:
        return kin.Keypair(seed=seed)
    except kin.KinErrors.StellarSecretInvalidError:
        return -1


async def exists(client, keypair):
    return await client.does_account_exists(keypair.public_address)


async def create_account(client, keypair=None):
    if keypair is None:
        keypair = get_keypair()
    exist = await client.does_account_exists(keypair.public_address)
    if exist:
        await client.acc
    else:
        await client.friendbot(keypair.public_address)


async def main():
    async with kin.KinClient(kin.TEST_ENVIRONMENT) as client:
        key_pair = get_keypair("SBIJHIEY4OR4LOMYWH4YQLDEQWUJHCFMIZDJZOOGOMEPTURM3KVZNZWT")
        print(key_pair)
        print(await exists(client,key_pair))
        account = client.kin_account('SBIJHIEY4OR4LOMYWH4YQLDEQWUJHCFMIZDJZOOGOMEPTURM3KVZNZWT')
        print(account)


asyncio.run(main())
