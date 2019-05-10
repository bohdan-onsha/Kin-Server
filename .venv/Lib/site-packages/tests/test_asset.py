# coding: utf-8
from unittest import TestCase
import pytest

from kin_base.asset import Asset
from kin_base.stellarxdr import Xdr


class TestAsset(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (
            'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z')
        cls.cny = Asset('CNY', cls.source)

    def test_native(self):
        assert 'KIN' == Asset.native().code
        assert Asset.native().issuer is None
        assert 'native' == Asset.native().type

    def test_is_native(self):
        native = Asset('KIN')
        assert native.is_native()
        assert not self.cny.is_native()

    def test_to_xdr_object(self):
        assert isinstance(self.cny.to_xdr_object(), Xdr.types.Asset)

    def test_too_long(self):
        with pytest.raises(Exception, match='Asset code is invalid'):
            Asset('123456789012TooLong', self.source)

    def test_no_issuer(self):
        with pytest.raises(Exception, match='Issuer cannot be `None` except native asset.'):
            Asset('beer', None)

    def test_xdr(self):
        xdr = b'AAAAAUNOWQAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2M='
        assert xdr == self.cny.xdr()

    def test_unxdr(self):
        xdr = self.cny.xdr()
        cny_x = Asset.from_xdr(xdr)
        assert self.cny == cny_x

    def test_asset_to_dict(self):
        native = Asset('KIN')
        assert native.to_dict() == {'code': 'KIN', 'type': 'native'}
        assert self.cny.to_dict() == {
            'code': 'CNY',
            'issuer': self.source,
            'type': 'credit_alphanum4'
        }
