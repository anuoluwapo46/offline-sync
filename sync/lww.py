from dataclasses import dataclass

@dataclass
class Entry:
    value: object
    ts: float
    device: str

class LWWStore:
    def __init__(self):
        self.entries = {}

    def write(self, key, value, ts, device):
        new = Entry(value, ts, device)
        old = self.entries.get(key)
        if old is None or (new.ts, new.device) > (old.ts, old.device):
            self.entries[key] = new

    def merge(self, other):
        for key, entry in other.entries.items():
            self.write(key, entry.value, entry.ts, entry.device)

