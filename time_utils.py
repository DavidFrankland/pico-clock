import time

# This is MicroPython, so we can't just:
# import datetime
# We have to handle our own time zone.

old_year = 0
bst_start = 0
bst_end = 0


def localtime():
    global old_year, bst_start, bst_end
    # get UTC time components
    year, month, day, hour, minute, second, weekday, yearday = time.gmtime()
    if year != old_year:
        old_year = year
        bst_start = last_sunday_in_march(year)
        print(f'BST starts {format_time(bst_start)} UTC')
        bst_end = last_sunday_in_october(year)
        print(f'BST ends {format_time(bst_end)} UTC')

    # calculate offset for BST/GMT
    seconds_since_epoch = time.time()
    if seconds_since_epoch >= bst_start and seconds_since_epoch < bst_end:
        time_zone_offset = 3600
    else:
        time_zone_offset = 0

    # return UTC + offset
    return time.gmtime(seconds_since_epoch + time_zone_offset)


def format_time(secs: int) -> str:
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year, month, day, hour, minute, second, weekday, yearday = time.gmtime(secs)
    return f'{day} {month_names[month]} {year} {hour:02}:{minute:02}:{second:02}'


def last_sunday_in_march(year: int) -> int:
    return last_sunday_in_month(year, 3)


def last_sunday_in_october(year: int) -> int:
    return last_sunday_in_month(year, 10)


def last_sunday_in_month(year: int, month: int) -> int:
    first_of_next_month = (time.mktime((year, month+1, 1, 1, 0, 0, 0, 0)))
    weekday = time.gmtime(first_of_next_month)[6]
    first_sunday_of_next_month = (year, month+1, 7-weekday, 1, 0, 0, 0, 0)
    return time.mktime(first_sunday_of_next_month)-7*86400
