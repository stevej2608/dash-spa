import datetime

def time_ms():
    tnow = datetime.datetime.timestamp(datetime.datetime.now())
    return int(tnow * 1000)
