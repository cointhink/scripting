import websocket
import json
import logging
import time
import traceback
import sys

def on_message(ws, message):
    logger.info(message)
    payload = json.loads(message)
    cointhink.on_message(payload)

def on_error(ws, error):
    if isinstance(error, KeyboardInterrupt):
      raise error
    else:
      tb = sys.exc_info()[2]
      last_frame = traceback.extract_tb(tb)[-1]
      err_nice = "error {} line {} in '{}': {} {}".format(
          last_frame.filename, last_frame.lineno, last_frame.name , error, type(error))
      logger.info("### start.py: "+err_nice)
      if not isinstance(error, IOError):
        cointhink.log(err_nice)

def on_close(ws):
    # no cointhink.log here
    logger.info("### start.py: closed ###")

def on_open(ws):
    global made_connection
    if made_connection:
        logger.info("### start.py: open (reconnect, skipping init)")
    else:
        made_connection = True
        logger.info("### start.py: open ###")
        cointhink.init(auth, ws, settings)
    cointhink.heartbeat()

def setup_socket():
    url = "ws://10.0.0.1:8085/"
    logger.info("### start.py: connecting %s ###", url)
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
      try:
        import cointhink
        ws.run_forever()
        logger.info("### start.py: connection lost. waiting 1 second")
        time.sleep(1)
      except KeyboardInterrupt:
        logger.info("### start.py: stopping")
        break
      except:
        e = sys.exc_info()
        logger.error("### start.py: ws.run_forever aborted: "+str(e[0]))
        logger.error(traceback.format_tb(e[2]))
        time.sleep(2)
