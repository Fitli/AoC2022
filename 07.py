import re
from typing import Optional, List


class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.is_dir = True
        self.size = 0
        self.content = {}


class File:
    def __init__(self, name, parent, size):
        self.name = name
        self.parent = parent
        self.size = size
        self.is_dir = False


def read_lines(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return f.readlines()


def recalculate_size(d: Dir):
    d.size = sum([item.size for item in d.content.values()])
    return d.size


def cd(d: Optional[Dir], new_dir_name: str) -> (Dir, int):
    if new_dir_name == "..":
        if d:
            recalculate_size(d)
        return d.parent, d.size
    if not d:
        return Dir(new_dir_name, d), 0
    return d.content[new_dir_name], 0


def ls_line(d: Dir, name: str, size: str):
    if name in d.content:
        return
    if size == "dir":
        new_d = Dir(name, d)
        d.content[name] = new_d
    else:
        new_f = File(name, d, int(size))
        d.content[name] = new_f


def task1(lines: List[str]) -> int:
    d = None
    s = 0
    for line in lines:
        line = line.strip()
        cd_match = re.match(r"\$ cd (.+)$", line)
        if cd_match:
            d, size = cd(d, cd_match.group(1))
            if size < 100000:
                s += size
        ls_match = re.match(r"(dir|\d+) (.+)$", line)
        if ls_match:
            ls_line(d, ls_match.group(2), ls_match.group(1))
    while d:
        recalculate_size(d)
        if d.size < 100000:
            s += d.size
        d = d.parent
    return s


def find_min_bigger(d: Dir, lower_bound: int) -> int:
    m_size = d.size
    for ch in d.content.values():
        if ch.is_dir and ch.size > lower_bound:
            m_size = min(m_size, find_min_bigger(ch, lower_bound))
    return m_size


def task2(lines: List[str]) -> int:
    d = None
    for line in lines:
        line = line.strip()
        cd_match = re.match(r"\$ cd (.+)$", line)
        if cd_match:
            d, size = cd(d, cd_match.group(1))
        ls_match = re.match(r"(dir|\d+) (.+)$", line)
        if ls_match:
            ls_line(d, ls_match.group(2), ls_match.group(1))

    while d.parent:
        recalculate_size(d)
        d = d.parent
    root_size = recalculate_size(d)

    return find_min_bigger(d, 30000000 - (70000000 - root_size))


lns = read_lines("07in.txt")
print(task1(lns))
print(task2(lns))
