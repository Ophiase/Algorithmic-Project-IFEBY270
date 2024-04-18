TESTS = simplexe knapsack

test:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test);)

test_verbose:
	$(foreach test,$(TESTS),python3 -m unittest tests.$(test) -v;)