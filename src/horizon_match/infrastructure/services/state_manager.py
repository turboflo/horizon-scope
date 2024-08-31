from queue import Queue
from threading import Lock
import time


class StateManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(StateManager, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._state = "Initializing"
        self._queue = Queue()
        self._running = True
        self._initialized = True

    def update_state(self, new_state):
        with self._lock:
            self._state = new_state
            self._queue.put(new_state)

    def get_current_state(self):
        with self._lock:
            return self._state

    def state_stream(self):
        while self._running:
            if not self._queue.empty():
                yield self._queue.get()
            else:
                time.sleep(0.1)  # Short sleep to prevent busy-waiting

    def stop(self):
        self._running = False
