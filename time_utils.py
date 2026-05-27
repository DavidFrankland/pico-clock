import time

# This is MicroPython, so we can't just:
# import datetime
# We have to handle our own time zone.


def localtime():
    # get UTC time components
    year, month, day, hour, minute, second, weekday, yearday = time.gmtime()

    # calculate offset for BST/GMT
    # get last Sunday in March / October for the current year
    seconds_since_epoch = time.time()
    if seconds_since_epoch >= last_sunday_in_march(year) and seconds_since_epoch < last_sunday_in_october(year):
        time_zone_offset = 3600
    else:
        time_zone_offset = 0

    # return UTC + offset
    return time.gmtime(time.time() + time_zone_offset)


def last_sunday_in_march(year: int) -> int:
    return last_sunday_in_month(year, 3)


def last_sunday_in_october(year: int) -> int:
    return last_sunday_in_month(year, 10)


def last_sunday_in_month(year: int, month: int) -> int:
    first_of_next_month = (time.mktime((year, month+1, 1, 1, 0, 0, 0, 0)))
    weekday = time.gmtime(first_of_next_month)[6]
    first_sunday_of_next_month = (year, month+1, 7-weekday, 1, 0, 0, 0, 0)
    return time.mktime(first_sunday_of_next_month)-7*86400
