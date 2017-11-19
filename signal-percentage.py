# signal-percentage
import datetime

price_last = False
signal_percentage = 100

def init(cointhink):
    cointhink.log("settings: "+str(cointhink.settings))
    cointhink.notify("price-percent begin.")
    signal_percentage = float(cointhink.settings['percent_change'])

def market_prices(cointhink, prices):
    global price_last
    global signal_percentage
    for price in prices.Prices:
        new_price = float(price.Amount)
        received_at = datetime.datetime.strptime(price.ReceivedAt, "%Y-%m-%dT%H:%M:%SZ")
        if price.Market.lower() == cointhink.settings['market']:
          if price_last:
            price_delta = new_price - price_last[0]
            chg_price_ratio = price_delta / new_price
            chg_time = received_at - price_last[1]
            log_msg = "{} price ${:.2f} changed ${:.2f} {:.2%} in {}".format(
              cointhink.settings['market'], new_price, price_delta, chg_price_ratio,
              time_words(chg_time))
            cointhink.log(log_msg)
            if abs(chg_price_ratio) > (signal_percentage/100.0):
              cointhink.notify(log_msg)
              price_last = (new_price, received_at)
          else:
            log_msg = "{} first price ${}".format(cointhink.settings['market'], new_price)
            cointhink.log(log_msg)
            price_last = (new_price, received_at)

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
    if time.seconds > 60 * 60:
      value = time.seconds / 60 / 60
      unit = "hours"
    if time.seconds > 60 * 60 * 24:
      value = time.seconds / 60 / 60 / 24
      unit = "days"
    return "{:.1f} {}".format(value, unit)
