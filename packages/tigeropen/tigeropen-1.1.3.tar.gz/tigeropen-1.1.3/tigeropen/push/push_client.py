# -*- coding: utf-8 -*-
"""
Created on 2018/10/30

@author: gaoan
"""
import sys
import json
import stomp
import six
import traceback
import logging
from stomp.exception import ConnectFailedException
from tigeropen.common.util.signature_utils import sign_with_rsa
from tigeropen.common.util.order_utils import get_order_status
from tigeropen.common.consts.push_types import RequestType, ResponseType
from tigeropen.common.consts.quote_keys import QuoteChangeKey

QUOTE_KEYS_MAPPINGS = {field.value: field.name for field in QuoteChangeKey}  # like {'askPrice': 'ask_price'}
REVERSED_QUOTE_KEYS_MAPPINGS = {field.name: field.value for field in QuoteChangeKey}  # like {'ask_price': 'askPrice'}

ASSET_KEYS_MAPPINGS = {'buyingPower': 'buying_power', 'cashBalance': 'cash',
                       'grossPositionValue': 'gross_position_value',
                       'netLiquidation': 'net_liquidation', 'equityWithLoan': 'equity_with_loan',
                       'initMarginReq': 'initial_margin_requirement',
                       'maintMarginReq': 'maintenance_margin_requirement',
                       'availableFunds': 'available_funds', 'excessLiquidity': 'excess_liquidity',
                       'dayTradesRemaining': 'day_trades_remaining', 'currency': 'currency'}

POSITION_KEYS_MAPPINGS = {'averageCost': 'average_cost', 'position': 'quantity', 'latestPrice': 'market_price',
                          'marketValue': 'market_value', 'orderType': 'order_type', 'realizedPnl': 'realized_pnl',
                          'unrealizedPnl': 'unrealized_pnl', 'secType': 'sec_type', 'localSymbol': 'local_symbol',
                          'originSymbol': 'origin_symbol', 'contractId': 'contract_id', 'symbol': 'symbol',
                          'currency': 'currency', 'strike': 'strike', 'expiry': 'expiry', 'right': 'right'}

ORDER_KEYS_MAPPINGS = {'parentId': 'parent_id', 'orderId': 'order_id', 'orderType': 'order_type',
                       'limitPrice': 'limit_price', 'auxPrice': 'aux_price', 'avgFillPrice': 'avg_fill_price',
                       'totalQuantity': 'quantity', 'filledQuantity': 'filled', 'lastFillPrice': 'last_fill_price',
                       'realizedPnl': 'realized_pnl', 'secType': 'sec_type',
                       'remark': 'reason', 'localSymbol': 'local_symbol', 'originSymbol': 'origin_symbol',
                       'outsideRth': 'outside_rth', 'timeInForce': 'time_in_force', 'openTime': 'order_time',
                       'latestTime': 'trade_time', 'contractId': 'contract_id', 'trailStopPrice': 'trail_stop_price',
                       'trailingPercent': 'trailing_percent', 'percentOffset': 'percent_offset', 'action': 'action',
                       'status': 'status', 'currency': 'currency', 'remaining': 'remaining', 'id': 'id'}

if sys.platform == 'linux' or sys.platform == 'linux2':
    KEEPALIVE = True
else:
    KEEPALIVE = False


