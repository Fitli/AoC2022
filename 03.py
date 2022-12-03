def fts(path):
    with open(path, "r") as f:
        return f.read()

def to_priority(item):
    if(item == item.lower()):
        return ord(item)-ord("a")+1
    else:
        return ord(item)-ord("A")+27

a = fts("03_in.txt").split()
suma = 0
for it in a:
    middle = len(it)//2
    letters = set(it[:middle])
    for i in range(middle, middle*2):
        if it[i] in letters:
            suma += to_priority(it[i])
            break;
print(suma)
            
print("TASK TWO")

suma = 0
for j in range(len(a)//3):
    it = a[3*j]
    letters = set(it)
    letters = letters.intersection(a[3*j+1])
    letters = letters.intersection(a[3*j+2])
    suma += to_priority(letters.pop())
print(suma)
