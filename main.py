from outlets import bild, faz, focus, handelsblatt, ntv, spon, sz, tonline, welt, zeit
import twittertrends
import DB_writer
import schedule
import time
import datetime
import sys

outlets = [bild, faz, focus, handelsblatt, ntv, spon, sz, tonline, welt, zeit]

def get_openers():
    errors = 0
    start = datetime.datetime.now()
    print('Run started at: {}'.format(start))
    for o in outlets:
        try:
            opener = vars(o.get_opener())
            DB_writer.insert_opener(opener)
        except:
            errors += 1
            e = sys.exc_info()
            err = {"Error": str(e[0]),
                   "Outlet": o.name,
                   "tmstmp": start}
            print(err)
            DB_writer.insert_error(err)
    end = datetime.datetime.now()
    print('Errors encountered: {}'.format(errors))
    print('Run completed at: {}'.format(end))


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
    print('running')
    schedule.every().hour.at(":00").do(get_openers)
    schedule.every().hour.at(":00").do(get_twitter)

    while True:
        schedule.run_pending()
        time.sleep(1)


def get_single_opener(outlet):
    opener = vars(outlet.get_opener())
    DB_writer.insert_opener(opener)


if __name__ == "__main__":
    schedule_queries()