# coding: utf-8
from .utils import xdr_hash

NETWORKS = {
    'PUBLIC': 'Kin Mainnet ; December 2018',
    'TESTNET': 'Kin Testnet ; December 2018'
}

from typing import Optional

class Network:
    """The :class:`Network` object, which represents a Stellar network.

    This class represents such a stellar network such as the public livenet and
    the Stellar Development Foundation Test network.

    :param str passphrase: The passphrase for the network. (ex. 'Public Global Stellar Network ; September 2015')

    """

    def __init__(self, passphrase: Optional[str] = None):
        if passphrase is None:
            self.passphrase = NETWORKS['TESTNET']
        else:
            self.passphrase = passphrase

    def network_id(self) -> bytes:
        """Get the network ID of the network.

        Get the network ID of the network, which is an XDR hash of the
        passphrase.

        """
        return xdr_hash(self.passphrase.encode())


def test_network() -> Network:
    """Get the :class:`Network` representing the Test Network."""
    return Network(NETWORKS['TESTNET'])


def live_network() -> Network:
    """Get the :class:`Network` representing the live Network."""
    return Network(NETWORKS['PUBLIC'])
