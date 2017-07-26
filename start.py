import websocket
import json
import script
import cointhink

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print("### error ###")
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### open ###")
    cointhink.log('Algorithm Run # started')
    script.init(cointhink)

if __name__ == "__main__":
    with open('auth.json') as json_data:
        print("### auth ###")
        auth = json.load(json_data)
        print("### connect ###")
        ws = websocket.WebSocketApp("ws://10.0.0.1:8085/",
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)
        cointhink.init(auth, ws)
        ws.on_open = on_open
        ws.run_forever()
