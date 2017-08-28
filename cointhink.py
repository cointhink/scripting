from google.protobuf.json_format import MessageToJson
import algolog_pb2
import rpc_pb2
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def init(_auth, _ws):
    global auth, ws
    ws = _ws
    auth = _auth
    logger.info("init")

def on_message(msg):
    logger.info(msg)

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
