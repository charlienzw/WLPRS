import sys
from inventory import Inventory
from distances import Distances
from computePath import ComputePath

def main(argv):
    if(sys.argv[1] == '-Import'):
        fileName = sys.argv[2];
        my_inventory = Inventory()
        my_inventory.writeData()
        my_inventory.readData()
        my_inventory.importItems(fileName)
        my_inventory.writeData()
        print("Import Success")
    elif(sys.argv[1] == '-Display'):
        my_inventory = Inventory()
        my_inventory.readData()
        my_inventory.displayMap()
    elif(sys.argv[1] == '-Position'):
        productId = sys.argv[2]
        my_inventory = Inventory()
        my_inventory.readData()
        (x, y) = my_inventory.getLocationById(productId)
        print("Position is (" + str(x) + ", " + str(y) + ")")
    elif(sys.argv[1] == '-Path'):
        productId = sys.argv[2]
        my_inventory = Inventory()
        fileName = 'example_inventory.txt'
        my_inventory.importItems(fileName)
        instructionList = my_inventory.getPathToOneProductFromZero(productId)
        for instruction in instructionList:
            print(instruction)
    # elif(sys.argv[1] == '-Algo'):
    #     order_list = [219, 302, 364, 444]
    #     my_inventory = Inventory()
    #     fileName = 'example_inventory.txt'
    #     my_inventory.importItems(fileName)
    #     distance_obj = Distances(my_inventory, (0, 0))
    #     distance_obj.calculateDistances()
    #     comp_obj = ComputePath(distance_obj)
    #     result = comp_obj.bruteForce(order_list)
    #     print(result)

if __name__ == '__main__':
    main(sys.argv)
