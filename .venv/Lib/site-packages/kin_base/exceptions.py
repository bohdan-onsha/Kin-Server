HORIZON_NS_PREFIX = 'https://stellar.org/horizon-errors/'
"""
Horizon error example:

{
    'status': 400,
    'title': 'Transaction Failed',
    'detail': 'The transaction failed when submitted to the stellar network. The `extras.result_codes` field on this '
              'response contains further details.  Descriptions of each code can be found at: '
              'https://www.stellar.org/developers/learn/concepts/list-of-operations.html',
    'instance': '903d29404b0e/DAurVuBoL4-004368',
    'extras': 	{
        'result_codes': {
            'operations': ['op_no_destination'],
            'transaction': 'tx_failed'
        }, 
        'envelope_xdr': 'AAAAAJgXswhWU+pdHmHIurQuHk4ziNlKFxEJltbMOpF6EqETAAAAZAAAed0AAAAQAAAAAAAAAAAAAAABAAAAAAAAA'
                        'AEAAAAAxbIcFBPzPZbzjWdkSB5FCSIva+WdQ2Oi70GUmFvFmOcAAAABVEVTVAAAAAD284i665ald1Kiq064FGlL+'
                        'Aeych/b9UQngBHR37ZeiwAAAAAF9eEAAAAAAAAAAAF6EqETAAAAQN5x3xaOaeDS5EF3tE0X9zXymhqkOg95Tyfgu'
                        '//TCbv9XN49CHoH5K+BUH04o1ZAZdHbnBABxh44bu7zbFLgQQU=',
        'invalid_field': None,
        'result_xdr': 'AAAAAAAAAGT/////AAAAAQAAAAAAAAAB////+wAAAAA='
    },
    'type': 'https://stellar.org/horizon-errors/transaction_failed'
}
"""


class StellarError(Exception):
    def __init__(self, msg):
        super(StellarError, self).__init__(msg)


class BadSignatureError(StellarError):
    pass


class AssetCodeInvalidError(StellarError):
    pass


class StellarAddressInvalidError(StellarError):
    pass


class StellarSecretInvalidError(StellarError):
    pass


class NoStellarSecretOrAddressError(StellarError):
    pass


class SequenceError(StellarError):
    pass


class ConfigurationError(StellarError):
    pass


class NoApproximationError(StellarError):
    pass


class HorizonError(StellarError):
    """A :exc:`HorizonError` that represents an issue stemming from
    Stellar Horizon.

    """
    def __init__(self, msg: dict):
        super(HorizonError, self).__init__(msg)
        for key, value in msg.items():
            setattr(self, key, value)
        self.type = self.type.replace(HORIZON_NS_PREFIX, '')


class HorizonRequestError(StellarError):
    """A :exc:`HorizonRequestError` that represents we cannot connect
    to Stellar Horizon.

    """
    pass


class SignatureExistError(StellarError):
    pass


class DecodeError(StellarError):
    pass


class NotValidParamError(StellarError):
    pass


class MnemonicError(StellarError):
    pass


class MissingSigningKeyError(StellarError):
    pass


class FederationError(Exception):
    """A :exc:`FederationError` that represents an issue stemming from
    Stellar Federation.

    """
