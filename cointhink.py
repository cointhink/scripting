import sys
import logging
from google.protobuf.json_format import MessageToJson, Parse
from proto import algolog_pb2, tick_tock_pb2, trade_signal_pb2
from proto import notify_pb2, rpc_pb2, market_prices_pb2
import json
import datetime
import websocket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def init(_auth, _ws, _settings):
    global auth, ws, settings
    ws = _ws
    auth = _auth
    settings = _settings
    log('init '+auth['AlgorunId'])
    import script
    if hasattr(script, 'init'):
        script.init(sys.modules[__name__])
    else:
        log('warning: script has no init(cointhink) method')
def on_message(msg):
    logger.info("recv %s", msg)
    if msg['method'] == 'TickTock':
        pb_json = json.dumps(msg['object'])
        ticktock = tick_tock_pb2.TickTock()
        Parse(pb_json, ticktock)
        ttime = datetime.datetime.strptime(ticktock.Time, "%Y-%m-%dT%H:%M:%SZ")
        if hasattr(script, 'each_day'):
            script.each_day(sys.modules[__name__], ttime)
    if msg['method'] == 'MarketPrices':
        pb_json = json.dumps(msg['object'])
        prices = market_prices_pb2.MarketPrices()
        Parse(pb_json, prices)
        if hasattr(script, 'market_prices'):
            script.market_prices(sys.modules[__name__], prices)

def log(msg):
    global auth
    logger.info("log: "+msg)
    if 'auth' in globals():
        alog = algolog_pb2.Algolog()
        alog.AlgorunId = auth['AlgorunId']
        alog.Event = 'start'
        alog.Level = 'info'
        alog.Message = msg
        rpc("Algolog", alog)
    else:
        logger.info("cointhink.log aborted. no auth data")

def rpc(method, payload):
    rpc = rpc_pb2.Rpc()
    rpc.Token = auth['Token']
    rpc.Method = method
    rpc.Object.Pack(payload)
    json_msg = MessageToJson(rpc)
    logger.info("RPC %s", json.dumps(json.loads(json_msg), separators=(',', ':')))
    send(json_msg)

def send(json_msg):
    try:
        ws.send(json_msg)
    except websocket.WebSocketException as e:
        logger.error("### cointhink.py: ws.send aborted: "+str(e)+" for "+json_msg)

def trade():
    trade = trade_signal_pb2.TradeSignal()
    trade.Market = "BTC/USD"
    log("trade() "+str(trade))
    rpc("TradeSignal", trade)

def notify(summary, detail=None):
    summary = str(summary)
    notify = notify_pb2.Notify()
    notify.Summary = summary
    if detail:
        notify.Detail = detail
    log("notify: "+summary)
    rpc("Notify", notify)
