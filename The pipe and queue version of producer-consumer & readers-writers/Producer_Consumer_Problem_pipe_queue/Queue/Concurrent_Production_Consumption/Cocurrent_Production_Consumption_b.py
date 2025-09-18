from gettext import find
import multiprocessing
from multiprocessing.synchronize import Event
import random
import time
import queue
'''
message_type:
0: producer generated item
1: consumer consumed item
'''
MAX_SIZE = 30

PRODUCER_NUMBER = 3
CONSUMER_NUMBER = 5


class Message:
    def __init__(self,message_type, process_number, item):
        self.message_type = message_type
        self.process_number = process_number
        self.item = item
        self.read_list = [False for i in range (PRODUCER_NUMBER + CONSUMER_NUMBER)]


    def set_read(self, type_t, number):
        self.read_list[PRODUCER_NUMBER * type_t + number - 1] = True


    def check_read(self, type_t, number):
        return self.read_list[PRODUCER_NUMBER * type_t + number - 1]
    
    def get_info(self, type_t, number):
        self.set_read(type_t, number)
        return self.message_type, self.process_number, self.item
    def check_list(self):
        flag = True
        for i in self.read_list:
            if not i:
                flag = False
        return flag
    def get_infosss(self):
        print(self.message_type, self.process_number, self.item, self.read_list)

class producer(multiprocessing.Process):
    def __init__(self, queue, number, stop_event, sleep_start, sleep_end):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.number = number
        self.stop_event = stop_event
        self.sleep_start = sleep_start
        self.sleep_end = sleep_end
    def run(self) :
        global MAX_SIZE

        counter = 0
        waiting = 0
        items = []

        while not self.stop_event.is_set():

            item_list = []
            while True:
                if not self.queue.empty():
                    T = self.queue.get()
                    item_list.append(T)  
                    if not T.check_read(0, self.number):
                        message_type, process_number, item = T.get_info(0, self.number)
                        if message_type == 0:
                            waiting += 1
                            items.append((process_number, item))
                        elif message_type == 1:
                            if (process_number, item) in items:
                                items.remove((process_number, item))
                            waiting -= 1                
                else:
                    break

            for item in item_list:
                if not item.check_list():

                    self.queue.put(item)


            if waiting < MAX_SIZE:
                item = counter
                message = Message(0, self.number, item)
                counter += 1
                message.set_read(0, self.number)
                self.queue.put(message)
                items.append((self.number, item))
                waiting += 1
                message.set_read(0, self.number)
                print ("Process Producer : item %d produced and added to queue by producer NO. %s"\
                    % (item,self.number))
                sleep_time = random.uniform(self.sleep_start, self.sleep_end)
                time.sleep(sleep_time)                
            else:
                print('STOPPING PRODUCTION! Max size limit reached, Producer waiting, queues are full.')
                time.sleep(0.5)                
 



class consumer(multiprocessing.Process):
    def __init__(self, queue, number, stop_event, sleep_start, sleep_end):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.number = number
        self.stop_event = stop_event
        self.sleep_start = sleep_start
        self.sleep_end = sleep_end


    def run(self):

        global MAX_SIZE

        waiting = 0
        items = []

        while not self.stop_event.is_set():
            item_list = []
            while True:
                if not self.queue.empty():
                    T = self.queue.get()
                    if not T.check_read(1, self.number):
                        message_type, process_number, item = T.get_info(1, self.number)
                        if message_type == 0:
                            waiting += 1
                            items.append((process_number, item))
                        elif message_type == 1:
                            if (process_number, item) in items:
                                items.remove((process_number, item))
                            waiting -= 1   
                        item_list.append(T)
                else:
                    break

            for item in item_list:
                if not item.check_list():
                    self.queue.put(item)


            if waiting > 0:
                
                number, item = items[0]
                message = Message(1, number, item)
                message.set_read(1, self.number)
                self.queue.put(message)
                items.remove((number, item))
                waiting -= 1
                print (f'Process Consumer : item {item} which is produced by producer number {number} consumed and poped from queue by consumer NO. {self.number}')
                sleep_time = random.uniform(self.sleep_start, self.sleep_end)
                time.sleep(sleep_time)  
            else :
                print('STOPING CONSUMPTION! size is zero, consumer waiting, queues are empty.')
                time.sleep(0.5)     



if __name__ == '__main__':
    queue = multiprocessing.Queue()
    stop_event: Event = multiprocessing.Event()

    process_producer = [producer(queue, i, stop_event, 0.4, 0.6) for i in range(PRODUCER_NUMBER)]
    process_consumer = [consumer(queue, i, stop_event,0.9, 1.1)for i in range(CONSUMER_NUMBER)]
    for produce in process_producer:

        produce.start()
    for consume in process_consumer:

        consume.start()
    time.sleep(20)
    print('Program runtime has finished, stopping ...')
    stop_event.set()
    for produce in process_producer:

        produce.join()
    for consume in process_consumer:

        consume.join()



        
        
         
