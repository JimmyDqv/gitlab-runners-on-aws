import logging
import json
import os
import boto3

logger = logging.getLogger("scalein")
logger.setLevel(logging.DEBUG)


def handler(event, context):
    instance_id = get_instance_id(event['RunnerDefinition'])
    status = terminate_instance(instance_id)

    event['RunnerDefinition']['Terminated'] = (status != 'running')

    return event


def get_instance_id(runner_definition):
    if runner_definition['Type'] == 'EC2':
        return runner_definition['InstanceId']


def terminate_instance(instance_id):
    client = boto3.client('ec2')
    response = client.terminate_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=False
    )

    return response['TerminatingInstances'][0]['CurrentState']['Name']


def debug_print(message):
    logger.debug(message)
