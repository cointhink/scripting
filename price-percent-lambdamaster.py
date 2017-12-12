# price-percent-lambdamaster
import datetime

price_last = False
signal_ratio = 1.0

def init(cointhink):
    global signal_ratio
    cointhink.log("settings: "+str(cointhink.settings))
    cointhink.notify("price-percent-lambdamaster begin.")

def market_prices_auth(token, settings, cointhink, prices):
    signal_ratio = float(settings.get('percent_change', 100))/100.0
    for price in prices.Prices:
        exchange = settings['exchange']
        if price.Exchange.lower() == exchange:
          market = settings['market']
          if price.Market.lower() == market:
            received_at = datetime.datetime.strptime(price.ReceivedAt, "%Y-%m-%dT%H:%M:%SZ")
            new_price = float(price.Amount)
            price_last = settings.get('price_last')
            if price_last:
              price_delta = new_price - price_last[0]
              chg_price_ratio = price_delta / new_price
              chg_time = received_at - price_last[1]
              updown = "down"
              if chg_price_ratio >= 0:
                updown = "up"
              log_msg = "{} ${:.2f} {} ${:.2f} {:.2%} of {:.2%} in {}".format(
                market, new_price, updown, price_delta, chg_price_ratio,
                signal_ratio, time_words(chg_time))
              cointhink.log(token, log_msg)
              if abs(chg_price_ratio) >= signal_ratio:
                cointhink.notify(token, log_msg)
                settings['price_last'] = (new_price, received_at)
            else:
              log_msg = "{} first price ${}".format(market, new_price)
              cointhink.log(token, log_msg)
              settings['price_last'] = (new_price, received_at)

def each_day_auth(token, settings, cointhink, date):
    log_msg = "Day report:"
    price_last = settings.get('price_last')
    if price_last:
      log_msg = log_msg + " price_last price {} date {}".format(price_last[0], price_last[1])
    cointhink.log(token, log_msg)

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
