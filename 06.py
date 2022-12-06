from typing import Set


def fts(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def text_to_set(text: str) -> Set[str]:
    s = set()
    for ch in text:
        s.add(ch)
    return s


def find_first_marker(text: str, marker_len: int) -> int:
    for i in range(len(text) + 1 - marker_len):
        if len(text_to_set(text[i:i + marker_len])) == marker_len:
            return i + marker_len


inp = fts("06in.txt")
print(find_first_marker(inp, 4))
print(find_first_marker(inp, 14))
