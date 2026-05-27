import threading
import random
import time

buffer = []
BUFFER_LIMIT = 5
condition = threading.Condition()
stop_event = threading.Event()

def producer(producer_id):
    while not stop_event.is_set():
        item = random.randint(1, 100)
        with condition:
            while len(buffer) >= BUFFER_LIMIT and not stop_event.is_set():
                condition.wait()
            
            if not stop_event.is_set():
                buffer.append(item)
                print(f"[Producer-{producer_id}] Added {item}. Buffer: {buffer}")
                condition.notify_all()
        
        time.sleep(random.uniform(0.5, 1.5))

def consumer(consumer_id):
    while not stop_event.is_set():
        with condition:
            while not buffer and not stop_event.is_set():
                condition.wait()
            
            if buffer:
                item = buffer.pop(0)
                print(f"[Consumer-{consumer_id}] Consumed {item}. Buffer: {buffer}")
        
        time.sleep(random.uniform(1.0, 2.0))
