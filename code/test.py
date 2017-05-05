import multiprocessing
import time

def worker():
    """thread worker function"""
    print 'Worker:'
    lol = 0
    for i in range(2):
        print(lol)
        lol += 1
        time.sleep(1)
    return

if __name__ == '__main__':
    jobs = []
    p = multiprocessing.Process(target=worker)
    jobs.append(p)
    p.start()
    for i in range(2):
        print("b")
        time.sleep(1)
    multiprocessing.Process(target=worker).start()