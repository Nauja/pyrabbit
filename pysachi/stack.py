__all__ = ["Stack"]


class Stack:
    def __init__(self):
        self._stack = []

    @property
    def depth(self):
        return len(self._stack)

    @property
    def parent(self):
        return self.at(self.depth - 2)

    def _push(self, item):
        self._stack.append(item)

    def pop(self):
        return self._stack.pop()

    @property
    def peek(self):
        return self._stack[self.depth - 1] if self.depth > 0 else None

    def at(self, index):
        return self._stack[index] if self.depth > index else None
