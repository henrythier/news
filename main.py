import tonline
import zeit
import faz
import DB_writer
import schedule
import time
import datetime
import sys

outlets = [faz, tonline, zeit]
counter = 0

def get_openers():
    now = datetime.datetime.now()
    print('RUN AT: {0}'.format(now))
    for o in outlets:
        opener = vars(o.get_opener())
        DB_writer.insert_opener(opener)
        try:
            opener = vars(o.get_opener())
            DB_writer.insert_opener(opener)
        except:
            e = sys.exc_info()
            print('Error: {0},\nAt: {1},\nOutlet: {2}'.format(e[0],
                                                              now,
                                                              o.name))

schedule.every().hour.do(get_openers)

while True:
    schedule.run_pending()
    time.sleep(1)


