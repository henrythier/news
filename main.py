import tonline
import zeit

def hello_world():
    print('hello world')


#schedule.every(10).seconds.do(hello_world)

'''while True:
    schedule.run_pending()
    time.sleep(1)'''

a = zeit.get_opener()
print(a)


