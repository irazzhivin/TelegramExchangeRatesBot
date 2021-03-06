import logging
from datetime import datetime
from decimal import Decimal
from typing import Tuple

import requests
from cached_property import cached_property
from jsonschema import ValidationError, validate

from app.exchanges.base import ECurrency, Exchange, Pair, PairData
from app.exchanges.exceptions import (
    APIChangedException,
    APIErrorException,
    PairNotExistsException,
)
from app.queries import get_all_currency_codes


class BittrexExchange(Exchange):
    """
    https://bittrex.github.io/

    Maximum of 60 API calls per minute.
    Calls after the limit will fail, with the limit resetting at the start of the next minute.
    """

    name = (
        "[bittrex.com](https://bittrex.com/Account/Register?referralCode=YIV-CNI-13Q)"
    )

    @cached_property
    def _get_data(self) -> dict:
        try:
            response = requests.get(
                "https://api.bittrex.com/api/v1.1/public/getmarketsummaries"
            )
            response.raise_for_status()
            data = response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            raise APIErrorException(e)

        try:
            schema = {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "result": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "MarketName": {"type": "string"},
                                "High": {"type": ["number", "null"]},
                                "Low": {"type": ["number", "null"]},
                                "TimeStamp": {"type": "string"},
                                "Bid": {"type": ["number", "null"]},
                                "Ask": {"type": ["number", "null"]},
                                "PrevDay": {"type": ["number", "null"]},
                            },
                            "required": [
                                "MarketName",
                                "High",
                                "Low",
                                "TimeStamp",
                                "Bid",
                                "Ask",
                                "PrevDay",
                            ],
                        },
                    },
                },
                "required": ["success", "result"],
            }
            validate(data, schema)
        except ValidationError as e:
            raise APIErrorException(e)

        result = {}
        all_currency_codes = get_all_currency_codes()
        for x in data["result"]:
            # reverse
            to_currency, from_currency = x["MarketName"].upper().split("-")

            if not x["Bid"] or not x["Ask"]:
                if (
                    to_currency in all_currency_codes
                    and from_currency in all_currency_codes
                ):
                    logging.info("Bittrex no Bid Ask: %s", x)
                continue

            del x["MarketName"]
            result[Pair(ECurrency(from_currency), ECurrency(to_currency))] = x

        return result

    @cached_property
    def list_pairs(self) -> Tuple[Pair]:
        return tuple(self._get_data.keys())

    @cached_property
    def list_currencies(self) -> Tuple[ECurrency]:
        currencies = set()

        for from_currency, to_currency in self.list_pairs:
            currencies.add(from_currency)
            currencies.add(to_currency)

        return tuple(currencies)

    def get_pair_info(self, pair: Pair) -> PairData:
        if not self.is_pair_exists(pair):
            raise PairNotExistsException(pair)

        pair_data = self._get_data[pair]

        mid = (
            Decimal(str(pair_data["Bid"])) + Decimal(str(pair_data["Ask"]))
        ) / Decimal("2")

        try:
            ts_without_ms = pair_data["TimeStamp"].split(".")[0]
            last_trade_at = datetime.strptime(ts_without_ms, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise APIChangedException("TimeStamp format.")

        if pair_data["Low"] and pair_data["High"]:
            low24h = Decimal(str(pair_data["Low"]))
            high24h = Decimal(str(pair_data["High"]))
        else:
            low24h = high24h = None

        rate_open = Decimal(str(pair_data["PrevDay"])) if pair_data["PrevDay"] else None

        return PairData(
            pair=pair,
            rate=mid,
            rate_open=rate_open,
            low24h=low24h,
            high24h=high24h,
            last_trade_at=last_trade_at,
        )
