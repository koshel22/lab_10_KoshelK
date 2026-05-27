import threading
import time
import random

BUFFER_SIZE = 5
BUFFER = []

empty_slots = threading.Semaphore(BUFFER_SIZE)
full_slots = threading.Semaphore(0)
mutex = threading.Lock()
stop_event = threading.Event()

def producer():
    while not stop_event.is_set():
        item = random.randint(1, 100)
        if empty_slots.acquire(timeout=1):
            with mutex:
                BUFFER.append(item)
                print(f"[Producer] Додав: {item}. Буфер: {BUFFER}")
            full_slots.release()
            time.sleep(random.uniform(0.5, 1.0))

def consumer():
    while not stop_event.is_set():
        if full_slots.acquire(timeout=1):
            with mutex:
                item = BUFFER.pop(0)
                print(f"[Consumer] Забрав: {item}. Буфер: {BUFFER}")
            empty_slots.release()
            time.sleep(random.uniform(0.5, 1.0))

if __name__ == "__main__":
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    
    t1.start()
    t2.start()
    
    time.sleep(5)
    stop_event.set()
    
    t1.join()
    t2.join()
    print("Виконання програми закінчено.")