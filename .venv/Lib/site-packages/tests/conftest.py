import asyncio

import pytest
from aiohttp import ClientSession

from kin_base.asset import Asset
from kin_base.keypair import Keypair
from kin_base.builder import Builder
from kin_base.horizon import Horizon

import logging
logging.basicConfig()


def pytest_addoption(parser):
    parser.addoption(
        "--testnet",
        action="store_true",
        default=False,
        help="whether testing on testnet instead of local")


@pytest.fixture(scope='session')
def testnet(request):
    return request.config.getoption("--testnet")


@pytest.fixture(scope='session')
def setup():
    class Struct:
        """Handy variable holder"""

        def __init__(self, **entries):
            self.__dict__.update(entries)

    issuer_keypair = Keypair.random()
    test_asset = Asset('TEST', issuer_keypair.address().decode())

    # local testnet (kinecosystem docker)
    from kin_base.network import NETWORKS
    # we will leave this passphrase instead of changing every envelop in the test suite
    NETWORKS['CUSTOM'] = 'Integration Test Network ; zulucrypto'
    return Struct(
        type='local',
        network='CUSTOM',
        issuer_keypair=issuer_keypair,
        test_asset=test_asset,
        horizon_endpoint_uri='http://localhost:8008',
        friendbot_url='http://localhost:8001')


@pytest.yield_fixture(scope='session')
async def aio_session():
    session = ClientSession()
    yield session
    await session.close()


class Helpers:
    """A container for helper functions available to all tests"""

    @staticmethod
    async def fund_account(setup, address, aio_session):
        for attempt in range(3):
            try:
                async with aio_session.get(setup.friendbot_url +
                                 '?addr=' + address) as r:
                    j = await r.json()
                if 'hash' in j:
                    print('\naccount {} funded successfully'.format(address))
                    return
                elif 'op_already_exists' in j:
                    print('\naccount {} already exists, not funded'.format(
                        address))
                    return
                else:
                    raise Exception('unexpected friendbot reply')
            except Exception as e:
                print(e)
                print('\naccount {} funding error: {} {}'.format(
                    address, r.status, await r.text()))
        raise Exception('account {} funding failed'.format(address))

    @staticmethod
    async def trust_asset(setup, secret_key, memo_text=None):
        """A helper to establish a trustline"""
        async with Horizon(setup.horizon_endpoint_uri) as horizon:
            builder = Builder(
                secret=secret_key,
                horizon=horizon,
                network_name=setup.network,
                fee=100)
            builder.append_trust_op(setup.test_asset.issuer, setup.test_asset.code)
            if memo_text:
                builder.add_text_memo(memo_text[:28])  # max memo length is 28
            builder.sign()
            reply = await builder.submit()
        return reply.get('hash')

    @classmethod
    async def fund_asset(cls, setup, address, amount, memo_text=None):
        """A helper to fund account with test asset"""
        return cls.send_asset(setup, setup.issuer_keypair.seed(), address,
                              amount, memo_text)

    @classmethod
    async def send_asset(cls, setup, secret_key, address, amount, memo_text=None):
        """A helper to send asset"""
        async with Horizon(setup.horizon_endpoint_uri) as horizon:
            builder = Builder(
                secret=secret_key,
                horizon=horizon,
                network_name=setup.network,
                fee=100)
            builder.append_payment_op(address, amount, setup.test_asset.code,
                                      setup.test_asset.issuer)
            if memo_text:
                builder.add_text_memo(memo_text[:28])  # max memo length is 28
            builder.sign()
            reply = await builder.submit()
        return reply.get('hash')


@pytest.fixture(scope='session')
def helpers():
    return Helpers

@pytest.yield_fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
