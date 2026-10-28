"""A doubly linked list with insertion, removal, and bidirectional traversal."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class _Node(Generic[T]):
    value: T
    previous: _Node[T] | None = None
    next: _Node[T] | None = None


class DoublyLinkedList(Generic[T]):
    """A mutable list whose nodes link to both their neighbors."""

    def __init__(self) -> None:
        self._head: _Node[T] | None = None
        self._tail: _Node[T] | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: object) -> bool:
        return any(item == value for item in self)

    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __reversed__(self) -> Iterator[T]:
        current = self._tail
        while current is not None:
            yield current.value
            current = current.previous

    def __repr__(self) -> str:
        return f"DoublyLinkedList({list(self)!r})"

    def append(self, value: T) -> None:
        """Add a value to the end of the list."""
        node = _Node(value, previous=self._tail)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def prepend(self, value: T) -> None:
        """Add a value to the start of the list."""
        node = _Node(value, next=self._head)
        if self._head is None:
            self._tail = node
        else:
            self._head.previous = node
        self._head = node
        self._size += 1

    def insert_after(self, target: T, value: T) -> bool:
        """Insert after the first matching target; return False if not found."""
        current = self._head
        while current is not None and current.value != target:
            current = current.next

        if current is None:
            return False

        node = _Node(value, previous=current, next=current.next)
        if current.next is None:
            self._tail = node
        else:
            current.next.previous = node
        current.next = node
        self._size += 1
        return True

    def find(self, value: T) -> int | None:
        """Return the index of the first matching value, or None."""
        for index, item in enumerate(self):
            if item == value:
                return index
        return None

    def remove(self, value: T) -> bool:
        """Remove the first matching value; return False if not found."""
        current = self._head
        while current is not None and current.value != value:
            current = current.next

        if current is None:
            return False

        if current.previous is None:
            self._head = current.next
        else:
            current.previous.next = current.next

        if current.next is None:
            self._tail = current.previous
        else:
            current.next.previous = current.previous

        self._size -= 1
        return True

    def clear(self) -> None:
        """Remove all values from the list."""
        self._head = None
        self._tail = None
        self._size = 0


if __name__ == "__main__":
    numbers = DoublyLinkedList[int]()
    numbers.append(10)
    numbers.append(30)
    numbers.prepend(5)
    numbers.insert_after(10, 20)

    print("Forward:", list(numbers))
    print("Backward:", list(reversed(numbers)))
    print("Index of 20:", numbers.find(20))
    numbers.remove(20)
    print("After removing 20:", list(numbers))
