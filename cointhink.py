from google.protobuf.json_format import MessageToJson
import algolog_pb2
import rpc_pb2
import logging

logging.basicConfig()

def init(_auth, _ws):
    global auth, ws
    ws = _ws
    auth = _auth

def log(msg):
    print("### log ###")
    alog = algolog_pb2.Algolog()
    print(auth)
    alog.AlgorunId = auth['AlgorunId']
    alog.Event = 'start'
    alog.Level = 'info'
    alog.Message = msg
    rpc = rpc_pb2.Rpc()
    rpc.Token = auth['Token']
    rpc.Method = "Algolog"
    rpc.Object.Pack(alog)
    json_msg = MessageToJson(rpc)
    print(json_msg)
    ws.send(json_msg)
