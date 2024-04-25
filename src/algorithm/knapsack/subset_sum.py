import random
import numpy as np
from math import ceil, floor

def print_matrix(matrix):
    for row in matrix:
        print("|", end="")
        for value in row:
            print("{:10.2f}".format(value), end="")
        print(" |")

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
        Args:
            n (int): number of elements in the generated set. /!\ the elements are exponentials in n, it is not recommanded to set n bigger than 20.
        Returns:
            SubSet: random subset problem
        """
        if(n == None):
            n = random.randrange(20)
        target = random.randrange(1<<n)
        set = [random.randrange(min(1<<n,target)) for _ in range (n)]
        return SubSet(set,target)
    
    def create_basis(self):
        """
            Create the initial basis for the LLL algorithm
        Returns:
            list: the basis
        """
        if (len(self.set) == 0 or self.target == 0):
            self.generate_random_low_density_subset_problem()
        B = np.identity(len(self.set) + 1)
        all = self.set + [self.target]
        root = np.sqrt(len(self.set))

        B[len(self.set)] = 1/2
        for i in range(len(all)):
            B[i][len(self.set)] = all[i] * ceil(root / 2)

        return B
    
    def density(self):
        """
            Calculate the density of the subset problem
        Returns:
            float: the density
        """
        return len(self.set) / np.log2(self.target)
    
    def RED(self, basis, mu, k, l):
        if np.abs(mu[k][l]) > 1/2:
            r = floor(mu[k][l] + 1/2)
            basis[k] = basis[k] - r * basis[l]
            for j in range(l):
                mu[k][j] = mu[k][j] - r * mu[l][j]
            mu[k][l] = mu[k][l] - r
        return basis, mu
                    
    def LLL(self, basis):
        """
            The LLL algorithm
        Args:
            list: the basis
        Returns:
            list: the reduced basis
        """
        n = len(basis)
        basis_c = np.copy(basis)
        b_star = np.copy(basis_c)
        B = np.array(n * [0])
        mu = np.zeros((n,n))

        # Step 1 & 2
        B[0] = b_star[0] @ b_star[0]
        for i in range(1,n):
            b_star[i] = basis_c[i]
            for j in range(i):
                mu[i][j] = (basis_c[i] @ b_star[j]) / B[j]
                b_star[i] = b_star[i] - mu[i][j] * b_star[j]
                B[i] = (b_star[i] @ b_star[i])

        # Step 3
        k = 1

        while (1):
            # Step 4
            basis_c, mu = self.RED(basis_c, mu, k, k - 1)

            # Step 5
            if (B[k] >= (3/4 - mu[k][k-1]*mu[k][k-1]) * B[k-1]):
                for l in range(k-2,-1,-1):
                    basis_c, mu = self.RED(basis_c, mu, k, l)
                k += 1
                if k >= n:
                    return basis_c
            else:
                m = mu[k][k-1]
                b = B[k] + m * m * B[k-1]
                mu[k][k-1] = m * B[k-1] / b
                B[k] = B[k-1] * B[k] / b
                B[k-1] = b
                basis_c[k], basis_c[k-1] = basis_c[k-1], basis_c[k]
                if k > 1:
                    for j in range (k-2):
                        mu[k][j], mu[k-1][j] = mu[k-1][j], mu[k][j]
                for i in range (k+1, n):
                    t = mu[i][k]
                    mu[i][k] = mu[i][k-1] - m * t
                    mu[i][k-1] = t + mu[k][k-1] * mu[i][k]
                k = max(k-1,1)

        return basis_c

    def solve_LLL(self):
        """
            Solve the subset problem using the LLL algorithm
        Returns:
            int, list: the target (or the closest value to it), and the subset.
        """
        B = self.LLL(self.create_basis())
        X = np.zeros(len(self.set)+1)
        n = len(self.set)

        print_matrix(B)

        for y in B:
            if y[-1] == 0 and (y[i] == 1/2 or y[i] == -1/2 for i in range(len(y) - 1)):
                for i in range(n):
                    X[i] = y[i] + 1/2
                if y @ X == self.target:
                    return X
                for i in range(n):
                    X[i] = -y[i] + 1/2
                if y @ X == self.target:
                    return X

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
