import multiprocessing
import time
import random

read_count = multiprocessing.Value('i', 0)
mutex = multiprocessing.Semaphore(1)
rw_mutex = multiprocessing.Semaphore(1)
waiting_readers = multiprocessing.Value('i', 0) 

def reader(reader_id,count, mutex, rw_mutex, waiting_readers):
    while True:
        waiting_readers.value += 1
        mutex.acquire()
        count.value += 1
        if count.value == 1:
            rw_mutex.acquire()
        waiting_readers.value -= 1

        print(f"Reader {reader_id} is reading. Active readers: {count.value}")
        time.sleep(random.uniform(0.1, 0.5))


        count.value -= 1
        print(f'Reader {reader_id} done. Active readers: {count.value}')
        if count.value == 0:
            rw_mutex.release()
        mutex.release()

        time.sleep(random.uniform(0.5, 1.0)) 

def writer(writer_id, rw_mutex, waiting_readers):
    while True:
        if waiting_readers.value == 0:

            rw_mutex.acquire()
            print(f"Writer {writer_id} is writing.")
            time.sleep(random.uniform(0.5, 1.0))
            rw_mutex.release() 
            print(f'Writer {writer_id} done.')

            time.sleep(random.uniform(1.0, 2.0))
        else:
            print(f'Writer {writer_id} is waiting')

            time.sleep(0.5)

if __name__ == "__main__":
    num_readers = 3
    num_writers = 2

    processes = []
    for i in range(num_readers):
        p = multiprocessing.Process(target=reader, args=(i,read_count,mutex, rw_mutex,waiting_readers))
        processes.append(p)
    for i in range(num_writers):
        p = multiprocessing.Process(target=writer, args=(i,rw_mutex,waiting_readers))
        processes.append(p)

    for p in processes:
        p.start()

    time.sleep(10)

    for p in processes:
        p.terminate()

    print("Simulation finished.")
