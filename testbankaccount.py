import unittest

from bankaccount import BankAccount

class TestBankAcount(unittest.TestCase):

    def setUp(self):
        # Create a test BankAccount object
        self.account = BankAccount()

        # Provide it with some property values        
        self.account.balance = 1000.0

    def test_legal_deposit_works(self):
        # Your code here to test that depsositing money using the account's
        # 'deposit' function adds the amount to the balance.
        self.account.deposit(200)
        self.assertEqual(self.account.balance, 1200.00)


    def test_illegal_deposit_raises_exception(self):
        # Your code here to test that depositing an illegal value (like 'bananas'
        # or such - something which is NOT a float) results in an exception being
        # raised.

        self.assertRaises((TypeError, ValueError), self.account.deposit('bananas'))
        self.assertRaises((TypeError, ValueError), self.account.deposit([]))
        self.assertRaises((TypeError, ValueError), self.account.deposit('123.s'))


    def test_legal_withdrawal(self):
        # Your code here to test that withdrawing a legal amount subtracts the
        # funds from the balance.
        self.account.withdraw(28.50)
        self.assertEqual(self.account.balance, 971.50)
        

    def test_illegal_withdrawal(self):
        # Your code here to test that withdrawing an illegal amount (like 'bananas'
        # or such - something which is NOT a float) raises a suitable exception.
        self.assertRaises((TypeError, ValueError), self.account.withdraw('bananas'))
        self.assertRaises((TypeError, ValueError), self.account.withdraw([]))
        self.assertRaises((TypeError, ValueError), self.account.withdraw('[]'))


    def test_insufficient_funds_withdrawal(self):
        # Your code here to test that you can only withdraw funds which are available.
        # For example, if you have a balance of 500.00 dollars then that is the maximum
        # that can be withdrawn. If you tried to withdraw 600.00 then a suitable exception
        # should be raised and the withdrawal should NOT be applied to the account balance
        # or the account's transaction list.
        """ withdraw 500 first """
        self.assertRaises((TypeError, ValueError), self.account.withdraw(500.00))
        
        """ confirm the balance is 500"""
        self.assertEqual(self.account.balance, 500.00)

        """ confirm you cannot withdraw more than the balance"""
        self.assertRaises((TypeError, ValueError), self.account.withdraw(600.00))


# Run the unit tests in the above test case
unittest.main()       
