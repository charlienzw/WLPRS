import os
from product import Product
import json
import sys


class Inventory:

    def __init__(self, start_point=(0, 0), end_point=(0, 0)):
        self.inventory = {}
        self.shelves = set()  # Shelf locations
        self.needs_recalculation = True
        self.base_distance_array = []  # 2D array for distances of the vertices except start and end points
        self.distance_array = []  # 2D array for distances of the vertices
        self.start_point = start_point
        self.end_point = end_point
        self.ID2Index = {}  # Given a product ID, eturn the index in dist.
        self.grid_size = 0
        self.data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    def addItem(self, item):
        '''Adds the given item to the inventory'''
        if item.getID() in self.inventory:
            print("Given product is already in the inventory!")
            return False
        else:
            self.inventory[item.getID()] = item.__dict__
            print("Given product has been successfully added to the" +
                  " inventory!")
            return True

    def calculateDistances(self):
        '''
            For a given inventory calculate distances between each 2 products
            Input: Inventory object
            Output: Success or Error message for updating the array!
        '''
        if not self.needs_recalculation:
            self.readDistances()
            self.readID2Index()
            self.readShelves()
            return
        print("Calculating the distances...")
        self.distance_array = []
        # We will treat the product coordinates in the inventory
        # as shelves. The distances will be calculated based the
        # accessibility of each product.
        accessibility = {}
        start_point_ID = '000'  # As a convention
        end_point_ID = '-1'  # As a convention
        accessibility[self.start_point] = [1, 1, 1, 1]  # Start loc access
        accessibility[self.end_point] = [1, 1, 1, 1]  # End loc access
        # We add one to the start_point to make it look like there is a shelf.
        self.shelves.add(self.start_point)
        self.shelves.add(self.end_point)
        # loc2ID tells us which items are in that location
        loc2ID = {}
        loc2ID[self.start_point] = [start_point_ID]
        if self.start_point == self.end_point:
            loc2ID[self.end_point].append(end_point_ID)
        else:
            loc2ID[self.end_point] = [end_point_ID]
        for ID in self.inventory.keys():
            loc = self.getLocationByID(ID)
            self.shelves.add(loc)  # Add the shelf to shelf list.
            # Create the loc2ID dictionary
            if loc not in loc2ID:
                loc2ID[loc] = [ID]
            else:
                loc2ID[loc].append(ID)
            # Create the accessibility of the locations
            if loc not in accessibility:
                accessibility[loc] = self.getAccessibilityfromID(ID)
        progress = 0
        finish = len(self.shelves)
        finish = (finish*(finish-1))/2  # Finish calculation for progress bar
        # After initializing the necessary data,
        # do BFS to calculate shortest distances.
        to_visit = self.shelves.copy()
        for i, point in enumerate(self.shelves):
            # Set the ID to index dictionary
            for id in loc2ID[point]:
                self.ID2Index[id] = i
            distance_list = [0]
            to_visit.remove(point)
            src_access = accessibility[point]
            sourcept = self.getPickupPoint(point, src_access)
            for j, dest_coord in enumerate(to_visit):
                dest_access = accessibility[dest_coord]
                destpt = self.getPickupPoint(dest_coord, dest_access)
                distance = self.traverse(sourcept, destpt)
                if distance == -1:
                    print("Location {} is unreachable from {}!"
                          .format(destpt, sourcept))
                distance_list.append(distance)
                progress += 1
                percentage = (float(progress)/finish)*100
                sys.stdout.write("Distance Calculation Progress: %.02f%%\r" % (percentage))
                sys.stdout.flush()
            self.distance_array.append(distance_list)
        # Take the symmetric of the distance matrix to fill the empty spaces.
        for i in range(1, len(self.distance_array)):
            prefix = []
            for j in range(i):
                prefix.append(self.distance_array[j][i])
            self.distance_array[i] = prefix + self.distance_array[i]
        # distance array contains the 2D distance matrix we need
        print("Distances have been calculated successfully!")
        # Dump the distances to a file
        self.dump_distances()
        self.dump_ID2Index()
        self.shelves.remove(self.start_point)  # We remove them as shelves
        if self.start_point != self.end_point:
            self.shelves.remove(self.end_point)  # so that path can go through
        self.dump_shelves()

    def displayMap(self):
        lines = []
        inventoryMap = [['.' for i in range(self.grid_size+1)]
                        for j in range(self.grid_size+1)]
        for productID in self.inventory.keys():
            (x, y) = self.inventory[productID]['location']
            inventoryMap[x][y] = 's'
        for i in range(len(inventoryMap)-1, -1, -1):
            if i < 10:
                line = str(i) + ':  |   '
            else:
                line = str(i) + ': |   '
            for j in range(len(inventoryMap[i])):
                line = line + str(inventoryMap[j][i]) + '  '
            lines.append(line)
        underscore = '    |' + "_" * len(inventoryMap[0]*3) + '____'
        lines.append(underscore)
        line = '        '
        for i in range(len(inventoryMap[0])):
            if i < 10:
                line = line + str(i) + '  '
            else:
                line = line + str(i) + ' '
        lines.append(line)
        for line in lines:
            print(line)

    def displayPathMap(self, paths, sequence):
        lines = []
        inventoryMap = [['.' for i in range(self.grid_size+1)]
                        for j in range(self.grid_size+1)]
        for productID in self.inventory.keys():
            (x, y) = self.inventory[productID]['location']
            inventoryMap[x][y] = 's'
        for path in paths:
            for product in path:
                (x, y) = product
                inventoryMap[x][y] = 0
        for product_id in sequence:
            (x, y) = self.inventory[product_id]['location']
            inventoryMap[x][y] = 1

        for i in range(len(inventoryMap)-1, -1, -1):
            if i < 10:
                line = str(i) + ':  |   '
            else:
                line = str(i) + ': |   '
            for j in range(len(inventoryMap[i])):
                line = line + str(inventoryMap[j][i]) + '  '
            lines.append(line)
        underscore = '    |' + "_" * len(inventoryMap[0]*3) + '____'
        lines.append(underscore)
        line = '        '
        for i in range(len(inventoryMap[0])):
            if i < 10:
                line = line + str(i) + '  '
            else:
                line = line + str(i) + ' '
        lines.append(line)
        for line in lines:
            print(line)

    def dump_distances(self):
        '''Dumps the distances to a txt file'''
        distance_path = os.path.join(self.data_path, 'distances.txt')
        with open(distance_path, 'w') as file:
            file.writelines('\t'.join(str(j) for j in i) + '\n' for i in self.distance_array)

    def dump_ID2Index(self):
        '''Dumps the ID2Index dictionary to a file'''
        ID2Index_path = os.path.join(self.data_path, 'ID2Index.json')
        with open(ID2Index_path, 'w') as f:
            json.dump(self.ID2Index, f)

    def dump_shelves(self):
        '''Dumps the shelves data to a file'''
        shelves_path = os.path.join(self.data_path, 'shelves.txt')
        with open(shelves_path, 'w') as file:
            for shelf in self.shelves:
                file.write(str(shelf) + '\n')

    def findPath(self, sourcept, destpt, shelves):
        '''Returns the list of coordinates in order to move from src to dest'''
        rowNum = [-1, 0, 0, 1]  # Row/Col helper list for checking adjacent
        colNum = [0, -1, 1, 0]  # tiles.
        visited = {}  # Initialize the visited dictionary.
        for i in range(self.grid_size + 1):
            for j in range(self.grid_size + 1):
                visited[(i, j)] = False
        visited[sourcept] = True  # Make the source point visited.
        distances = {}
        distances[sourcept] = 0
        reached_from = {}  # Dictionary indicating how we got to that point.
        # Start the BFS
        prev_node = (0, 0)
        found_flag = 0
        to_visit = [sourcept]
        while(to_visit):
            current_node = to_visit[0]
            if current_node == destpt:  # If we reached our destination return!
                found_flag = 1
                break
            # Otherwise pop from queue and look for its neighbours to traverse.
            to_visit.pop(0)
            for i in range(4):
                row = current_node[0] + rowNum[i]
                col = current_node[1] + colNum[i]
                if self.isValid((row, col)) \
                    and (row, col) not in shelves \
                        and not visited[(row, col)]:
                    visited[(row, col)] = True
                    distances[(row, col)] = distances[current_node] + 1
                    reached_from[(row, col)] = current_node
                    to_visit.append((row, col))
            prev_node = current_node
        if not found_flag:
            print("The product is unreachable!")
            return []  # If we cannot reach the destination
        else:
            my_path_list = [destpt]
            while(current_node != sourcept):
                prev_node = reached_from[current_node]
                my_path_list = [prev_node] + my_path_list
                current_node = prev_node
            return my_path_list

    def getAccessibilityfromID(self, ID):
        '''Get the product accesibility list from its ID'''
        return self.inventory[ID]['accessibility']

    def getItem(self, ID):
        '''Returns the product with the given ID from the inventory'''
        if ID in self.inventory:
            return self.inventory[ID]
        else:
            print("No product with the given ID exists in the inventory!")

    def getLocationByID(self, ID):
        '''Get the product location from its ID'''
        if ID in self.inventory:
            return self.inventory[ID]['location']
        else:
            # Given product ID is not in the inventory
            return (-1, -1)

    def getPathBetweenProduct(self, sourceProductID, destProductID):
        '''Find the path between the given two products.'''
        if sourceProductID in self.inventory:
            sourcept = self.inventory[sourceProductID]['location']
        else:
            print("\n\nGiven source product ID is not in the inventory")
            return []

        if destProductID == '-1':
            destpt = self.end_point
        elif destProductID in self.inventory:
            destpt = self.inventory[destProductID]['location']
        else:
            print("\n\nGiven dest product ID is not in the inventory")
            return []

        sourcept = (sourcept[0], sourcept[1] + 1)
        if destProductID != '-1':
            destpt = (destpt[0], destpt[1] + 1)
        path = self.findPath(sourcept, destpt, self.shelves)
        return path

    def getPathToProduct(self, productID):
        '''Given a product ID it finds the path from start to that product'''
        if productID in self.inventory:
            destpt = self.inventory[productID]['location']
        else:
            print("\n\nGiven product ID is not in the inventory")
            return []
        destpt = (destpt[0], destpt[1] + 1)
        sourcept = self.start_point
        path = self.findPath(sourcept, destpt, self.shelves)
        return path

    def getPickupPoint(self, point, access):
        '''Given a point and an accessibility list, calculate where to aim'''
        if point == self.start_point:
            return point
        else:
            if access[0]:  # Can be accessed from North
                return (point[0], point[1] + 1)
            elif access[1]:  # Can be accessed from West
                return (point[0] - 1, point[1])
            elif access[2]:  # Can be accessed from South
                return (point[0], point[1] - 1)
            else:  # Can be accessed from East
                return (point[0] + 1, point[1])

    def importItems(self, file_name):
        '''Parse the given file and add the products to the inventory'''
        if file_name.endswith('.txt'):
            self._importfromtxt(file_name)
            temp_file_path = os.path.join(self.data_path, 'temp.json')
            self.writeData(temp_file_path)
            current_invent = self.readData(temp_file_path)
            cached_json = self.readData()
            self.needs_recalculation = not (current_invent == cached_json)
            if self.needs_recalculation:
                self.writeData()
                print("\n\nInventory file has been changed recalculation is needed!\n")
        elif file_name.endswith('.csv'):
            # self._importfromcsv(file_name)  # TODO: implement import from csv
            raise ValueError("Import from csv is not implemented yet!")
        else:
            raise ValueError("Invalid file type is given!")

    def isValid(self, position):
        '''Is the given coordinate valid in the grid or not'''
        if (position[0] <= self.grid_size) \
            and position[1] <= self.grid_size \
                and position[0] >= 0 and position[1] >= 0:
            return True
        else:
            return False

    def readData(self, path=None):
        '''Read Inventory Data from Json file'''
        if not path:
            path = os.path.join(self.data_path, 'Inventory.json')
        try:
            with open(path, 'r') as f:
                res = json.load(f)
        except FileNotFoundError:
            return {}
        return res

    def readDistances(self):
        '''Reads the distances from the file'''
        distances_array = []
        distance_path = os.path.join(self.data_path, 'distances.txt')
        with open(distance_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                temp_line = line.replace('\n', '').split('\t')
                temp_vec = []
                for ele in temp_line:
                    temp_vec.append(int(ele))
                distances_array.append(temp_vec)
        self.distance_array = distances_array

    def readID2Index(self):
        '''Reads ID2Index file'''
        ID2Index_path = os.path.join(self.data_path, 'ID2Index.json')
        res = self.readData(ID2Index_path)
        self.ID2Index = res

    def readShelves(self):
        '''Reads shelf file'''
        shelves_path = os.path.join(self.data_path, 'shelves.txt')
        with open(shelves_path, 'r') as file:
            shelves = file.readlines()
            for line in shelves:
                if not line:
                    continue
                line = line.replace('\n', '').replace(',', '').replace('(', '').replace(')', '').split(' ')
                loc = (int(line[0]), int(line[1]))
                self.shelves.add(loc)

    def removeItem(self, ID):
        '''Removes the product with the given ID from the inventory'''
        if ID in self.inventory:
            del self.inventory[ID]
            print("Product with the given ID has been successfully" +
                  " removed from the inventory!")
            return True
        else:
            print("No product with the given ID exists in the inventory!")
            return False

    def setEndPoint(self, point):
        if not self.isValid(point):
            print("Given point exceeds grid size!\n\n")
            return
        self.end_point = point
        print("End point has been successfully changed!\n\n")
        self.updateDistances()

    def setGridSize(self, n):
        '''Set the grid size for the warehouse'''
        self.grid_size = n

    def setStartPoint(self, point):
        if not self.isValid(point):
            print("Given point exceeds grid size!\n\n")
            return
        self.start_point = point
        print("Start point has been successfully changed!\n\n")
        self.updateDistances()

    def traverse(self, sourcept, destpt):
        '''Traverses from start to destination and returns the shortest path'''
        shelf_locs = self.shelves.copy()
        shelf_locs.discard(self.start_point)
        if self.start_point != self.end_point:
            shelf_locs.discard(self.end_point)  # so that path can go through
        rowNum = [-1, 0, 0, 1]  # Row/Col helper list for checking adjacent
        colNum = [0, -1, 1, 0]  # tiles.
        visited = {}  # Initialize the visited dictionary.
        for i in range(self.grid_size + 1):
            for j in range(self.grid_size + 1):
                visited[(i, j)] = False
        visited[sourcept] = True  # Make the source point visited.
        distances = {}
        distances[sourcept] = 0
        to_visit = [sourcept]
        while(to_visit):
            current_node = to_visit[0]
            if current_node == destpt:  # If we reached our destination return!
                return distances[current_node]
            # Otherwise pop from queue and look for its neighbours to traverse.
            to_visit.pop(0)
            for i in range(4):
                row = current_node[0] + rowNum[i]
                col = current_node[1] + colNum[i]
                if self.isValid((row, col)) \
                    and (row, col) not in shelf_locs \
                        and not visited[(row, col)]:
                    visited[(row, col)] = True
                    distances[(row, col)] = distances[current_node] + 1
                    to_visit.append((row, col))
        return -1  # If we cannot reach the destination

    def updateDistances(self):
        start_point_ID = '000'  # As a convention
        end_point_ID = '-1'  # As a convention
        start_index = self.ID2Index[start_point_ID]
        end_index = self.ID2Index[end_point_ID]

        accessibility = {}
        accessibility[self.start_point] = [1, 1, 1, 1]  # Start loc access
        accessibility[self.end_point] = [1, 1, 1, 1]  # End loc access
        for ID in self.inventory.keys():
            loc = self.getLocationByID(ID)
            # Create the accessibility of the locations
            if loc not in accessibility:
                accessibility[loc] = self.getAccessibilityfromID(ID)

        to_visit = self.shelves.copy()
        to_visit.add(self.start_point)
        to_visit.add(self.end_point)

        distance_list = [0]
        src_access = accessibility[self.start_point]
        sourcept = self.getPickupPoint(self.start_point, src_access)
        for j, dest_coord in enumerate(to_visit):
            dest_access = accessibility[dest_coord]
            destpt = self.getPickupPoint(dest_coord, dest_access)
            distance = self.traverse(sourcept, destpt)
            if distance == -1:
                print("Location {} is unreachable from {}!"
                      .format(destpt, sourcept))
            distance_list.append(distance)
        self.distance_array[start_index] = distance_list

        distance_list = [0]
        src_access = accessibility[self.end_point]
        sourcept = self.getPickupPoint(self.end_point, src_access)
        for j, dest_coord in enumerate(to_visit):
            dest_access = accessibility[dest_coord]
            destpt = self.getPickupPoint(dest_coord, dest_access)
            distance = self.traverse(sourcept, destpt)
            if distance == -1:
                print("Location {} is unreachable from {}!"
                      .format(destpt, sourcept))
            distance_list.append(distance)
        self.distance_array[end_index] = distance_list

        for i in range(len(self.distance_array)):
            self.distance_array[i][start_index] = self.distance_array[start_index][i]
            self.distance_array[i][end_index] = self.distance_array[end_index][i]

        print("Distances have been updated successfully!")

    def updateItem(self, item):
        '''Updates the given item to the inventory'''
        self.inventory[item.getID()] = item.__dict__
        print("Given product has been successfully updated to the" +
              " inventory!")

    def writeData(self, path=None):
        '''Dump the inventory data to a json file'''
        if not path:
            path = os.path.join(self.data_path, 'Inventory.json')
        with open(path, 'w') as f:
            json.dump(self.inventory, f)

    def _importfromtxt(self, file_name):
        '''Imports the inventory list from a text file'''
        # file_path = os.path.join(os.path.join(os.getcwd(),
        #                                       'inventory_data'),
        #                                       file_name)

        file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'inventory_data'), file_name)
        with open(file_path, 'r') as f:
            file_contents = f.read().split('\n')
            # file_contents is a list of the lines in the file
        item_descriptions = []
        max_coordinate = 0
        for line in file_contents:  # for each line in the contents
            line = line.split('\t')  # split it with tabs
            if line:  # if the line is not empty
                item_descriptions.append(line)  # add it to the list
        item_descriptions = item_descriptions[1:]  # remove the headers
        count = 0  # Number of products that was successfully added.
        for each_item in item_descriptions:
            if len(each_item) != 7:
                continue
            ID = each_item[0]  # Product ID
            x = int(float(each_item[1]))
            y = int(float(each_item[2]))
            location = (x, y)  # Location=(x,y)
            max_coordinate = max(x, y) if x > max_coordinate \
                or y > max_coordinate else max_coordinate
            # Max coordinate is used for grid size calculation
            accessibility = each_item[3:]  # accessibility = [N,W,S,E]
            # Create the product with the given values
            new_product = Product(ID=ID,
                                  location=location,
                                  accessibility=accessibility)
            count += 1  # Increase the count
            self.inventory[ID] = new_product.__dict__
            # If the item is already in the inventory the previous line -->
            # is going to update the product.
        self.setGridSize(max_coordinate+1)  # Expand one more for accessibility
        print("Inventory has been successfully created from the given file!")
        print("Number of products that are added to the inventory: {}"
              .format(str(count)))
        # End of _importfromtxt


def main():
    my_inventory = Inventory((0, 0))
    # my_inventory.importItems('qvBox-warehouse-data-s19-v01.txt')
    my_inventory.importItems('example_inventory.txt')
    # my_inventory.importItems('example.txt')
    my_inventory.calculateDistances()
    my_inventory.readDistances()
    # for line in my_inventory.distance_upper:
    #     print(line)
    # for line in my_inventory.distance_array:
    #     print(line)
    # print(my_inventory.shelves)
    my_inventory.displayMap()


if __name__ == '__main__':
    main()
