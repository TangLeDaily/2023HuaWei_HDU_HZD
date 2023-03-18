

if __name__ == "__main__":
    ff = open("testRandom.txt", "r", encoding="utf - 8")
    ww = open("best50file.txt", "w", encoding="utf - 8")
    list = ff.readlines()
    listOut = sorted(list, reverse=True, key=lambda x: int(x.split(' ')[0]))

    for i in range(50):
        if i >= len(listOut):
            break
        print(listOut[i])
        ww.write(listOut[i])

    ff.close()
    ww.close()