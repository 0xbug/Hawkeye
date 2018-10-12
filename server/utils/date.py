import time


def timestamp():
    return int(time.time())


def today_start():
    zero_timestamp = time.mktime(
        time.strptime(time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time())), '%Y-%m-%d %H:%M:%S'))

    return int(zero_timestamp)
