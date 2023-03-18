import os
import subprocess

def getResult(command):
    tt = os.popen(command)
    return tt.read()

def sumScore():
    score = 0
    for i in range(4):
        res = getResult(
            'H:\\PROJECT\\2023HW\\WindowsRelease\\Robot.exe -m H:\\PROJECT\\2023HW\\WindowsRelease\\maps/'+str(i+1)+'.txt -c H:\\PROJECT\\2023HW\\WindowsRelease\\2023HuaWei_HDU_HZD\\our "python main.py" -f')
        resList = res.split('"score":')
        scoreList = resList[1].split('}')
        thisScore = scoreList[0]
        score += int(thisScore)
    return score

if __name__ == "__main__":
    print(sumScore())