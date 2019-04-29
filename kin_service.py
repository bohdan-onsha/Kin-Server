import asyncio
import kin

import errors

app_id = 'NM8e'


def get_keypair(seed=None) -> kin.Keypair:
    """
        Gets the kin.Keypair instance with the given seed.
        Creates new one if seed is None


        :param seed: Secret seed of kin wallet

        :return: :class kin.Keypair

        :raises: :class: errors.StellarSecretInvalidError if the given seed is invalid

    """
    if seed is None:
        return kin.Keypair()
    try:
        return kin.Keypair(seed=seed)
    except kin.KinErrors.StellarSecretInvalidError:
        raise


async def create_account(client: kin.KinClient, account: kin.KinAccount, keypair=None) -> kin.KinAccount:
    """
        Create a new instance of the kin.KinClient to query the Kin blockchain
        with the given keypair or with new one


        :param client: :class kin.KinClient performs operations to query to the Kin Blockchain
        :param account: :class kin.KinAccount account for the initial transaction
        :param keypair: :class kin.Keypair keypair of the kin wallet

        :return: :class kin.KinAccount allows you to perform authenticated actions on the Kim Blockchain

    """
    if keypair is None or not isinstance(keypair, kin.Keypair):
        keypair = get_keypair()
    if not await client.does_account_exists(keypair.public_address):
        await account.create_account(keypair.public_address, 0, 100)
    return client.kin_account(keypair.secret_seed, app_id=app_id)


def whitelist_tx(client: kin.KinClient, account: kin.KinAccount, tx_hash: str):
    whitelisted_tx = account.whitelist_transaction(tx_hash)
    return kin.decode_transaction(whitelisted_tx)


async def send_kin(client: kin.KinClient, account: kin.KinAccount, destination: str, amount: int,
                   memo_text='') -> dict:
    """
        Send KIN to the account identified by the provided address.

        :param client: :class kin.KinClient performs operations to query to the Kin Blockchain
        :param account: :class kin.KinAccount account-sender
        :param destination: kin wallet public address of recipient
        :param amount: :class amount of kin
        :param memo_text: additional transaction text

        :return: dictionary with the transaction details

        :raises: :class kin.KinErrors.LowBalanceEroor if there is not enough KIN to send and pay transaction fee
        :raises: :class kin.KinErrors.NotValidParamError if the memo is longer than MEMO_CAP characters
    """
    minimum_fee = await client.get_minimum_fee()
    try:
        tx_hash = await account.send_kin(destination, amount, fee=minimum_fee, memo_text=memo_text)
        transaction = await client.get_transaction_data(tx_hash=tx_hash)
        transaction.operation = vars(transaction.operation)
        return vars(transaction)
    except (kin.KinErrors.LowBalanceError, kin.KinErrors.NotValidParamError):
        raise


async def get_wallet_balance(public_address: str) -> int:
    """
        Returns current balance of kin wallet with the given address

        :param public_address: public address of kin wallet

        :return: amount of kin available on account

    """
    async with get_client() as client:
        try:
            return await client.get_account_balance(public_address)
        except kin.errors.AccountNotFoundError:
            raise errors.ItemNotFoundError
        except kin.errors.StellarAddressInvalidError:
            raise


def get_client():
    return kin.KinClient(kin.TEST_ENVIRONMENT)


async def main():
    pass

# asyncio.run(main())
