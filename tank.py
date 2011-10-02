class Tank(object):
    def __init__(self, attributes_dictionary):
        self.set_attributes(attributes_dictionary)

    def set_attributes(self, attributes_dictionary):
        self.index = attributes_dictionary['index']
        self.status = attributes_dictionary['status']
        self.flag = attributes_dictionary['flag']
        self.x = attributes_dictionary['x']
        self.y = attributes_dictionary['y']
        self.angle = attributes_dictionary['angle']
        self.angvel = attributes_dictionary['angvel']
        self.xv = attributes_dictionary['xv']
        self.yv = attributes_dictionary['vy']

    def react(self, environment):
        """Calculate, based on the environment, what my next action should be."""
        #environment is adicitonary
        #TODO
