import uuid
from caching.data_entry import Entry


class LRUCache:
    def __init__(self, location, size=None):
        self._start = None
        self._end = None
        self._hash_map = {}
        self._size = size if size else 3
        self._is_expired = False
        self._location = location
        self._id = uuid.uuid4()

    @property
    def id(self):
        return self._id

    @property
    def is_expired(self):
        return self._is_expired

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def least_recently_used(self):
        return self._end

    @property
    def most_recently_used(self):
        return self._start

    def activate(self):
        self._is_expired = False

    def deactivate(self):
        self._is_expired = True

    def _move_entry_to_top(self, entry):
        if self._start:
            self._start.left = entry
        entry.right = self._start
        entry.left = None
        self._start = entry
        if not self._end:
            self._end = self._start

    def _remove_entry(self, entry):
        if entry.left:
            entry.left.right = entry.right
        else:
            self._start = entry.right
        if entry.right:
            entry.right.left = entry.left
        else:
            self._end = entry.left

    def getEntry(self, key):
        if key in self._hash_map:
            entry = self._hash_map.get(key)
            self._remove_entry(entry)
            self._move_entry_to_top(entry)
            return entry.value
        return None

    def addEntry(self, key, value):
        if key in self._hash_map:
            self._hash_map[key].value = value
            entry = self._hash_map.get(key)
            self._remove_entry(entry)
            self._move_entry_to_top(entry)
        else:
            entry = Entry()
            entry.key = key
            entry.value = value
            if len(self._hash_map.keys()) == self._size:
                del self._hash_map[self._end.key]
                self._remove_entry(self._end)
                self._move_entry_to_top(entry)
            else:
                self._move_entry_to_top(entry)
            self._hash_map[entry.key] = entry

    def update_cache_from(cache):
        location = self._location
        self = cache
        self._location = location
