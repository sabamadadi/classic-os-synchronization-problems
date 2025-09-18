import threading
import time
import random

read_count = 0
mutex = threading.Semaphore(1)
rw_mutex = threading.Semaphore(1)
waiting_readers = 0
TERMINATE = True

def reader(reader_id):
    global read_count
    global mutex
    global rw_mutex
    global waiting_readers
    global TERMINATE
    while TERMINATE:

        waiting_readers += 1
        mutex.acquire()
        read_count += 1
        if read_count == 1:
            rw_mutex.acquire()
        waiting_readers -= 1

        print(f"Reader {reader_id} is reading. Active readers: {read_count}")
        time.sleep(random.uniform(0.1, 0.5))


        read_count -= 1
        print(f'Reader {reader_id} done. Active readers: {read_count}')
        if read_count == 0:
            rw_mutex.release()
        mutex.release()

        time.sleep(random.uniform(0.5, 1.0)) 

def writer(writer_id):
    global read_count
    global mutex
    global rw_mutex
    global waiting_readers
    global TERMINATE
    while TERMINATE:
        if waiting_readers == 0:

            rw_mutex.acquire()
            print(f"Writer {writer_id} is writing.")
            time.sleep(random.uniform(0.5, 1.0))
            rw_mutex.release() 
            print(f'Writer {writer_id} done.')

            time.sleep(random.uniform(1.0, 2.0))
        else:
            print(f'Writer {writer_id} is waiting')

            time.sleep(0.5)
def main():
    num_readers = 3
    num_writers = 2

    threads = []

    for i in range(num_readers):
        t = threading.Thread(target=reader, args=(i + 1,))
        threads.append(t)

    for i in range(num_writers):
        t = threading.Thread(target=writer, args=(i + 1,))
        threads.append(t)

    for t in threads:
        t.start()
    time.sleep(5)
    global TERMINATE
    TERMINATE = False
    for t in threads:
        t.join()

    print("Simulation finished.")
if __name__ == "__main__":
    main()