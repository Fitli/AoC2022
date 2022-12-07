import re
from typing import Optional, List


class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.is_dir = True
        self.size = 0
        self.content = {}

    def ls_line(self, name: str, size: str):
        if name in self.content:
            return
        if size == "dir":
            new_d = Dir(name, self)
            self.content[name] = new_d
        else:
            new_f = File(name, self, int(size))
            self.content[name] = new_f

    def recalculate_size(self):
        self.size = sum([item.size for item in self.content.values()])
        return self.size

    def find_min_bigger(self, lower_bound: int) -> int:
        m_size = self.size
        for ch in self.content.values():
            if ch.is_dir and ch.size > lower_bound:
                m_size = min(m_size, ch.find_min_bigger(lower_bound))
        return m_size

    def cd(self, new_dir_name: str) -> ('Dir', int):
        if new_dir_name == "..":
            self.recalculate_size()
            return self.parent, self.size
        return self.content[new_dir_name], 0


class File:
    def __init__(self, name, parent, size):
        self.name = name
        self.parent = parent
        self.size = size
        self.is_dir = False


def read_lines(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return f.readlines()


def task1(lines: List[str]) -> int:
    d = None
    s = 0
    for line in lines:
        line = line.strip()
        cd_match = re.match(r"\$ cd (.+)$", line)
        if cd_match:
            if not d:
                d, size = Dir(cd_match.group(1), d), 0
            else:
                d, size = d.cd(cd_match.group(1))
            if size < 100000:
                s += size
        ls_match = re.match(r"(dir|\d+) (.+)$", line)
        if ls_match:
            d.ls_line(ls_match.group(2), ls_match.group(1))
    while d:
        d.recalculate_size()
        if d.size < 100000:
            s += d.size
        d = d.parent
    return s


def task2(lines: List[str]) -> int:
    d = None
    for line in lines:
        line = line.strip()
        cd_match = re.match(r"\$ cd (.+)$", line)
        if cd_match:
            if not d:
                d = Dir(cd_match.group(1), d)
            else:
                d, size = d.cd(cd_match.group(1))
        ls_match = re.match(r"(dir|\d+) (.+)$", line)
        if ls_match:
            d.ls_line(ls_match.group(2), ls_match.group(1))

    while d.parent:
        d.recalculate_size()
        d = d.parent
    root_size = d.recalculate_size()

    return d.find_min_bigger(30000000 - (70000000 - root_size))


lns = read_lines("07in.txt")
print(task1(lns))
print(task2(lns))
