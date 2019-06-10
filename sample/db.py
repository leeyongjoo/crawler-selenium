import os

def makeCtl(fileDirPath, fileName, compName):
    content = """LOAD DATA
CHARACTERSET UTF8
INFILE '""" + fileDirPath+fileName + """'
replace
INTO TABLE cpu
FIELDS TERMINATED BY ','
(
name,manufacturer,socket,nm,core,thread,clock,l2,l3,bit,tdp,gpu_name,gpu_core,img,etc,price
)"""
    f = open("ctl"+compName+".ctl", "w")
    f.write(content)
    f.close()

def saveDB(compName):
    os.system("sqlldr 'CONCAT_EX/1234' control='"+compName+".ctl' errors=200 bad='./log/"+compName+".bad'")

if __name__=="__main__":
    pass
    # makeCtl(dirPath, 'cpu_190610_1728.csv', 'cpu')
    # saveDB('cpu')