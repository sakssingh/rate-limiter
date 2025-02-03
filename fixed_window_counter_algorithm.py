import threading
import time

class FixedWindowCounterAlgorithm:
    def __init__(self, rate: int, window_size: int):
        self.rate = rate
        self.window_size = window_size
        self.windows = {}
        thread = threading.Thread(target=self.reset_counter_for_each_window, daemon=True)
        thread.start()

    def is_valid(self, client_ip) -> bool:
        print(len(self.windows))
        if client_ip in self.windows:
            if self.windows[client_ip].request_counter >= self.rate:
                return False
            self.windows[client_ip].request_counter += 1
            return True
        else:
            new_window = _Window(client_ip, self.rate, self.window_size)
            new_window.request_counter += 1
            self.windows[client_ip] = new_window
            return True

    def reset_counter_for_each_window(self) -> None:
        while True:
            time.sleep(self.window_size)
            for key in self.windows:
                self.windows[key].request_counter = 0 

class _Window:
    def __init__(self, client_ip, rate, window_size):
        self.client_ip = client_ip
        self.rate = rate
        self.window_size = window_size
        self.request_counter = 0