from inventory import Inventory


class Distances:

    def __init__(self, inventory, start_point):
        self.vertices = []  # Vertex list in the graph
        self.distance_array = []  # 2D array for distances of the vertices
        self.start_point = start_point
        self.inventory = inventory

    def run(self):
        self.calculateDistances()
        return self.distance_array

    def calculateDistances(self):
        '''
            For a given inventory calculate distances between each 2 products
            Input: Inventory object
            Output: Success or Error message for updating the array!
        '''
        # We will treat the product coordinates in the inventory
        # as shelves. The distances will be calculated based the
        # accessibility of each product.

        start_point_ID = '000000'  # For now we are assuming this.
        axis = [start_point_ID]
        coordinates = [(self.start_point[0] + 1, self.start_point[1])]

        # axis = []
        # coordinates = []

        # We add one to the start_point to make it look like there is a shelf.
        for ID in self.inventory.inventory.keys():
            my_product = self.inventory.inventory[ID]
            axis.append(ID)  # Axis of the matrix, which product it represents.
            coordinates.append(my_product['location'])
            # TODO: Add accessibility here as well.
            # For now, we know that they can be accessed from only one side.
        to_visit = coordinates[:]
        to_visitId = axis[:]
        for i in range(len(coordinates)):
            point = coordinates[i]
            distance_list = [0]
            to_visit.remove(point)
            to_visitId.remove(axis[i])
            sourcept = (point[0] - 1, point[1])
            for j in range(len(to_visit)):
                coordinate = to_visit[j]
                destpt = (coordinate[0] - 1, coordinate[1])
                distance = self.traverse(sourcept, destpt, coordinates)
                if distance == -1:
                    raise ValueError("From " + axis[i] + " to " + to_visitId[j] + " is unreachable!")
                distance_list.append(distance)
            # print(distance_list)
            self.distance_array.append(distance_list)
        # Take the symmetric of the distance matrix to fill the empty spaces.
        for i in range(1, len(self.distance_array)):
            prefix = []
            for j in range(i):
                prefix.append(self.distance_array[j][i])
            self.distance_array[i] = prefix + self.distance_array[i]
        # distance array contains the 2D distance matrix we need

    def traverse(self, sourcept, destpt, shelves):
        '''Traverses from start to destination and returns the shortest path'''
        rowNum = [-1, 0, 0, 1]  # Row/Col helper list for checking adjacent
        colNum = [0, -1, 1, 0]  # tiles.
        visited = {}  # Initialize the visited dictionary.
        for i in range(self.inventory.grid_size):
            for j in range(self.inventory.grid_size):
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
                    and (row, col) not in shelves \
                        and not visited[(row, col)]:
                    visited[(row, col)] = True
                    distances[(row, col)] = distances[current_node] + 1
                    to_visit.append((row, col))
        return -1  # If we cannot reach the destination

    def isValid(self, position):
        '''Is the given coordinate valid in the grid or not'''
        if (position[0] < self.inventory.grid_size) \
            and position[1] < self.inventory.grid_size \
                and position[0] >= 0 and position[1] >= 0:
            return True
        else:
            return False


def main():
    start_point = (0, 0)
    my_inventory = Inventory()
    #my_inventory.importItems('example_inventory.txt')
    my_inventory.importItems('qvBox-warehouse-data-s19-v01.txt')
    my_distance = Distances(my_inventory, start_point)
    print(my_distance.run())


if __name__ == '__main__':
    main()
