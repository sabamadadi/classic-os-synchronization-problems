import threading
import time
import random
import math
NUM_PHILOSOPHERS = 5
TERMINATE = True
room = threading.Semaphore(math.floor(NUM_PHILOSOPHERS / 2))
wait_list = []
forks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]


def philosopher(id):
    waiting = False
    global wait_list

    global TERMINATE
    while TERMINATE:
        if waiting:
            print('waiting for others due to preventing starvation')

        else:
            print(f"Philosopher {id} is thinking...")
            time.sleep(random.uniform(1, 3))
            wait_list.append(id)
        room.acquire()
        if wait_list[0] != id:
            room.release()
            time.sleep(0.05)
            waiting = True
        else:
            waiting = False
            wait_list.remove(id)
            left_fork = forks[id]
            right_fork = forks[(id + 1) % NUM_PHILOSOPHERS]

            left_fork.acquire()
            print(f"Philosopher {id} picked up the left fork.")

            right_fork.acquire()
            print(f"Philosopher {id} picked up the right fork.")

            print(f"Philosopher {id} is eating...")
            time.sleep(random.uniform(1, 2))

            left_fork.release()
            print(f"Philosopher {id} put down the left fork.")

            right_fork.release()
            print(f"Philosopher {id} put down the right fork.")

            room.release()


def main():
    philosophers = []
    for i in range(NUM_PHILOSOPHERS):
        t = threading.Thread(target=philosopher, args=(i,))
        philosophers.append(t)
        t.start()
    time.sleep(5)
    global TERMINATE
    TERMINATE = False
    for t in philosophers:
        t.join()


if __name__ == "__main__":
    main()
