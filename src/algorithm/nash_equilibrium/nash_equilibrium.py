import numpy as np
import pulp

import contextlib
from contextlib import contextmanager, suppress

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
        # 
        raise NotImplementedError()

    def _compute_max_gain(self):
        raise NotImplementedError()

    def _make_constraints(self):
        self.prob += pulp.lpSum(self.xa) == 1.0 # stochastic vectors
        self.prob += pulp.lpSum(self.xb) == 1.0 # stochastic vectors

        # compute potential gains
        self._compute_potential_gain()
        # compute max gains
        self._compute_max_gain()

        # if xi > 0 => ri = 0
        # if xi = 0 => ri <= S
        # therefore ri <= (1-delta_i).S
        
        raise NotImplementedError()


    def solve(self, verbose = True) -> np.array:
        self.prob = pulp.LpProblem("Nash Equilibrium", pulp.LpMinimize)

        # VARIABLES
        self._init_variables()
        # CONSTRAINTS
        self._make_constraints()

        # OBJECTIVE FUNCTION
        self.prob += \
            pulp.lpSum(self.ra) + pulp.lpSum(self.rb) 
            # + pulp.abs(pulp.lpSum(ra) - pulp.lpSum(rb)) # contrast ?

        # SOLVE
        with contextlib.redirect_stdout(None):
            self.prob.solve()
    
        if verbose :
            print(f"Status: {pulp.LpStatus[self.prob.status]}")
            for v in self.prob.variables():
                print(f"{v.name}: {v.value()}")
            print(f"Objective: {pulp.value(self.prob.objective)}")
        
        self.solution = pulp.value(self.prob.objective)

        # EXTRACT STRATEGIE

        # TODO

        return self.solution
