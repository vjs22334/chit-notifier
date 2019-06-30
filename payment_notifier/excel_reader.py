import pandas as pd
import os
from os import listdir
from os.path import isfile,join

chitGroup = ""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def clean(filename):
   
    sheetX = read(filename)
    chitGroup = sheetX['Jagapathi Chits Pvt ltd'][6]

    print(chitGroup)

    sheetX = sheetX[7:]

    sheetX = sheetX.drop('Unnamed: 1',axis=1)
    sheetX = sheetX.drop('Unnamed: 2',axis=1)
    sheetX = sheetX.drop('Unnamed: 3',axis=1)
    sheetX = sheetX.drop('Unnamed: 5',axis=1)
    sheetX = sheetX.drop('Unnamed: 8',axis=1)

    for key in sheetX.keys():
        sheetX = sheetX.rename(columns = {
            key:sheetX[key][7]
        })

    sheetX = sheetX[1:]
    sheetX = sheetX.dropna(subset=['Subscriber Name'])

    filename = filename.split('.')[0]+"_cleaned.xls"
    print('filename:'+filename)

    sheetX.to_excel(filename,sheet_name='Sheet1',index=False)
    chitGroup = chitGroup.split(':')[-1].lstrip()
    return (read(filename,True),chitGroup)



def get_file(dirname,filename):
    files = [f for f in listdir(dirname) if isfile(join(dirname,f))]
    try:
        f = files[files.index(filename)]
        return join(dirname,f)
    except:
        return ""


def get_files(dirname,extension):
    files = [f for f in listdir(dirname) if isfile(join(dirname,f))]
    files = [f for f in files if f.endswith(extension)]
    files = [join(dirname,f) for f in files]
    return files

def read(filename,delete = False):
    xls = pd.ExcelFile(filename)
    sheetX = xls.parse(0)
    if delete:
        os.remove(filename)

    return sheetX

if __name__ == "__main__":
    files = get_files(join(BASE_DIR,"testfiles"),"xls")
    for file in files:
        print(clean(file))

