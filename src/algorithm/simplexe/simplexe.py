class Simplexe:
    def init_table(self, canonical_form):
        var_nb = len(canonical_form[0])
        constr_nb = len(canonical_form)
        table = [[0 for _ in range(var_nb + constr_nb)] for _ in range(constr_nb + 1)]
        return table
    
    def print_table(self):
        for row in self.table:
            print(row)

    def __init__(self, canonical_form):
        self.table = self.init_table(canonical_form)

    
    
    