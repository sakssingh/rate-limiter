import threading
import time

class BucketTokenAlgorithm:
    def __init__(self, rate: int):
        self.rate = rate
        self.buckets = []
        thread = threading.Thread(target=self._add_token_to_each_bucket, daemon=True)
        thread.start()

    def _add_token_to_each_bucket(self):
        while True:
            time.sleep(1)
            for bucket in self.buckets:
                if bucket.tokens < bucket.max_tokens:
                    bucket.tokens += 1

    def is_valid(self, client_ip: str) -> bool:
        for b in self.buckets:
            if b.client == client_ip:
                return b.is_valid()
        else:
            new_bucket = _Bucket(client_ip, self.rate)
            self.buckets.append(new_bucket)
            return new_bucket.is_valid()

class _Bucket:
    def __init__(self, client: str, tokens: int):
        self.client = client
        self.max_tokens = tokens
        self.tokens = tokens 
    
    def is_valid(self) -> bool:
        if (self.tokens > 0):
            self.tokens -= 1;
            return True
        else:
            return False
