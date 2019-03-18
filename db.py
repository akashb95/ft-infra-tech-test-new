import boto3
import os
from dotenv import load_dotenv
load_dotenv()


def dyn_connection():
    """
    Connect to AWS and find required table.
    :return: DynamoDB connection instance
    """
    dyn = boto3.resource("dynamodb",
                         aws_access_key_id=os.getenv("AWS_ACCESS"), aws_secret_access_key=os.getenv("AWS_SECRET"),
                         region_name=os.getenv("AWS_REGION"), endpoint_url=os.getenv("DYNAMO_ENDPOINT"))
    table = dyn.Table(os.getenv("DYNAMO_TABLE"))
    return table
