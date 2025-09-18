import multiprocessing
import random
import time
import queue



MAX_SIZE = 30



def producer(pipe_1, pipe_2, sleep_start, sleep_end, stop_event):
    global MAX_SIZE

    output_pipe, _ = pipe_1
    _, input_pipe = pipe_2
    
    waiting = 0
    items = queue.Queue()
    counter = 0

    while not stop_event.is_set():
  
        if input_pipe.poll():
            input = input_pipe.recv()
            waiting -= 1
            items.get()

        if waiting != MAX_SIZE:

            item = counter
            output_pipe.send(item)
            items.put(item)
            waiting += 1
            print(f" Producer: Produced item {item} ")
            counter += 1
            sleep_time = random.uniform(sleep_start, sleep_end)
            time.sleep(sleep_time)

        else:
            print(' STOPING PRODUCTION! Max size limit reached, Producer waiting, queues are full.')
            input = input_pipe.recv()
            waiting -= 1
            items.get()

    output_pipe.close()




def consumer(pipe_1, pipe_2, sleep_start, sleep_end, stop_event):
    global MAX_SIZE

    waiting = 0
    items = queue.Queue()


    _, input_pipe = pipe_1
    output_pipe, _ = pipe_2

    while not stop_event.is_set():

        item=None
        if input_pipe.poll():
            inputs = input_pipe.recv()
            items.put(inputs)
            waiting += 1
        if waiting != 0:
            item = items.get()
            print(f"Consumer: Consumed item {item}")
            waiting -= 1
            output_pipe.send(item)

            sleep_time = random.uniform(sleep_start, sleep_end)
            time.sleep(sleep_time)
        else:
            print(' STOPING CONSUMPTION! size is zero, consumer waiting, queues are empty.')

            item = input_pipe.recv()
            items.put(item)
            waiting += 1
        
    output_pipe.close()




if __name__ == '__main__':

    pipe_1 = multiprocessing.Pipe(True)
    pipe_2 = multiprocessing.Pipe(True)
    stop_event = multiprocessing.Event()

    producer_process = multiprocessing.Process(target=producer, args=(pipe_1, pipe_2, 0.1, 0.3, stop_event))
    consumer_process = multiprocessing.Process(target=consumer, args=(pipe_1, pipe_2, 1.1, 2.0, stop_event))

    producer_process.start()
    consumer_process.start()


    time.sleep(20)
    print('Program runtime has finished, stopping ...')
    stop_event.set()
    pipe_1[0].close()
    pipe_2[0].close()
    pipe_1[1].close()
    pipe_2[1].close()    
    producer_process.join()
    consumer_process.join()
