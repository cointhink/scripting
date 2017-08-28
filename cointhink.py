import sys
import logging
from google.protobuf.json_format import MessageToJson
import algolog_pb2
import rpc_pb2
import script

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
        script.eachMinute(sys.modules[__name__])

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
