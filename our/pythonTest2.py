import datetime
import os
import random
import subprocess

# parser.add_argument("--towardSpeedAlpha", default=2.8, type=str, help="train root path")
# parser.add_argument("--towardSpeedBeta", default=-0.3, type=str, help="test root path")
# parser.add_argument("--boomDistance", default=2.6,  type=float, help="use cuda?")
# parser.add_argument("--slowSpeed", default=3.5, type=float, help="use cuda?")
# parser.add_argument("--initSpeed", default=6.8, type=float, help="use cuda?")
# parser.add_argument("--sellDistanceB", default=8, type=float, help="use cuda?")
def getResult(command):
    tt = os.popen(command)
    return tt.read()

def sumScore(a,b,c,d,e,f):
    score = 0
    for i in range(4):
        res = getResult(
            'H:\\PROJECT\\2023HW\\WindowsRelease\\Robot.exe -m H:\\PROJECT\\2023HW\\WindowsRelease\\maps/'+str(i+1)
            +'.txt -c H:\\PROJECT\\2023HW\\WindowsRelease\\2023HuaWei_HDU_HZD\\our "python main2.py --towardSpeedAlpha '+str(a)
            +' --towardSpeedBeta '+str(b)
            +' --boomDistance '+str(c)
            +' --slowSpeed '+str(d)
            + ' --initSpeed ' + str(e)
            + ' --sellDistanceB ' + str(f)
            +'" -f')
        resList = res.split('"score":')
        scoreList = resList[1].split('}')
        thisScore = scoreList[0]
        score += int(thisScore)
    print(score)
    return score

if __name__ == "__main__":

    for i in range(1000):
        ff = open("testRandom.txt", "a", encoding="utf - 8")
        a = round(random.random()*8,4)
        b = round(2-random.random()*4, 4)
        c = round(2+random.random()*1.5, 4)
        d = round(2+random.random()*3, 4)
        e = round(6 + random.random() * 2, 4)
        f = round(random.random() * 12, 4)
        print('H:\\PROJECT\\2023HW\\WindowsRelease\\Robot.exe -m H:\\PROJECT\\2023HW\\WindowsRelease\\maps/'+str(i+1)
            +'.txt -c H:\\PROJECT\\2023HW\\WindowsRelease\\2023HuaWei_HDU_HZD\\our "python main2.py --towardSpeedAlpha '+str(a)
            +' --towardSpeedBeta '+str(b)
            +' --boomDistance '+str(c)
            +' --slowSpeed '+str(d)
              + ' --initSpeed ' + str(e)
              + ' --sellDistanceB ' + str(f)
            +'" -f')
        score = sumScore(a,b,c,d,e,f)
        ff.write(str(score)+' --towardSpeedAlpha '+str(a)
            +' --towardSpeedBeta '+str(b)
            +' --boomDistance '+str(c)
            +' --slowSpeed '+str(d)
                + ' --initSpeed ' + str(e)
                + ' --sellDistanceB ' + str(f)
        + ' '+str(datetime.datetime.now())
                +'\n')
        ff.close()