class PushClient(object):
    def __init__(self, host, port, use_ssl=True, connection_timeout=120, auto_reconnect=True):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.stomp_connection = None
        self.counter = 0
        self.subscriptions = {}  # subscription callbacks indexed by subscriber's ID

        self.tiger_id = None
        self.sign = None

        self.subscribed_symbols = None
        self.quote_changed = None
        self.asset_changed = None
        self.position_changed = None
        self.order_changed = None
        self.connect_callback = None
        self.disconnect_callback = None
        self.error_callback = None
        self._connection_timeout = connection_timeout
        self._auto_reconnect = auto_reconnect

    def _connect(self):
        try:
            if self.stomp_connection:
                self.stomp_connection.remove_listener('push')
                self.stomp_connection.transport.cleanup()
        except:
            pass

        self.stomp_connection = stomp.Connection10(host_and_ports=[(self.host, self.port), ], use_ssl=self.use_ssl,
                                                   keepalive=KEEPALIVE, timeout=self._connection_timeout)
        self.stomp_connection.set_listener('push', self)
        self.stomp_connection.start()
        try:
            self.stomp_connection.connect(self.tiger_id, self.sign, wait=True)
        except ConnectFailedException:
            logging.warning('Stomp connection failed')

    def connect(self, tiger_id, private_key):
        self.tiger_id = tiger_id
        self.sign = sign_with_rsa(private_key, tiger_id, 'utf-8')
        self._connect()

    def disconnect(self):
        if self.stomp_connection:
            self.stomp_connection.disconnect()

    def on_connected(self, headers, body):
        if self.connect_callback:
            self.connect_callback()

    def on_disconnected(self):
        if self.disconnect_callback:
            self.disconnect_callback()
        elif self._auto_reconnect:
            self._connect()

    def on_message(self, headers, body):
        """
        Called by the STOMP connection when a MESSAGE frame is received.

        :param dict headers: a dictionary containing all headers sent by the server as key/value pairs.
        :param body: the frame's payload - the message body.
        """
        try:
            response_type = headers.get('ret-type')
            if response_type == str(ResponseType.GET_SUB_SYMBOLS_END.value):
                if self.subscribed_symbols:
                    data = json.loads(body)
                    limit = data.get('limit')
                    symbols = data.get('subscribedSymbols')
                    used = data.get('used')
                    symbol_focus_keys = data.get('symbolFocusKeys')
                    focus_keys = dict()
                    for sym, keys in symbol_focus_keys.items():
                        keys = [QUOTE_KEYS_MAPPINGS.get(key, key) for key in keys]
                        focus_keys[sym] = keys
                    self.subscribed_symbols(symbols, focus_keys, limit, used)
            elif response_type == str(ResponseType.GET_QUOTE_CHANGE_END.value):
                if self.quote_changed:
                    data = json.loads(body)
                    hour_trading = False
                    if 'hourTradingLatestPrice' in data:
                        hour_trading = True
                    if 'symbol' in data:
                        symbol = data.get('symbol')
                        items = []
                        for key, value in data.items():
                            if key.startswith('hourTrading'):
                                key = key[11:]
                            if key == 'latestTime' and isinstance(value, six.string_types):
                                continue
                            if key in QUOTE_KEYS_MAPPINGS:
                                items.append((QUOTE_KEYS_MAPPINGS.get(key), value))
                        if items:
                            self.quote_changed(symbol, items, hour_trading)
            elif response_type == str(ResponseType.SUBSCRIBE_ASSET.value):
                if self.asset_changed:
                    data = json.loads(body)
                    if 'account' in data:
                        account = data.get('account')
                        items = []
                        for key, value in data.items():
                            if key in ASSET_KEYS_MAPPINGS:
                                items.append((ASSET_KEYS_MAPPINGS.get(key), value))
                        if items:
                            self.asset_changed(account, items)
            elif response_type == str(ResponseType.SUBSCRIBE_POSITION.value):
                if self.position_changed:
                    data = json.loads(body)
                    if 'account' in data:
                        account = data.get('account')
                        items = []
                        for key, value in data.items():
                            if key in POSITION_KEYS_MAPPINGS:
                                items.append((POSITION_KEYS_MAPPINGS.get(key), value))
                        if items:
                            self.position_changed(account, items)
            elif response_type == str(ResponseType.SUBSCRIBE_ORDER_STATUS.value):
                if self.order_changed:
                    data = json.loads(body)
                    if 'account' in data:
                        account = data.get('account')
                        items = []
                        for key, value in data.items():
                            if key in ORDER_KEYS_MAPPINGS:
                                if key == 'status':
                                    value = get_order_status(value)
                                items.append((ORDER_KEYS_MAPPINGS.get(key), value))
                        if items:
                            self.order_changed(account, items)
        except Exception as e:
            print(traceback.format_exc())

    def on_error(self, headers, body):
        pass

    def subscribe_asset(self, account=None):
        """
        订阅账户资产更新
        :return:
        """
        id = "sub-" + str(self.counter)
        headers = dict()
        headers['destination'] = 'trade/asset'
        headers['subscription'] = 'Asset'
        headers['id'] = id
        self.counter += 1

        self.stomp_connection.subscribe('trade/asset', id=id, headers=headers)

        return id

    def unsubscribe_asset(self, id=None, account=None):
        """
        退订账户资产更新
        :return:
        """
        headers = dict()
        headers['destination'] = 'trade/asset'
        headers['subscription'] = 'Asset'
        if id:
            headers['id'] = id
        self.stomp_connection.subscribe('trade/asset', id=id, headers=headers)

    def subscribe_position(self, account=None):
        """
        订阅账户持仓更新
        :return:
        """
        id = "sub-" + str(self.counter)
        headers = dict()
        headers['destination'] = 'trade/position'
        headers['subscription'] = 'Position'
        headers['id'] = id
        self.counter += 1

        self.stomp_connection.subscribe('trade/position', id=id, headers=headers)

    def unsubscribe_position(self, id=None, account=None):
        """
        退订账户持仓更新
        :return:
        """
        headers = dict()
        headers['destination'] = 'trade/position'
        headers['subscription'] = 'Position'
        if id:
            headers['id'] = id

        self.stomp_connection.subscribe('trade/position', id=id, headers=headers)

    def subscribe_order(self):
        """
        订阅账户订单更新
        :return:
        """
        id = "sub-" + str(self.counter)
        headers = dict()
        headers['destination'] = 'trade/order'
        headers['subscription'] = 'OrderStatus'
        headers['id'] = id
        self.counter += 1

        self.stomp_connection.subscribe('trade/order', id=id, headers=headers)

    def unsubscribe_order(self, id=None, account=None):
        """
        退订账户订单更新
        :return:
        """
        headers = dict()
        headers['destination'] = 'trade/order'
        headers['subscription'] = 'OrderStatus'
        if id:
            headers['id'] = id

        self.stomp_connection.unsubscribe('trade/order', id=id, headers=headers)

    def subscribe_quote(self, symbols, focus_keys=None):
        """
        订阅行情更新
        :return:
        """
        id = "sub-" + str(self.counter)
        headers = dict()
        headers['destination'] = 'quote'
        headers['subscription'] = 'Quote'
        headers['id'] = id
        if symbols:
            headers['symbols'] = ','.join(symbols)
        if focus_keys:
            keys = list()
            for key in focus_keys:
                if isinstance(key, str):
                    key = REVERSED_QUOTE_KEYS_MAPPINGS.get(key, key)
                    keys.append(key)
                else:
                    keys.append(key.value)
            headers['keys'] = ','.join(keys)
        self.counter += 1

        self.stomp_connection.subscribe('quote', id=id, headers=headers)

    def query_subscribed_quote(self):
        """
        查询已订阅行情的合约
        :return:
        """
        headers = dict()
        headers['destination'] = 'quote'
        headers['req-type'] = RequestType.REQ_SUB_SYMBOLS.value
        self.stomp_connection.send('quote', "{}", headers=headers)

    def unsubscribe_quote(self, symbols=None, id=None):
        """
        退订行情更新
        :return:
        """
        headers = dict()
        headers['destination'] = 'quote'
        headers['subscription'] = 'Quote'
        if id:
            headers['id'] = id
        if symbols:
            headers['symbols'] = ','.join(symbols)

        self.stomp_connection.unsubscribe('quote', id=id, headers=headers)
