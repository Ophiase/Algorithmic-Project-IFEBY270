class Simplexe:
    def init_table(self, canonical_form):
        var_nb = len(canonical_form[0])
        constr_nb = len(canonical_form)
        table = [[0 for _ in range(var_nb + constr_nb)] for _ in range(constr_nb + 1)]
        return table
    
    def print_table(self):
        for row in self.table:
            print(row)

    def print_basic_sol(self):
        if not self.is_optimal():
            basic_sol = [0 for _ in range(len(self.table[0]) - 1)]
            b = [self.canonical_form[i][-1] for i in range(1, len(self.canonical_form))]
            for j in range(len(self.canonical_form[0]), len(self.table[0]) - 1):
                basic_sol[j] = self.canonical_form[j-1][-1]
            print(basic_sol)
        else:
            basic_sol = [0 for _ in range(len(self.table[0]) - 1)]
            for j in range (1, len(self.table)):
                basic_sol[self.vars[j - 1]] = self.table[j][-1]
            print(basic_sol)

    def print_all(self):
        if self.is_optimal():
            print("Optimal basic solution:", end=' ')
            self.print_basic_sol()
            print("Objective function value:", end=' ')
            print(-self.table[0][-1])
        else:
            print("Basic solution:", end=' ')
            self.print_basic_sol()
    
    def pivot(self):
        table_np = np.array(self.table)
        
        for e, coefficient in enumerate(table_np[0, :len(table_np[0]) - 1 - len(self.vars)]):
            if coefficient > 0:
                non_zero_entries = table_np[1:, e] > 0
                if np.any(non_zero_entries):
                    ratios = table_np[1:, -1] / np.where(table_np[1:, e] != 0, table_np[1:, e], 1e-100)
                    min_ratio_index = np.argmin(ratios) + 1
                    return (e, min_ratio_index)
                else:
                    return -1

        return 1 if all(elem <= 0 for elem in table_np[0]) else -1
    
    def update(self):
        pivot_result = self.pivot()
        if pivot_result == 1:
            return 1
        if pivot_result == -1:
            return -1
        incoming, outgoing = pivot_result
        self.vars[outgoing - 1] = incoming

        pivot_value = float(self.table[outgoing][incoming])
        table_copy = [row.copy() for row in self.table]

        for i in range(1, len(table_copy)):
            if i != outgoing:
                factor = self.table[i][incoming] / pivot_value
                table_copy[i] = [x - self.table[outgoing][j] * factor for j, x in enumerate(table_copy[i])]

        table_copy[outgoing] = [x / pivot_value for x in table_copy[outgoing]]

        pivot_row_multiplier = [self.table[0][incoming] * x for x in table_copy[outgoing]]
        table_copy[0] = [x - y for x, y in zip(self.table[0], pivot_row_multiplier)]

        self.table = table_copy

    def execute_simplexe(self):
            while not self.is_optimal():
                res = self.update()
                if res == -1:
                    print("[❌]No optimal solution found.")
                    return
                elif res == 1:
                    print("[✅]Optimal solution found.")
                    return
                
    

    
    
    