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
        if price.Market.lower() == "btc/usd":
          if btc_last:
            price_delta = new_price - btc_last[0]
            chg_percent = price_delta/new_price
            chg_time = received_at - btc_last[1]
            log_msg = "BTC price ${} changed ${:.4f} {:.1%} in {:.1f} mins".format(
              new_price, price_delta, chg_percent, chg_time.seconds/60)
            cointhink.log(log_msg)
          else:
            log_msg = "BTC first price ${}".format(new_price)
            cointhink.log(log_msg)
          btc_last = (new_price, received_at)

def each_day(cointhink, date):
    cointhink.log("Day report - btc_price_avg "+str(btc_price_avg))
