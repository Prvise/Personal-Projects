import pytest 
from wallet import Wallet
from tools import read_receipt
from tools import convert_currency


def test_currency():
    assert convert_currency(5) == 86.6

def test_invalid_currency():
    with pytest.raises(ValueError):
        convert_currency('R20')

def test_read_receipt():
    with pytest.raises(FileNotFoundError):
        read_receipt("random_path")
    
def test_wallet():
    wallet = Wallet(20)
    assert wallet.balance() == 20

def test_wallet_withdraw():
    bank = Wallet(100)
    bank.withdraw(50)
    assert bank.balance() == 50

def test_wallet_deposit():
    card = Wallet()
    card.deposit(25)
    assert card.balance() == 25

def test_wallet_invalid_deposit():
    money = Wallet()
    with pytest.raises(ValueError):
        money.deposit("money")
    


