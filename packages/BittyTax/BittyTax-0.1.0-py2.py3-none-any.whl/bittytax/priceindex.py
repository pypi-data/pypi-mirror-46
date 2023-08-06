#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) Nano Nano Ltd 2018
# $Id: priceindex.py,v 1.1.1.1 2019/02/18 23:07:13 scottgreen Exp $

import os
import sys
import argparse
import datetime
import pickle
from decimal import Decimal

import requests
import dateutil.parser

from .config import log, config

BTC = "BTC"
GBP = "GBP"

COINDESK = True
prices = {}

def _symbol(asset):
    if asset in config.FIAT_LIST or asset == BTC:
        return u'£'
    return u'฿'

def _get_price(asset, timestamp):
    if asset not in prices:
        prices[asset] = {}

    k = timestamp.strftime('%Y-%m-%d')

    if k in prices[asset]:
        if prices[asset][k] is not None:
            log.debug("Price on %s, 1 %s=%s%s", k, asset, _symbol(asset), str(prices[asset][k]))
        else:
            log.debug("Price (%s) for %s is not available", asset, k)

        return prices[asset][k]
    else:
        if asset == BTC and COINDESK:
            prices[asset].update(_get_historical_data_coindesk(asset, timestamp))
        elif asset in config.FIAT_LIST:
            prices[asset].update(_get_historical_data_ratesapi(asset, timestamp))
        else:
            prices[asset].update(_get_historical_data_cryptocompare(asset, timestamp))

        if k not in prices[asset] or prices[asset][k] is None:
            prices[asset].update(_get_historical_data_coingecko(asset, timestamp))

        if k in prices[asset]:
            if prices[asset][k] is not None:
                log.debug("Price on %s, 1 %s=%s%s", k, asset, _symbol(asset), str(prices[asset][k]))
            else:
                log.debug("Price (%s) for %s is not available", asset, k)

            return prices[asset][k]
        else:
            log.debug("Price (%s) for %s is not available", asset, k)
            return None

def get_value_gbp(asset, timestamp, amount):
    if asset == GBP:
        price = 1
    elif asset == BTC or asset in config.FIAT_LIST:
        price = _get_price(asset, timestamp)
    else:
        price_btc = _get_price(BTC, timestamp)
        if price_btc is not None:
            price = _get_price(asset, timestamp)
            if price is not None:
                price = price_btc * price

    if price is not None:
        price = amount * price

    return price

def get_value(asset, timestamp, quantity, value_gbp):
    price = get_value_gbp(asset, timestamp, quantity)

    if value_gbp is None:
        # Don't overwrite if fixed price
        value_gbp = price
    else:
        if price is None:
            log.warning("Using fixed GBP value: £%s", '{:0,.2f}'.format(value_gbp))
        else:
            log.warning("Using fixed GBP value: £" + '{:0,.2f}'.format(value_gbp) + ", not price index (£" + '{:0,.2f}'.format(price) + ")")

    if value_gbp is None:
        log.warning("Value is not available, default to £0.00")
        value_gbp = Decimal(0)

    return value_gbp

def _get_historical_data_ratesapi(asset, timestamp):
    url = (
        'https://ratesapi.io/api/{}'
        '?base={}&symbols=GBP'.format(
            timestamp.strftime('%Y-%m-%d'), asset
        )
    )

    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    if data['rates']['GBP']:
        prices[asset][timestamp.strftime('%Y-%m-%d')] = Decimal(str(data['rates']['GBP']))
    else:
        prices[asset][timestamp.strftime('%Y-%m-%d')] = None
    return prices


def _get_historical_data_coindesk(asset, start):
    end = datetime.date.today()
    url = (
        'https://api.coindesk.com/v1/bpi/historical/close.json'
        '?start={}&end={}&currency=GBP'.format(
            start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')
        )
    )

    r = requests.get(url)
    r.raise_for_status()

    data = r.json()
    prices = data['bpi']
    prices = {k: Decimal(str(v)) for (k, v) in prices.items()}
    return prices


