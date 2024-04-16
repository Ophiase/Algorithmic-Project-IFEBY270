import numpy as np
import pulp

# import contextlib
# from contextlib import contextmanager, suppress

'''
    Find the pair of strategy (x, y) that corresponds to a nash equilibrium for a gain matrix A, B.
'''
class NashEquilibrium:
    def __init__(self, A : np.array, B : np.array):
        self.A = A
        self.B = B

        if A.shape != B.shape :
            raise ValueError()

        self.m = A.shape[0]
        self.n = A.shape[1]

        self.max_regret_a = np.max(A) - np.min(A)
        self.max_regret_b = np.max(B) - np.min(B)

    @staticmethod
    def score(A, B, solution : tuple) -> tuple:
        return (
            solution[0] @ A @ solution[1],
            solution[0] @ B @ solution[1]
        )

    @staticmethod
    def is_valid(solution : tuple) -> bool:
        raise NotImplementedError()

    @staticmethod
    def _init_xrs_variables(i, x, r, s, potential_gain, letter, r_bound):
        x.append(pulp.LpVariable(f"x{letter}_{i}", lowBound=0, upBound=1)) # [0, 1]
        r.append(pulp.LpVariable(f"r{letter}_{i}", lowBound=0, upBound=r_bound)) # >= 0
        s.append(pulp.LpVariable(f"s{letter}_{i}", cat=pulp.LpBinary)) # {0, 1}
        potential_gain.append(
            pulp.LpVariable(
                f"potential_gain_{letter}_{i}", lowBound=0, upBound=r_bound)) # >= 0
    
    def _init_variables(self):
        self.xa, self.xb = [], [] # strategies (delta_i)
        self.ra, self.rb = [], [] # regrets
        self.sa, self.sb = [], [] # supports

        self.potential_gain_a, self.potential_gain_b = [], []

        for i in range(self.m) :
            NashEquilibrium._init_xrs_variables(i, 
                self.xa, self.ra, self.sa,
                self.potential_gain_a,
                "a", self.max_regret_a)
        for j in range(self.n):
            NashEquilibrium._init_xrs_variables(j, 
                self.xb, self.rb, self.sb, 
                self.potential_gain_b, 
                "b", self.max_regret_b)

        self.max_gain_a = pulp.LpVariable(
            f"max_gain_a", lowBound=0, upBound=self.max_regret_a)
        self.max_gain_b = pulp.LpVariable(
            f"max_gain_b", lowBound=0, upBound=self.max_regret_b)

    def _compute_potential_gain(self):
        for i in range(self.m):
            self.prob += self.potential_gain_a[i] ==  \
                pulp.lpSum([self.A[i][j] * self.xb[j] for j in range(self.n)])

        for j in range(self.n):
            self.prob += self.potential_gain_b[j] ==  \
                pulp.lpSum([self.B[i][j] * self.xa[i] for i in range(self.m)])

    def _compute_max_gain(self):
        for gain in self.potential_gain_a:
            self.prob += self.max_gain_a >= gain
        for gain in self.potential_gain_b:
            self.prob += self.max_gain_b >= gain

    def _compute_risk(self):
        for i in range(self.m):
            self.prob += self.ra[i] == \
                (self.max_gain_a - self.potential_gain_a[i])
        for j in range(self.n) :
            self.prob += self.rb[j] == \
                (self.max_gain_b - self.potential_gain_b[i])

    def _best_strategy_constraint(self):

        for i in range(self.m):
            self.prob += self.sa[i] == (self.xa[i] != 0)
            self.prob += self.ra[i] <= (1 - self.sa[i]) * self.max_regret_a

        for j in range(self.n) :
            self.prob += self.sb[j] == (self.xb[j] != 0)
            self.prob += self.rb[j] <= (1 - self.sb[j])*self.max_regret_b

    def _make_constraints(self):
        self.prob += pulp.lpSum(self.xa) == 1.0 # stochastic vectors
        self.prob += pulp.lpSum(self.xb) == 1.0 # stochastic vectors

        self._compute_potential_gain()
        self._compute_max_gain()
        self._compute_risk()
        self._best_strategy_constraint()
        
        #raise NotImplementedError()

    def solve(self, verbose = False) -> np.array:
        '''
            Returns a couple (x,y) of pure strategies that corresponds 
            to a Nash Equilibrium.
            Validity and Scores of this couple can be verified 
            using the static methods is_valid and score,

        '''
        self.prob = pulp.LpProblem("Nash_Equilibrium", pulp.LpMinimize)

        # VARIABLES
        self._init_variables()
        # CONSTRAINTS
        self._make_constraints()

        # OBJECTIVE FUNCTION
        self.prob += \
            pulp.lpSum(self.ra) + pulp.lpSum(self.rb) 
            # + pulp.abs(pulp.lpSum(ra) - pulp.lpSum(rb)) # contrast ?

        # SOLVE
        self.prob.solve(pulp.apis.PULP_CBC_CMD(msg=False))
    
        if verbose :
            print(f"Status: {pulp.LpStatus[self.prob.status]}")
            for v in self.prob.variables():
                print(f"{v.name}: {v.value()}")
            print(f"Objective: {pulp.value(self.prob.objective)}")
        
        self.solution = pulp.value(self.prob.objective)

        # EXTRACT STRATEGIE

        return (
            np.array([v.varValue for v in self.xa]),
            np.array([v.varValue for v in self.xb])
        )
