# signal-5%
import datetime

btc_last = False

def init(cointhink):
    cointhink.log("settings: "+str(cointhink.settings))
    cointhink.notify("signal-5% begin.")

def market_prices(cointhink, prices):
    global btc_last
    for price in prices.Prices:
        new_price = float(price.Amount)
        received_at = datetime.datetime.strptime(price.ReceivedAt, "%Y-%m-%dT%H:%M:%SZ")
        if price.Market.lower() == cointhink.settings['Market']:
          if btc_last:
            price_delta = new_price - btc_last[0]
            chg_price_ratio = price_delta / new_price
            chg_time = received_at - btc_last[1]
            log_msg = "{} price ${:.2f} changed ${:.4f} {:.2%} in {:.1f} mins".format(
              cointhink.settings['Market'], new_price, price_delta, chg_price_ratio,
              chg_time.seconds/60)
            cointhink.log(log_msg)
            if chg_price_ratio > 0.01:
              cointhink.notify(log_msg)
          else:
            log_msg = "{} first price ${}".format(cointhink.settings['Market'], new_price)
            cointhink.log(log_msg)
          btc_last = (new_price, received_at)

def each_day(cointhink, date):
    log_msg = "Day report"
    if btc_last:
      log_msg = log_msg + "btc_last price {} date {}".format(btc_last[0], btc_last[1])
    cointhink.log(log_msg)
