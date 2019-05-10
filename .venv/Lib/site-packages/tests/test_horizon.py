# encoding: utf-8
import asyncio
import pytest

from kin_base.keypair import Keypair
from kin_base.operation import *
from kin_base.horizon import Horizon
from kin_base.transaction import Transaction
from kin_base.transaction_envelope import TransactionEnvelope as Te


async def make_envelope(network, horizon, address, seed, *args, **kwargs):
    opts = {
        'sequence': int((await horizon.account(address))['sequence']) + 1,
        'fee': 100 * len(args)
    }
    for opt, value in kwargs.items():
        opts[opt] = value
    tx = Transaction(address, **opts)
    for count, op in enumerate(args):
        tx.add_operation(op)
    envelope = Te(tx, network_id=network)
    signer = Keypair.from_seed(seed)
    envelope.sign(signer)
    envelope_xdr = envelope.xdr()
    return envelope_xdr


@pytest.mark.asyncio
async def test_submit(setup, helpers, aio_session):
    kp = Keypair.random()
    address = kp.address().decode()
    seed = kp.seed()

    await helpers.fund_account(setup, address, aio_session)

    async with Horizon(setup.horizon_endpoint_uri) as horizon:
        envelope_xdr = await make_envelope(setup.network, horizon, address, seed,
                                     Payment(
                                         destination=address,
                                         asset=Asset.native(),
                                         amount="0.1618"))
        response = await horizon.submit(envelope_xdr.decode())
        assert 'hash' in response


@pytest.mark.asyncio
async def test_sse(setup, helpers, aio_session):
    kp = Keypair.random()
    address = kp.address().decode()

    events = []
    async def sse_handler(events):
        async with Horizon(setup.horizon_endpoint_uri) as horizon:
            async for event in await horizon.account_transactions('GA3FLH3EVYHZUHTPQZU63JPX7ECJQL2XZFCMALPCLFYMSYC4JKVLAJWM',
                                                            sse=True):
                events.append(event)
                break
    handler = asyncio.ensure_future(sse_handler(events))
    await helpers.fund_account(setup, address, aio_session)
    await asyncio.sleep(5)
    assert len(events) == 1


@pytest.mark.asyncio
async def test_sse_event_timeout(setup, helpers, aio_session):
    kp = Keypair.random()
    address = kp.address().decode()

    events = []

    async def sse_handler(events):
        async with Horizon(setup.horizon_endpoint_uri) as horizon:
            async for event in await horizon.account_transactions(
                    'GA3FLH3EVYHZUHTPQZU63JPX7ECJQL2XZFCMALPCLFYMSYC4JKVLAJWM',
                    sse=True, sse_timeout=15):
                events.append(event)

    handler = asyncio.ensure_future(sse_handler(events))
    await helpers.fund_account(setup, address, aio_session)
    await asyncio.sleep(5)
    assert len(events) == 1
    await asyncio.sleep(20)
    # Make sure that the sse generator raised timeout error
    with pytest.raises(asyncio.TimeoutError):
        raise handler.exception()

# TODO: test horizon retries once we move to response mocking