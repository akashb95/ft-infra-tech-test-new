from datetime import datetime
from decimal import Decimal


class Bank:
    def __init__(self, initial):
        initial = Decimal(initial)
        if not self.checks(initial):
            raise RuntimeError("Class not initialised.")

        self.amount = initial
        self.transactions = [self.amount]
        self.times = [self.get_date()]
        return

    def deposit(self, amount):
        amount = Decimal(amount)
        if not self.checks(amount):
            return False

        self.amount += amount
        self.transactions.append(amount)
        self.times.append(self.get_date())
        return self.get_balance()

    def withdraw(self, amount):
        amount = Decimal(amount)
        if not self.checks(amount):
            return False

        if self.amount.compare(amount) == Decimal(-1):
            print("Warning: You are now into overdraft.\n")

        self.amount -= amount
        self.transactions.append(Decimal(-1) * amount)
        self.times.append(self.get_date())
        return self.get_balance()

    def get_balance(self):
        return self.amount.__float__()

    def statement(self):
        s = "| date || credit || debit || balance |\n"

        balance = self.amount
        i = len(self.transactions) - 1
        while i >= 0:
            if self.transactions[i].compare(Decimal(0)) == 1:
                credit = self.transactions[i]
                debit = 0

            else:
                credit = 0
                debit = -self.transactions[i]

            s += "| {t} || {c} || {d} || {b} |\n"\
                .format(t=self.times[i], c=round(credit, 2), d=round(debit, 2), b=round(balance, 2))

            balance = (balance - self.transactions[i])

            i -= 1
        print(s)
        return s

    @staticmethod
    def checks(amount):
        if Decimal(0).compare(amount) != Decimal("-1"):
            print("Sorry, you can only transact positive amounts of money.\n")
            return False
        return True

    @staticmethod
    def get_date():
        return datetime.now().strftime("%d/%m/%y")
