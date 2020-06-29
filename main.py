import tonline
import zeit
import faz
import DB_writer

def get_opners():
    print('hello world')

'''while True:
    schedule.run_pending()
    time.sleep(1)'''

a = vars(zeit.get_opener())
DB_writer.insert_opener(a)


