# Welcome to python-coinzo 0.1.0

python-coinzo is a simple Python wrapper for [coinzo REST API](https://docs.coinzo.com). It requires Python 3.6+

---

## Features
* Implementation of REST endpoints
* Simple handling of authentication
* Response exception handling


## Quick Start

* Register an account with [coinzo](https://www.coinzo.com/?ref=397461825936130049).
* [Generate an API Key](https://www.coinzo.com/account/api) and assign relevant permissions.
* Install the python package using the following command.

```bash
pip install python-coinzo
```


## Examples

### Initializing the API Client
```python
from coinzo.api import coinzo
coinzo = coinzo("<your_api_key>", "<your_api_secret>")
```

### Fetch ticker information for all trading pairs
```python
tickers = coinzo.get_all_tickers()
```
```json
{
    "BTC-TRY": {
        "low": "37972",
        "high": "41289",
        "last": "41019",
        "volume": "445.04",
        "daily_change": "2255",
        "daily_change_percentage": "5.81"
    },
    "CNZ-TRY": {
        "low": "0.078402",
        "high": "0.085452",
        "last": "0.084379",
        "volume": "14396298.29",
        "daily_change": "0.005059",
        "daily_change_percentage": "6.37"
    },
    ...
}
```
### Fetch ticker information for BTC-TRY pair
```python
ticker = coinzo.get_ticker("BTC-TRY")
```
```json
{
    "BTC-TRY": {
        "low": "37972",
        "high": "41289",
        "last": "41019",
        "volume": "445.04",
        "daily_change": "2255",
        "daily_change_percentage": "5.81"
    }
}
```
### Fetch market depth (order book info) for HOT-TRY pair
```python
depth = coinzo.get_order_book(pair="HOT-TRY")
```
```json
{
    "asks": [{
        "price": 0.0076643,
        "amount": 67637,
        "count": 1
    }, {
        "price": 0.007704,
        "amount": 112916,
        "count": 1
    },
    ...
    ],
    "bids": [{
        "price": 0.0076311,
        "amount": 129139,
        "count": 1
    }, {
        "price": 0.0076246,
        "amount": 78436,
        "count": 1
    },
    ...
    ],
    "total": {
        "bid": 350621.63142392,
        "ask": 54458830.79696769
    }
}
```

### Fetch latest trades for HOT-TRY pair
```python
trades = coinzo.get_latest_trades(pair="HOT-TRY")
```
```json
[{
    "price": 0.0076221,
    "amount": 33597,
    "side": "BUY",
    "created_at": 1557603438
}, {
    "price": 0.0076235,
    "amount": 27715,
    "side": "SELL",
    "created_at": 1557603378
},
...
]
```

### Place a market buy order
```python
order = coinzo.place_market_buy_order(pair="NEO-TRY", amount="1")
```
```json
{
    "id": "123456789012345678"
}
```

### Place a limit buy order
```python
order = coinzo.place_limit_buy_order(
    pair="NEO-TRY",
    amount="1",
    limit_price="50.01",
)
```
```json
{
    "id": "123456789012345678"
}
```

### Place a stop market buy order
```python
order = coinzo.place_stop_market_buy_order(
    pair="NEO-TRY",
    amount="1",
    stop_price="59.99",
)
```
```json
{
    "id": "123456789012345678"
}
```

### Place a stop limit buy order
```python
order = coinzo.place_stop_limit_buy_order(
    pair="NEO-TRY",
    amount="1",
    limit_price="50.01",
    stop_price="50.99",
)
```
```json
{
    "id": "123456789012345678"
}
```

### Fetch an order
```python
order = coinzo.get_order(order_id="123456789012345678")
```
```json
{
    "id": "123456789012345678",
    "pair": "NEO-TRY",
    "side": "BUY",
    "type": "LIMIT",
    "limit_price": 50.01,
    "stop_price": 0,
    "original_amount": 1,
    "executed_amount": 0,
    "remaining_amount": 1,
    "active": True,
    "cancelled": False,
    "updated_at": 1557604055
}
```

### Fetch all open orders
```python
orders = coinzo.get_open_orders()
```
```json
[{
    "id": "123456789012345678",
    "pair": "NEO-TRY",
    "side": "BUY",
    "type": "LIMIT",
    "limit_price": 50.01,
    "stop_price": 0,
    "original_amount": 1,
    "executed_amount": 0,
    "remaining_amount": 1,
    "active": true,
    "cancelled": false,
    "updated_at": 1557604055
}, {
    "id": "123456789012345678",
    "pair": "HOT-TRY",
    "side": "SELL",
    "type": "LIMIT",
    "limit_price": 0.1,
    "stop_price": 0,
    "original_amount": 100000,
    "executed_amount": 0,
    "remaining_amount": 100000,
    "active": true,
    "cancelled": false,
    "updated_at": 1549109505
},
...
]
```

### Fetch a list of recent fills
```python
fills = coinzo.get_fills()
```
```json
[{
    "id": "123456789012345678",
    "order_id": "12345987630291234",
    "coin": "NEO",
    "fiat": "TRY",
    "side": "BUY",
    "price": 53.383,
    "amount": 30,
    "taker": true,
    "fee": 20.29591797,
    "used_cnz": true,
    "cnz_bonus": 0,
    "created_at": 1557446830
}, {
    "id": "987654321098765432",
    "order_id": "12345987671349876",
    "coin": "CNZ",
    "fiat": "TRY",
    "side": "SELL",
    "price": 0.078907,
    "amount": 20350,
    "taker": true,
    "fee": 3.2115149,
    "used_cnz": false,
    "cnz_bonus": 4.38821466,
    "created_at": 1557446668
}]
```

### Cancel an order
```python
coinzo.cancel_order(order_id="123456789012345678")
```
```json
true
```

### Cancel all open orders
```python
coinzo.cancel_all_orders()
```
```json
true
```

### Fetch a deposit address for BTC
```python
address = coinzo.get_deposit_address(asset="BTC")
```
```json
{
    "asset": "BTC",
    "address": "34cFKPBTaq12NKTNfs4HmhB9876SQDZfoE"
}
```

### Fetch list of deposits

`limit` and `page` are optional, defaults: limit=100, page=1

```python
deposits = coinzo.get_deposit_history(limit=2, page=2)
```
```json
[{
    "id": "123456789012345678",
    "tx_id": "201901011234A567890",
    "asset": "TRY",
    "address": "CZ12345678",
    "amount": 100,
    "confirmations": 1,
    "completed": true,
    "created_at": 1554702411
}, {
    "id": "987654321098765432",
    "tx_id": "abc01de2fabcdefabc345d6e060c15a15364eee8b449eb63e10c6f809d44d987",
    "asset": "EOS",
    "address": "EOS123456789",
    "amount": 10,
    "confirmations": 3,
    "completed": true,
    "created_at": 1553425199
}]
```

### Withdraw 10 EOS
```python
coinzo.withdraw(
    asset="EOS",
    address="EOS123456789",
    amount="10",
    memo="EOS6Uabc1Ggua2stBtyqxiKxyzzVSdZSXYCFwZ9AB35cDefECxyzm",
)
```
```json
{
    "amount": 10,
    "asset": "EOS",
    "id": "450693154343354369"
}
```

### Fetch list of withdrawals

`limit` and `page` are optional, defaults: limit=100, page=1

```python
withdrawals = coinzo.get_withdrawal_history(limit=1, page=3)
```
```json
[
  {
    "id": "321425023135652252",
    "tx_id": "95DD0893F9B2F0CBFEACDAF11672BAFC5BE1F097F450CD51F0420B44D81BF3C1",
    "asset": "XRP",
    "address": "rDQGVYCKC3StBmJV6my9uL1Dn9q7TzEGqS:964641378",
    "amount": 19,
    "status": 1,
    "created_at": 1529758242
  }
]
```

