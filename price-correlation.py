# two-instrument correlation
import numpy

tokenA_history = numpy.array([])
tokenB_history = numpy.array([])

def init(cointhink):
    cointhink.log('init(cointhink) price-correlation numpy')

def market_prices(cointhink, prices):
    global tokenA_history, tokenB_history
    exchange_a = cointhink.settings['exchange_a']
    market_a = cointhink.settings['market_a']
    exchange_b = cointhink.settings['exchange_b']
    market_b = cointhink.settings['market_b']
    flag_a = False
    flag_b = False
    for price in prices.Prices:
      out_a = price_push(tokenA_history, price, exchange_a, market_a, 6)
      if out_a is not None:
        flag_a = True
        tokenA_history = out_a
      out_b = price_push(tokenB_history, price, exchange_b, market_b, 6)
      if out_b is not None:
        flag_b = True
        tokenB_history = out_b

    if flag_a and flag_b:
      print("coef for {} and {}".format(tokenA_history, tokenB_history))
      coef = numpy.cov(tokenA_history, tokenB_history)
      cointhink.log(exchange_a+':'+market_a+' '+exchange_b+':'+market_b + '{}'.format(coef))
    else:
      if flag_a:
        cointhink.log('missing a ' + exchange_a+':'+market_a)
      if flag_b:
        cointhink.log('missing b ' + exchange_b+':'+market_b)

def each_day(cointhink, date):
    cointhink.log('each_day(cointhink, date)')

def price_push(history, price, exchange, market, depth):
    if price.Exchange.lower() == exchange:
      if price.Market.lower() == market:
        new_price = float(price.Amount)
        history = numpy.append(history, new_price)
        history = numpy.resize(history, depth)
        print("pushed {}".format(history))
        return history
