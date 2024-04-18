class KnapSack:
    def __init__(self, w, iw, iv):
        self.weight_capacity = w
        self.items_weights = iw
        self.items_values = iv
        
    @staticmethod
    def _insert_in_sorted_array(ratio, ratio_array, i, i_array):
        """
            internal function
            Insert ratio in the sorted array ratio_array, and insert i in i_array at the same index.
        """
        index = 0
        for index in range (len(ratio_array)):
            if ratio_array[index] < ratio:
                break
        temp = 0
        tempi = 0
        for k in range(index, len(ratio_array)):
            if(ratio_array[k] == 0.0):
                ratio_array[k] = ratio    
                i_array[k] = i
                break        
            temp = ratio_array[k]
            ratio_array[k] = ratio
            ratio = temp

            tempi = i_array[k]
            i_array[k] = i
            i = tempi
        return ratio_array, i_array

    def _sort_by_ratio(self):
        """
            internal function
            return the array of items sorted by ratio of items_values/items_weights by descending order
        """
        number_of_items = len(self.items_weights)
        ratio_array = [0.0]*number_of_items
        i_array = [0]*number_of_items
        for i in range(number_of_items):
            ratio_array, i_array = KnapSack._insert_in_sorted_array(self.items_values[i]/self.items_weights[i], ratio_array, i, i_array)
        return i_array

    def upper_bound(self):
        upper_bound = 0.0
        i_array = self._sort_by_ratio()
        weight_available = self.weight_capacity
        for i in range(len(self.items_weights)):
            if(self.items_weights[i_array[i]] > weight_available):
                return upper_bound + self.items_values[i_array[i]]*weight_available/self.items_weights[i_array[i]]
            weight_available -= self.items_weights[i_array[i]]
            upper_bound += self.items_values[i_array[i]]
        return upper_bound

    def lower_bound(self):
        lower_bound = 0
        i_array = self._sort_by_ratio()
        weight_available = self.weight_capacity
        for i in range(len(self.items_weights)):
            if(self.items_weights[i_array[i]] <= weight_available):
                weight_available -= self.items_weights[i_array[i]]
                lower_bound += self.items_values[i_array[i]]
        return lower_bound
    
    def branch_and_bound(self):
        """
            Solve the knapsack problem with a branch and bound approach.
        """
        value1 = 0
        if (self.weight_capacity >= self.items_weights[0]):
            with_first_item = KnapSack(self.weight_capacity-self.items_weights[0],self.items_weights[1:],self.items_values[1:])
            value1 = self.items_values[0] + with_first_item.branch_and_bound()
        withouth_first_item = KnapSack(self.weight_capacity,self.items_weights[1:],self.items_values[1:])
        value2 = withouth_first_item.branch_and_bound()
        return max(value1,value2)
    
    def dynamic_prog(self):
        """
            Solve the knapsack problem with dynamic programmation.
        """
        return 0
    
    def dynamic_prog_scale_change(self):
        """
            Solve the knapsack problem with dynamic programmation.
        """
        return 0