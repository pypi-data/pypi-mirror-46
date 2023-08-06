""" Module for container classes that access items specific to a data type. """

from typing import AbstractSet, Collection, Iterator, MutableMapping, MutableSequence, MutableSet, Sequence

from .collection import use_if_object_is
from .container import Container, MutableContainer, MutableKeyContainer
from spectra_lexer.types import delegate_to


@use_if_object_is(Collection)
class SizedContainer(Container):
    """ A sized iterable item container. The most generic acceptable type of iterable container.
        No order is assumed, so the items may be sorted for display. Mappings do not need a subclass beyond this. """

    _AUTOSORT_MAXSIZE: int = 200

    __len__ = delegate_to("_obj")

    def __iter__(self) -> Iterator:
        """ If the container is under a certain size, attempt to sort its objects by key.
            A sort operation may fail if some keys aren't comparable. """
        if len(self) < self._AUTOSORT_MAXSIZE:
            try:
                return iter(sorted(self._obj))
            except TypeError:
                pass
        return iter(self._obj)

    __getitem__ = delegate_to("_obj")

    def type_str(self) -> str:
        """ Add the number of items to the type field. """
        n = len(self)
        return f" - {n} item" + "s" * (n != 1)


@use_if_object_is(MutableMapping)
class MutableMappingContainer(SizedContainer, MutableKeyContainer):
    """ The default methods work well for mappings. No changes need to be made. """


@use_if_object_is(AbstractSet)
class SetContainer(SizedContainer):

    key_tooltip = "Hash value of the object. Cannot be edited."

    def __getitem__(self, key):
        """ The key is the item itself. """
        if key in self._obj:
            return key
        raise KeyError(key)

    def key_str(self, key) -> str:
        """ Since the items are both the keys and the values, display the hashes in the key field. """
        return str(hash(key))


@use_if_object_is(MutableSet)
class MutableSetContainer(SetContainer, MutableContainer):

    def __delitem__(self, key) -> None:
        """ The key is the old item itself. Remove it. """
        self._obj.discard(key)

    def __setitem__(self, key, value) -> None:
        """ The key is the old item itself. Remove it and add the new item. """
        del self[key]
        self._obj.add(value)


@use_if_object_is(Sequence)
class SequenceContainer(SizedContainer):

    def __iter__(self) -> Iterator:
        """ Generate sequential index numbers as the keys. """
        return iter(range(len(self)))

    def key_str(self, key:int) -> str:
        """ Add a dot in front of each index for clarity. """
        return f".{key}"


@use_if_object_is(MutableSequence)
class MutableSequenceContainer(SequenceContainer, MutableKeyContainer):

    key_tooltip = "Double-click to move this item to a new index (non-negative integers only)."

    def moveitem(self, old_key:int, new_key:str) -> None:
        """ Moving a sequence item from one index to another can be done, but it will affect every item before it. """
        k = int(new_key)
        self[k:k] = [self[old_key]]
        del self[old_key + (old_key >= k)]
