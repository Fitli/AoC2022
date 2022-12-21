import time
from typing import List


def construct(items, start, end, parent, side):
    tree = IntervalTree(parent, side)
    tree.size = end - start
    if tree.size == 1:
        tree.value = items[start]
    else:
        middle = start + tree.size // 2
        tree.left = construct(items, start, middle, tree, 0)
        tree.right = construct(items, middle, end, tree, 1)
    return tree


class IntervalTree:
    def __init__(self, parent, side):
        self.parent = parent
        self.side = side
        self.size = 0
        self.left = None
        self.right = None
        self.value = None

    def pop_nth(self, n):
        assert n < self.size
        if self.size == 1:
            if self.side == 0:
                self.parent.left = None
            else:
                self.parent.right = None
            self.parent = None
            return self
        if self.left.size > n:
            leaf = self.left.pop_nth(n)
            if self.left is None:
                if self.parent is None:
                    self.size = self.right.size
                    self.left = self.right.left
                    self.left.parent = self
                    self.right = self.right.right
                    self.right.parent = self
                    return leaf
                self.right.side = self.side
                self.right.parent = self.parent
                if self.side == 0:
                    self.parent.left = self.right
                else:
                    self.parent.right = self.right
        else:
            leaf = self.right.pop_nth(n-self.left.size)
            if self.right is None:
                if self.parent is None:
                    self.size = self.left.size
                    self.right = self.left.right
                    self.right.parent = self
                    self.left = self.left.left
                    self.left.parent = self
                    return leaf
                self.left.side = self.side
                self.left.parent = self.parent
                if self.side == 0:
                    self.parent.left = self.left
                else:
                    self.parent.right = self.left
        self.size -= 1
        return leaf

    def get_position(self):
        pos = 0
        x = self
        while x.parent:
            if x.side == 1:
                pos += x.parent.left.size
            x = x.parent
        return pos

    def insert(self, position, leaf):
        assert position <= self.size
        if self.size == 1:
            new_tree = IntervalTree(self.parent, self.side)
            if self.side == 0:
                self.parent.left = new_tree
            else:
                self.parent.right = new_tree
            self.parent = new_tree
            leaf.parent = new_tree

            if position == 0:
                new_tree.left = leaf
                leaf.side = 0
                new_tree.right = self
                self.side = 1
            else:
                new_tree.left = self
                self.side = 0
                new_tree.right = leaf
                leaf.side = 1
            new_tree.size = 2
            return
        if position <= self.left.size:
            self.left.insert(position, leaf)
        else:
            self.right.insert(position-self.left.size, leaf)
        self.size += 1

    def get_leaves(self, leaves):
        if self.size == 1:
            leaves.append(self)
            return
        self.left.get_leaves(leaves)
        self.right.get_leaves(leaves)


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def mix(numbers, iters):
    tree = construct(numbers, 0, len(numbers), None, None)
    leaves: List[IntervalTree] = []
    tree.get_leaves(leaves)
    for _ in range(iters):
        for leave in leaves:
            pos = leave.get_position()
            tree.pop_nth(pos)
            val = leave.value
            new_pos = (pos + val) % tree.size
            if new_pos == 0:
                new_pos = tree.size
            tree.insert(new_pos, leave)
    final_leaves = []
    tree.get_leaves(final_leaves)
    return [l.value for l in final_leaves]


def get_score(numbers):
    zero = 0
    for i, n in enumerate(numbers):
        if n == 0:
            zero = i
    return sum([numbers[(zero + i*1000) % len(numbers)] for i in range(1, 4)])


def task1(text):
    numbers = list(map(int, text.strip().split()))
    numbers = mix(numbers, 1)
    return get_score(numbers)


def task2(text):
    numbers = list(map(lambda x: int(x) * 811589153, text.strip().split()))
    numbers = mix(numbers, 10)
    return get_score(numbers)


if __name__ == "__main__":
    inp = fts("20in.txt")
    start_t = time.time()
    print(task1(inp))
    print(f"{time.time() - start_t} s")
    start_t = time.time()
    print(task2(inp))
    print(f"{time.time() - start_t} s")
