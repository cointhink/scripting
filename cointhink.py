import sys
import logging
from google.protobuf.json_format import MessageToJson, Parse
import algolog_pb2
import tick_tock_pb2
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
    logger.info("init %s", auth['AlgorunId'])
    script.init(sys.modules[__name__])

def on_message(msg):
    logger.info(msg)
    if msg['method'] == 'TickTock':
        pb_json = json.dumps(msg['object'])
        ticktock = tick_tock_pb2.TickTock()
        Parse(pb_json, ticktock)
        ttime = datetime.datetime.strptime(ticktock.Time, "%Y-%m-%dT%H:%M:%SZ")
        script.eachDay(sys.modules[__name__], ttime)

def log(msg):
    logger.info("### log ###")
    alog = algolog_pb2.Algolog()
    logger.info(auth)
    alog.AlgorunId = auth['AlgorunId']
    alog.Event = 'start'
    alog.Level = 'info'
    alog.Message = msg
    rpc = rpc_pb2.Rpc()
    rpc.Token = auth['Token']
    rpc.Method = "Algolog"
    rpc.Object.Pack(alog)
    json_msg = MessageToJson(rpc)
    logger.info(json_msg)
    ws.send(json_msg)
