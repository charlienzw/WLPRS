from inventory import Inventory
from computePath import ComputePath
from memory_profiler import profile
from order import Order
import time

class algoTest:

    def __init__(self):
        self.inventory = None
        self.order = Order()
        self.start_point = (0, 0)
        print("Importing inventory...")
        self.importInventory('qvBox-warehouse-data-s19-v01.txt')
        print("Inventory imported successfully!")

    def importInventory(self, file_name):
        self.inventory = Inventory(self.start_point)
        self.inventory.importItems(file_name)
        self.inventory.calculateDistances()

    def importOrder(self, file_name):
        self.order.importOrder(file_name)

    def computePath(self, algo = 'DP'):
        if not self.inventory:
            print("\n\nInventory has not been imported yet.\n\n")
        computer = ComputePath(self.inventory.distance_array,
                               self.inventory.ID2Index)
        if algo == 'BRUTEFORCE' or algo == 'DP' or algo == 'GREEDY':
            sequence = computer.run(self.order.id_list, algo)
        else:
            print("\n\nGiven algorithm has not been implemented yet!\n\n")
        return sequence

    def getPathBySequence(self, sequence):
        curSource = -1
        paths = []
        for productId in sequence:
            if curSource == -1:
                path = self.inventory.getPathToProduct(productId)
                curSource = productId
            else:
                path = self.inventory.getPathBetweenProduct(curSource, productId)
                curSource = productId
            paths.append(path)
        return paths

    def getLocationByID(self, productID):
        return self.inventory.getLocationByID(productID)

    def run(self, orderSize):
        if (orderSize == 1):
            orderFile = 'order_of_one.txt'
        elif (orderSize == 5):
            orderFile = 'order_of_five.txt'
        elif (orderSize == 10):
            orderFile = 'order_of_ten.txt'
        elif (orderSize == 15):
            orderFile = 'order_of_fifteen.txt'
        print("Algorithm performance test for ordersize = " + str(orderSize) + " begin...")

        print("Importing orderList...")
        self.importOrder(orderFile)
        print("OrderList imported successfully!")

        # start = time.time()
        # self.runBRUTEFORCE()
        # end = time.time()
        # duration = round((end - start), 4)
        # print("Time of BRUTEFORCE is " + str(duration) + "s")

        start = time.time()
        self.runDP()
        end = time.time()
        duration = round((end - start), 4)
        print("Time of DP is " + str(duration) + "s")

        start = time.time()
        self.runGREEDY()
        end = time.time()
        duration = round((end - start), 4)
        print("Time of GREEDY is " + str(duration) + "s")
        
    @profile(precision=8)
    def runBRUTEFORCE(self):
        print("Run BRUTEFORCE")
        self.computePath('BRUTEFORCE')
    
    @profile(precision=8)
    def runDP(self):
        print("Run DP")
        self.computePath('DP')

    @profile(precision=8)
    def runGREEDY(self):
        print("Run GREEDY")
        self.computePath('GREEDY')

def main():
    testCase = algoTest()
    #testCase.run(1)
    #testCase.run(5)
    #testCase.run(10)
    testCase.run(15)

if __name__ == '__main__':
    main()
        
    


                    
