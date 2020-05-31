"""
Source: https://github.com/anrom7/Graph_linked

Author: Andriy Romaniuk

Author's annotation: Common data and method implementations for collections.
Assumes that each collection type supports an iterator and
an add method.

Note: Modified to suit PEP recommendation
"""
from typing import Collection, Any, Iterator


class AbstractCollection:
    """Represent an abstract collection for all collection types."""

    def __init__(self, source_collection: Collection):
        """Will copy items to self from sourceCollection if it's present."""
        self._size = 0
        if source_collection:
            for item in source_collection:
                self.add(item)

    def add(self, item: Any):
        """Abstract method for further use."""
        raise NotImplemented("add method is an abstract method")

    def __len__(self) -> int:
        """Return The number of items in self."""
        return self._size

    def is_empty(self) -> bool:
        """Return True if collection is empty, False otherwise."""
        return len(self) == 0

    def __str__(self) -> str:
        """Return the string representation of the collection.

        Using the format [<item-1>, <item-2>, . . ., <item-n>].
        """
        return f"[{', '.join(map(str, self))}]"

    def __iter__(self) -> Iterator:
        """An abstract iterator method."""
        raise NotImplemented("itearation is not supported for abstract "
                             "collection")

    def __add__(self, other: Collection):
        """Return a new collection consisting of items in self and other."""
        result = type(self)(self)
        for item in other:
            result.add(item)
        return result

    def __eq__(self, other: Collection):
        """Compare two abstract collections."""
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if len(self) != len(other):
            return False
        other_items = iter(other)
        for item in self:
            if item != next(other_items):
                return False
        return True
