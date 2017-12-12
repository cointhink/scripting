import sys
import json
import datetime
import websocket
import auth
from google.protobuf.json_format import MessageToJson, Parse
from proto import algolog_pb2, tick_tock_pb2, trade_signal_pb2
from proto import notify_pb2, rpc_pb2, market_prices_pb2, heartbeat_pb2
from proto import lambda_pb2, lambda_response_pb2

def init(_credential, _ws, _settings):
    global settings
    settings = _settings
    auth.init(_credential, _ws, sys.modules[__name__])

def heartbeat():
    beat = heartbeat_pb2.Heartbeat()
    auth.rpc(auth.credential['Token'], "Heartbeat", beat)

def on_message(msg):
    pb_json = json.dumps(msg['object'])
    if msg['method'] == 'Lambda':
        _lambda = lambda_pb2.Lambda()
        Parse(pb_json, _lambda)
        settings_json = auth.lambda_dispatch(_lambda)
        _lambdar = lambda_response_pb2.LambdaResponse()
        _lambdar.StateOut = settings_json
        _lambdar.Token = _lambda.Token
        auth.rpc(auth.credential['Token'], "LambdaResponse", _lambdar)
    if msg['method'] == 'TickTock':
        ticktock = tick_tock_pb2.TickTock()
        Parse(pb_json, ticktock)
        ttime = datetime.datetime.strptime(ticktock.Time, "%Y-%m-%dT%H:%M:%SZ")
        if hasattr(auth.script, 'each_day'):
            auth.script.each_day(sys.modules[__name__], ttime)
    if msg['method'] == 'MarketPrices':
        prices = market_prices_pb2.MarketPrices()
        Parse(pb_json, prices)
        if hasattr(auth.script, 'market_prices'):
            auth.script.market_prices(sys.modules[__name__], prices)

def log(msg):
    if auth.credential:
        auth.log(auth.credential['Token'], msg)
    else:
        auth.logger.info("cointhink.log aborted. no auth.credential data.")

def trade():
    trade = trade_signal_pb2.TradeSignal()
    trade.Market = "BTC/USD"
    log("trade() "+str(trade))
    auth.rpc(auth.credential['Token'], "TradeSignal", trade)

def notify(summary, detail=None):
    summary = str(summary)
    notify = notify_pb2.Notify()
    notify.Summary = summary
    if detail:
        notify.Detail = detail
    log("notify: "+summary)
    auth.rpc(auth.credential['Token'], "Notify", notify)
