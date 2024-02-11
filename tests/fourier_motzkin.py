import unittest
from .utils import describe_test
from src.algorithm.fourier_motzkin.fourier_motzkin import FourierMotzkin

class TestFourierMotzkin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Fourier Motzkin")

    def test_something(self):
        assert(True)

    def test_something_else(self):
        assert(True)

if __name__ == '__main__':
    unittest.main()
