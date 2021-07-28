import json
import datetime


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
    year = datetime.datetime.utcfromtimestamp(ts).strftime('%Y')
    weekday = datetime.datetime.fromtimestamp(ts).isocalendar()[1]
    year_week = year + '- week ' + str(weekday)

    return year_week