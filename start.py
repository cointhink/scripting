import websocket
import json
import cointhink
import logging
import time

def on_message(ws, message):
    logger.info(message)
    payload = json.loads(message)
    cointhink.on_message(payload)

def on_error(ws, error):
    # no cointhink.log here
    logger.info("### error: %s", error)

def on_close(ws):
    # no cointhink.log here
    logger.info("### closed ###")

def on_open(ws):
    global made_connection
    if made_connection:
        logger.info("### open (reconnect, skipping init)")
    else:
        made_connection = True
        logger.info("### open ###")
        cointhink.init(auth, ws, settings)

def setup_socket():
    url = "ws://10.0.0.1:8085/"
    logger.info("### connecting %s ###", url)
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              on_open = on_open)
    return ws

if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    with open('auth.json') as json_data:
        auth = json.load(json_data)
    with open('settings.json') as json_data:
        settings = json.load(json_data)
    made_connection = False
    ws = setup_socket()
    while True:
        ws.run_forever()
        logger.info("### connection lost. waiting 1 second")
        time.sleep(1)
