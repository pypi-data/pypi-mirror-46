from collections import UserDict


class Lazy(UserDict):
    def __getitem__(self, key):
        value = super().__getitem__(key)
        if callable(value):
            value = value(self)
        return value
