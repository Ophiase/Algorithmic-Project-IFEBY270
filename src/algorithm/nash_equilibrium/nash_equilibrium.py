import numpy as np
import pulp

# import contextlib
# from contextlib import contextmanager, suppress

'''
    Find the pair of strategy (x, y) that corresponds to a nash equilibrium for a gain matrix A, B.
'''
class NashEquilibrium:

    def __init__(self, A : np.array, B : np.array):
        """Initialize the NashEquilibrium class with the gain matrices A and B.

        Args:
            A (np.array): The gain matrix for the first player.
            B (np.array): The gain matrix for the second player.

        Raises:
            ValueError: If the shapes of the input matrices A and B are not the same.
        """
        
        self.A = A
        self.B = B

        if A.shape != B.shape :
            raise ValueError()

        self.m = A.shape[0]
        self.n = A.shape[1]

        self.max_a = np.max(A)
        self.max_b = np.max(B)
        self.min_a = np.min(A)
        self.min_b = np.min(B)
        self.max_regret_a = np.max(A) - np.min(A)
        self.max_regret_b = np.max(B) - np.min(B)

    @staticmethod
    def score(A, B, solution : tuple) -> tuple:
        """Calculate the scores for the given solution in the two-player game.

        The score for each player is calculated as the dot product of their strategy
        vector with the corresponding gain matrix and the opponent's strategy vector.

        Args:
            A (np.array): The gain matrix for the first player.
            B (np.array): The gain matrix for the second player.
            solution (tuple): A tuple containing the strategy vectors for the two players,
                in the form (x, y), where x is the strategy vector for the first player
                and y is the strategy vector for the second player.

        Returns:
            tuple: A tuple containing the scores for the two players, in the form
                (score_a, score_b), where score_a is the score for the first player
                and score_b is the score for the second player.
        """
        return (
            solution[0] @ A @ solution[1],
            solution[0] @ B @ solution[1]
        )

    @staticmethod
    def is_valid(A: np.array, B: np.array, solution: tuple, 
                verbose: bool = False, epsilon: float = 1e-4) -> bool:
        """Check if a solution is indeed a Nash equilibrium for the matrices A and B.

        This method checks if the given solution (x, y) is a Nash equilibrium by
        verifying that the current gain for each player is equal to the maximum
        possible gain for that player, within a given tolerance specified by the
        `epsilon` parameter.

        Args:
            A (np.array): The gain matrix for the first player.
            B (np.array): The gain matrix for the second player.
            solution (tuple): A tuple containing the strategy vectors for the two players,
                in the form (x, y), where x is the strategy vector for the first player
                and y is the strategy vector for the second player.
            verbose (bool, optional): If True, print additional information about the
                validity of the solution. Defaults to False.
            epsilon (float, optional): The tolerance value used to check if the current
                gain is equal to the maximum possible gain. Defaults to 1e-6.

        Returns:
            bool: True if the given solution is a Nash equilibrium, False otherwise.
        """
        x, y = solution

        current_gain_a = (x @ A) @ y
        current_gain_b = (x @ B) @ y

        max_gain_a = np.max(np.dot(A, y))
        max_gain_b = np.max(np.dot(x, B))

        is_a_valid = abs(current_gain_a - max_gain_a) <= epsilon
        is_b_valid = abs(current_gain_b - max_gain_b) <= epsilon

        if verbose:
            if not is_a_valid :
                print("x is not valid")
                print(f"Current gain {current_gain_a} \t Wanted gain: {max_gain_a}")
            if not is_b_valid :
                print("y is not valid")
                print(f"Current gain {current_gain_b} \t Wanted gain: {max_gain_b}")

        return is_a_valid and is_b_valid
    
    @staticmethod
    def to_pure(solution: tuple[np.array], seed: int = None) -> tuple[int]:
        """Convert a mixed strategy solution to a pure strategy solution.

        Given a mixed strategy solution (x, y), where x and y are probability
        distributions over the strategies for the two players, this method
        selects a pure strategy for each player by taking the argmax of the
        corresponding probability distribution.

        If there are multiple elements in the argmax of either x or y, one
        of them is chosen randomly. If a seed is provided, the random
        selection is made in a pseudo-random manner using the provided seed.

        Args:
            solution (tuple[np.array]): A tuple containing the mixed strategy
                vectors for the two players, in the form (x, y), where x is
                the mixed strategy vector for the first player and y is the
                mixed strategy vector for the second player.
            seed (int, optional): A seed value to be used for the pseudo-random
                selection of the pure strategy, if there are multiple elements
                in the argmax of either x or y. If not provided, the selection
                will be made using the default random number generator. Defaults
                to None.

        Returns:
            tuple[int]: A tuple containing the indices of the pure strategies
                selected for the two players, in the form (i, j), where i is
                the index of the pure strategy selected for the first player
                and j is the index of the pure strategy selected for the
                second player.
        """
        x, y = solution
        
        if seed is not None:
            np.random.seed(seed)
        
        i = np.random.choice(np.where(x == np.max(x))[0])
        j = np.random.choice(np.where(y == np.max(y))[0])
        
        return (i, j)
    
    @staticmethod
    def _init_xrs_variables(
        i, x, r, s, 
        potential_gain, 
        letter, 
        risk_bound, gain_low_bound, gain_up_bound
        ):
        """
        Init Variables
        """
        x.append(pulp.LpVariable(f"x{letter}_{i}", lowBound=0, upBound=1)) # [0, 1]
        r.append(pulp.LpVariable(f"r{letter}_{i}", lowBound=0, upBound=risk_bound)) # >= 0
        s.append(pulp.LpVariable(f"s{letter}_{i}", cat=pulp.LpBinary)) # {0, 1}
        potential_gain.append(
            pulp.LpVariable(
                f"potential_gain_{letter}_{i}", lowBound=gain_low_bound, upBound=gain_up_bound))
    
    def _init_variables(self):
        '''
        Init Variables
        '''
        
        self.xa, self.xb = [], [] # strategies
        self.ra, self.rb = [], [] # regrets
        self.sa, self.sb = [], [] # supports

        self.potential_gain_a, self.potential_gain_b = [], []

        for i in range(self.m) :
            NashEquilibrium._init_xrs_variables(i, 
                self.xa, self.ra, self.sa,
                self.potential_gain_a,
                "a", self.max_regret_a, self.min_a, self.max_a)
        for j in range(self.n):
            NashEquilibrium._init_xrs_variables(j, 
                self.xb, self.rb, self.sb, 
                self.potential_gain_b, 
                "b", self.max_regret_b, self.min_b, self.max_b)
            
        self.max_gain_a = pulp.LpVariable(
            f"max_gain_a", lowBound=self.min_a, upBound=self.max_a)
        self.max_gain_b = pulp.LpVariable(
            f"max_gain_b", lowBound=self.min_b, upBound=self.max_b)

    def _compute_potential_gain(self):
        '''
        Constraints
        '''

        for i in range(self.m):
            self.prob += self.potential_gain_a[i] ==  \
                pulp.lpSum([self.A[i][j] * self.xb[j] for j in range(self.n)])

        for j in range(self.n):
            self.prob += self.potential_gain_b[j] ==  \
                pulp.lpSum([self.B[i][j] * self.xa[i] for i in range(self.m)])

    def _compute_max_gain(self):
        '''
        Constraints
        '''
                
        for gain in self.potential_gain_a:
            self.prob += self.max_gain_a >= gain
        for gain in self.potential_gain_b:
            self.prob += self.max_gain_b >= gain

    def _compute_risk(self):
        '''
        Constraints
        '''
                
        for i in range(self.m):
            self.prob += self.ra[i] == \
                (self.max_gain_a - self.potential_gain_a[i])
        for j in range(self.n) :
            self.prob += self.rb[j] == \
                (self.max_gain_b - self.potential_gain_b[j])

    def _best_strategy_constraint(self):
        '''
        Constraints
        '''
                
        for i in range(self.m):
            self.prob += self.xa[i] <= self.sa[i]
            self.prob += self.ra[i] <= (1 - self.sa[i]) * self.max_regret_a

        for j in range(self.n) :
            self.prob += self.xb[j] <= self.sb[j]
            self.prob += self.rb[j] <= (1 - self.sb[j]) * self.max_regret_b

    def _make_constraints(self):
        '''
        Constraints
        '''
                
        self.prob += pulp.lpSum(self.xa) == 1.0 # stochastic vectors
        self.prob += pulp.lpSum(self.xb) == 1.0 # stochastic vectors

        self._compute_potential_gain()
        self._compute_max_gain()
        self._compute_risk()
        self._best_strategy_constraint()

    def solve(self, verbose: bool = False) -> tuple[np.array, np.array]:
        """Find a pair of pure strategies that correspond to a Nash equilibrium.

        This method attempts to find a pair of pure strategies (x, y) that
        constitute a Nash equilibrium for the given gain matrices A and B.
        
        The validity and scores of the resulting solution can be verified
        using the `is_valid` and `score` static methods. Perhaps, if properly
        configured, Pulp should not be able to give invalid solution.

        Args:
            verbose (bool, optional): If True, print additional information
                about the solution process. Defaults to False.

        Returns:
            tuple[np.array, np.array]: A tuple containing the pure strategy
                vectors for the two players, in the form (x, y), where x is
                the pure strategy vector for the first player and y is the
                pure strategy vector for the second player. 
                A Nash Equilibrium should always exists, perhaps if no Nash
                equilibrium is found, the method returns `None`.
        """

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

        if self.prob.status == pulp.LpSolutionInfeasible :
            return None

        # EXTRACT STRATEGIE
        return (
            np.array([v.varValue for v in self.xa]),
            np.array([v.varValue for v in self.xb])
        )
