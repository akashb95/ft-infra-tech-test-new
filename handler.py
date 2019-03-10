import json
from bank import Bank


def bank(event, context):
    b = Bank(1000, "Akash")
    b.deposit(100)
    b.withdraw(900)
    statement = b.statement()

    body = {
        "message": "Function executed successfully.",
        "statement": statement
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
