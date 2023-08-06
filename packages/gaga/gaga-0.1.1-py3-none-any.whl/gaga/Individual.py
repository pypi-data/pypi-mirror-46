# This is the class file for an individual in the population.
# The genes of the individual are passed in when the GA is created
'''
HELLO
'''
class Individual:

    def __init__(self, chromosome):

        self.genes = self.validate(chromosome)
        self.evaluate()
        self.data = {}

