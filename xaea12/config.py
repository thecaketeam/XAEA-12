import os
import json

class Config:
    def __init__(self, name):
        self.name = name

        self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.name, 'r') as f:
                self._config = json.load(f)
        except Exception:
            self._config = {}

    def save(self):
        with open(self.name, 'w') as f:
            json.dump(self._config.copy(), f)

    def get(self, key, *args):
        return self._config.get(key, *args)

    def put(self, key, value):
        self._conifg[key] = value
        self.save()

    def remove(self, key):
        del self._config[key]
        self.save()

    def __contains__(self, item):
        return str(item) in self._db

    def __getitem__(self, item):
        return self._db[str(item)]

    def __len__(self):
        return len(self._db)
