import tonline
import zeit
import faz

def hello_world():
    print('hello world')


#schedule.every(10).seconds.do(hello_world)

'''while True:
    schedule.run_pending()
    time.sleep(1)'''

outlets = [faz, tonline, zeit]

for o in outlets:
    print(o.get_opener())


