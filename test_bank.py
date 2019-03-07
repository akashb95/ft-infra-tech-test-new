import unittest
import bank


class TestBank(unittest.TestCase):
    def setUp(self):
        self.b = bank.Bank(1000)
        self.amts = [10000, 100, 20, 0.56, 95.6678]
        self.invalid_amts = [-1000, 0, -0.0001]

    def test_initialize(self):
        # check invalid initialisation amounts
        for ia in self.invalid_amts:
            with self.assertRaises(RuntimeError):
                bank.Bank(ia)

    def test_deposit(self):
        # ensure get_balance() works well
        self.assertEqual(self.b.get_balance(), 1000)

        for i in range(0, len(self.amts)):
            # as we now know get_balance() works
            curr_balance = self.b.get_balance()

            # since doing float calculations, use AlmostEqual
            self.assertAlmostEqual(self.b.deposit(self.amts[i]), curr_balance + self.amts[i])

        # should return False if initialised, but invalid values entered
        for i in range(0, len(self.invalid_amts)):
            self.assertFalse(self.b.deposit(self.invalid_amts[i]))

    def test_withdraw(self):
        # ensure get_balance() works well
        self.assertEqual(self.b.get_balance(), 1000)

        for i in range(0, len(self.amts)):
            # as we now know get_balance() works
            curr_balance = self.b.get_balance()

            # since doing float calculations, use AlmostEqual
            self.assertAlmostEqual(self.b.withdraw(self.amts[i]), curr_balance - self.amts[i])

        # should return False if initialised, but invalid values entered
        for i in range(0, len(self.invalid_amts)):
            self.assertFalse(self.b.withdraw(self.invalid_amts[i]))

    def test_statement(self):
        expected = """| date || credit || debit || balance |
| 07/03/19 || 95.67 || 0 || 11175.11 |
| 07/03/19 || 0 || 0.56 || 11079.44 |
| 07/03/19 || 0 || 20.00 || 11080.00 |
| 07/03/19 || 100.00 || 0 || 11100.00 |
| 07/03/19 || 10000.00 || 0 || 11000.00 |
| 07/03/19 || 1000.00 || 0 || 1000.00 |
"""

        self.b.deposit(10000)
        self.b.deposit(100)
        self.b.withdraw(20)
        self.b.withdraw(0.56)
        self.b.deposit(95.6678)
        self.assertEqual(self.b.statement(), expected)


if __name__ == "__main__":
    unittest.main()
