from json_response import JsonResponse
from math import e
from datetime import datetime
import arrow, pytz
from dateutil import tz as dateutil_tz


def delete_db_object(db_object, **options):
    # method_delete => return object if exists or none
    message_ok_delete = options.get('message_ok_delete', 'delete ok')
    message_error_on_delete = options.get('message_error_on_delete', 'error on delete')
    if db_object:
        db_object.delete()
        return JsonResponse({"results": message_ok_delete, "error": None})
    return JsonResponse({"results": None, "error": message_error_on_delete})


def electrical_conductivity_to_25C_method_ratio_model(ce_value, temperature_value, **options):
    contant_value = options.get('contant_value', 0.02)
    return ce_value / (1 + contant_value * (temperature_value - 25))


def electrical_conductivity_to_25C_method_exponencial_model(ce_value, temperature_value):
    return ce_value * (0.4470 + 1.4034 * pow(e, (-1 * temperature_value / 26.815)))


def time_string_to_utc_datetime(time, timezone):
    date = datetime.now().date()
    time_formated = datetime.strptime(time, '%H:%M')
    date_to_convert = datetime.combine(date, time_formated.time())
    #tz = pytz.timezone(timezone)
    tz = dateutil_tz.gettz(timezone)
    datetime_to_arrow = arrow.get(date_to_convert, tz)
    return datetime_to_arrow.to('utc').datetime


def datetime_utc_to_localtime(datetime_utc,timezone):
    tz = pytz.timezone('utc')
    datetime_utc_to_arrow = arrow.get(datetime_utc,tz)
    return datetime_utc_to_arrow.to(timezone).datetime

def shift_datetime(datetime,**kwargs):
    return arrow.get(datetime).shift(**kwargs).datetime

def list_pytz_timezones():
    data = list()
    for tz in pytz.all_timezones:
        data.append({
            'tz':tz
        })
    return data
