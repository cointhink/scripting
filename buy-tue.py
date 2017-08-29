# buy-weekly-tue

def init(cointhink):
    cointhink.log("init: go")
    cointhink.trade()

def eachDay(cointhink, date):
    cointhink.log("eachDay go "+date.strftime("%Y-%m-%d %H:%M:%S"))
    trade()