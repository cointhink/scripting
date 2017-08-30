import sys
import logging
from google.protobuf.json_format import MessageToJson, Parse
import algolog_pb2
import tick_tock_pb2
import trade_signal_pb2
import rpc_pb2
import script
import json
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def init(_auth, _ws):
    global auth, ws
    ws = _ws
    auth = _auth
    log('init '+auth['AlgorunId'])
    script.init(sys.modules[__name__])

def on_message(msg):
    logger.info("recv %s", msg)
    if msg['method'] == 'TickTock':
        pb_json = json.dumps(msg['object'])
        ticktock = tick_tock_pb2.TickTock()
        Parse(pb_json, ticktock)
        ttime = datetime.datetime.strptime(ticktock.Time, "%Y-%m-%dT%H:%M:%SZ")
        script.eachDay(sys.modules[__name__], ttime)

def log(msg):
    logger.info("log: "+msg)
    alog = algolog_pb2.Algolog()
    logger.info(auth)
    alog.AlgorunId = auth['AlgorunId']
    alog.Event = 'start'
    alog.Level = 'info'
    alog.Message = msg
    rpc("Algolog", alog)

def rpc(method, payload):
    rpc = rpc_pb2.Rpc()
    rpc.Token = auth['Token']
    rpc.Method = method
    rpc.Object.Pack(payload)
    json_msg = MessageToJson(rpc)
    logger.info("RPC %s", json.dumps(json.loads(json_msg), separators=(',', ':')))
    ws.send(json_msg)

def trade():
    trade = trade_signal_pb2.TradeSignal()
    trade.Market = "BTC/USD"
    log("trade() "+str(trade))
    rpc("TradeSignal", trade)

