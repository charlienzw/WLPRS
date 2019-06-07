class Product:

    def __init__(self,
                 ID=None,
                 name=None,
                 description=None,
                 location=None,
                 accessibility=None):
        self.ID = ID  # ID of the product
        self.name = name  # string -> Human Readable form of the product ID
        self.description = description  # string -> description of the product
        self.location = location  # [(x,y)] tuple -> location of the product
        self.accessibility = accessibility  # 2D array -> accessibility matrix

    def getID(self):
        '''Returns ID of the product'''
        return self.ID

    def getName(self):
        '''Returns name of the product'''
        return self.name

    def getDescription(self):
        '''Returns description of the product'''
        return self.description

    def getLocation(self):
        '''Returns location of the product'''
        return self.location

    def getAccessibility(self):
        '''Returns accessibility of the product'''
        return self.accessibility

    def setName(self, name):
        '''Sets the name of the product'''
        self.name = name
        print("Name of the product has been successfully set!")

    def setDescription(self, description):
        '''Sets the description of the product'''
        self.description = description
        print("Description of the product has been successfully set!")

    def setLocation(self, location):
        '''Sets the location of the product'''
        self.location = location
        print("Location of the product has been successfully set!")

    def setAccessibility(self, accessibility):
        '''Sets the accessibility of the product'''
        self.accessibility = accessibility
        print("Accessibility of the product has been successfully set!")
