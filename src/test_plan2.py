from wplrs import WPLRS
import time

class Inter:

    def __init__(self):
        self.order_list_file_label = ''
        self.program = WPLRS()

    def importin(self):

        fileName = 'qvBox-warehouse-data-s19-v01.txt'
        self.program.importInventory(fileName)
        print('\n')
        time.sleep(1)
        point = (6, 0)
        self.program.setStartPoint(point)
        time.sleep(1)
        point2 = (10, 1)
        self.program.setEndPoint(point2)
        time.sleep(1)



    def orderlist(self):
        list_name = 'order_of_fifteen.txt'
        self.program.importOrder(list_name)
        print('\n')
        time.sleep(1)

    def getpath(self):
        sequence = self.program.computePath('GA')
        paths = self.program.getPathBySequence(sequence)
        print("The optimal sequence is the following: ")
        print(sequence)
        print('\n')

        print("Please follow this instruction to get the products:")
        instrs = self.program.paths2Instrs(paths)
        for instr in instrs:
            print(instr)
            time.sleep(0.1)
        time.sleep(1)

test = Inter()
test.importin()
test.orderlist()
test.getpath()


