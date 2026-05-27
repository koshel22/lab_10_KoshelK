import threading
import random
import time

BUFFER_LIMIT = 5
NUM_PRODUCERS = 3
NUM_CONSUMERS = 2
buffer = []

condition = threading.Condition()
stop_event = threading.Event()


def producer(p_id):
    while not stop_event.is_set():
        item = random.randint(1, 100)
        with condition:
            while (
                len(buffer) >= BUFFER_LIMIT
                and not stop_event.is_set()
            ):
                condition.wait()
            if not stop_event.is_set():
                buffer.append(item)
                print(
                    f"[Producer-{p_id}] Added {item}. Buffer: {buffer}"
                )
                condition.notify_all()
        time.sleep(random.uniform(0.5, 1.0))


def consumer(c_id):
    while not stop_event.is_set():
        with condition:
            while not buffer and not stop_event.is_set():
                condition.wait()
            if buffer:
                item = buffer.pop(0)
                print(
                    f"[Consumer-{c_id}] Consumed {item}. Buffer: {buffer}"
                )
                condition.notify_all()
        time.sleep(random.uniform(1.0, 1.5))


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

    try:
        time.sleep(5)
    finally:
        print("\n--- Stopping monitor task ---")
        stop_event.set()
        with condition:
            condition.notify_all()

        for t in threads:
            t.join()
    print("Monitor task finished.")
