def time_to_seconds(time_obj):
    seconds = (time_obj.hour * 60 + time_obj.minute) * 60 + time_obj.second
    return seconds

def init_list(length=None):
    if length:
        return [None]*length
    else:
        return [None]*24

def format_date(date,period):
    if period == "day":
        return date.strftime("%Y-%m-%d")
    elif period == "month" or period == "year":
        return date
