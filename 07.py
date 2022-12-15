import re
from typing import List


class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.is_dir = True
        self.size = 0
        self.content = {}

    def cd(self, new_dir_name: str) -> 'Dir':
        if new_dir_name == "..":
            self.recalculate_size()
            return self.parent
        return self.content[new_dir_name]

    def ls_line(self, name: str, size: str) -> None:
        if name in self.content:
            return
        if size == "dir":
            self.content[name] = Dir(name, self)
        else:
            self.content[name] = File(name, self, int(size))

    def recalculate_size(self) -> int:
        self.size = sum([item.size for item in self.content.values()])
        return self.size

    def find_min_bigger(self, lower_bound: int) -> int:
        m_size = self.size
        for ch in self.content.values():
            if ch.is_dir and ch.size > lower_bound:
                m_size = min(m_size, ch.find_min_bigger(lower_bound))
        return m_size

    def find_sum_of_all_smaller(self, upper_bound: int) -> int:
        s = 0
        if self.size <= upper_bound:
            s += self.size
        for ch in self.content.values():
            if ch.is_dir:
                s += ch.find_sum_of_all_smaller(upper_bound)
        return s


class File:
    def __init__(self, name, parent, size):
        self.name = name
        self.parent = parent
        self.size = size
        self.is_dir = False


def fts(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def tree_from_lines(lines: List[str]) -> Dir:
    d = None
    for line in lines:
        line = line.strip()
        cd_match = re.match(r"\$ cd (.+)$", line)
        if cd_match:
            if not d:
                d = Dir(cd_match.group(1), d)
            else:
                d = d.cd(cd_match.group(1))
        ls_match = re.match(r"(dir|\d+) (.+)$", line)
        if ls_match:
            d.ls_line(ls_match.group(2), ls_match.group(1))
    while d.parent:
        d.recalculate_size()
        d = d.parent
    d.recalculate_size()
    return d


def task1(text: str) -> int:
    lines = text.strip().split("\n")
    root = tree_from_lines(lines)
    return root.find_sum_of_all_smaller(100000)


def task2(text: str) -> int:
    lines = text.strip().split("\n")
    root = tree_from_lines(lines)
    return root.find_min_bigger(30000000 - (70000000 - root.size))


if __name__ == "__main__":
    inp = fts("07in.txt")
    print(task1(inp))
    print(task2(inp))
