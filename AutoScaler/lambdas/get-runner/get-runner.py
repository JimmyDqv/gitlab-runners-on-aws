import logging
import json
import os
import boto3

logger = logging.getLogger("lookup-runner")
logger.setLevel(logging.DEBUG)


def handler(event, context):
    debug_print(json.dumps(event, indent=2))
    details = get_runner_details(event)

    return details


def get_runner_details(event):
    runner_details = {}
    runner_details['Type'] = 'LAMBDA'
    event_details = event['detail']['runner']
    if event_details:
        if 'description' in event_details:
            runner_details['Runner'] = event_details['description']
            if event_details['description'].startswith('ec2'):
                runner_details['Type'] = 'EC2'
                runner_details['InstanceId'] = event_details['description'][4:]

    return runner_details


def debug_print(message):
    logger.debug(message)
