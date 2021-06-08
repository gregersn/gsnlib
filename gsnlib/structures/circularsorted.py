from typing import List
from collections import UserList


class CircularSorted(UserList):
    data: List[int]

    def append(self, item: int):
        if len(self.data) < 1:
            self.data.append(item)
            return

        if item < self.data[0]:
            i = len(self.data) - 1
            while i > 0 and self.data[i] > item and self.data[i] < self.data[0]:
                i -= 1
            self.data.insert(i + 1, item)

        else:
            i = 0
            while i < len(self.data) and self.data[i] < item:
                i += 1
            self.data.insert(i, item)
