# price-percent
import datetime

price_last = False
signal_ratio = 1.0

def init(cointhink):
    global signal_ratio
    cointhink.log("settings: "+str(cointhink.settings))
    cointhink.notify("price-percent begin.")
    signal_ratio = float(cointhink.settings['percent_change'])/100.0

def market_prices(cointhink, prices):
    global price_last
    global signal_ratio
    for price in prices.Prices:
        exchange = cointhink.settings['exchange']
        if price.Exchange.lower() == exchange:
          market = cointhink.settings['market']
          if price.Market.lower() == market:
            received_at = datetime.datetime.strptime(price.ReceivedAt, "%Y-%m-%dT%H:%M:%SZ")
            new_price = float(price.Amount)
            if price_last:
              price_delta = new_price - price_last[0]
              chg_price_ratio = price_delta / new_price
              chg_time = received_at - price_last[1]
              updown = "down"
              if chg_price_ratio >= 0:
                updown = "up"
              log_msg = "{} ${:.2f} {} ${:.2f} {:.2%} of {:.2%} in {}".format(
                cointhink.settings['market'], new_price, updown, price_delta, chg_price_ratio,
                signal_ratio, time_words(chg_time))
              cointhink.log(log_msg)
              if abs(chg_price_ratio) >= signal_ratio:
                cointhink.notify(log_msg)
                price_last = (new_price, received_at)
            else:
              log_msg = "{} first price ${}".format(cointhink.settings['market'], new_price)
              cointhink.log(log_msg)
              price_last = (new_price, received_at)

def each_day(cointhink, date):
    log_msg = "Day report:"
    if price_last:
      log_msg = log_msg + " price_last price {} date {}".format(price_last[0], price_last[1])
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
