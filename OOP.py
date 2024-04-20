class BankAccount:
    def __init__(self, account_number, owner_name, balance):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance
    def deposit(self, amount):
        self.balance +=  amount 
       
    def withdraw(self, amount):
        self.balance -=  amount       

    def get_balance(self):
       return self.balance

    
Brianna = BankAccount(12345, 'Brianna Kwami', 5000)
Nicole = BankAccount(4567, 'Nicole Kwami', 98765)

Brianna.withdraw(136)
print(Brianna.get_balance())
Nicole.deposit(4500)
print(Nicole.get_balance())

