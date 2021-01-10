import logging
import json
import os
import boto3

logger = logging.getLogger("trigger")
logger.setLevel(logging.DEBUG)


def handler(event, context):
    debug_print(json.dumps(event, indent=2))
    runner = event['RunnerDefinition']
    start_lambda_sync(runner['Arn'], event)


def start_lambda_sync(arn, event):
    client = boto3.client('lambda')
    client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )


def debug_print(message):
    logger.debug(message)
