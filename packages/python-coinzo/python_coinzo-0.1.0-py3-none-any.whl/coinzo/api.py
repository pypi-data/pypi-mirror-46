import logging
from . import exceptions
import hashlib
import hmac
import base64
import json
import requests
from time import time
from http import HTTPStatus
from urllib.parse import urljoin


class coinzo:
    API_ENDPOINT = "https://api.coinzo.com"

    SIDE_BUY = "BUY"
    SIDE_SELL = "SELL"

    ORDER_TYPE_LIMIT = "LIMIT"
    ORDER_TYPE_MARKET = "MARKET"
    ORDER_TYPE_STOP_MARKET = "STOP"
    ORDER_TYPE_STOP_LIMIT = "STOP LIMIT"

    def __init__(self, api_key, api_secret):
        self.API_KEY = api_key
        self.API_SECRET = api_secret

    def _generate_signature(self, payload):
        """
        Helper method which generates the
        base64-encoded signature for authentication.
        """
        secret = self.API_SECRET.encode("utf-8")
        return base64.b64encode(
            hmac.new(key=secret, msg=payload, digestmod=hashlib.sha384).digest()
        )

    def _generate_payload(self, data):
        """
        Helper method which generates the
        base64-encoded payload for API requests.
        """
        data.update({"nonce": int(time() * 1000)})
        return base64.b64encode(json.dumps(data).encode("utf-8"))

    def _make_request(self, method, path, data={}, params=None):
        """
        Helper method which makes authenticated requests.

        Raises:
            exceptions.DeleteError: [description]
            exceptions.BadResponse: [description]

        Returns:
            if possible:
                [dict] -- [response json object]
            otherwise:
                [bool] -- [True for successful requests]
        """
        logging.info("Making a request...")

        url = urljoin(self.API_ENDPOINT, path)
        payload = self._generate_payload(data)
        signature = self._generate_signature(payload)

        headers = {
            "Content-Type": "application/json",
            "X-CNZ-APIKEY": self.API_KEY,
            "X-CNZ-PAYLOAD": payload,
            "X-CNZ-SIGNATURE": signature,
        }

        response = requests.request(method, url, headers=headers, params=params)
        exceptions.detect_and_raise_error(response)

        if response.status_code == HTTPStatus.ACCEPTED:
            return True
        if method == "delete":
            if response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.OK):
                return True
            else:
                raise exceptions.DeleteError(response)
        try:
            r = response.json()
        except ValueError:
            raise exceptions.BadResponse

        return r

    def _get_request(self, path, data={}, params=None):
        """
        Helper method which makes authenticated get requests.
        """
        return self._make_request("get", path, data, params=params)

    def _post_request(self, path, data={}):
        """
        Helper method which makes authenticated post requests.
        """
        return self._make_request("post", path, data)

    def _delete_request(self, path, data={}):
        """
        Helper method which makes authenticated delete requests.
        """
        return self._make_request("delete", path, data)

    ###########################################################################
    #   PRIVATE API > USER INFO >>> Permissions: Info
    ###########################################################################
    def get_account_info(self):
        """
        Get account information.

        https://docs.coinzo.com/#fills
        """
        logging.info(f"Getting user info...")
        path = "/usage"

        return self._get_request(path)

    def get_balances(self):
        """
        Get account balances.

        https://docs.coinzo.com/#balances
        """
        logging.info(f"Getting account balances...")
        path = "/balances"

        return self._get_request(path)

    ###########################################################################
    #   PRIVATE API > ORDERS >>> Permissions: Info + (Trade)
    ###########################################################################
    def get_open_orders(self, limit=100, page=1):
        """
        List your current open orders. Only open or un-settled
        orders are returned. As soon as an order is no longer open
        and settled, it will no longer appear in the default request.

        https://docs.coinzo.com/#list-orders
        """
        logging.info(f"Getting all open orders...")
        path = "/orders"
        data = {"limit": limit, "page": page}

        return self._get_request(path, data)

    def get_order(self, order_id):
        """
        Get information about a given order.

        https://docs.coinzo.com/#get-order-status
        """
        logging.info(f"Getting order with id {order_id}...")
        path = "/order"
        data = {"id": order_id}

        return self._get_request(path, data)

    def _place_order(self, pair, type, side, amount, limit_price, stop_price=None):
        """
        Create new order and put it to the orders processing queue.

        https://docs.coinzo.com/#place-a-new-order
        """
        logging.info(
            f"Creating {type} order for {pair} {amount}@{limit_price} ({stop_price})..."
        )
        path = "/order/new"
        data = {
            "pair": pair,
            "type": type,
            "side": side,
            "amount": amount,
            "limitPrice": limit_price,
        }

        if stop_price:
            data.update({"stopPrice": stop_price})

        return self._post_request(path, data)

    def place_limit_buy_order(self, pair, amount, limit_price):
        """
        Place a limit buy order.

        https://docs.coinzo.com/#place-a-new-order
        """
        return self._place_order(
            pair=pair,
            type=self.ORDER_TYPE_LIMIT,
            side=self.SIDE_BUY,
            amount=amount,
            limit_price=limit_price,
        )

    def place_limit_sell_order(self, pair, amount, limit_price):
        """
        Place a limit sell order.

        https://docs.coinzo.com/#place-a-new-order
        """
        return self._place_order(
            pair=pair,
            type=self.ORDER_TYPE_LIMIT,
            side=self.SIDE_SELL,
            amount=amount,
            limit_price=limit_price,
        )

    def place_stop_limit_buy_order(self, pair, amount, limit_price, stop_price):
        """
        Place a stop limit buy order.

        https://docs.coinzo.com/#place-a-new-order
        """
        return self._place_order(
            pair=pair,
            type=self.ORDER_TYPE_STOP_LIMIT,
            side=self.SIDE_BUY,
            amount=amount,
            limit_price=limit_price,
            stop_price=stop_price,
        )

    def place_stop_limit_sell_order(self, pair, amount, limit_price, stop_price):
        """
        Place a stop limit sell order.

        https://docs.coinzo.com/#place-a-new-order
        """
        return self._place_order(
            pair=pair,
            type=self.ORDER_TYPE_STOP_LIMIT,
            side=self.SIDE_SELL,
            amount=amount,
            limit_price=limit_price,
            stop_price=stop_price,
        )

    def place_market_buy_order(self, pair, amount):
        """
        Place a market buy order.

        https://docs.coinzo.com/#place-a-new-order
        """
        return self._place_order(
            pair=pair,
            type=self.ORDER_TYPE_MARKET,
            side=self.SIDE_BUY,
            amount=amount,
            limit_price="0",
        )

    def place_market_sell_order(self, pair, amount):
        """
        Place a market sell order.

        https://docs.coinzo.com/#place-a-new-order
        """
        return self._place_order(
            pair=pair,
            type=self.ORDER_TYPE_MARKET,
            side=self.SIDE_SELL,
            amount=amount,
            limit_price="0",
        )

    def place_stop_market_buy_order(self, pair, amount, stop_price):
        """
        Place a stop market buy order.

        https://docs.coinzo.com/#place-a-new-order
        """
        return self._place_order(
            pair=pair,
            type=self.ORDER_TYPE_STOP_MARKET,
            side=self.SIDE_BUY,
            amount=amount,
            limit_price="0",
            stop_price=stop_price,
        )

    def place_stop_market_sell_order(self, pair, amount, stop_price):
        """
        Place a stop market sell order.

        https://docs.coinzo.com/#place-a-new-order
        """
        return self._place_order(
            pair=pair,
            type=self.ORDER_TYPE_STOP_MARKET,
            side=self.SIDE_SELL,
            amount=amount,
            limit_price="0",
            stop_price=stop_price,
        )

    def cancel_order(self, order_id):
        """
        Cancel an order.

        https://docs.coinzo.com/#cancel-an-order
        """
        logging.info(f"Cancelling order {order_id}...")
        path = "/order"
        data = {"id": order_id}

        return self._delete_request(path, data)

    def cancel_all_orders(self):
        """
        Cancel all open orders.

        https://docs.coinzo.com/#cancel-all-orders
        """
        logging.info(f"Cancelling all open orders...")
        path = "/orders"

        return self._delete_request(path)

    def get_fills(self, limit=100, page=1):
        """
        Get the list of recent fills.

        https://docs.coinzo.com/#fills
        """
        logging.info(f"Getting recent fills...")
        path = "/fills"
        data = {"limit": limit, "page": page}

        return self._get_request(path, data)

    ###########################################################################
    #   PRIVATE API > DEPOSIT/WITHDRAWAL >>> Permissions: Info + (Withdrawal)
    ###########################################################################
    def get_deposit_address(self, asset):
        """
        Get the deposit address for an asset.

        https://docs.coinzo.com/#show-deposit-address
        """
        logging.info(f"Getting deposit address for {asset}...")
        path = "/deposit/address"
        data = {"asset": asset}

        return self._get_request(path, data)

    def get_deposit_history(self, limit=100, page=1):
        """
        Get your deposit history.

        https://docs.coinzo.com/#list-deposits
        """
        logging.info(f"Getting deposit history...")
        path = "/deposit/list"
        data = {"limit": limit, "page": page}

        return self._get_request(path, data)

    def withdraw(self, asset, address, amount, tag=None, memo=None):
        """
        Withdraw funds to a crypto address.

        https://docs.coinzo.com/#new-withdraw
        """
        logging.info(
            f"Creating withdrawal request of {amount} {asset} to {address} ({tag}{memo})..."
        )
        path = "/withdraw"
        data = {"asset": asset, "address": address, "amount": amount}

        if tag:
            data.update({"tag": tag})

        if memo:
            data.update({"memo": memo})

        return self._post_request(path, data)

    def get_withdrawal_history(self, limit=100, page=1):
        """
        Get your withdrawal history.

        https://docs.coinzo.com/#list-withdrawals
        """
        logging.info(f"Getting withdrawal history...")
        path = "/withdraw/list"
        data = {"limit": limit, "page": page}

        return self._get_request(path, data)

    ###########################################################################
    #   PUBLIC API >>> No permissions needed
    ###########################################################################
    def get_all_tickers(self):
        """
        Get the list tickers for all trading pairs.
        Snapshot information about the last trade (tick),
        24h low, high price and volume.

        https://docs.coinzo.com/#ticker
        """
        logging.info(f"Getting all tickers...")
        path = "/tickers"

        return self._get_request(path)

    def get_ticker(self, pair):
        """
        Get the ticker for a pair.
        Snapshot information about the last trade (tick),
        24h low, high price and volume.

        https://docs.coinzo.com/#ticker
        """
        logging.info(f"Getting ticker for {pair}...")
        path = "/ticker"
        params = {"pair": pair}

        return self._get_request(path, params=params)

    def get_order_book(self, pair):
        """
        Get the order book for a pair.

        https://docs.coinzo.com/#order-book
        """
        logging.info(f"Getting order book for {pair}...")
        path = "/order-book"
        params = {"pair": pair}

        return self._get_request(path, params=params)

    def get_latest_trades(self, pair):
        """
        Get the latest trades for a pair

        https://docs.coinzo.com/#trades
        """
        logging.info(f"Getting recent trades for {pair}...")
        path = "/trades"
        params = {"pair": pair}

        return self._get_request(path, params=params)
