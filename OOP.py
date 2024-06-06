import logging

logging.basicConfig(filename='BankAccount.log', level=logging.INFO, format ='%(asctime)s:%(levelname)s:%(message)s')

class BankAccount:
    """ A class to represent a bank account. 
    ...
    
    Attributes
    ----------
    account_number : int
        account number 
    owner_name : str 
        account holders name
    balance : int
        account balance

    Methods
    -------
    deposit(amount) 
        Deposits specified amount in account
    withdraw(amount)
        withdraws specified amount from account
    get_balance()
        pulls current account balance 
    """
    def __init__(self, account_number, owner_name, balance=0):
        """ 
        Parameters
        -----------
        account_number : int
            Account number 
        owner_name : str
            Account holders name 
        balance : int
            Account balance. If balance isn't passed, default balance is used. 
        """

        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance

        logging.info('Created Bank Account. Account Number:{} - Account Holder:{} - Account Balance:{}'.format(self.account_number, self.owner_name, self.balance))

    def deposit(self, amount: int = 0) -> int:
        """Deposits specified amount in account.
        if amount isn't passed, default amount is used.

        Parameters
        ----------
        amount : int, optional 
            The amount deposited. Deault is 0 
        """
        self.balance +=  amount 
       
        logging.info('{} deposited. New balance is {}'.format(amount, self.balance))

    def withdraw(self, amount: int = 0) -> int:
        """Withdraws specified amount from account.
        if amount isn't passed, default amount is used

        Parameters
        ----------
        amount : int, optional 
            The amount withdrawn. Deault is 0. 

        Raises
        ------
        ValueError
            if withdawal amount is greater than account balance. 
        """
        if self.balance < amount:
            logging.exception("You cannot withdraw more than your account balance.") 
        else:
            self.balance -=  amount
        logging.info('{} withdrawn. New balance is {}'.format(amount, self.balance))

    def get_balance(self):
        """Returns current balance."""
        logging.info('Balance is {}'.format(self.balance))
        return self.balance
        
        

    
Brianna = BankAccount(12345, 'Brianna Kwami', 5000)
Nicole = BankAccount(4567, 'Nicole Kwami', 98765)

Brianna.withdraw(6578)
print(Brianna.get_balance())
Nicole.deposit(4500)
print(Nicole.get_balance())
