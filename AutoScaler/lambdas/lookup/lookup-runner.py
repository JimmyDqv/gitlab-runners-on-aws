import logging
import json
import os
import boto3

logger = logging.getLogger("lookup-runner")
logger.setLevel(logging.DEBUG)


def handler(event, context):
    job_name = get_job_name(event)
    debug_print(f"Job name: {job_name}")
    runner = find_runner_for_job(job_name=job_name)
    return {
        "Arn": runner['arn'],
        "Type": runner['type']
    }


def get_job_name(event):
    return event['detail']['build_name']


def find_runner_for_job(job_name):
    pk = f"job#{job_name}"
    dynamodb_client = boto3.client('dynamodb')

    response = dynamodb_client.query(
        TableName=os.environ["RUNNERS_TABLE"],
        KeyConditionExpression='pk = :pk',
        ExpressionAttributeValues={
            ':pk': {'S': pk}
        }
    )

    if len(response['Items']) > 0:
        runner = {
            "type": response['Items'][0]['type']['S']
        }
        if runner['type'] == 'LAMBDA':
            runner['arn'] = response['Items'][0]['arn']['S'],
        else:
            runner['arn'] = '-'
        return runner

    # No runner found, return default
    return {
        "arn": os.environ['DEFAULT_RUNNER'],
        "type": "LAMBDA"
    }


def debug_print(message):
    logger.debug(message)
