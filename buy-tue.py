# buy-weekly-tue

def init(cointhink):
    cointhink.log("script init")
    cointhink.trade()

def eachDay(cointhink, date):
    cointhink.log("eachDay "+date.strftime("%Y-%m-%d %H:%M:%S"))
    cointhink.trade()