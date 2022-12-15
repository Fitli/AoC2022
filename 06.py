from typing import Set, Dict


def fts(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def find_first_marker(text: str, marker_len: int) -> int:
    letters: Dict[str, int] = {}
    for i in range(len(text)):
        letters[text[i]] = letters.get(text[i], 0) + 1
        if i >= marker_len:
            letters[text[i-marker_len]] -= 1
            if letters[text[i-marker_len]] == 0:
                letters.pop(text[i-marker_len])
        if len(letters) == marker_len:
            return i + 1


def task1(text: str):
    return find_first_marker(text, 4)


def task2(text: str):
    return find_first_marker(text, 14)


if __name__ == "__main__":
    inp = fts("06in.txt")
    print(task1(inp))
    print(task2(inp))
