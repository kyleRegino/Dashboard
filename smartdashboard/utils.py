def time_to_seconds(time_obj):
    seconds = (time_obj.hour * 60 + time_obj.minute) * 60 + time_obj.second
    return seconds