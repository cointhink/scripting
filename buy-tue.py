# buy-weekly-tue

def init(cointhink):
    cointhink.log("settings: "+str(cointhink.settings))
    cointhink.notify("buy-tue begin")

def eachDay(cointhink, date):
    now = date.strftime("%Y-%m-%d %H:%M:%S")
    weekday = date.strftime("%a")
    if weekday == "Tue":
        cointhink.log("its Tuesday!")
    cointhink.log("eachDay is "+weekday+". "+now)
    cointhink.trade()
