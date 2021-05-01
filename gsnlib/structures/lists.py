from typing import Union, Any


class DoubleLinkedNode():
    prev: Union['DoubleLinkedNode', None]
    next: Union['DoubleLinkedNode', None]
    data: Any

    def __init__(self, data):
        self.data = data

    def add(self, data) -> 'DoubleLinkedNode':
        n = self.__class__(data)
        self.next = n
        n.prev = self

        return n

    def remove(self,
               node: Union['DoubleLinkedNode', None] = None) ->\
            Union['DoubleLinkedNode', None]:
        if node is None:
            node = self

        if node.next and node.prev:
            node.next.prev = node.prev
            node.prev.next = node.next

        if node.next and not node.prev:
            node.next.prev = None

        if node.prev and not node.next:
            node.prev.next = None

        if node.prev:
            return node.prev
        elif node.next:
            return node.next

    def head(self) -> 'DoubleLinkedNode':
        c = self
        while c.prev is not None:
            c = c.prev
        return c

    def tail(self) -> 'DoubleLinkedNode':
        c = self
        while c.next is not None:
            c = c.next
        return c

    def length(self) -> int:
        cur = self.head()
        size = 0
        while cur.next is not None:
            size += 1
            cur = cur.next

        return size


class DoubleLinkedList():
    root: DoubleLinkedNode

    def __init__(self):
        pass