def _get_historical_data_cryptocompare(asset, end):
    MAX_DAYS = 2000
    prices = {}

    end = end + datetime.timedelta(days=MAX_DAYS)
    url = (
        'https://min-api.cryptocompare.com/data/histoday'
        '?aggregate=1&e=CCCAGG&extraParams=CryptoCompare'
        '&fsym={}&tsym=BTC&limit={}&tryConversion=false&toTs={}'.format(
            asset, MAX_DAYS, end.strftime('%s')
        )
    )
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    for d in data['Data']:
        prices[datetime.datetime.fromtimestamp(d['time']).strftime('%Y-%m-%d')] = Decimal(str(d['close'])) or None

    return prices

def _get_historical_data_coingecko(asset, timestamp):
    url = 'https://api.coingecko.com/api/v3/coins/list'
    r = requests.get(url)
    r.raise_for_status()

    data = r.json()
    id = ''
    for c in data:
        if c['symbol'] == asset.lower():
            id = c['id']
            break

    if id == '':
        log.debug('Id for asset: %s not found', asset)
        prices[asset][timestamp.strftime('%Y-%m-%d')] = None
        return prices

    url = (
        'https://api.coingecko.com/api/v3/coins/{}/history'
        '?date={}&localiztion=false'.format(
            id, timestamp.strftime('%d-%m-%Y')
        )
    )

    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    if 'market_data' in data:
        prices[asset][timestamp.strftime('%Y-%m-%d')] = Decimal(str(data['market_data']['current_price']['btc']))
    else:
        prices[asset][timestamp.strftime('%Y-%m-%d')] = None
    return prices

def dump_price_history_data():
    if not os.path.exists(config.BITTYTAX_PATH):
        os.makedirs(config.BITTYTAX_PATH)

    with open(os.path.join(config.BITTYTAX_PATH, "prices.pickle"), 'wb') as p:
        pickle.dump(prices, p, pickle.HIGHEST_PROTOCOL)

def load_price_history_data():
    global prices
    try:
        with open(os.path.join(config.BITTYTAX_PATH, "prices.pickle"), "rb") as p:
            prices = pickle.load(p)
    except:
        log.debug("Price Index cannot be loaded")
        prices = {}

    for a in sorted(prices):
        log.debug("Price Index loaded for (%s)", a)

def epoch(timestamp):
    epoch = (timestamp - datetime.datetime(1970, 1, 1, tzinfo=config.TZ_UTC)).total_seconds()
    return int(epoch)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("date", type=str, nargs=1, help="Date (YYYY-MM-DD)")
    parser.add_argument("asset", type=str, nargs=1, help="Asset symbol for crypto or fiat (i.e. BTC/LTC/ETH or EUR/USD)")
    parser.add_argument("quantity", type=str, nargs='?', help="Quantity")
    parser.add_argument("-d", "--debug", action='store_true', help="Enabled debug logging")
    config.args = parser.parse_args()

    if config.args.debug:
        config.debug_logging_enable()

    # retrieve price index data if previously run
    prices = load_price_history_data()
    timestamp = dateutil.parser.parse(config.args.date[0])

    if config.args.asset[0] == GBP:
        price = 1
    elif config.args.asset[0] == BTC or config.args.asset[0] in config.FIAT_LIST:
        price = _get_price(config.args.asset[0], timestamp)
    else:
        price_btc = _get_price(BTC, timestamp)
        if price_btc is not None:
            price = _get_price(config.args.asset[0], timestamp)
            if price is not None:
                price = price_btc * price

    if price is not None:
        log.info("1 %s=£%s", config.args.asset[0], '{:0,.2f}'.format(price))
        if config.args.quantity:
            quantity = Decimal(config.args.quantity)
            log.info("%s %s=£%s", str(quantity), config.args.asset[0], '{:0,.2f}'.format(quantity * price))

    dump_price_history_data()
