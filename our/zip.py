import shutil
import os

if __name__ == '__main__':
    listFiles = os.listdir("version2")
    maxId = -1
    for strr in listFiles:
        maxId = max(maxId, int(strr.split('-')[2].split('.')[0]))
    maxId+=1
    shutil.make_archive("version2/beta-1-"+str(maxId), 'zip', "our")
