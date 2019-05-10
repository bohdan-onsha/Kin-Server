# coding:utf-8
import pytest

from kin_base.operation import *
from kin_base.asset import Asset
from kin_base.keypair import Keypair
from kin_base.transaction import Transaction
from kin_base.transaction_envelope import TransactionEnvelope as Te


class TestOp:
    source = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
    seed = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
    dest = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
    amount = "1"

    def do(self, network, op):
        tx = Transaction(self.source, sequence=2)
        tx.add_operation(op)
        envelope = Te(tx, network_id=network)
        signer = Keypair.from_seed(self.seed)
        envelope.sign(signer)
        envelope_b64 = envelope.xdr()
        print(envelope_b64)
        return envelope_b64

    def test_createAccount_min(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAGGoAAAAAAAAAABzT4TYwAAAEAd1YRwvsfZpr/DJk0FDJQmINcefgfh/cg8ez82JuaRtAXdkDRQyy++HIQQFoKASCTy3y6gWLrhhex4QLgHODMF'
        generated_result = self.do(
            setup.network,
            op=CreateAccount(
                destination=self.dest,
                starting_balance=self.amount,
            ))
        assert result == generated_result

    def test_payment_min(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAAABhqAAAAAAAAAAAc0+E2MAAABA38jqPW3m8yeamMmzG65hUsjz5PqJwi4zW5LwOcs7vJVk+lPGOSpG5Qvbe0m7eZN9glfZQRfj5UYyB6bWJgxXAw=='
        generated_result = self.do(
            setup.network,
            op=Payment(
                source=self.source,
                destination=self.dest,
                asset=Asset.native(),
                amount=self.amount,
            ))
        assert result == generated_result

    def test_payment_short_asset(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABVVNENAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAAAAYagAAAAAAAAAAHNPhNjAAAAQGdGYF96SPGbe+PoSXejnYdR/ZqcAI+L17V3Dhn7/Munj/cCY6fWHxUR9i3Z8z7/YJpyWIVId1X4C2RDo0TTDQE='
        generated_result = self.do(
            setup.network,
            op=Payment(
                source=self.source,
                destination=self.dest,
                asset=Asset('USD4', self.source),
                amount=self.amount,
            ))
        assert result == generated_result

    def test_payment_long_asset(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACU05BQ0tTNzg5QUJDAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAAAABhqAAAAAAAAAAAc0+E2MAAABAVZAZ6qnMRld3XMKazaRyQWzJ5c2fGPCwFFJAtIWtGCJE3jGeRzfagQPDRZS+dze+jyp1iNztV2XVhIAaWddJAA=='
        generated_result = self.do(
            setup.network,
            op=Payment(
                source=self.source,
                destination=self.dest,
                asset=Asset('SNACKS789ABC', self.source),
                amount=self.amount,
            ))
        assert result == generated_result

    def test_pathPayment_min(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAIAAAAAAAAAAAABhqAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAAABhqAAAAAAAAAAAAAAAAHNPhNjAAAAQGWG1c11+P5HUofw6Wm0X1JpLtlTUA/z3keudcwVFBt0rjqi2xNHcBdon2yeVDrAdJy6ekEfUIrSW+WopWlUlAw='
        generated_result = self.do(
            setup.network,
            op=PathPayment(
                source=self.source,
                destination=self.dest,
                send_asset=Asset.native(),
                dest_asset=Asset.native(),
                send_max=self.amount,
                dest_amount=self.amount,
                path=[],
            ))
        assert result == generated_result

    def test_manageOffer_min(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAMAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAAACYloAABMsvAAGGoAAAAAAAAAABAAAAAAAAAAHNPhNjAAAAQFLiIbhd97SZ79ilXZvqL+WpJsZ0J5PmrrEQVtogAGFnRAOAUO1fi1nKgnBWYw0WtLpnv66wGljFzBVaGVG4TQw='
        generated_result = self.do(
            setup.network,
            op=ManageOffer(
                selling=Asset('beer', self.source),
                buying=Asset('beer', self.dest),
                amount="100",
                price=3.14159,
                offer_id=1,
            ))
        assert result == generated_result

    def test_createPassiveOffer_min(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAAACYloAABMsvAAGGoAAAAAAAAAABzT4TYwAAAECHcqJBPR2A4wLrJ5uc7ubrK/zcyLPj2XbPvEVZgVkVA/L4jD564uZpclEELdCN7pIyMwgJqvJ6vsmn3ENG6zEC'
        generated_result = self.do(
            setup.network,
            op=CreatePassiveOffer(
                selling=Asset('beer', self.source),
                buying=Asset('beer', self.dest),
                amount="100",
                price=3.14159,
            ))
        assert result == generated_result

    def test_SetOptions_empty(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAc0+E2MAAABAffce5U9sUC0cmi3ecjVayerdg+btd5u7fw1XguZO5mp3EjlZwATvCGdbSQbzH2wJrddAix8cHUgvJD1DdXr8DQ=='
        generated_result = self.do(setup.network, op=SetOptions())
        assert result == generated_result

    def test_changeTrust_min(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABYmVlcgAAAACtrhaIK8Wv+/J1OJRtJAXQfCSoSs/zBzoFRBq/epJAjn//////////AAAAAAAAAAHNPhNjAAAAQEMLKLk6BmEehiEqR155eZoHTMf0bFoZcsvTZpv1KDPXkOdyJZlinNR6FHv7Odk/kvxV5pYET+zqrLCJUwhcjgs='
        generated_result = self.do(
            setup.network, op=ChangeTrust(asset=Asset('beer', self.dest), ))
        assert result == generated_result

    def test_allowTrust_shortAsset(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAcAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABYmVlcgAAAAEAAAAAAAAAAc0+E2MAAABAV3Lq9RaWrhckFLidPp3WwDnGmJfY/oTQECxJqinkP0PVgS94egZt6bY9hXNWXNrLePID1XpBzVm8K6plpW6qBw=='
        generated_result = self.do(
            setup.network,
            op=AllowTrust(
                trustor=self.dest,
                asset_code='beer',
                authorize=True,
            ))
        assert result == generated_result

    def test_allowTrust_longAsset(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAcAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACcG9ja2V0a25pdmVzAAAAAQAAAAAAAAABzT4TYwAAAEDGsNazdiNzGOy11OwmnTjRAqZFw3IWasKUrqj7jldElyRYZYILZ56N3PFkIUQXfE4+GI6uiQ3kN8eXQFLXBVUH'
        generated_result = self.do(
            setup.network,
            op=AllowTrust(
                trustor=self.dest,
                asset_code='pocketknives',
                authorize=True,
            ))
        assert result == generated_result

    def test_accountMerge_min(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAgAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAc0+E2MAAABA0CkEVv6elPyZRDX554X2r51z3L1RFxOpdNNT4VHk8C/zi7pUPv92tJB7jZAExkCFOX0nDPYrb74RXYTzVxSZDg=='
        generated_result = self.do(
            setup.network, op=AccountMerge(destination=self.dest))
        assert result == generated_result

    def test_inflation(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAkAAAAAAAAAAc0+E2MAAABAg4Tj3VkLb4/I/BjtdUEoSJRO3plqsw8fApTVazJaYlCafePH3mWcJyQefELPTRlFqbPxyTaQoRD9WK86g0CPAw=='
        generated_result = self.do(setup.network, op=Inflation())
        assert result == generated_result

    def test_manage_data(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAoAAAAiMUtGSEU3dzhCaGFFTkFzd3dyeWFvY2NEYjZxY1Q2RGJZWQAAAAAAAQAAADhHREpWRkRHNU9DVzVQWVdIQjY0TUdUSEdGRjU3RFJSSkVEVUVGREVMMlNMTklPT05IWUpXSEEzWgAAAAAAAAABzT4TYwAAAEAwMGuJaQ2p5FGcFWms7omrCGbph64RslNqNLj5o6SfKFfKviCVbjzVm6FhNA3iOfBcAEPZgnSCcvRsirkiUvwK'
        generated_result = self.do(
            setup.network,
            op=ManageData(
                data_name='1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
                data_value=self.source,
            ))
        assert result == generated_result

    def test_bump_sequence(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAsAAAAFbsMSkgAAAAAAAAABzT4TYwAAAEBCy2YhkcyBpz3Wz3BSchLX/0R1GY5aS1LJ3VJigadB8nt6t++/4j/9YEMWWEDl3JhRTOMhPN8SSSs/zK1S1NIM'
        generated_result = self.do(
            setup.network,
            op=BumpSequence(bump_to=23333114514))
        assert result == generated_result


class TestMultiOp:
    address = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
    seed = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
    accounts = [
        {
            'address':
                'GCKMUHUBYSJNEIPMJ2ZHSXGSI7LLROFM5U43SWMRDV7J23HI63M7RW2D',
            'seed': 'SDKGBZFUZZEP3QKAFNLEINQ2MPD5QZJ35ZV7YNS6XCQ4NEHI6ND3ZMWC',
        },
        {
            'address':
                'GBG2TM6PGHAWRBVS37MBGOCQ7H7QQH7N2Y2WVUY7IMCEJ6MSF7LWQNIP',
            'seed': 'SAMM4N3BI447BUSTHPGO5NRHQY2J5QWECMPVHLXHZ3UKENU52UJ7MJLQ',
        },
        {
            'address':
                'GCQEAE6KDHPQMO3AJBRPSFV6FAPFYP27Q3EGE4PY4MZCTIV5RRA3KDBS',
            'seed': 'SDWJCTX6T3NJ6HEPDWFPMP33M2UDBPFKUCN7BIRFQYKXQTLO7NGDEVZE',
        },
    ]
    amount = "20"

    def make_envelope(self, network, *args, **kwargs):
        opts = {'sequence': 2, 'fee': 100 * len(args)}
        for opt, value in kwargs.items():
            opts[opt] = value
        tx = Transaction(self.address, **opts)
        for count, op in enumerate(args):
            tx.add_operation(op)
        envelope = Te(tx, network_id=network)
        signer = Keypair.from_seed(self.seed)
        envelope.sign(signer)
        envelope_b64 = envelope.xdr()
        print(envelope_b64)
        return envelope_b64

    def test_double_create_account(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAyAAAAAAAAAACAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAAB6EgAAAAAAAAAAAAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAAAA9CQAAAAAAAAAAAc0+E2MAAABA50I26sfyWprGVKxnqobmP1WBJLSNAC6wBld86/+6FmV1GZehgDKRSu0Ek3iPM65klo5cbsG/EqyadWtAtyGwBQ=='
        generated_result = self.make_envelope(
            setup.network,
            CreateAccount(
                destination=self.accounts[0]['address'],
                starting_balance=self.amount,
            ),
            CreateAccount(
                destination=self.accounts[1]['address'],
                starting_balance="40",
            ),
        )
        assert result == generated_result

    def test_double_payment(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAyAAAAAAAAAACAAAAAAAAAAAAAAACAAAAAAAAAAEAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAAAAAAAAehIAAAAAAAAAAAQAAAABNqbPPMcFohrLf2BM4UPn/CB/t1jVq0x9DBET5ki/XaAAAAAAAAAAAAD0JAAAAAAAAAAABzT4TYwAAAEB5lgq+jygYUAHyPNvDyhImdNJEInQ1H3dkWOMNX9x7s99Us+o23nx2yWDQAJcDOFMgwM2tbaFKijY3HQEopigI'
        generated_result = self.make_envelope(
            setup.network,
            Payment(
                destination=self.accounts[0]['address'],
                asset=Asset.native(),
                amount=self.amount,
            ),
            Payment(
                destination=self.accounts[1]['address'],
                asset=Asset.native(),
                amount="40",
            ),
        )
        assert result == generated_result

    def test_mix_1(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAADhAAAAAAAAAACAAAAAAAAAAAAAAAJAAAAAAAAAAAAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAAB6EgAAAAAAAAAABAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAAAAAAAAAHoSAAAAAAAAAAAIAAAAAAAAAAAAehIAAAAAAoEATyhnfBjtgSGL5Fr4oHlw/X4bIYnH44zIpor2MQbUAAAAAAAAAAAAehIAAAAAAAAAAAAAAAAMAAAABYmVlcgAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAFiZWVyAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAAACYloAABMsvAAGGoAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAABNqbPPMcFohrLf2BM4UPn/CB/t1jVq0x9DBET5ki/XaAAAAAFiZWVyAAAAAKBAE8oZ3wY7YEhi+Ra+KB5cP1+GyGJx+OMyKaK9jEG1AAAAAACYloAABMsvAAGGoAAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAABYmVlcgAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+H//////////AAAAAAAAAAcAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAABYmVlcgAAAAEAAAAAAAAACAAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAAAAAABzT4TYwAAAEA2ATIf8i+oHGbZqbzRrz9la4N83uIIvlkDwzvSG3P9IQnDnmu3SsvmmE62ldxqLAOmkNDzsARFno2ki3ZS8jIE'
        generated_result = self.make_envelope(
            setup.network,
            CreateAccount(
                destination=self.accounts[0]['address'],
                starting_balance=self.amount,
            ),
            Payment(
                destination=self.accounts[1]['address'],
                asset=Asset.native(),
                amount=self.amount,
            ),
            PathPayment(
                destination=self.accounts[2]['address'],
                send_asset=Asset.native(),
                dest_asset=Asset.native(),
                send_max=self.amount,
                dest_amount=self.amount,
                path=[],
            ),
            ManageOffer(
                selling=Asset('beer', self.accounts[0]['address']),
                buying=Asset('beer', self.accounts[1]['address']),
                amount="100",
                price=3.14159,
                offer_id=1,
            ),
            CreatePassiveOffer(
                selling=Asset('beer', self.accounts[1]['address']),
                buying=Asset('beer', self.accounts[2]['address']),
                amount="100",
                price=3.14159,
            ), SetOptions(),
            ChangeTrust(
                asset=Asset('beer', self.accounts[0]['address']), ),
            AllowTrust(
                trustor=self.accounts[0]['address'],
                asset_code='beer',
                authorize=True,
            ), AccountMerge(destination=self.accounts[0]['address'], ))
        assert result == generated_result

    def test_mix_2(self, setup):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAABkAAAAAAAAAACAAAAAAAAAAAAAAAEAAAAAAAAAAUAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAABRVVSAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAWvMQekAAAAAAAAAAAAcAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAABRVVSAAAAAAEAAAAAAAAAAQAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAFFVVIAAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAABa8xB6QAAAAAAAAAAAAc0+E2MAAABAPHgIBJbGKmNALe+2h/ZXDkKQejZi717P2UKV7jt4EMh81QPX0+PMINIJsZDhZokawfQsXw157pnxe0z28c5MAA=='
        generated_result = self.make_envelope(
            setup.network,
            SetOptions(set_flags=1),
            ChangeTrust(
                asset=Asset('EUR', self.address), limit="1000000000"),
            AllowTrust(
                authorize=True, asset_code='EUR',
                trustor=self.address),
            Payment(
                destination=self.accounts[0]['address'],
                asset=Asset('EUR', self.address),
                amount="1000000000"))
        assert result == generated_result
