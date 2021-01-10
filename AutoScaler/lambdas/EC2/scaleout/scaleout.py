import logging
import json
import os
import boto3
import random

logger = logging.getLogger("scaleout")
logger.setLevel(logging.DEBUG)

# Get all SSM Parameters for GitLab Runners
client = boto3.client('ssm')
config_path = os.environ['CONFIG_PATH']
if not config_path.startswith('/'):
    config_path = '/' + config_path

param_details = client.get_parameters_by_path(
    Path=config_path,
    Recursive=False,
    WithDecryption=True
)

if 'Parameters' in param_details:
    for param in param_details.get('Parameters'):
        param_name = param.get('Name').split("/")[-1]
        param_value = param.get('Value')
        os.environ[param_name] = param_value


def handler(event, context):
    debug_print(json.dumps(event, indent=2))
    run_instance()


def run_instance():
    registration_token = os.environ['RegistrationToken']
    url = os.environ['Url']

    user_data = f'''#!/bin/sh

    sudo -s

    instance_id=$(wget -q -O - http://169.254.169.254/latest/meta-data/instance-id)

    gitlab-runner register --non-interactive --name ec2-$instance_id --tag-list aws,ec2,docker --url {url} --registration-token {registration_token} --executor docker --docker-image alpine:3.7

    runner_token=$(wq -i toml .runners[0].token /etc/gitlab-runner/config.toml)

    aws ec2 create-tags --resources $instance_id --tags Key=gitlab,Value=$runner_token Key=Name,Value=gitlab-runner-$runner_token

    gitlab-runner run-single -u {url} -t $runner_token --description ec2-$instance_id --executor docker --docker-image alpine:3.7 --max-builds 1

    '''

    ami = os.environ['AMI_ID']
    instance_type = os.environ['INSTANCE_TYPE']
    sg = os.environ['SECURITY_GROUP_ID']
    subnets = os.environ['SUBNETS'].split(',')
    iam = os.environ['IAM_INSTANCE_PROFILE_NAME']

    if 'SSH_KEY_NAME' in os.environ:
        kwargs = {'KeyName': os.environ['SSH_KEY_NAME']}
    else:
        kwargs = {}

    client = boto3.client('ec2')

    response = client.run_instances(
        ImageId=ami,
        InstanceType=instance_type,
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=[
            sg,
        ],
        SubnetId=random.choice(subnets),
        UserData=user_data,
        EbsOptimized=True,
        IamInstanceProfile={
            'Name': iam
        },
        InstanceInitiatedShutdownBehavior='terminate',
        TagSpecifications=[
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'gitlab-runner'
                    },
                ]
            },
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'gitlab-runner'
                    },
                ]
            },
        ],
        InstanceMarketOptions={
            'MarketType': 'spot',
            'SpotOptions': {
                'SpotInstanceType': 'one-time',
                'InstanceInterruptionBehavior': 'terminate'
            }
        },
        **kwargs
    )

    debug_print(response)


def debug_print(message):
    logger.debug(message)
