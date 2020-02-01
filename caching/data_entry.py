class Entry:
    """This is class for data entry in a cache"""
    def __init__(self):
        """
        This a constructor for Entry class.

        Parameters:
        No parameter is required.
        """
        self._left = None
        self._right = None
        self._key = None
        self._value = None

    @property
    def left(self):
        """Get left entry"""
        return self._left

    @left.setter
    def left(self, value):
        """Set left entry"""
        self._left = value

    @property
    def right(self):
        """Get right entry"""
        return self._right

    @right.setter
    def right(self, value):
        """Set right entry"""
        self._right = value

    @property
    def key(self):
        """Get key for entry"""
        return self._key

    @key.setter
    def key(self, value):
        """Set key for entry"""
        self._key = value

    @property
    def value(self):
        """Get value for entry"""
        return self._value

    @value.setter
    def value(self, value):
        """Set value for entry"""
        self._value = value