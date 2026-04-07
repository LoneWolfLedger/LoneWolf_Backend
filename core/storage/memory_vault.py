import json, os, threading
class ThreadSafeVault:
    def __init__(self, file_path="matrix_ledger.json"):
        self.file_path = file_path
        self.lock = threading.Lock()
        self.memory_cache = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f: self.memory_cache = json.load(f)
    def get_matrix(self):
        with self.lock: return self.memory_cache
    def update_matrix(self, new_data):
        with self.lock:
            self.memory_cache = new_data
            with open(self.file_path, "w") as f: json.dump(self.memory_cache, f)
            return True
vault = ThreadSafeVault()
