from datetime import datetime
from decimal import Decimal


class Bank:
    def __init__(self, initial):
        if not self.checks(initial):
            raise RuntimeError("Class not initialised.")

        self.amount = Decimal(initial)
        self.transactions = [self.amount]
        self.times = [self.get_date()]
        return

    def deposit(self, amount):
        amount = Decimal(amount)
        if not self.checks(amount):
            return

        self.amount += amount
        self.transactions.append(amount)
        self.times.append(self.get_date())
        return

    def withdraw(self, amount):
        amount = Decimal(amount)
        if not self.checks(amount):
            return

        if self.amount.compare(amount) == Decimal(-1):
            print("Warning: You are now into overdraft.\n")

        self.amount -= amount
        self.transactions.append(Decimal(-1) * amount)
        self.times.append(self.get_date())
        return

    def statement(self):
        print("| date || credit || debit || balance |")

        balance = self.amount
        i = len(self.transactions) - 1
        while i >= 0:
            if self.transactions[i].compare(Decimal(0)) == 1:
                credit = self.transactions[i].__float__()
                debit = 0

            else:
                credit = 0
                debit = -self.transactions[i].__float__()

            print("| {t} || {c} || {d} || {b} |".format(t=self.times[i], c=credit, d=debit, b=balance))

            balance = (balance - self.transactions[i])

            i -= 1

        # print(self.amount)
        # print(self.transactions)
        # print(self.times)
        return

    @staticmethod
    def checks(amount):
        if Decimal(0).compare(amount) != Decimal("-1"):
            print("Sorry, you can only transact positive amounts of money.\n")
            return False
        return True

    @staticmethod
    def get_date():
        return datetime.now().strftime("%d/%m/%y")


