# import os
# import threading

# t1 = threading.Thread(target=os.system, args=("python 1.py",))
# t1.start()
# t2 = threading.Thread(target=os.system, args=("python 2.py",))
# t2.start()


from multiprocessing import Pool
import os
import time
import random


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(3)
    p.apply_async(os.system, args=("python 1.py",))
    p.apply_async(os.system, args=("python 2.py",))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
