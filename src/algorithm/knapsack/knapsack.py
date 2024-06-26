import sys
import random

class KnapSack:
    def __init__(self, weight_capacity, items_weights, items_values):
        self.weight_capacity = weight_capacity
        self.items_weights = items_weights
        self.items_values = items_values

    def __str__(self):
        return f"KnapSack of weight capacity : {self.weight_capacity}, of items weights : {self.items_weights} and of items values : {self.items_values}"

    @staticmethod
    def generate_random_knapsack(seed = 989389237839084, n = None):
        """
            Generate a random knapsack.
        Args:
            n (int): number of elements in the knapsack must
        Returns:
            KnapSack: random knsapsack
        """
        random.seed(seed)
        if(n == None):
            n = random.randrange(1,20)
        weight_capacity = random.randrange(1,n*n+1)
        items_weights = [random.randrange(weight_capacity) for _ in range (n)]
        items_values = [random.randrange(n*n+1) for _ in range (n)]
        return KnapSack(weight_capacity, items_weights, items_values)

    def _partition(self, low, high):
        if self.items_weights[high] == 0 :
            pivot = self.items_values[high]
        else :
            pivot = self.items_values[high]/self.items_weights[high]
        i = low - 1
        for j in range(low, high):
            if self.items_weights[j] == 0 or self.items_values[j]/self.items_weights[j] > pivot:
                i = i + 1
                (self.items_values[i], self.items_values[j]) = (self.items_values[j], self.items_values[i])
                (self.items_weights[i], self.items_weights[j]) = (self.items_weights[j], self.items_weights[i])
        (self.items_values[i + 1], self.items_values[high]) = (self.items_values[high], self.items_values[i + 1])
        (self.items_weights[i + 1], self.items_weights[high]) = (self.items_weights[high], self.items_weights[i + 1])
        return i + 1

    def _partition(self, low, high):
        pivot = self.items_values[high]/self.items_weights[high]
        i = low - 1
        for j in range(low, high):
            if self.items_values[j]/self.items_weights[j] > pivot:
                i = i + 1
                (self.items_values[i], self.items_values[j]) = (self.items_values[j], self.items_values[i])
                (self.items_weights[i], self.items_weights[j]) = (self.items_weights[j], self.items_weights[i])
        (self.items_values[i + 1], self.items_values[high]) = (self.items_values[high], self.items_values[i + 1])
        (self.items_weights[i + 1], self.items_weights[high]) = (self.items_weights[high], self.items_weights[i + 1])
        return i + 1

    def _quickSort(self, low, high):
        if low < high:
            pi = self._partition(low, high)
            self._quickSort(low, pi - 1)
            self._quickSort(pi + 1, high)

    def _sort_by_ratio(self):
        """
            Sort self.items_weights and self.items_values by ratio items_values/items_weights in descending order by calling quicksort algorithm.
        """
        self._quickSort(0, len(self.items_values)-1)

    def upper_bound(self):
        """
           Returns an upper_bound in O(n) by sorting the elements of the knapsack by ratio of value/weight
        Returns:
            int: an upper_bound of the knapsack maximum value
        """
        upper_bound = 0.0
        self._sort_by_ratio()
        weight_available = self.weight_capacity
        for i in range(len(self.items_weights)):
            if(self.items_weights[i] > weight_available):
                return upper_bound + self.items_values[i]*weight_available/self.items_weights[i]
            weight_available -= self.items_weights[i]
            upper_bound += self.items_values[i]
        return upper_bound

    def lower_bound(self):
        """
           Returns a lower_bound in O(n) by sorting the elements of the knapsack by ratio of value/weight 
        Returns:
            int: a lower_bound of the knapsack maximum value
        """
        lower_bound = 0
        self._sort_by_ratio()
        weight_available = self.weight_capacity
        for i in range(len(self.items_weights)):
            if(self.items_weights[i] <= weight_available):
                weight_available -= self.items_weights[i]
                lower_bound += self.items_values[i]
        return lower_bound

    def _branch_and_bound(self,max_iteration):
        if max_iteration <= 0 or len(self.items_weights) == 0:
            return 0,max_iteration
        upper_bound = self.upper_bound()
        if upper_bound == self.lower_bound():#if both bounds are equals, then it's the value of the knapsack.
            return int(upper_bound),max_iteration
        value1 = 0
        if (self.weight_capacity >= self.items_weights[0]):
            with_first_item = KnapSack(self.weight_capacity - self.items_weights[0],self.items_weights[1:],self.items_values[1:])
            value1,max_iteration = with_first_item._branch_and_bound(max_iteration-1)
            value1 += self.items_values[0]
            if(value1 == upper_bound):#if it's equal to the upper bound, then it's the value of the knapsack.
                return int(value1),max_iteration
        if max_iteration <= 0:
            return int(value1),max_iteration
        withouth_first_item = KnapSack(self.weight_capacity,self.items_weights[1:],self.items_values[1:])
        value2,max_iteration = withouth_first_item._branch_and_bound(max_iteration-1)
        return int(max(value1,value2)),max_iteration

    def solve_branch_and_bound(self, return_max_iteration = False, max_iteration = 50, max_recursion_depth = 1000):
        """
            Solve the knapsack problem with a branch and bound approach.
        Args:
            return_max_iteration (bool): set it to True if you wish the function to return both the knapsack value, and the number of iteration remaining.If the number of iteration returned is 0, the result may not be the max value.
            max_iteration (int): maximum amount of recursive calls.
            max_recursion_depth (int): maximum depth of recursive calls (no need to modify it unless bag length > 1000).
            return_max_iteration (bool): set it to True if you wish the function to return both the knapsack value, and the number of iteration remaining.If the number of iteration returned is 0, the result may not be the max value.
        Returns:
            int: the maximum value of the knapsack
        """
        sys.setrecursionlimit(max_recursion_depth)
        self._sort_by_ratio()
        if(return_max_iteration):
            return KnapSack._branch_and_bound(self,max_iteration)
        return KnapSack._branch_and_bound(self,max_iteration)[0]

    @staticmethod
    def _delete_redudant_elements(array):
        """
            Removes all unecessary values in the list for the dynamic programmtion solver of knapsack
        Args:
            array (list of two ints): the array to sort
        Returns:
            list of list of two ints: the sorted array
        """
        i = 0
        while i < len(array):
            j = i + 1
            while j < len(array):
            #sort by value
                if array[i][0] > array[j][0]:
                    if array[i][1] <= array[j][1]:
                        del array[j]
                        continue #continue skips j += 1
                elif array[i][0] < array[j][0]:
                    if array[i][1] >= array[j][1]:
                        del array[i]
                        i -= 1
                        break
                else : # array[i][0] == array[j][0]
                    if array[i][1] <= array[j][1]:
                        del array[j]
                        continue #continue skips j += 1
                    else:
                        del array[i]
                        i -= 1
                        break
            #sort by weight
                if array[i][1] < array[j][1]:
                    if array[i][0] >= array[j][0]:
                        del array[j]
                        continue #continue skips j += 1
                elif array[i][1] > array[j][1]:
                    if array[i][0] <= array[j][0]:
                        del array[i]
                        i -= 1
                        break
                else: # array[i][1] == array[j][1]:
                    if array[i][0] >= array[j][0]:
                        del array[j]
                        continue #continue skips j += 1
                    else:
                        del array[i]
                        i -= 1
                        break
                j += 1
            i += 1
        return array

    def solve_dynamic_prog(self):
        """
            Solve the knapsack problem with dynamic programmation.
        Returns:
            int: the maximum value of the knapsack
        """
        S = [[0,0]]
        for i in range(len(self.items_values)):
            S_size = len(S)
            for j in range(S_size):
                if(S[j][1] + self.items_weights[i] <= self.weight_capacity):
                    S.append([S[j][0] + self.items_values[i], S[j][1] + self.items_weights[i]])
            KnapSack._delete_redudant_elements(S)

        #returns the max value of S
        max = 0
        for w in S:
            if w[0] > max:
               max = w[0]
        return max

    def solve_dynamic_prog_scale_change(self, mu = 2):
        """
            Solve the knapsack problem with dynamic programmation and scale change.
        Args:
            mu (int): the int by which the items values will be divided for the scale change.
        Returns:
            int: the maximum value of the knapsack.
        """
        S = [[0,0]]
        for i in range(len(self.items_values)):
            S_size = len(S)
            for j in range(S_size):
                if(S[j][1] + self.items_weights[i] <= self.weight_capacity):
                    S.append([S[j][0] + self.items_values[i]//mu, S[j][1] + self.items_weights[i]])
            KnapSack._delete_redudant_elements(S)
        #returns the max value of S
        max = 0
        for w in S:
            if w[0] > max:
               max = w[0]
        return max*mu
