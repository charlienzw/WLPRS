from order import Order
import os

class OrderList:

    def __init__(self):
        self.curIndex = -1
        self.fulfilled = []
        self.order_list = []

    def importOrderList(self, file_name):
        if file_name.endswith('.txt'):
            self._importfromtxt(file_name)
        elif file_name.endswith('.csv'):
            # self._importfromcsv(file_name)  # TODO: implement import from csv
            raise ValueError("Import from csv is not implemented yet!")
        else:
            raise ValueError("Invalid file type is given!")
    
    def _importfromtxt(self, file_name):
        self.order_list = []
        self.fulfilled = []
        self.curIndex = -1
        file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'order_lists'),
                                              file_name)
        with open(file_path, 'r') as f:
            orders = f.read().strip().split('\n')
        
        for order in orders:
            products = order.strip().split('\t')
            self.order_list.append(products)
            self.fulfilled.append(0)
        print("\nOrder list has been successfully loaded from the given file.")

    def inputOrder(self, order_string):
        products = order_string.strip().split('\t')
        self.order_list.append(products)
        self.fulfilled.append(0)
        print("\nThe new order has been successfully added to the order list.")
    
    def nextOrder(self):
        if self.curIndex >= len(self.order_list):
            return (-1, [])
        
        self.curIndex += 1
        while self.fulfilled[self.curIndex] == 1:
            self.curIndex += 1
        self.fulfilled[self.curIndex] = 1
        return (self.curIndex, self.order_list[self.curIndex])

    def specificOrder(self, index):
        if index >= len(self.order_list):
            return (-1, [])
        if self.fulfilled[index] == 1:
            return (0, self.order_list[index])
        self.fulfilled[index] = 1
        return (1, self.order_list[index])

    

def main():
    my_order_list = OrderList()
    my_order_list.importOrderList("qvBox-warehouse-orders-list-part01.txt")
    print(my_order_list.nextOrder())
    print(my_order_list.specificOrder(10))


if  __name__ == "__main__":
    main()
