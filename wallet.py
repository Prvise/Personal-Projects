
"""
wallet class used to track user's current amount to purchase music

:param: class takes in certain amounts of money into bank and withdraws a certain amount if needed
:type: int and float values
:raise ValueError: class raises a value error indicating insufficient bank balance if user try to use unavailable cash 
:raises ValueError: class raises a value error if user deposits an invalid input on amount of money such as a str instead of int or float
"""
class Wallet:

    def __init__(self, amount=0):
        self.amount = amount


    def deposit(self, amount):
        try:
            amount = float(amount)
            self.amount += amount
        except ValueError:
            raise ValueError
  

    
    def withdraw(self, amount):
        if not (self.amount - amount) < 0:
            self.amount -= amount
        else:
            raise ValueError("Insufficient balance")
        
    def balance(self):
        return self.amount

        
    @property
    def current_amount(self):
        return self._amount
    
    @current_amount.setter
    def current_amount(self, amount):
        try:
            money = float(amount)
            self._amount = money
            return self._amount
        except ValueError:
            raise ValueError("Invalid input")
        


