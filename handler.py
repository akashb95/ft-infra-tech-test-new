"""
Handler functions for Serverless endpoints
Adapted from:
https://medium.com/devopslinks/aws-lambda-serverless-framework-python-part-1-a-step-by-step-hello-world-4182202aba4a
"""

import json
from bank import Bank


def bank(event, context):
    """
    Does sample banking transactions
    :param event:
    :param context:
    :return:
    """

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
