import os

d = {}
d['cpu'] = "name,manufacturer,socket,nm,core,thread,clock,l2,l3,bit,tdp,gpu_name,gpu_core,img,etc,price"
d['ram'] = "name,manufacturer,ddr,use,count,heatsink,dimm,capacity,clock,img,etc,price"
d['hdd'] = "name,manufacturer,type,size,capacity,sata,rpm,buffer,thickness,noise,as,img,etc,price"
d['mainboard'] = "name,manufacturer,socket,chipset,size,phase,ddr,capacity,vga_connet,pcie_slot,sata3,m_2_slot,output,ps_2,usb_2_0,usb_3_1_1,usb_3_1_2,img,etc,price"
d['power'] = "name,manufacturer,standard,w,fan_size,fan_num,pfc,rail,a,4pin_ide,sata,6+2pin_pci-e,as,img,etc,price"
d['vga'] = "name,manufacturer,prod_name,nm,clock,b_clock,sp,PCIe,gddr,memory_c,memory_v,memory_b,img,etc,price"


def makeCtl(fileDirPath, fileName, compName):
    content = """LOAD DATA
CHARACTERSET UTF8
INFILE '""" + fileDirPath+fileName + """'
replace 
INTO TABLE """+compName+"""
FIELDS TERMINATED BY ',' optionally enclosed by '"'
("""+ d[compName] +""")"""
    f = open("./ctl/"+compName+".ctl", "w")
    f.write(content)
    f.close()

def saveDB(compName):
    os.system("sqlldr 'CONCAT_EX/1234' control='./ctl/"+compName+".ctl' log='./log/"
            + compName +".log' errors=200 bad='./log/"+compName+".bad'")

if __name__=="__main__":
    pass
    # makeCtl(dirPath, 'cpu_190610_1728.csv', 'cpu')
    # saveDB('cpu')