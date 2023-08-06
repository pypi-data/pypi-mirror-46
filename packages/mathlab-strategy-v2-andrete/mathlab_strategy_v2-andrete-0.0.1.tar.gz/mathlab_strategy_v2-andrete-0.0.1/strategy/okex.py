#!/usr/bin/env python

# WS client example

import asyncio
import base64
import hmac
import json
import os
import sys
import threading
import time
import zlib
import aiohttp
import requests
import websockets
import datetime

from .trade_tool import TradeTool
from .utf8logger import INFO, WARN


def print_during_input(string):
    sys.stdout.write(
        # Save cursor position
        "\N{ESC}7"
        # Add a new line
        "\N{LINE FEED}"
        # Move cursor up
        "\N{ESC}[A"
        # Insert blank line, scroll last line down
        "\N{ESC}[L"
        # Print string in the inserted blank line
        f"{string}\N{LINE FEED}"
        # Restore cursor position
        "\N{ESC}8"
        # Move cursor down
        "\N{ESC}[B"
    )
    sys.stdout.flush()

class OKEx():
    def __init__(self, loop, strategy, pair):
        self.loop = loop
        self.instrument_id = None
        # self.key = '1957674e-8d18-4c24-bd35-8c80fbaebccf'
        # self.secret = 'C1F9D221E1AC8D990CD08C8B67CA5746'
        self.key = 'e3df3679-409b-42d7-b7f7-22f834a6c9cb'
        self.secret = 'AB300727C16C38BAFEF4B35DA0DA92CC'
        self.passphrase = 'Lol2018'
        self.host = 'https://www.okex.com'
        self.CONTENT_TYPE = 'Content-TYPE'
        self.OK_ACCESS_KEY = 'OK-ACCESS-KEY'
        self.OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
        self.OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
        self.OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
        self.APPLICATION_JSON = 'application/json'
        self.bid = None
        self.ask = None
        self.strategy = strategy
        self.pair = pair
        self.OKEX_PAIR_MAP = {
            'ETHUSD': {
                'underlying_index': 'ETH',
                'quote_currency': 'USD',
            },
            'BTCUSD': {
                'underlying_index': 'BTC',
                'quote_currency': 'USD',
            },
            'EOSUSD': {
                'underlying_index': 'EOS',
                'quote_currency': 'USD',
            },
            'XRPUSD': {
                'underlying_index': 'XRP',
                'quote_currency': 'USD',
            },
            'LTCUSD': {
                'underlying_index': 'LTC',
                'quote_currency': 'USD',
            },
            'ETCUSD': {
                'underlying_index': 'ETC',
                'quote_currency': 'USD',
            },
        }

    def inflate(self, data):
        decompress = zlib.decompressobj(
                -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated.decode('utf8')

    def signature(self, timestamp, method, request_path, body):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(self.secret, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d).decode('utf8')

    def get_header(self, sign, timestamp):
        header = dict()
        header[self.CONTENT_TYPE] = self.APPLICATION_JSON
        header[self.OK_ACCESS_KEY] = self.key
        header[self.OK_ACCESS_SIGN] = sign
        header[self.OK_ACCESS_TIMESTAMP] = str(timestamp)
        header[self.OK_ACCESS_PASSPHRASE] = self.passphrase
        return header

    async def __aenter__(self):
        self._conn = websockets.connect('wss://real.okex.com:10442/ws/v3')
        self.websocket = await self._conn.__aenter__()
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def send(self, message):
        print_during_input("< " + message)
        await self.websocket.send(message)

    async def receive(self):
        received = await self.websocket.recv()
        return self.inflate(received)

    async def login(self):
        timestamp = '%.3f' % time.time()
        login = {'op': 'login', 'args': [self.key, self.passphrase, timestamp, self.signature(timestamp, 'GET', '/users/self/verify', '')]}
        await self.send(json.dumps(login))

    async def subscribe(self):
        self.instrument_id = self.get_latest_future_instrument_id(self.pair)
        INFO("subscribe instrument id: {}".format(self.instrument_id))
        subscribe = {
            'op': 'subscribe',
            'args': [
                'futures/ticker:' + self.instrument_id,
                'futures/position:' + self.instrument_id,
                'futures/account:' + self.OKEX_PAIR_MAP[self.pair]['underlying_index'],
                'futures/order:' + self.instrument_id,
                'spot/account:' + self.OKEX_PAIR_MAP[self.pair]['underlying_index']
            ]
        }
        await self.send(json.dumps(subscribe))

    async def request(self, path, req={}, method='get'):
        timestamp = '%.3f' % time.time()
        data_str = ""
        if req:
            url = '?'
            for key, value in req.items():
                url = url + str(key) + '=' + str(value) + '&'
            path += url[0: -1]
            data_str = json.dumps(req)
        urlpath = os.path.join(self.host, path)
        if method == "get":
            header = self.get_header(self.signature(timestamp, 'GET', '/' + path, data_str), timestamp)
            r = await self.session.get(urlpath, headers=header)
        elif method == 'post':
            header = self.get_header(self.signature(timestamp, 'POST', '/' + path, data_str), timestamp)
            r = await self.session.post(urlpath, data=data_str, headers=header)
        return await r.json()

    def parseTicker(self, data):
        if 'best_bid' in data and self.bid != data['best_bid']:
            self.bid = data['best_bid']
        if 'best_ask' in data and self.ask != data['best_ask']:
            self.ask = data['best_ask']

    def get_latest_future_instrument_id(self, pair):
        while 1:
            try:
                response = requests.get('https://www.okex.com/api/futures/v3/instruments', timeout=3)
                instruments = response.json()
                break
            except Exception as e:
                WARN('OKEX instruments request timeout' + str(e))
                continue
        future_delivery_date = ''
        future_instrument_id = ''
        for instrument in instruments:
            if instrument['underlying_index'] == self.OKEX_PAIR_MAP[pair]['underlying_index'] and \
                    instrument['quote_currency'] == self.OKEX_PAIR_MAP[pair]['quote_currency']:
                listing = instrument['listing'].split('-')
                delivery = instrument['delivery'].split('-')
                listing_date = datetime.datetime(int(listing[0]), int(listing[1]), int(listing[2]))
                delivery_date = datetime.datetime(int(delivery[0]), int(delivery[1]), int(delivery[2]))
                if (delivery_date - listing_date).days < 90:
                    continue
                if (not future_delivery_date) or int(time.mktime(delivery_date.timetuple())) > int(time.mktime(time.strptime(future_delivery_date, "%Y-%m-%d"))):
                    future_instrument_id = instrument['instrument_id']
        return future_instrument_id

    async def getWallet(self):
        r = await self.request(path = 'api/spot/v3/accounts/' + self.OKEX_PAIR_MAP[self.pair]['underlying_index'] + '/ledger')
        print_during_input(r)

    async def getPosition(self):
        self.instrument_id = self.get_latest_future_instrument_id(self.pair)
        r = await self.request(path = 'api/futures/v3/{0}/position'.format(self.instrument_id))
        print_during_input(r)
        if r['holding']:
            self.parsePosition(r['holding'][0])

    def parsePosition(self, data):
        if 'long_avail_qty' in data:
            self.strategy.setLongAvailQty(data['long_avail_qty'])
        if 'short_avail_qty' in data:
            self.strategy.setShortAvailQty(data['short_avail_qty'])
        if 'long_qty' in data:
            self.strategy.setLongQty(data['long_qty'])
        if 'short_qty' in data:
            self.strategy.setShortQty(data['short_qty'])

    def parseOrder(self, data):
        order_status = int(data["status"])
        order_id = data["order_id"]
        prefix = "type {0}, order_id {1},".format(data["type"], order_id)
        self.strategy.setOrderStatus(order_status, order_id)
        if order_status == 0:
            INFO(prefix + " order committed")
        elif order_status == 2:
            INFO(prefix + " order completed")
        else:
            INFO(prefix + " do nothing, status {0}".format(order_status))

    async def parse(self, message):
        body = json.loads(message)
        if 'event' in body:
            if 'login' == body['event'] and body['success']:
                asyncio.ensure_future(self.subscribe(), loop = self.loop)
            print_during_input("> " + message)
        elif 'table' in body:
            if 'futures/ticker' == body['table']:
                for item in body['data']:
                    self.parseTicker(item)
            if 'futures/position' == body['table']:
                self.parsePosition(body['data'][0])
                print_during_input("> " + message)
            if 'futures/order' == body['table']:
                for item in body['data']:
                    self.parseOrder(item)
                print_during_input("> " + message)
        else:
            print_during_input(f'Unknown message {message}')

    async def placeMakerOrder(self, side, vol):
        if side in [2, 3]:
            price = self.ask
        elif side in [1, 4]:
            price = self.bid
        r = await self.request('api/futures/v3/order', req={'instrument_id': self.instrument_id, 'type': side, 'price': price, 'size': vol, 'leverage': 20}, method='post')
        print_during_input(r)
        return r

    async def placeTakerOrder(self, side, vol):
        if side in [1, 4]:
            price = self.ask
        elif side in [2, 3]:
            price = self.bid
        r = await self.request('api/futures/v3/order', req={'instrument_id': self.instrument_id, 'type': side, 'price': price, 'size': vol, 'leverage': 20}, method='post')
        print_during_input(r)
        return r

    async def cancelOrder(self, oid):
        r = await self.request(
            'api/futures/v3/cancel_order/{0}/{1}'.format(self.instrument_id, oid),
            req={},
            method='post'
        )
        print_during_input(r)
        return r

async def runClient(loop, inputs, stop, strategy, pair="ETHUSD"):
    async with OKEx(loop, strategy, pair) as ex:
        asyncio.ensure_future(ex.login())
        asyncio.ensure_future(ex.getPosition())
        # asyncio.ensure_future(ex.getWallet())

        while True:
            incoming = asyncio.ensure_future(ex.receive(), loop=loop)
            outgoing = asyncio.ensure_future(inputs.get(), loop=loop)
            done, pending = await asyncio.wait(
                [incoming, outgoing, stop], return_when=asyncio.FIRST_COMPLETED
            )

            if incoming in pending:
                incoming.cancel()
            if outgoing in pending:
                outgoing.cancel()

            if incoming in done:
                try:
                    message = incoming.result()
                    asyncio.ensure_future(ex.parse(message), loop=loop)
                except Exception as e:
                    print_during_input(e)
                    break

            if outgoing in done:
                para_1, means, para_2 = outgoing.result()
                if means == "taker":
                    asyncio.ensure_future(ex.placeTakerOrder(para_1, para_2), loop=loop)
                elif means == "maker":
                    asyncio.ensure_future(ex.placeMakerOrder(para_1, para_2), loop=loop)
                elif means == "cancel":
                    asyncio.ensure_future(ex.cancelOrder(para_1), loop=loop)

            if stop in done:
                break
        print_during_input('Client Shutdown!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    inputs = asyncio.Queue(loop=loop)
    stop = loop.create_future()
    strategy = TradeTool(loop, inputs)
    asyncio.ensure_future(runClient(loop, inputs, stop, strategy), loop=loop)
    thread = threading.Thread(target=loop.run_forever)
    thread.start()
    try:
        while True:
            # Since there's no size limit, put_nowait is identical to put.
            message = input("> ")
            if message == 'open long':
                side = 1
            elif message == 'open short':
                side = 2
            elif message == 'close long':
                side = 3
            elif message == 'close short':
                side = 4
            else:
                continue
            loop.call_soon_threadsafe(inputs.put_nowait, (side, "taker", 1))
    except (KeyboardInterrupt, EOFError):  # ^C, ^D
        loop.call_soon_threadsafe(stop.set_result, None)
