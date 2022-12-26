import time


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()

def decrypt_ch(ch):
    if ch == "-":
        return -1
    elif ch == "=":
        return -2
    return int(ch)

def decrypt(string):
    n = 0
    for i, ch in enumerate(string[::-1]):
        n += decrypt_ch(ch) * 5**i
    return n

def encrypt(n):
    res = ""
    while n > 0:
        cif = n % 5
        n //= 5
        if cif < 3:
            res = str(cif) + res
        elif cif == 3:
            n += 1
            res = "=" + res
        elif cif == 4:
            n += 1
            res = "-" + res
    return res

def task1(text):
    values = [decrypt(line) for line in text.strip().split("\n")]
    s = sum(values)
    return encrypt(s)

def task2(text: str):
    return "TODO"


if __name__ == "__main__":
    start_t = time.time()
    inp = fts("25in.txt")
    print(task1(inp))
    print(f"{time.time() - start_t} s")
    start_t = time.time()
    print(task2(inp))
    print(f"{time.time() - start_t} s")