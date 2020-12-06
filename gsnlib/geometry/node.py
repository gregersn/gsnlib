from __future__ import annotations

import logging
from typing import List, Union
from gsnlib.geometry.segment import Segment
from gsnlib.geometry.line import Line

logger = logging.getLogger(__file__)


class Node():
    def __init__(self, segments: List[Segment] = []):
        self.line: Union[Line, None] = None
        self.right = None
        self.left = None
        self.segments: List[Segment] = []
        if len(segments) > 0:
            self.build(segments)

    def __repr__(self) -> str:
        return f"<Node({self.segments})>"

    def __eq__(self, o) -> bool:
        equal = True

        equal = o is not None
        equal = equal and self is not None

        equal = equal and self.line == o.line
        equal = equal and self.right == o.right
        equal = equal and self.left == o.left
        equal = equal and self.segments == o.segments

        return equal

    def clone(self):
        node = Node()
        node.line = self.line.clone() if self.line is not None else None
        node.left = self.left.clone() if self.left is not None else None
        node.right = self.right.clone() if self.right is not None else None

        node.segments = [s.clone() for s in self.segments]
        return node

    def invert(self):
        for i in range(len(self.segments)):
            self.segments[i].flip()

        if self.line:
            self.line.flip()

        if self.right:
            self.right.invert()

        if self.left:
            self.left.invert()

        self.right, self.left = self.left, self.right

    def clip_segments(self, segments: List[Segment]) -> List[Segment]:
        logger.debug("node-clip_segments")
        if not self.line:
            return segments.copy()

        right: List[Segment] = []
        left: List[Segment] = []

        for i in range(len(segments)):
            self.line.split_segment(segments[i], right, left, right, left)

        if self.right:
            right = self.right.clip_segments(right)

        if self.left:
            left = self.left.clip_segments(left)
        else:
            left = []

        return right + left

    def clip_to(self, bsp: Node):
        self.segments = bsp.clip_segments(self.segments)
        if self.right:
            self.right.clip_to(bsp)

        if self.left:
            self.left.clip_to(bsp)

    def all_segments(self) -> List[Segment]:
        segments: List[Segment] = self.segments.copy()
        if self.right:
            segments += self.right.all_segments()
        if self.left:
            segments += self.left.all_segments()

        return segments

    def build(self, segments: List[Segment], level=1):
        if level > 50:
            raise RecursionError
        logger.debug("node-build")
        if not segments or len(segments) < 1:
            return

        if not self.line:
            self.line = segments[0].line.clone()

        right: List[Segment] = []
        left: List[Segment] = []

        for segment in segments:
            self.line.split_segment(segment,
                                    self.segments,
                                    self.segments,
                                    right,
                                    left)

        if len(right) > 0:
            if not self.right:
                self.right = Node()
            self.right.build(right.copy(), level=level + 1)

        if len(left) > 0:
            if not self.left:
                self.left = Node()
            self.left.build(left.copy(), level=level + 1)
