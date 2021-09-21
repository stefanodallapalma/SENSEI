import json
import logging
from datetime import datetime
from traceback import format_exc

logger = logging.getLogger("Utils script")


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


def valid_year(year):
    if year and str(year).isdigit():
        if 1900 <= int(year) <= datetime.now().year:
            return True

    return False


def valid_month(month):
    if not month:
        return False

    logger.debug(type(month))

    if not month.isdigit():
        formats = ["%B", "%b"]
        for format in formats:
            try:
                datetime_object = datetime.strptime(str(month), format)
                logger.debug(datetime_object)
                return True
            except:
                logger.error(format_exc())
    else:
        if isinstance(month, str):
            month = int(month)

        if 1 <= month <= 12:
            return True

    return False


def convert_letteral_month_to_int(month):
    if not month:
        raise Exception("Invalid null month.")

    if not month.isdigit():
        formats = ["%B", "%b"]
        for format in formats:
            try:
                datetime_object = datetime.strptime(month, format)
                month_number = datetime_object.month
                if month_number < 10:
                    month_number = "0" + str(month_number)
                return str(month_number)
            except Exception as e:
                logger.error(format_exc())
    else:
        if isinstance(month, str):
            month = int(month)

        if month <= 0 or month > 12:
            raise Exception("Invalid range. Month must be included into 1-12.")
        if month < 10:
            return "0" + str(month)
        else:
            return str(month)

    raise Exception("Invalid month format. Format accepted: `February` OR `Feb`.")


def convert_numerical_month_to_str(month, format="%b"):
    logger.info(month)
    formats = ["%B", "%b"]
    if format not in formats:
        raise Exception("Invalid format!. The format must be %b or %B.")

    if not month:
        raise Exception("Invalid null month.")

    if not month.isdigit():
        try:
            month = int(month)
        except:
            raise Exception("Invalid month! The month must be a number between 1 and 12.")

    logger.info(month)
    if int(month) <= 0 or int(month) > 12:
        raise Exception("Invalid month! The month must be a number between 1 and 12.")

    datetime_object = datetime.strptime(str(month), "%m")
    month_name = datetime_object.strftime(format)
    return month_name