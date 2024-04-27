import unittest
import time
from .utils import separator, describe_test, truth_vs_computed
from src.algorithm.knapsack.knapsack import KnapSack


class TestKnapSack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Knap Sack")

    def run(self, test):
        result = super().run(test)
        print("\n" + "=" * 30 + "\n")
        return result

    @staticmethod
    def compute_time(method):
        start_time = time.time()
        method()
        end_time = time.time()
        return end_time - start_time

    @staticmethod
    def benchmark_time(knapsack):
        times = [
            ("Upper Bound       ", TestKnapSack.compute_time(knapsack.upper_bound)),
            ("Lower Bound       ", TestKnapSack.compute_time(knapsack.lower_bound)),
            ("Branch and Bound  ", TestKnapSack.compute_time(knapsack.solve_branch_and_bound)),
            ("Dynamic           ", TestKnapSack.compute_time(knapsack.solve_dynamic_prog)),
            ("Dynamic Adaptative", TestKnapSack.compute_time(knapsack.solve_dynamic_prog_scale_change))
        ]

        print("Times")
        for name, time in sorted(times, key=lambda x: x[1]):
            print(f"\t{name}: {time:.6f} seconds")

    @staticmethod
    def benchmark_precision(knapsack):
        results = [
            ("Dynamic           ", knapsack.solve_dynamic_prog()),
            ("Branch and Bound  ", knapsack.solve_branch_and_bound()),
            ("Upper Bound       ", knapsack.upper_bound()),
            ("Lower Bound       ", knapsack.lower_bound()),
            ("Dynamic Adaptative", knapsack.solve_dynamic_prog_scale_change())
        ]
        print("Results")
        knapsack_solution = results[0][1]
        for name, result in results:
            if(knapsack_solution == 0):
                percentage_off = str(100)
                if(result != 0):
                    percentage_off = "\u221e"#infinity symbole unicode
            else:
                percentage_off = str(round(100*result/knapsack_solution))
            print(f"\t{name} : {result}, {percentage_off}% of the solution , or {result-knapsack_solution} away from the solution")

    def normalized_test(self,
                         knapsack, upper_bound, lower_bound, result,
                         scale_heuristic, result_heuristic,
                         verbose=False, benchmark=True):
        succeed = True

        if upper_bound is not None:
            succeed &= truth_vs_computed("Upper Bound", knapsack.upper_bound(), upper_bound)
        if lower_bound is not None:
            succeed &= truth_vs_computed("Lower Bound", knapsack.lower_bound(), lower_bound)
        if result is not None:
            succeed &= truth_vs_computed("Branch and Bound result", knapsack.solve_branch_and_bound(), result)
            succeed &= truth_vs_computed("Dynamic result", knapsack.solve_dynamic_prog(), result)

        if scale_heuristic and result_heuristic is not None:
            succeed &= truth_vs_computed("Dynamic adaptative",
                                         knapsack.solve_dynamic_prog_scale_change(scale_heuristic),
                                         result_heuristic)

        if benchmark :
            TestKnapSack.benchmark_time(knapsack)
            TestKnapSack.benchmark_precision(knapsack)

        assert(succeed)


    def test_001(self):
        self.normalized_test(
            KnapSack(1,[2,2,2],[2,1,3]),
            1.5, 0,
            0,
            2, 0
        )

    def test_002(self):
        self.normalized_test(
            KnapSack(4,[1,1,1,2],[3,2,1,1]),
            6.5, 6,
            6,
            2, 4
        )

    def test_003(self):
        self.normalized_test(
            KnapSack(3,[1,1,1,2],[3,2,1,1]),
            6.0, 6,
            6,
            2, 4
        )

    def test_004(self):
        self.normalized_test(
            KnapSack(2,[1,1,1,2],[3,2,1,1]),
            5.0, 5,
            5,
            2, 4
        )

    def test_005(self):
        self.normalized_test(
            KnapSack(2,[3,2,1,1],[3,2,1,1]),
            2.0, 2,
            2,
            2, 2
        )

    def test_006(self):
        self.normalized_test(
            KnapSack(3,[2,2,2,2],[2,1,1,1]),
            2.5, 2,
            2,
            2, 2
        )

    def test_006(self):
        self.normalized_test(
            KnapSack(9,[2,2,2,2],[2,1,1,1]),
            5.0, 5,
            5,
            2, 2
        )

    def test_007(self):
        self.normalized_test(
            KnapSack(9,[5,5,4],[10,10,4]),
            18.0, 14,
            14,
            2, 14
        )

    def test_008(self):
        self.normalized_test(
            KnapSack(9,[7,5,4],[14,9,7]),
            17.6, 14,
            16,
            2, 14
        )

    def test_solve_dynamic_prog_scale_change_scale_change(self):
        assert(KnapSack(9,[5,5,4],[10,10,4]).solve_dynamic_prog_scale_change(4) == 12)
        assert(KnapSack(9,[7,5,4],[14,9,7]).solve_dynamic_prog_scale_change(4) == 12)
        assert(KnapSack(9,[5,5,4],[10,10,4]).solve_dynamic_prog_scale_change(5) == 10)
        assert(KnapSack(9,[7,5,4],[14,9,7]).solve_dynamic_prog_scale_change(5) == 10)

if __name__ == '__main__':
    unittest.main()
