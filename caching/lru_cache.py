import uuid
from caching.data_entry import Entry


class LRUCache:
    """This is a class for least recently used cache"""
    def __init__(self, location, size=None):
        """
        The constructor for LRUCache

        Parameters:
            location (Location): A location object representing the location of the cache
            size (int): The size of the cache
        """
        self._start = None
        self._end = None
        self._hash_map = {}
        self._size = size if size else 3
        self._is_expired = False
        self._location = location
        self._id = uuid.uuid4()

    @property
    def id(self):
        """Get the id of the cache"""
        return self._id

    @property
    def is_expired(self):
        """Get the expiration of the cache"""
        return self._is_expired

    @property
    def location(self):
        """Get the location of the cache"""
        return self._location

    @location.setter
    def location(self, value):
        """Set the location of the cache"""
        self._location = value

    @property
    def least_recently_used(self):
        """Get the entry at the bottom of the LRU cache"""
        return self._end

    @property
    def most_recently_used(self):
        """Get the entry on the top of the LRU cache"""
        return self._start

    def activate(self):
        """This function activate the cache"""
        self._is_expired = False

    def deactivate(self):
        """This function deactivate the cache"""
        self._is_expired = True

    def _move_entry_to_top(self, entry):
        """
        This function moves the entry to the top of the LRU cache

        Parameters:
            entry (Entry): The entry object to be removed
        """
        if self._start:
            self._start.left = entry
        entry.right = self._start
        entry.left = None
        self._start = entry
        if not self._end:
            self._end = self._start

    def _remove_entry(self, entry):
        """
        This function removes entry from the cache

        Parameters:
            entry (Entry): The entry object to be removed
        """
        if entry.left:
            entry.left.right = entry.right
        else:
            self._start = entry.right
        if entry.right:
            entry.right.left = entry.left
        else:
            self._end = entry.left

    def getEntry(self, key):
        """
        This function gets data from the cache

        Parameters:
            key (int): The key to the data to retrieve

        Returns:
            data (string): The data retrieved or None object
        """
        if key in self._hash_map:
            entry = self._hash_map.get(key)
            if entry.left != None:
                self._remove_entry(entry)
                self._move_entry_to_top(entry)
            return entry.value
        return None

    def addEntry(self, key, value):
        """
        This function adds or update cache and move entry to the top of LRU cache

        Parameters:
            key (int): The key of the data to be added
            value (string): Data to be stored
        """
        if key in self._hash_map:
            self._hash_map[key].value = value
            entry = self._hash_map.get(key)
            if entry.left != None:
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

    def update_cache_from(self, cache):
        """
        This function updates the cache from updates received

        Parameters:
            cache (LRUCache): The cache object with update
        """
        self._start = cache._start
        self._end = cache._end
        self._hash_map = cache._hash_map
