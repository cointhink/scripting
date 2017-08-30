import websocket
import json
import cointhink
import logging

def on_message(ws, message):
    logger.info(message)
    payload = json.loads(message)
    cointhink.on_message(payload)

def on_error(ws, error):
    logger.info("### error ###")
    logger.info(error)

def on_close(ws):
    logger.info("### closed ###")

def on_open(ws):
    logger.info("### open ###")
    cointhink.init(auth, ws, settings)

if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    with open('auth.json') as json_data:
        auth = json.load(json_data)
    with open('settings.json') as json_data:
        settings = json.load(json_data)
    url = "ws://10.0.0.1:8085/"
    logger.info("### connecting %s ###", url)
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    logger.info("### ws loop ###")
    ws.run_forever()
