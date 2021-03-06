import sys
import logging
import json
import datetime
from google.protobuf.json_format import MessageToJson, Parse
from proto import rpc_pb2, algolog_pb2, market_prices_pb2, lambda_response_pb2
from proto import notify_pb2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def init(_credential, _ws, module):
    global credential, ws, script
    ws = _ws
    credential = _credential
    log(credential['Token'], 'init '+credential['AlgorunId'])
    import script
    if hasattr(script, 'init'):
        script.init(module)
    else:
        log('warning: script has no init(cointhink) method')

def lambda_dispatch(_lambda):
    logger.info("lambda_dispatch %s", _lambda.Method)
    settings = json.loads(_lambda.StateIn)
    pb_json = MessageToJson(_lambda.Object)
    if _lambda.Method == "MarketPrices":
        logger.info("lambda_dispatch MarketPrices pb json %s", pb_json)
        gprices = json.loads(pb_json)
        gprices.pop('@type')
        pb2_json = json.dumps(gprices)
        logger.info("lambda_dispatch MarketPrices pb2 json %s", pb2_json)
        prices = market_prices_pb2.MarketPrices()
        Parse(pb2_json, prices)
        if hasattr(script, 'market_prices_auth'):
            script.market_prices_auth(_lambda.Token, settings, sys.modules[__name__], prices)
    return json.dumps(settings)

def rpc(token, method, payload):
    global logger
    rpc = rpc_pb2.Rpc()
    rpc.Token = token
    rpc.Method = method
    rpc.Object.Pack(payload)
    json_msg = MessageToJson(rpc)
    logger.info("send %s", json.dumps(json.loads(json_msg), separators=(',', ':')))
    send(json_msg)

def send(json_msg):
    global ws, logger
    try:
        ws.send(json_msg)
    except websocket.WebSocketException as e:
        logger.error("### cointhink.py: ws.send aborted: "+str(e)+" for "+json_msg)

def log(token, msg):
    logger.info("log: "+msg)
    alog = algolog_pb2.Algolog()
    alog.Event = 'message'
    alog.Level = 'info'
    alog.Message = msg
    rpc(token, "Algolog", alog)

def notify(token, summary, detail=None):
    summary = str(summary)
    notify = notify_pb2.Notify()
    notify.Summary = summary
    if detail:
        notify.Detail = detail
    log(token, "notify: "+summary)
    rpc(token, "Notify", notify)

