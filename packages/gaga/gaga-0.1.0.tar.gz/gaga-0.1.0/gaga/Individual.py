# This is the class file for an individual in the population.
# The genes of the individual are passed in when the GA is created

class Individual:

    def __init__(self, chromosome):

        self.CHROMOSOME = self.VALIDATE(chromosome)
        self.EVALUATE()
        self.data = {}

