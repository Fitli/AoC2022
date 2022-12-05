my_shapes = {"X": "rock",
             "Y": "paper",
             "Z": "scissors"}

opponent_shapes = {"A": "rock",
                   "B": "paper",
                   "C": "scissors"}

shape_values = {"rock": 1,
                "paper": 2,
                "scissors": 3}

win_values = {("rock", "rock"): 3,
              ("paper", "paper"): 3,
              ("scissors", "scissors"): 3,
              ("rock", "paper"): 0,
              ("rock", "scissors"): 6,
              ("paper", "rock"): 6,
              ("paper", "scissors"): 0,
              ("scissors", "rock"): 0,
              ("scissors", "paper"): 6}

my_results = {"X": 0,
              "Y": 3,
              "Z": 6}

my_strategies = {(his_s, res): my_s for (my_s, his_s), res in win_values.items()}


def task1(filename: str) -> int:
    s = 0
    with open(filename, "r") as f:
        for line in f:
            his, my = line.strip().split()
            his = opponent_shapes[his]
            my = my_shapes[my]
            s += shape_values[my]
            s += win_values[(my, his)]
    return s


def task2(filename: str) -> int:
    s = 0
    with open(filename, "r") as f:
        for line in f:
            his, my = line.strip().split()
            his = opponent_shapes[his]
            my = my_strategies[(his, my_results[my])]
            s += shape_values[my]
            s += win_values[(my, his)]
    return s


print(task1("02in.txt"))
print(task2("02in.txt"))
