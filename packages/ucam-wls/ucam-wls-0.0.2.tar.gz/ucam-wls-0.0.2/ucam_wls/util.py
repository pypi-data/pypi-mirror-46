import datetime

TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"


def datetime_to_protocol(dt):
    """
    Format a Python :class:`datetime` object into a string as required by the
    WAA2WLS protocol.
    """
    return dt.strftime(TIMESTAMP_FORMAT)


def datetime_from_protocol(date_string, naive=False):
    """
    Decode a date string in the format specified in the WAA2WLS protocol,
    returning a Python :class:`datetime` object.

    :param naive:   Return a 'naive' object, without UTC timezone information.
                    (default: :const:`False`)
    """
    dt = datetime.datetime.strptime(TIMESTAMP_FORMAT)
    dt.tzinfo = datetime.timezone.utc
    return dt
