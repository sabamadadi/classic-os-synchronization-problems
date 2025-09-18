import multiprocessing
import time
import random

read_count = multiprocessing.Value('i', 0)
reader_mutex = multiprocessing.Semaphore(1)
writer_mutex = multiprocessing.Semaphore(1)
writer_count = multiprocessing.Value('i', 0)

def reader(reader_id, read_count, reader_mutex, writer_mutex, writer_count):
    while True:
        reader_mutex.acquire()
        while writer_count.value > 0:
            print(f'Reader {reader_id} is waiting')
            reader_mutex.release()
            time.sleep(0.1)
            reader_mutex.acquire()
        read_count.value += 1

        reader_mutex.release()

        print(f"Reader {reader_id} is reading. Active readers: {read_count.value}")
        time.sleep(random.uniform(0.1, 0.5))

        reader_mutex.acquire()
        read_count.value -= 1
        print(f'Reader {reader_id} done. Active readers: {read_count.value}')

        reader_mutex.release()

        time.sleep(random.uniform(0.5, 1.0))

def writer(writer_id, read_count, reader_mutex, writer_mutex, writer_count):
    while True:
        writer_mutex.acquire()
        writer_count.value += 1
        writer_mutex.release()

        print(f"Writer {writer_id} is writing.")
        time.sleep(random.uniform(0.5, 1.0))

        writer_mutex.acquire()
        writer_count.value -= 1
        print(f'Writer {writer_id} done.')

        writer_mutex.release()

        time.sleep(random.uniform(1.0, 2.0))

if __name__ == "__main__":
    num_readers = 3
    num_writers = 2

    processes = []
    for i in range(num_readers):
        p = multiprocessing.Process(target=reader, args=(i, read_count, reader_mutex, writer_mutex, writer_count))
        processes.append(p)
    for i in range(num_writers):
        p = multiprocessing.Process(target=writer, args=(i, read_count, reader_mutex, writer_mutex, writer_count))
        processes.append(p)

    for p in processes:
        p.start()

    time.sleep(10)

    for p in processes:
        p.terminate()

    print("Simulation finished.")
