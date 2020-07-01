import bild
import faz
import focus
import handelsblatt
import ntv
import spon
import sz
import tonline
import welt
import zeit
import twittertrends
import DB_writer
import schedule
import time
import datetime
import sys

outlets = [bild, faz, focus, handelsblatt, ntv, spon, sz, tonline, welt, zeit]

def get_openers():
    now = datetime.datetime.now()
    print('RUN AT: {0}'.format(now))
    for o in outlets:
        try:
            opener = vars(o.get_opener())
            DB_writer.insert_opener(opener)
        except:
            e = sys.exc_info()
            err = {"Error": str(e[0]),
                   "Outlet": o.name,
                   "tmstmp": now}
            print(err)
            DB_writer.insert_error(err)


def get_twitter():
    try:
        twittertrends.get_trends()
    except:
        e = sys.exc_info()
        err = {"Error": str(e[0]),
               "Outlet": 'twitter',
               "tmstmp": datetime.datetime.now()}
        print(err)
        DB_writer.insert_error(err)


def schedule_queries():
    schedule.every().hour.at(":00").do(get_openers)
    schedule.every().hour.at(":00").do(get_twitter)

    while True:
        schedule.run_pending()
        time.sleep(1)


def get_single_opener(outlet):
    opener = vars(outlet.get_opener())
    DB_writer.insert_opener(opener)


schedule_queries()