def calories():
    with open("input1.txt") as f:
        maximum = 0
        suma = 0
        for line in f:
            if line == "\n":
                if suma > maximum:
                    maximum = suma
                suma = 0
            else:
                suma += int(line)
    return max(maximum, suma)

def check(suma, max3):
    for i in range(1,4):
        if(suma >= max3[-i]):
            max3.insert(3-i+1, suma)
            max3.pop(0)
            break
    print(max3)

def calories2():
    with open("input1.txt") as f:
        max3 = [0,0,0]
        suma = 0
        for line in f:
            if line == "\n":
                check(suma, max3)
                suma = 0
            else:
                suma += int(line)
    #check(suma, max3)
    print(max3)
    return sum(max3)

print(calories2())
