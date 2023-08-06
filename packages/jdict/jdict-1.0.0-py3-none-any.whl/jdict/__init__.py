from collections import UserDict
import json
import sys
from typing import Any, Dict, Hashable, List, Optional, Tuple

# Prevent importing jdict from versions below 3.6
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    raise Exception("jdict will not behave correctly on Python versions below 3.6.")

Key = Hashable
Value = Any
KeyValuePair = Tuple[Key, Value]


class jdict(UserDict):
    """Dictionary extended with convenience methods that depend heavily on dictionaries being ordered by insertion order"""

    # Protect attributes used for housekeeping
    protected_keys = (
        "data",
        "_keys",
        "_values",
        "_items",
        "_keysvalid",
        "_valuesvalid",
        "_itemsvalid",
    )

    @staticmethod
    def _first(obj):
        """Helper: Returns the first element in the object"""
        for elem in obj:
            return elem

    @staticmethod
    def _last(obj):
        """Helper: Returns the last element in the object"""
        try:
            return obj[-1]
        except IndexError:
            return None

    @staticmethod
    def _at(idx: int, enumiterator):
        """Helper: Returns the n'th element in the enumerated iterator"""
        for _idx, *item in enumiterator:
            if idx == _idx:
                return tuple(item)
        raise IndexError(idx)

    def _pop(self, key: Key):
        """Helper: pops the item at the key"""
        if len(self.data) == 0:
            raise IndexError("pop from empty jdict")
        value = self.data[key]
        del self.data[key]
        self._invalidate()
        return key, value

    def __init__(self, data=None, **kwargs):
        """Sets attributes used for housekeeping"""
        if data is not None:
            if isinstance(data, dict):
                self.data = data
            else:
                kwargs["data"] = data
                self.data = kwargs
        else:
            self.data = kwargs

        self._cleanse()
        self._invalidate()

    def _cleanse(self):
        """Drops everything"""
        self._keys = []
        self._values = []
        self._items = []

    def _invalidate(self):
        """Sets all flags to invalid (so the key_list, value_list and itemlist must be recalculated)"""
        self._keysvalid = False
        self._valuesvalid = False
        self._itemsvalid = False

    def _key_is_protected(self, key: Key) -> bool:
        """whether the key is protected (should not override default __setattr__ for this key)"""
        return key in jdict.protected_keys

    def __getattr__(self, key: Key):
        """Makes jdict.x equivalent to jdict['x']"""
        try:
            return self.data[key]
        except KeyError as ke:
            raise AttributeError(key) from ke

    def __setattr__(self, key: Key, value: Value):
        """Makes jdict.x = y equivalent to jdict['x'] = y"""
        if self._key_is_protected(key):
            return object.__setattr__(self, key, value)
        else:
            self.data[key] = value
            self._invalidate()

    def __add__(self, other):
        return {**self.data, **other.data}

    def __iadd__(self, other):
        for key, value in other.data.items():
            self.data[key] = value

    @property
    def list(self) -> List[KeyValuePair]:
        """a list of the items ((key, value)-pairs)"""
        if not self._itemsvalid:
            self._items = list(self.data.items())
            self._itemsvalid = True
        return self._items

    @property
    def key_list(self) -> List[Key]:
        """a list of the keys"""
        if not self._keysvalid:
            self._keys = list(self.data)
            self._keysvalid = True
        return self._keys

    @property
    def value_list(self) -> List[Value]:
        """a list of the values"""
        if not self._valuesvalid:
            self._values = list(self.data.values())
            self._valuesvalid = True
        return self._values

    @property
    def first(self) -> KeyValuePair:
        """the first item ((key, value)-pair)"""
        return self._first(self.data.items())

    @property
    def first_key(self) -> Key:
        """the first key"""
        return self._first(self.data.keys())

    @property
    def first_value(self) -> Value:
        """the first value"""
        return self._first(self.data.values())

    @property
    def last(self) -> KeyValuePair:
        """the last item ((key, value)-pair)"""
        return self._last(self.list)

    @property
    def last_key(self) -> Key:
        """the last key"""
        return self._last(self.key_list)

    @property
    def last_value(self) -> Value:
        """the last value"""
        return self._last(self.value_list)

    @property
    def any(self) -> KeyValuePair:
        """an item ((key, value)-pair) with no guarantees about which one it is"""
        return self.first

    @property
    def any_key(self) -> Key:
        """any key with no guarantees about which one it is"""
        return self.first_key

    @property
    def any_value(self) -> Value:
        """any value with no guarantees about which one it is"""
        return self.first_value

    @property
    def range(self):
        """range(len(self))"""
        return range(len(self))

    @property
    def enum(self):
        """(idx, key, value)-tuples"""
        return zip(self.range, self.data.keys(), self.data.values())

    @property
    def enum_keys(self):
        """(idx, key)-pairs"""
        return enumerate(self.data.keys())

    @property
    def enum_values(self):
        """(idx, value)-pairs"""
        return enumerate(self.data.values())

    @property
    def json(self) -> str:
        """a JSON representation"""
        return json.dumps(self.data)

    @property
    def series(self):
        """a pandas Series representation"""
        import pandas as pd

        return pd.Series(index=self.key_list, data=self.value_list)

    @property
    def datacol(self):
        """a representation as a pandas DataFrame with one column"""
        import pandas as pd

        return pd.DataFrame(self.series)

    @property
    def datarow(self):
        """a representation as a pandas DataFrame with one row"""
        import pandas as pd

        try:
            return pd.DataFrame(index=[0], data=self.data)
        except Exception as e:
            print(e)
            raise

    def at(self, idx: int) -> KeyValuePair:
        """the item at the index"""
        return self._at(idx, self.enum)

    def key_at(self, idx: int) -> Key:
        """the key at the index"""
        return self.at(idx)[0]

    def value_at(self, idx: int) -> Value:
        """the value at the index"""
        return self.at(idx)[1]

    def pop_first(self) -> KeyValuePair:
        """Pops the first (key, value)-pair and returns it"""
        return self._pop(self.first_key)

    def pop_last(self) -> KeyValuePair:
        """Pops the last (key, value)-pair and returns it"""
        return self._pop(self.last_key)

    def pop_first_key(self) -> Key:
        """Pops the first (key, value)-pair and returns the key"""
        return self.pop_first()[0]

    def pop_last_key(self) -> Key:
        """Pops the last (key, value)-pair and returns the key"""
        return self.pop_last()[0]

    def pop_first_value(self) -> Value:
        """Pops the first (key, value)-pair and returns the value"""
        return self.pop_first()[1]

    def pop_last_value(self) -> Value:
        """Pops the last (key, value)-pair and returns the key"""
        return self.pop_last()[1]

    def mapping(self, key_func=lambda x: x, value_func=lambda x: x):
        """Maps the keys by key_func and the values by value_func"""
        return jdict(
            {key_func(key): value_func(value) for key, value in self.data.items()}
        )

    def item_mapping(self, item_func=lambda key, value: (key, value)):
        """Maps the key-value pairs by item_func"""
        return jdict(dict(item_func(key, value) for key, value in self.data.items()))

    def key_mapping(self, key_func=lambda x: x):
        """Maps the keys by key_func"""
        return self.mapping(key_func=key_func)

    def value_mapping(self, value_func=lambda x: x):
        """Maps the values by value_func"""
        return self.mapping(value_func=value_func)

    def select(self, key_func=lambda x: True, value_func=lambda x: True):
        """Filters out items where the key doesn't fulfill key_func or the value doesn't fulfill value_func"""
        return jdict(
            {
                key: value
                for key, value in self.data.items()
                if key_func(key) and value_func(value)
            }
        )

    def item_select(self, item_func: lambda k, v: True):
        """Filters out items where the (key, value)-pair doesn't fulfill item_func"""
        return jdict(
            {key: value for key, value in self.data.items() if item_func(key, value)}
        )

    def key_select(self, key_func=lambda x: True):
        """Filters out items where the key doesn't fulfill key_func"""
        return self.select(key_func=key_func)

    def value_select(self, value_func=lambda x: True):
        """Filters out items where the value doesn't fulfill value_func"""
        return self.select(value_func=value_func)
