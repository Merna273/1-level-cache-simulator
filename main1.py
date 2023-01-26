import math
hit = 0
miss = 0
noOfAccesses = 0
noOfCycles = 0

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


app = QApplication(sys.argv)
win = QWidget()
table = QTableWidget()
layout = QVBoxLayout()
table.tableWidget = QTableWidget()
layout.addWidget(table.tableWidget)# win.addWidget(QLabel("Cache Simulator"))

sB = QLineEdit("Enter Cache Size")
layout.addWidget(sB)

lB = QLineEdit("Enter Line Size")
layout.addWidget(lB)

noOfCyclesB = QLineEdit("Enter Number of Cycles")
layout.addWidget(noOfCyclesB)

fB = QLineEdit("Enter File Name")
layout.addWidget(fB)


b2 = QPushButton("Submit") 
layout.addWidget(b2)       
        
def createTable():

    #Row count
    table.tableWidget.setRowCount(100) 

    #Column count
    table.tableWidget.setColumnCount(7)  

    table.tableWidget.setItem(0,0, QTableWidgetItem("Memory Access"))
    table.tableWidget.setItem(0,1, QTableWidgetItem("Tag"))
    table.tableWidget.setItem(0,2, QTableWidgetItem("Valid Bit"))
    table.tableWidget.setItem(0,3, QTableWidgetItem("Number of Accesses"))
    table.tableWidget.setItem(0,4, QTableWidgetItem("Hit Ratio"))
    table.tableWidget.setItem(0,5, QTableWidgetItem("Miss Ratio"))
    table.tableWidget.setItem(0,6, QTableWidgetItem("The Average Memory Access Time"))



    #Table will fit the screen horizontally
    table.tableWidget.horizontalHeader().setStretchLastSection(True)
    table.tableWidget.horizontalHeader().setSectionResizeMode(
        QHeaderView.Stretch)
        
 
def main():
    noOfCycles = str(noOfCyclesB.text())
    if int(noOfCycles) > 10 or int(noOfCycles) < 1:
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please enter a number between 1 and 10")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()  # this will show our messagebox
        
        noOfCycles = str(noOfCyclesB.text())
    
    else:    
        createTable()
        
        memoryDivision = []
        cache = []
        s = str(sB.text())
        l = str(lB.text())
        
        print(s, l)
        
        c = int(s)/int(l)

        offsetSize = round(math.log(int(l), 2))
        indexSize = round(math.log(c, 2))
        tagSize = 32 - (offsetSize + indexSize)
        readFromFile(offsetSize, indexSize, tagSize, memoryDivision, cache, l, c)
           
def window():
    
    win.setLayout(layout)
    win.setWindowTitle("Cache Simulator")
    win.setGeometry(100, 100, 1250, 500)
    win.show()

      

def cachePlacement(cache, memoryDivision): #to see whether tag is in the memory or not
    global miss
    global noOfAccesses
    global hit
    for i in range(0, len(memoryDivision)):
        for j in range(0, len(cache)):
            if((cache[j]["index"] == memoryDivision[i]["index"]) and (cache[j]["offset"] == memoryDivision[i]["offset"])):
                if(cache[j]["vBit"] == 1):  
                    if(cache[j]["tag"] == memoryDivision[i]["tag"]):# tag is found
                        hit = hit + 1
                        
                    else:#tag not found
                        miss = miss + 1 
                        noOfAccesses = noOfAccesses + 1
                        averageNoOfCycles = AMAT(hit, noOfAccesses)
                        cache[j]["tag"] = memoryDivision[i]["tag"]
                
                else: 
                    miss = miss + 1
                    noOfAccesses = noOfAccesses + 1
                    averageNoOfCycles = AMAT(hit, noOfAccesses)

                    cache[j]["tag"] = memoryDivision[i]["tag"]
                    cache[j]["vBit"] = 1    
     
                if noOfAccesses > 0 :         
                    table.tableWidget.setItem(j+1,0, QTableWidgetItem(str(memoryDivision[i]["index"]) + str(memoryDivision[i]["offset"])))
                    table.tableWidget.setItem(j+1,1, QTableWidgetItem(cache[j]["tag"]))
                    table.tableWidget.setItem(j+1,2, QTableWidgetItem(str(cache[j]["vBit"])))
                    table.tableWidget.setItem(j+1,3, QTableWidgetItem(str(noOfAccesses)))
                    table.tableWidget.setItem(j+1,4, QTableWidgetItem(str(hit/noOfAccesses)))
                    table.tableWidget.setItem(j+1,5, QTableWidgetItem(str(1 - hit/noOfAccesses)))
                    table.tableWidget.setItem(j+1,6, QTableWidgetItem(str(averageNoOfCycles)))
                    print(str(memoryDivision[i]["index"]) + str(memoryDivision[i]["offset"]))
                    print("Tag ",(cache[j]["tag"]))
                    print("Valid Bit ", (str(cache[j]["vBit"])))
                    print("Number of accesses ", (str(noOfAccesses)))
                    print("hit ratio ", (str(hit/noOfAccesses)))
                    print("miss ratio", (str(1 - hit/noOfAccesses)))
                    print("Average number of cycles ", (str(averageNoOfCycles)))

          

def createCache(offsetSize, indexSize, cache, memoryDivision):#get all possible cominations of index and offset and creates from them an empty cache 
    totalSize = pow(2, int(offsetSize) + int(indexSize))
    numOfBits = int(offsetSize) + int(indexSize) 
    allCombinations = []
    for i in range(0, totalSize):
        value = f'{i:0{numOfBits}b}'.format(i).replace("0b", "")
        allCombinations.append(value)
    for i in allCombinations:
        index = i[0 : int(indexSize)] 
        offset = i[int(indexSize) : int(indexSize + offsetSize)] 
        # print("index " , index, "offset " , offset)
        cache.append({"index" : str(index), "offset" : str(offset), "vBit" : 0, "tag" : ""})

def readFromFile(offsetSize, indexSize, tagSize, memoryDivision, cache, l, c):#read access sequence and creates the index,, offset and tag of each memory address
    f = fB.text()
    file1 = open(f, 'r')
    Lines = file1.readlines()
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        # print("Memory:", line.strip())
        # blockAddress = int(line.strip())/int(l)
        # # print("Address", blockAddress)
        # blockNumber = blockAddress % int(c)
        # print("block number", blockNumber)
        memBin = '{:032b}'.format(int(line.strip())).replace("0b", "")
        memBin = str(memBin)
        tag = memBin[0:int(tagSize)]
        index = memBin[int(tagSize): int(tagSize + indexSize)]
        offset = memBin[int(tagSize + indexSize) : int(tagSize + indexSize + offsetSize)]
        memoryDivision.append({"index" : index,  "offset" : offset, "tag": tag})
    #print("Memory Division: ", memoryDivision)
    createCache(offsetSize, indexSize, cache, memoryDivision)
    # window(cache, memoryDivision)
    cachePlacement(cache, memoryDivision)

def AMAT(hit, noOfAccesses):
    miss_ratio  = 1-(hit/noOfAccesses)
    noOfCycles = int(noOfCyclesB.text())
    return noOfCycles +  (miss_ratio * 100)


if __name__ == "__main__":
    window()
    b2.clicked.connect(main)
    layout.addWidget(b2)
    sys.exit(app.exec_())
