from inventory import Inventory
from computePath import ComputePath
from order import Order
from orderList import OrderList
import timeout_decorator



class WPLRS:

    def __init__(self):
        self.inventory = None
        self.order = Order()
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.order_list = OrderList()

    def importInventory(self, file_name):
        self.inventory = Inventory(start_point=self.start_point,
                                   end_point=self.end_point)
        self.inventory.importItems(file_name)
        print("\nDefault start point is (0, 0).")
        print("Default end point is (0, 0).\n")
        self.inventory.calculateDistances()

    def inventoryIsEmpty(self):
        return len(self.inventory.inventory) == 0

    def displayInventory(self):
        self.inventory.displayMap()

    def displayPathInventory(self, paths, sequence):
        self.inventory.displayPathMap(paths, sequence)

    def importOrder(self, file_name):
        self.order.importOrder(file_name)

    def orderIsEmpty(self):
        return len(self.order.id_list) == 0

    @timeout_decorator.timeout(25, timeout_exception=StopIteration)
    def computePath(self, order = []):
        if not self.inventory:
            print("\n\nInventory has not been imported yet.\n\n")
            return None
        computer = ComputePath(self.inventory.distance_array,
                               self.inventory.ID2Index)
        if len(order) == 0:
            order = self.order.id_list
        if len(order) < 51:
            algo = 'GA'
        else:
            algo = 'GREEDY'
        sequence = computer.run(order, algo)
        return sequence

    def getPathBySequence(self, sequence):
        curSource = -1  # Start point
        paths = []
        for productId in sequence:
            if curSource == -1:
                path = self.inventory.getPathToProduct(productId)
                curSource = productId
            else:
                path = self.inventory.getPathBetweenProduct(curSource, productId)
                curSource = productId
            paths.append(path)
        # From last item to end point:
        end_point_ID = '-1'
        path = self.inventory.getPathBetweenProduct(curSource, end_point_ID)
        paths.append(path)
        return paths

    def getPathToProduct(self, productID):
        return self.inventory.getPathToProduct(productID)

    def getLocationByID(self, productID):
        return self.inventory.getLocationByID(productID)

    def setStartPoint(self, point):
        if point == self.inventory.start_point:
            print("\n\nThe given point is already the start point.\n\n")
            return
        if point in self.inventory.shelves:
            print("\n\nStart point should not be on a shelf.\n\n")
            return
        self.start_point = point
        if self.inventory:
            self.inventory.setStartPoint(point)

    def setEndPoint(self, point):
        if point == self.inventory.end_point:
            print("\n\nThe given point is already the end point.\n\n")
            return
        if point in self.inventory.shelves:
            print("\n\nEnd point should not be on a shelf.\n\n")
            return
        self.end_point = point
        if self.inventory:
            self.inventory.setEndPoint(point)

    def addOrder(self, productID):
        if productID in self.inventory.inventory:
            self.order.addOrder(productID)
        else:
            print("\n\nGiven ID is not in the inventory.")

    def paths2Instrs(self, paths, order = []):
        '''Get the user friendly instruction from a path list'''
        instructions = []
        if len(order) == 0:
            item_ids = self.order.id_list
        else:
            item_ids = order
        # Dictionary indicating where to turn
        direct2turn = {('North', 'East'): 'Right', ('North', 'South'): 'Back', ('North', 'West'): 'Left',
                       ('East', 'North'): 'Left', ('East', 'South'): 'Right', ('East', 'West'): 'Back',
                       ('South', 'North'): 'Back', ('South', 'East'): 'Left', ('South', 'West'): 'Right',
                       ('West', 'North'): 'Right', ('West', 'East'): 'Back', ('West', 'South'): 'Left'}
        # Each path has a bunch on coordinates. Starts with the first coordinate.
        coord = paths[0][0]  # Start point
        next_coord = paths[0][1]
        direction = 'North'
        direction = self.getDirection(coord, next_coord, direction)
        instructions.append("Start at {}".format(coord))
        step_count = 0
        for idx, path in enumerate(paths):
            if len(path) == 1:
                instructions.append("Pick Up Item: {} at {}".format(item_ids[idx], next_coord))
                continue
            for i, coord in enumerate(path[:-1]):
                next_coord = path[i+1]
                next_direct = self.getDirection(coord, next_coord, direction)
                if direction == next_direct:
                    step_count += 1
                    continue
                else:
                    turn_direct = direct2turn[(direction, next_direct)]
                    instructions.append('Move Towards {}, For {} Steps, Until '.format(direction, step_count) +
                                        'You Reach Point {} and Turn {} to {} Direction.'.format(coord, turn_direct, next_direct))
                    step_count = 1  # Reset step count
                    direction = next_direct
            if idx == len(paths) - 1:
                instructions.append("Move Towards {}, For {} Steps and End Your Tour at {}".format(direction, step_count, next_coord))
            else:
                instructions.append("Move Towards {}, For {} Steps, and Pick Up Item: {} at {}".format(direction, step_count, item_ids[idx], next_coord))
                step_count = 0
        return instructions

    def getDirection(self, first_pt, next_pt, direction):
        if first_pt == next_pt:
            return direction
        is_north = next_pt == (first_pt[0], first_pt[1] + 1)
        is_east = next_pt == (first_pt[0] + 1, first_pt[1])
        is_south = next_pt == (first_pt[0], first_pt[1] - 1)
        is_west = next_pt == (first_pt[0] - 1, first_pt[1])
        if is_north:
            return 'North'
        elif is_east:
            return 'East'
        elif is_south:
            return 'South'
        elif is_west:
            return 'West'
        else:
            raise ValueError("The Given Two Points Are NOT One Step From One Another!!")

    def loadOrderList(self, file_name):
        self.order_list.importOrderList(file_name)

    def getNextOrder(self):
        return self.order_list.nextOrder()

    def getSpecificOrder(self, index):
        return self.order_list.specificOrder(index)

    def inputOrder(self, order_string):
        self.order_list.inputOrder(order_string)

    def orderListIsEmpty(self):
        return len(self.order_list.order_list) == 0



def main():
    my_prog = WPLRS()
    my_prog.importInventory('example_inventory.txt')
    my_prog.displayInventory()
    order_list = ['102', '149', '172', '231']
    for id in order_list:
        my_prog.order.addOrder(id)
    sequence = my_prog.computePath(algo = 'BRUTEFORCE')
    paths = my_prog.getPathBySequence(sequence)
    instrs = my_prog.paths2Instrs(paths)
    for line in instrs:
        print(line)


if __name__ == '__main__':
    main()
