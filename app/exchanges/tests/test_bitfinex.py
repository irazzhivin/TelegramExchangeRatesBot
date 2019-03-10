import datetime
from decimal import Decimal

import vcr

from suite.test.testcases import SimpleTestCase
from ..bitfinex import BitfinexExchange
from ..base import PairData, Pair, Currency
from ..exceptions import PairNotExistsException


my_vcr = vcr.VCR(
    cassette_library_dir='app/exchanges/tests/fixtures/vcr/bitfinex',
    record_mode='once',
    decode_compressed_response=True,
)


class BitfinexTest(SimpleTestCase):

    @my_vcr.use_cassette('symbols_200')
    def test_list_currencies(self):
        currencies = BitfinexExchange().list_currencies
        self.assertEqual(len(currencies), 127)
        self.assertTrue(Currency(code='USD') in currencies)
        self.assertTrue(Currency(code='BTC') in currencies)

    @my_vcr.use_cassette('symbols_200')
    def test_list_pairs(self):
        pairs = BitfinexExchange().list_pairs
        self.assertEqual(len(pairs), 339)
        self.assertTrue(Pair(Currency('USD'), Currency('BTC')) in pairs)

    @my_vcr.use_cassette('symbols_200')
    def test_is_pair_exists(self):
        exchange = BitfinexExchange()
        self.assertTrue(exchange.is_pair_exists(Pair(Currency('USD'), Currency('BTC'))))

        self.assertFalse(exchange.is_pair_exists(Pair(Currency('usd'), Currency('BTC'))))
        self.assertFalse(exchange.is_pair_exists(Pair(Currency('USD'), Currency('MONEY'))))

    @my_vcr.use_cassette('symbols_200')
    def test_is_currency_exists(self):
        exchange = BitfinexExchange()
        self.assertTrue(exchange.is_currency_exists(Currency(code='USD')))
        self.assertTrue(exchange.is_currency_exists(Currency(code='BTC')))

        self.assertFalse(exchange.is_currency_exists(Currency(code='usd')))
        self.assertFalse(exchange.is_currency_exists(Currency(code='MONEY')))

    @my_vcr.use_cassette('get_pair_200')
    def test_get_pair_info(self):
        pair = Pair(Currency('USD'), Currency('BTC'))
        self.assertEqual(
            BitfinexExchange().get_pair_info(pair),
            PairData(
                pair=pair,
                rate=Decimal('3996.05'),
                rate_open=None,
                low24h=Decimal('3850.0'),
                high24h=Decimal('4021.0'),
                volume24h=Decimal('9567.9947337399999735'),
                last_trade_at=datetime.datetime(2019, 3, 9, 11, 21, 12, 996645),
            )
        )

    @my_vcr.use_cassette('get_pair_200')
    def test_get_pair_info_no_pair(self):
        pair = Pair(Currency('USD'), Currency('MONEY'))
        with self.assertRaises(PairNotExistsException):
            BitfinexExchange().get_pair_info(pair)
