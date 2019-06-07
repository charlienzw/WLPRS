from wplrs import WPLRS
import time


class Interactive:

    def __init__(self):
        self.title = []
        self.title.append(r'__          ________ _      _____ ____  __  __ ______   _______ ____   __          _______  _      _____   _____')
        self.title.append(r'\ \        / /  ____| |    / ____/ __ \|  \/  |  ____| |__   __/ __ \  \ \        / /  __ \| |    |  __ \ / ____|')
        self.title.append(r' \ \  /\  / /| |__  | |   | |   | |  | | \  / | |__       | | | |  | |  \ \  /\  / /| |__) | |    | |__) | (___ ')
        self.title.append(r'  \ \/  \/ / |  __| | |   | |   | |  | | |\/| |  __|      | | | |  | |   \ \/  \/ / |  ___/| |    |  _  / \___ \ ')
        self.title.append(r'   \  /\  /  | |____| |___| |___| |__| | |  | | |____     | | | |__| |    \  /\  /  | |    | |____| | \ \ ____) |')
        self.title.append(r'    \/  \/   |______|______\_____\____/|_|  |_|______|    |_|  \____/      \/  \/   |_|    |______|_|  \_\_____/')
        self.title.append('\n')
        self.title.append(' ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ')
        self.title.append('|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|')
        self.title.append('\n\n\n')
        self.options = ''
        self.order_list_file_label = ''
        self.inventory_file_label = ''
        self.program = WPLRS()

    def run(self):
        self.printTitle()
        imported = 0
        while(1):
            self.printOption()
            inp = input("Please select an option: ")
            print('')
            if inp == '1':  # Import the inventory.
                inventory_file_name = input("Please enter the inventory file you want to load: ")
                try:
                    self.program.importInventory(inventory_file_name)
                except Exception:
                    print("Cannot find the file\n")
                    time.sleep(1)
                    continue
                self.inventory_file_label = '<' + inventory_file_name + '>'
                print('\n')
                time.sleep(1)
                imported = 1
            elif inp == '2':  # Display the Map
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                self.program.displayInventory()
                print('\n')
            elif inp == '3':  # Learn the location of a product.
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                productID = input('Please enter a product ID: ')
                (x, y) = self.program.getLocationByID(productID)
                if x == -1 and y == -1:
                    print("\n\nGiven product ID is not in the inventory")
                else:
                    print("\nPosition is (" + str(x) + ", " + str(y) + ")")
                print('\n')
                time.sleep(1)
            elif inp == '4':  # Compute the path to a product.
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                productID = input('Please enter a product ID: ')

                (x, y) = self.program.getLocationByID(productID)
                if x == -1 and y == -1:
                    print("\n\nGiven product ID is not in the inventory")
                    print('\n')
                    time.sleep(1)
                    continue

                path = self.program.getPathToProduct(productID)
                paths = []
                paths.append(path)
                print("Please follow this instruction to get the product:\n")
                instrs = self.program.paths2Instrs(paths)
                for instr in instrs:
                    print(instr)
                    time.sleep(0.25)
                time.sleep(1)
            elif inp == '5':  # Change start point.
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                x = int(input("Please enter x coordinate: "))
                y = int(input("Please enter y coordinate: "))
                point = (x, y)
                self.program.setStartPoint(point)
                print('\n')
                time.sleep(1)
            elif inp == '6':  # Change end point.
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                x = int(input("Please enter x coordinate: "))
                y = int(input("Please enter y coordinate: "))
                point = (x, y)
                self.program.setEndPoint(point)
                print('\n')
                time.sleep(1)
            elif inp == '7':  # Import Order List.
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                list_name = input("Please enter the file you want to import: ")
                try:
                    self.program.importOrder(list_name)
                except Exception:
                    print("Cannot find the file\n")
                    time.sleep(1)
                    continue
                print('\n')
                time.sleep(1)
            elif inp == '8':  # Add Order to the List
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                productID = input("Please enter the product ID: ")
                self.program.addOrder(productID)
                print('\n')
            elif inp == '9':  # Calculate shortest path with the order list
                # algo = input("Please enter the algorithm you want to use: (BRUTEFORCE / DP / GREEDY)\n")
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                if self.program.orderIsEmpty():
                    print("Please import order file with option [7] or input products manually with option [8] first.")
                    time.sleep(1)
                    continue
                try:
                    sequence = self.program.computePath()
                except Exception:
                    sequence = self.program.order.id_list
                    print("The execution time is over the timeout.\n")
                paths = self.program.getPathBySequence(sequence)
                print("The optimal sequence is the following: ")
                print(sequence)
                print('\n')

                print("Please follow this instruction to get the products:")
                instrs = self.program.paths2Instrs(paths)
                for instr in instrs:
                    print(instr)
                    time.sleep(0.1)

                self.program.displayPathInventory(paths, sequence)
                time.sleep(1)
            elif inp == '10': # Input Order Manually
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                input_order = input("Please enter the order that you want to input manually:")
                self.program.inputOrder(input_order)
                time.sleep(1)
            elif inp == '11': # Load Order List
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                order_list_file_name = input("Please enter the order list file you want to load: ")
                try:
                    self.program.loadOrderList(order_list_file_name)
                except Exception:
                    print("Cannot find the file\n")
                    time.sleep(1)
                    continue
                self.order_list_file_label = '<' + order_list_file_name + '>'
                time.sleep(1)

            elif inp == '12': # Get next order from Order List
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                if self.program.orderListIsEmpty():
                    print("Please import the order list with option [11] or input order manually with option [10] first.")
                    time.sleep(1)
                    continue
                (cur_index, cur_order) = self.program.getNextOrder()
                if cur_index == -1:
                    print("The order list are all fulfilled.\n")
                    time.sleep(1)
                else:
                    print("Order to fulfill: Order " + ("%04d" % (cur_index + 1)) + "\n")
                    output_products = ""
                    for cur_product in cur_order:
                        output_products += cur_product + " "
                    print("Items: " + output_products + "\n")
                    try:
                        sequence = self.program.computePath(cur_order)
                    except Exception:
                        sequence = cur_order
                        print("The execution time is over the timeout.\n")
                    paths = self.program.getPathBySequence(sequence)
                    print("The optimal sequence is the following: ")
                    print(sequence)
                    print('\n')

                    print("Please follow this instruction to get the products:")
                    instrs = self.program.paths2Instrs(paths, cur_order)
                    for instr in instrs:
                        print(instr)
                        time.sleep(0.1)

                    self.program.displayPathInventory(paths, sequence)
                    time.sleep(1)

            elif inp == '13': # Get specific order from Order List
                if not imported:
                    print("Please import the inventory with option [1] first.")
                    time.sleep(1)
                    continue
                if self.program.orderListIsEmpty():
                    print("Please import the order list with option [11] or input order manually with option [10] first.")
                    time.sleep(1)
                    continue
                order_index = int(input("Please enter the order's index that you want to access:"))
                (flag, cur_order) = self.program.getSpecificOrder(order_index - 1)
                if flag == -1:
                    print("The index is out of range.\n")
                    time.sleep(1)
                elif flag == 0:
                    print("The order of this index is fulfilled.\n")
                    time.sleep(1)
                else:
                    print("Order to fulfill: Order " + ("%04d" % order_index) + "\n")
                    output_products = ""
                    for cur_product in cur_order:
                        output_products += cur_product + " "
                    print("Items: " + output_products + "\n")
                    try:
                        sequence = self.program.computePath(cur_order)
                    except Exception:
                        sequence = cur_order
                        print("The execution time is over the timeout.\n")
                    paths = self.program.getPathBySequence(sequence)
                    print("The optimal sequence is the following: ")
                    print(sequence)
                    print('\n')

                    print("Please follow this instruction to get the products:")
                    instrs = self.program.paths2Instrs(paths, cur_order)
                    for instr in instrs:
                        print(instr)
                        time.sleep(0.1)

                    self.program.displayPathInventory(paths, sequence)
                    time.sleep(1)
                    


            elif inp == '0':
                print("\n\nTHANK YOU FOR USING WPLRS!!\n\n")
                time.sleep(1)
                break
            else:
                print("Invalid Option!\n")
                time.sleep(1)
                print("Please input a number between 1 and 13.\n\n")
                time.sleep(1)

    def printTitle(self):
        for line in self.title:
            print(line)

    def printOption(self):
        self.options += '\n\nHow can I help you today?\n\n'
        self.options += '---------- Inventory Option ----------\n'
        self.options += '1) Import an inventory. ' + self.inventory_file_label + '\n'
        self.options += '2) Display the Map\n'
        self.options += '3) Learn the location of a product.\n'
        self.options += '4) Compute the path to a product.\n'
        self.options += '5) Change start point.\n'
        self.options += '6) Change end point.\n'
        self.options += '\n'
        self.options += '---------- Single Order Option ----------\n'
        self.options += '7) Import Order.\n'
        self.options += '8) Add Product to the Order.\n'
        self.options += '9) Calculate shortest path with the order.\n'
        self.options += '\n'
        self.options += '---------- Order List Option ----------\n'
        self.options += '10) Input Order Manually.\n'
        self.options += '11) Load Order List. ' + self.order_list_file_label + '\n'
        self.options += '12) Get next order from Order List.\n'
        self.options += '13) Get specific order from Order List.\n'
        self.options += '\n0) Exit.\n\n\n'
        print(self.options)
        self.options = ''



def run():
    interactive = Interactive()
    interactive.run()


if __name__ == '__main__':
    run()
