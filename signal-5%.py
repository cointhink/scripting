# signal-5%

price_delta = 0

def init(cointhink):
    cointhink.log("settings: "+str(cointhink.settings))
    cointhink.notify("signal-5% begin.")

def market_prices(cointhink, prices):
    for price in prices.Prices:
        cointhink.log("market price update "+price.Market+" $"+price.Amount)

def each_day(cointhink, date):
    cointhink.log("day report - price_delta"+str(price_delta))
