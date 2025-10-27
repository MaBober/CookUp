import datetime as dt

def normalize_to_minutes(dt_obj: dt.datetime) -> dt.datetime:
    return dt_obj.replace(second=0, microsecond=0)