from datetime import datetime
from decimal import Decimal
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

import os
from dotenv import load_dotenv
load_dotenv()

dyn = boto3.resource("dynamodb",
                     aws_access_key_id=os.getenv("AWS_ACCESS"), aws_secret_access_key=os.getenv("AWS_SECRET"),
                     region_name=os.getenv("AWS_REGION"), endpoint_url="http://dynamodb.eu-west-1.amazonaws.com")
table = dyn.Table("bank")


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class Bank:
    def __init__(self, initial, name):
        initial = self.checks(initial)

        self.amount = initial

        if type(name) != str:
            raise TypeError("Name must be a valid string.")

        self.name = name
        ts = self.get_date()
        self.save_to_db(ts, self.name, initial)

        return

    def deposit(self, amount):
        amount = self.checks(amount)

        ts = self.get_date()

        self.save_to_db(ts, self.name, amount)

        self.amount += amount

        return self.get_balance()

    def withdraw(self, amount):
        amount = self.checks(amount)

        ts = self.get_date()

        if self.amount.compare(amount) == Decimal(-1):
            print("Warning: You are now into overdraft.")

        self.save_to_db(ts, self.name, -amount)

        self.amount -= amount
        return self.get_balance()

    def get_balance(self):
        return round(self.amount, 2)

    def statement(self):
        s = "| date || credit || debit || balance |\n"
        filter_exp = Key('name').eq(self.name)
        proj_exp = "ts, tr"

        response = table.scan(
            FilterExpression=filter_exp,
            ProjectionExpression=proj_exp
        )

        balance = self.amount
        history = response[u'Items']
        i = len(history) - 1
        while i >= 0:
            if history[i]["tr"] < 0:
                credit = 0
                debit = -history[i]["tr"]

            else:
                credit = history[i]["tr"]
                debit = 0

            time = datetime.fromtimestamp(history[i]["ts"]).strftime("%d/%m/%y")

            s += "| {t} || {c} || {d} || {b} |\n".format(t=time, c=credit, d=debit, b=balance)
            balance -= history[i]["tr"]
            i -= 1

        return s

    @staticmethod
    def save_to_db(ts, name, amount):
        resp = table.put_item(Item={
            'ts': Decimal(ts),
            'name': name,
            'tr': Decimal(amount)
        })

        return resp

    @staticmethod
    def checks(amount):
        if type(amount) != int and type(amount) != float:
            raise TypeError("Expecting float, or int, as transaction amount. Got {t} instead.".format(t=type(amount)))

        amount = Decimal(amount)

        if Decimal(0).compare(amount) != Decimal("-1"):
            raise ValueError("Sorry, you can only transact positive amounts of money.")
        return amount

    @staticmethod
    def get_date():
        return datetime.now().timestamp()


if __name__ == "__main__":
    b = Bank(1000, "Akash")
    b.deposit(100)
    b.withdraw(900)
    print(b.statement())
