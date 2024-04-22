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
            n is the number of elements in the generated set.
        """
        if(n == None):
            n = random.randrange(20)
        set = [random.randrange(1<<n) for _ in range (n + 1)]
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
        n = len(self.set)
        matrix = [[False] * (self.target + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            matrix[i][0] = True
        for i in range(1, n + 1):
            for j in range(1, self.target + 1):
                if self.set[i - 1] > j:
                    matrix[i][j] = matrix[i - 1][j]
                else:
                    matrix[i][j] = matrix[i - 1][j] or matrix[i - 1][j - self.set[i - 1]]
        if matrix[n][self.target]:
            subset = []
            i, j = n, self.target
            while i > 0 and j > 0:
                if matrix[i][j] != matrix[i - 1][j]:
                    subset.append(self.set[i - 1])
                    j -= self.set[i - 1]
                i -= 1
            return subset[::-1]
        return None