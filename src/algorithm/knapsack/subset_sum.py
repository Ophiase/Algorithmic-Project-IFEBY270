import random
import numpy as np
from fractions import Fraction

class SubSet:
    def __init__(self, set, target = None):
        if target == None :
            self.target = set[-1]
            self.set = set[:-1]
        else :
            self.set = set
            self.target = target

    @staticmethod
    def generate_random_low_density_subset_problem(n = None, density = 0.5):
        """
            Generate a random case of the subset problem with low density.
        Args:
            n (int): number of elements in the generated set. /!\ the elements are exponentials in n, it is not recommanded to set n bigger than 20.
        Returns:
            SubSet: random subset problem
        """
        if(n == None):
            n = random.randrange(20)
        sup = n/density
        set = [random.randrange(1 << round(sup) - 1, 1 << round(sup)) for _ in range (n)]

        length = random.randint(1, n)
        l = [random.randint(0, n-1) for _ in range(length)]
        target = np.sum([set[i] for i in l])
        return SubSet(set,target)
    
    def create_basis(self):
        """
            Create the initial basis for the LLL algorithm
        Returns:
            list: the basis
        """
        if (len(self.set) == 0 or self.target == 0):
            self.generate_random_low_density_subset_problem()
        B = np.identity(len(self.set) + 1) * 2
        all = self.set + [self.target]
        root = np.sqrt(len(self.set))

        B[len(self.set)] = 1
        for i in range(len(all)):
            B[i][len(self.set)] = all[i]

        return B
    
    def density(self):
        """
            Calculate the density of the subset problem
        Returns:
            float: the density
        """
        return len(self.set) / np.log2(self.target)
    
    @staticmethod
    def GramSchmidt(basis):
        """
            The Gram-Schmidt algorithm
        Args:
            list: the basis
        Returns:
            list: the orthogonalized basis
        """
        u = []
        for vi in basis:
            ui = np.array(vi)
            for uj in u:
                ui = ui - (np.dot(vi, uj) / np.dot(uj, uj)) * uj
            if any(ui):
                u.append(ui)
        return u
    
    def Normalize(self, basis, ortho, mu_kj, k, j):
        """
            Normalize the basis
        Args:
            list: the basis
            list: the orthogonalized basis
            float: the value of the element mu_kj
            int: the index k
            int: the index j
        Returns:
            list, list: the normalized basis and the orthogonalized basis
        """
        if abs(mu_kj) > 0.5:
            basis[k] = basis[k] - basis[j] * round(mu_kj)
            ortho = self.GramSchmidt(basis)
        return basis, ortho
    
    def LLL(self, basis):
        """
            The LLL algorithm
        Args:
            list: the basis
        Returns:
            list: the reduced basis
        """
        n = len(basis)
        basis = np.array(basis, dtype=float)
        ortho = self.GramSchmidt(basis)
        delta = 0.75

        def mu(i, j) -> Fraction:
            return np.dot(ortho[j], basis[i]) / np.dot(ortho[j], ortho[j])
        
        k = 1
        while k < n:
            for j in range(k - 1, -1, -1):
                mu_kj = mu(k,j)
                basis, ortho = self.Normalize(basis, ortho, mu_kj, k, j)
            if np.dot(ortho[k], ortho[k]) >= (delta - mu(k, k - 1) ** 2) * np.dot(ortho[k - 1], ortho[k - 1]):
                k += 1
            else:
                temp = np.copy(basis[k])
                basis[k] = np.copy(basis[k - 1])
                basis[k - 1] = np.copy(temp)
                ortho = self.GramSchmidt(basis)
                k = max(k - 1, 1)
        
        return basis


    def solve_LLL(self):
        """
            Solve the subset problem using the LLL algorithm
        Returns:
            int, list: the target (or the closest value to it), and the subset.
        """
        B = self.LLL(self.create_basis())

        for y in B:
            if y[-1] == 0. and all(y[i] == 1 or y[i] == -1 for i in range(len(y) - 1)):
                X = [1 if val == -1 else 0 for val in y[:-1]]
                res = np.dot(self.set, X)
                if res == self.target:
                    return X
                break

        return None
    
    def solve_dynamic_prog(self):
        """
            Solve the subset problem using dynamic programmation.
        Returns:
            int, list: the target (or the closest value to it), and the subset.
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
            return self.target, subset[::-1]
        else:
            # Find the closest value to the target sum
            closest_sum = 0
            for i in range(self.target, -1, -1):
                if matrix[n][i]:
                    closest_sum = i
                    break
            # Reconstruct the subset for the closest sum
            subset = []
            i, j = n, closest_sum
            while i > 0 and j > 0:
                if matrix[i][j] != matrix[i - 1][j]:
                    subset.append(self.set[i - 1])
                    j -= self.set[i - 1]
                i -= 1
            return closest_sum, subset[::-1]
