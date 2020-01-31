from caching.data_entry import Entry


class LRUCache:
    def __init__(self, size=None):
        self._start = None
        self._end = None
        self._hash_map = {}
        self._size = size if size else 3

    def _move_entry_to_top(entry):
        if self._start:
            self._start.left = entry
        entry.right = self._start
        entry.left = None
        self._start = entry
        if not self._end:
            self._end = self._start

    def _remove_entry(entry):
        if entry.left:
            entry.left.right = entry.right
        else:
            self._start = entry.right
        if entry.right:
            entry.right.left = entry.left
        else:
            self._end = entry.left

    def getEntry(key):
        if key in self._hash_map:
            entry = self._hash_map.get(key)
            self._remove_entry(entry)
            self._move_entry_to_top(entry)
            return entry.value
        return 'Not found, go fetch at store'

    def addEntry(key, value):
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
