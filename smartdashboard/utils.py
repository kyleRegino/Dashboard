def time_to_seconds(time_obj):
    seconds = (time_obj.hour * 60 + time_obj.minute) * 60 + time_obj.second
    return seconds

def init_list(length=None,val=None):
    if length != None and val != None:
        return [val]*length
    elif length:
        return [None]*length
    else:
        return [None]*24

def format_date(date,period):
    if period == "day":
        return date.strftime("%Y-%m-%d")
    elif period == "month" or period == "year":
        return date

def insert_sku(lookup, hour, amt, cnt):
    if hour == 5:
        lookup["amount"][0] = str(amt)
        lookup["count"][0] = str(cnt)
    elif hour == 9:
        lookup["amount"][1] = str(amt)
        lookup["count"][1] = str(cnt)
    elif hour == 13:
        lookup["amount"][2] = str(amt)
        lookup["count"][2] = str(cnt)
    elif hour == 17:
        lookup["amount"][3] = str(amt)
        lookup["count"][3] = str(cnt)
    elif hour == 21:
        lookup["amount"][4] = str(amt)
        lookup["count"][4] = str(cnt)
    elif hour == 1:
        lookup["amount"][5] = str(amt)
        lookup["count"][5] = str(cnt)

def number_formatter(num):
    return '{0:,}'.format(num) if num != None else "Null"
        