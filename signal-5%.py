# signal-5%

btc_last_price = False

def init(cointhink):
    cointhink.log("settings: "+str(cointhink.settings))
    cointhink.notify("signal-5% begin.")

def market_prices(cointhink, prices):
    global btc_last_price
    for price in prices.Prices:
        cointhink.log("market price update received "+price.Market+" $"+price.Amount)
        new_price = float(price.Amount)
        if price.Market == "BTC/USD":
          if btc_last_price:
            price_delta = new_price - btc_last_price
            chg_percent = price_delta/new_price
            cointhink.log("BTC price change of $"+str(price_delta)+ " "+str(chg_percent)+"%")
          btc_last_price = new_price

def each_day(cointhink, date):
    cointhink.log("Day report - btc_price_avg "+str(btc_price_avg))
