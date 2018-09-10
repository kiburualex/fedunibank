

class BankAccount:

    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        self.account_number = '0'
        self.pin_number = ''
        self.balance = 0.0
        self.interest_rate = 0.0
        self.transaction_list = []

    def deposit(self, amount):

        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        try:
            self.balance = round(float(self.balance) + float(amount), 2)

            """ validate errors """
            self.transaction_list.append(("Deposit", "%.2f" % (float(amount))))
            return "success"
        except (TypeError, ValueError) as errorMsg:
            return "Invalid data format!"

    def withdraw(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        try:
            if self.balance < float(amount):
                raise ValueError("cannot withdraw more than the balance!")
            self.balance = round(float(self.balance) - float(amount), 2)

            """ validate errors """
            self.transaction_list.append(("Withdrawal", "%.2f" % (float(amount))))
            return "success"
        except (TypeError, ValueError) as errorMsg:
            if "withdraw more" in str(errorMsg):
                return "cannot withdraw more than the balance!"
            return "Invalid data format!"
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''
        transaction_string = ''
        for transaction in self.transaction_list:
            name, amount = transaction
            transaction_string += str(name)+'\n'+str(amount)+'\n'

        return transaction_string


    def export_to_account_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        account_file = str(self.account_number) + '.txt'

        with open(account_file, 'w') as f:
            f.write("%s\n" % self.account_number)
            f.write("%s\n" % self.pin_number)
            f.write("%s\n" % self.balance)
            f.write("%s\n" % self.interest_rate)

            """ write the transactions """
            for item in self.transaction_list:
                a, b = item
                f.write("%s\n" % a)
                f.write("%s\n" % b)
