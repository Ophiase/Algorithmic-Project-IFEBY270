# Algorithmic-Project-IFEBY270

An algorithmic project for a University course.
- Implemented
    - Simplexe
    - Nash Equilibrium
    - Knapsack + Reduction basis + Subset sum

# Execution

Execute tests
```bash
./run_tests # first method
make test_verbose # second method
python3 -m unittest tests.<test_name> # for specific test
```

Update Gamut tests
```bash
make update_gamut
```

# More Tests

To add more tests using *unittest* to `src/algorithm/<problem>/<problem>.py`, modify `tests/<problem>.py`.

All methods with a name that begins with `test_` will be executed as tests.

Execute tests with :
```bash
python3 -m unittest tests.<test_name>
```

## Example

To add another *Nash Equilibrium* example, edit `tests/nash_equilibrium.py`, and add the following method to TestNashEquilibrium's class :

```python
def test_example(self):
    self.check_equilibrium(
        A = np.array([[3, 2], [1, 4]]), 
        B = np.array([[2, 1], [3, 2]])
    )
```

