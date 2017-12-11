import sys
from google.protobuf.json_format import MessageToJson, Parse
from proto import algolog_pb2, tick_tock_pb2, trade_signal_pb2
from proto import notify_pb2, rpc_pb2, market_prices_pb2, heartbeat_pb2
from proto import lambda_pb2
import json
import datetime
import websocket
import auth

def init(_credential, _ws, _settings):
    global settings
    settings = _settings
    auth.init(_credential, _ws, sys.modules[__name__])

def heartbeat():
    beat = heartbeat_pb2.Heartbeat()
    auth.rpc(auth.credential['Token'], "Heartbeat", beat)

def on_message(msg):
    auth.logger.info("recv %s", msg)
    pb_json = json.dumps(msg['object'])
    if msg['method'] == 'Lambda':
        _lambda = lambda_pb2.Lambda()
        lambda_dispatch(_lambda)

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

def lambda_dispatch(_lambda):
    #pb_json = json.dumps(_lambda.Object)
    pb_json = MessageToJson(_lambda.Object)
    if _lambda.Method == "MarketPrices":
        prices = market_prices_pb2.MarketPrices()
        Parse(pb_json, prices)
        auth.script.market_prices_auth.credential(_lambda.Token, sys.modules[__name__], prices)

def log(msg):
    auth.logger.info("log: "+msg)
    if auth.credential:
        alog = algolog_pb2.Algolog()
        alog.AlgorunId = auth.credential['AlgorunId']
        alog.Event = 'start'
        alog.Level = 'info'
        alog.Message = msg
        auth.rpc(auth.credential['Token'], "Algolog", alog)
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
