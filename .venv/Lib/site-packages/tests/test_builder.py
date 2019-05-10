# encoding: utf-8

import time

import pytest

from kin_base.builder import Builder
from kin_base.keypair import Keypair
from kin_base.exceptions import SignatureExistError, StellarSecretInvalidError
from kin_base.horizon import Horizon

# TODO: These endpoints really need to be mocked out.


@pytest.yield_fixture(scope='module')
async def test_data(setup, helpers, aio_session):
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)

    cold = Keypair.random()
    cold_secret = cold.seed()
    cold_account = cold.address().decode()
    horizon = Horizon(setup.horizon_endpoint_uri)

    await helpers.fund_account(setup, cold.address().decode(), aio_session)

    yield Struct(cold_secret=cold_secret, cold_account=cold_account, horizon=horizon)
    await horizon.close()


@pytest.mark.asyncio
async def test_builder_(setup, test_data):
    hot = Keypair.random()
    hot_account = hot.address().decode()
    hot_secret = hot.seed()

    cold = Builder(secret=test_data.cold_secret, horizon=test_data.horizon, network_name=setup.network, fee=100) \
        .append_create_account_op(hot_account, '200') \
        .append_set_options_op(inflation_dest=test_data.cold_account, set_flags=1,
                               home_domain='256kw.com', master_weight=10,
                               low_threshold=5, ) \
        .append_change_trust_op('BEER', test_data.cold_account, '1000', hot_account) \
        .append_allow_trust_op(hot_account, 'BEER', True)
    # append twice for test
    cold.append_payment_op(hot_account, '50.123', 'BEER', test_data.cold_account) \
        .append_payment_op(hot_account, '50.123', 'BEER', test_data.cold_account)
    # TODO: append_bump_sequence_op test
    await cold.update_sequence()
    cold.sign()
    cold.sign(hot_secret)
    # try to sign twice
    with pytest.raises(SignatureExistError):
        cold.sign(hot_secret)

    assert len(cold.te.signatures) == 2
    assert len(cold.ops) == 5

    response = await cold.submit()
    assert response.get('hash') == cold.hash_hex()


@pytest.mark.asyncio
async def test_builder_xdr(setup, helpers, test_data, aio_session):
    hot = Keypair.random()
    hot_account = hot.address().decode()
    hot_secret = hot.seed()

    await helpers.fund_account(setup, hot_account, aio_session)

    cold = Builder(secret=test_data.cold_secret, horizon=test_data.horizon, network_name=setup.network, fee=100) \
        .append_change_trust_op('BEER', test_data.cold_account, '1000', hot_account) \
        .append_allow_trust_op(hot_account, 'BEER', True, test_data.cold_account) \
        .append_payment_op(hot_account, '100', 'BEER', test_data.cold_account, test_data.cold_account) \
        .append_payment_op(test_data.cold_account, '2.222', 'BEER', test_data.cold_account, hot_account)
    await cold.update_sequence()
    cold.sign()

    xdr = cold.gen_xdr()

    hot = Builder(
        secret=hot_secret,
        horizon=test_data.horizon,
        network_name=setup.network, fee=100)
    hot.import_from_xdr(xdr)
    hot.sign()

    assert len(hot.te.signatures) == 2
    assert len(hot.ops) == 4

    response = await hot.submit()
    assert response.get('hash') == hot.hash_hex()


def test_create_fail():
    with pytest.raises(StellarSecretInvalidError):
        Builder(secret='bad', network_name=None, horizon=None, fee=100)


def test_create():
    seed = 'SASKOJJOG7MLXAWJGE6QNCWH5ZIBH5LWQCXPRGDHUKUOB4RBRWXXFZ2T'
    address = 'GCAZ7QXD6UJ5NOVWYTNKLNP36DPJZMRO67LQ4X5CH2IHY3OG5QGECGYQ'

    # with secret
    builder = Builder(secret=seed, network_name=None, horizon=None, fee=100)
    assert builder
    assert builder.keypair.seed().decode() == seed
    assert builder.address == address


@pytest.fixture(scope='module')
def test_builder(test_data, setup):
    builder = Builder(secret=test_data.cold_secret,
                      horizon=test_data.horizon,
                      network_name=setup.network,
                      fee=100)
    return builder


@pytest.mark.asyncio
async def test_sign(test_builder):
    address = 'GCAZ7QXD6UJ5NOVWYTNKLNP36DPJZMRO67LQ4X5CH2IHY3OG5QGECGYQ'

    test_builder.append_create_account_op(address, '100')
    assert len(test_builder.ops) == 1
    await test_builder.update_sequence()
    test_builder.sign()
    assert test_builder.te
    assert test_builder.tx


@pytest.mark.asyncio
async def test_update_sequence(test_builder):
    await test_builder.update_sequence()
    assert test_builder.sequence


@pytest.mark.asyncio
async def test_set_channel(setup, helpers, test_builder, aio_session):
    channel_addr = 'GBC6PXY4ZSO356NUPF2A2SDVEBQB2RG7XN6337NBW4F24APGHEVR3IIU'
    channel = 'SA4BHY26Q3C3BSYKKGDM7UVMZ4YF6YBLX6AOWYEDBXPLOR7WQ5EJXN6X'
    await helpers.fund_account(setup, channel_addr, aio_session)
    time.sleep(5)
    await test_builder.set_channel(channel)
    assert test_builder.address == channel_addr
    assert test_builder.sequence

