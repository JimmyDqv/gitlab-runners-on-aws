import logging
import json
import os
import boto3

logger = logging.getLogger("unregister")
logger.setLevel(logging.DEBUG)


def handler(event, context):
    instance_id = get_instance_id(event['RunnerDefinition'])

    if instance_id:
        ssm_document = os.environ['SSM_DOCUMENT']
        success = run_ssm_command(ssm_document, instance_id)
        event['RunnerDefinition']['UnRegistered'] = success

    return event


def get_instance_id(runner_definition):
    if runner_definition['Type'] == 'EC2':
        return runner_definition['InstanceId']

    return None


def run_ssm_command(ssm_document, instance_id):
    ssm_client = boto3.client('ssm')
    try:
        instances = [str(instance_id)]
        debug_print("DocumentName {}".format(ssm_document))
        debug_print("InstanceIds {}".format(instances))
        response = ssm_client.send_command(DocumentName=ssm_document,
                                           InstanceIds=instances,
                                           Comment='Unregister GitLab Runner',
                                           TimeoutSeconds=1200)
    except Exception as e:
        debug_print(e)
        return False
    return True


def debug_print(message):
    logger.debug(message)
