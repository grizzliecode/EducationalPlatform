with open("output.txt", "w") as fout:
    with open("input.txt") as fin:
        n = int(fin.readline())
        acc = 0
        for i in range(n):
            x = int(fin.readline())
            acc += x
            fout.write(str(x)+"\n")