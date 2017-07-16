from random import randint
from config import *
import time


def get_request_headers():
    agents = ['Mozilla/5.0', 'Safari/533.1', 'Chrome/33.0.1750.117']
    return {'User-Agents': agents[randint(0, len(agents)-1)]}


def get_rand_in_range(min, max):
    return randint(min, max)


def get_scrapper_sleep():
    return get_rand_in_range(SCRAPPER_SLEEP_MIN, SCRAPPER_SLEEP_MAX)


def sleep_scrapper(scrapper_name):
    val = get_scrapper_sleep()
    print "\n\n[%s] SLEEP %d seconds.....\n\n" % (scrapper_name, val)
    time.sleep(val)
    print "\n\n[%s] RESUMED \n\n" % scrapper_name


def txt_write(fname, msg):
    msg = msg.encode("utf-8")
    f = open(fname, "w")
    f.write("%s" % msg)
    f.close()


if __name__ == '__main__':

    for i in range(0, 20):
        print get_request_headers()
