import json
from datetime import datetime


def load_json(path):
    with open(path) as json_file:
        data = json.loads(json_file.read())

    return data


def date_formatter(timestamp):
    """
    Format the timestamp based on the following syntax - yyyy- week mm
    :param timestamp: timestamp (int)
    :return: the format data
    """

    ts = float(timestamp)
    year = datetime.utcfromtimestamp(ts).strftime('%Y')
    weekday = datetime.fromtimestamp(ts).isocalendar()[1]
    year_week = year + '- week ' + str(weekday)

    return year_week


def first_day_timestamp(timestamp):
    """
    Reset the timestamp passed in input with the first day
    Example:
        input: 1612264332 (Tue Feb 02 2021 12:12:12)
        output: 1612134000 (Mon Feb 01 2021 00:00:00)
    """

    date = datetime.fromtimestamp(int(timestamp))

    # Convert the date into a year/month format
    year_month = '{:%Y-%m}'.format(datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    year_month = datetime.strptime(year_month, '%Y-%m')

    first_dat_timestamp = int(datetime.timestamp(year_month))

    return first_dat_timestamp


def month_year_date_format(timestamp):
    """
    Convert a timestamp into a Month Year format
    Example:
        input: 1612264332 (Tue Feb 02 2021 12:12:12)
        output: February 2021
    """

    date_ts = datetime.fromtimestamp(int(timestamp))
    month_name = date_ts.strftime("%B")
    year = date_ts.year

    return month_name + " " + str(year)