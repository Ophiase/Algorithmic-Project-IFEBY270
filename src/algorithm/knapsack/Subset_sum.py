import random

class SubSet:
    def __init__(self, set, target = None):
        if target == None :
            self.target = set[-1]
            self.set = set[:-1]
        else :
            self.set = set
            self.target = target
        
    @staticmethod
    def generate_random_low_density_subset_problem(n = None):
        """
            Generate a random case of the subset problem with low density.
            n is the number of element of in the generated set.
        """
        if(n == None):
            n = random.randrange(20)
        set = [random.randrange(1<<n) for i in range (n + 1)]
        return SubSet(set)
    
    def LLL(self):
        """
            Solve the subset problem using the LLL algorithm
        """
        return
    
    def dynamic_prog(self):
        """
            Solve the subset problem using dynamic programmation.
        """
        return