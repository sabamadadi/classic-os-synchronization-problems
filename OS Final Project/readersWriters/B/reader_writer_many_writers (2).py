import threading
import time
import random

read_count = 0
reader_mutex = threading.Semaphore(1)
writer_mutex = threading.Semaphore(1)
writer_count = 0
TERMINATE = True

def reader(reader_id):
    global TERMINATE
    global read_count
    global reader_mutex
    global writer_count
    while TERMINATE:
        reader_mutex.acquire()
        while writer_count > 0:
            print(f'Reader {reader_id} is waiting')
            reader_mutex.release()
            time.sleep(0.1)
            reader_mutex.acquire()
        read_count += 1

        reader_mutex.release()

        print(f"Reader {reader_id} is reading. Active readers: {read_count}")
        time.sleep(random.uniform(0.1, 0.5))

        reader_mutex.acquire()
        read_count -= 1
        print(f'Reader {reader_id} done. Active readers: {read_count}')

        reader_mutex.release()

        time.sleep(random.uniform(0.5, 1.0))

def writer(writer_id):
    global TERMINATE

    global writer_mutex
    global writer_count
    while TERMINATE:
        writer_mutex.acquire()
        writer_count += 1
        writer_mutex.release()

        print(f"Writer {writer_id} is writing.")
        time.sleep(random.uniform(0.5, 1.0))

        writer_mutex.acquire()
        writer_count -= 1
        print(f'Writer {writer_id} done.')

        writer_mutex.release()

        time.sleep(random.uniform(1.0, 2.0))

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

