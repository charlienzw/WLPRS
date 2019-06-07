import os


class Order:

    def __init__(self, id_list=[]):
        self.id_list = id_list

    def addOrder(self, ID):
        '''Adds the given ID to the order list'''
        if ID not in self.id_list:
            self.id_list.append(ID)
            print("Given ID has been successfully added to the order")
        else:
            print("Given product is already in the order list!")

    def importOrder(self, file_name):
        '''Gets the product ID list from the given file'''

        if file_name.endswith('.txt'):
            self._importfromtxt(file_name)
        elif file_name.endswith('.csv'):
            # self._importfromcsv(file_name)  # TODO: implement import from csv
            raise ValueError("Import from csv is not implemented yet!")
        else:
            raise ValueError("Invalid file type is given!")

    def _importfromtxt(self, file_name):
        '''Imports the order list from a txt file, each line one product ID'''
        # file_path = os.path.join(os.path.join(os.getcwd(),
        #                                       'order_lists'),
        #                                       file_name)
        file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'order_lists'),
                                              file_name)
        with open(file_path, 'r') as f:
            file_contents = f.read().split('\n')
        for line in file_contents:
            if line:
                self.id_list.append(line)
        print("\nOrder list has been successfully imported from the given file.")


def main():
    my_order = Order()
    my_order.importOrder('order_of_fifteen.txt')
    for id in my_order.id_list:
        print(id)


if __name__ == '__main__':
    main()
