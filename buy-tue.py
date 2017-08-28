# buy-weekly-tue

def init(context):
    context.log("init: go")

def eachDay(context, date):
    context.log("eachDay go "+date.strftime("%Y-%m-%d %H:%M:%S"))
