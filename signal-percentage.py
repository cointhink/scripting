# signal-percentage
import datetime

btc_last = False
signal_percentage = 0

def init(cointhink):
    cointhink.log("settings: "+str(cointhink.settings))
    cointhink.notify("signal-percentage begin.")
    signal_percentage = float(cointhink.settings['percent_change'])

def market_prices(cointhink, prices):
    global btc_last
    global signal_percentage
    for price in prices.Prices:
        new_price = float(price.Amount)
        received_at = datetime.datetime.strptime(price.ReceivedAt, "%Y-%m-%dT%H:%M:%SZ")
        if price.Market.lower() == cointhink.settings['market']:
          if btc_last:
            price_delta = new_price - btc_last[0]
            chg_price_ratio = price_delta / new_price
            chg_time = received_at - btc_last[1]
            log_msg = "{} price ${:.2f} changed ${:.2f} {:.2%} in {}".format(
              cointhink.settings['market'], new_price, price_delta, chg_price_ratio,
              time_words(chg_time))
            cointhink.log(log_msg)
            if abs(chg_price_ratio) > signal_percentage:
              cointhink.notify(log_msg)
          else:
            log_msg = "{} first price ${}".format(cointhink.settings['market'], new_price)
            cointhink.log(log_msg)
          btc_last = (new_price, received_at)

def each_day(cointhink, date):
    log_msg = "Day report:"
    if btc_last:
      log_msg = log_msg + " btc_last price {} date {}".format(btc_last[0], btc_last[1])
    cointhink.log(log_msg)

def time_words(time):
    value = time.seconds
    unit = "seconds"
    if time.seconds > 60:
      value = time.seconds / 60
      unit = "minutes"
    return "{:.1f} {}".format(value, unit)
