import threading
import time
import random

BUFFER_SIZE = 5
NUM_PRODUCERS = 3
NUM_CONSUMERS = 2
BUFFER = []

empty_slots = threading.Semaphore(BUFFER_SIZE)
full_slots = threading.Semaphore(0)
mutex = threading.Lock()
stop_event = threading.Event()


def producer(producer_id):
    while not stop_event.is_set():
        item = random.randint(1, 100)
        if empty_slots.acquire(timeout=1):
            with mutex:
                BUFFER.append(item)
                print(
                    f"[Producer-{producer_id}] Added {item}. Buffer: {BUFFER}"
                )
            full_slots.release()
            time.sleep(random.uniform(0.5, 1.5))


def consumer(consumer_id):
    while not stop_event.is_set():
        if full_slots.acquire(timeout=1):
            with mutex:
                if BUFFER:
                    item = BUFFER.pop(0)
                    print(
                        f"[Consumer-{consumer_id}] Taken {item}. "
                        f"Buffer: {BUFFER}"
                    )
            empty_slots.release()
            time.sleep(random.uniform(1.0, 2.0))


if __name__ == "__main__":
    threads = []

    for i in range(NUM_PRODUCERS):
        t = threading.Thread(target=producer, args=(i,))
        threads.append(t)
        t.start()

    for i in range(NUM_CONSUMERS):
        t = threading.Thread(target=consumer, args=(i,))
        threads.append(t)
        t.start()

    time.sleep(7)
    print("\n--- Stopping threads ---")
    stop_event.set()

    for t in threads:
        t.join()

    print("All threads stopped. Program finished.")
