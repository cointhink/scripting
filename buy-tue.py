# buy-weekly-tue

def init(cointhink):
    cointhink.log("settings: "+str(cointhink.settings))
    cointhink.notify("buy-tue begin")

def each_day(cointhink, date):
    now = date.strftime("%Y-%m-%d %H:%M:%S")
    weekday = date.strftime("%a")
    if weekday == "Tue":
        cointhink.log("today is Tuesday!")
    cointhink.log("eachDay is "+weekday+". "+now)
    cointhink.trade()
