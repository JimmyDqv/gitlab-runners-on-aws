import argparse
import os
import json
import boto3


def update_dynamo_db(tablename):
    with open('job_runner_registry.json') as json_file:
        data = json.load(json_file)

        for job in data['jobs']:
            type = job['type']
            name = job['name']
            tags = job['tags']

            pk = f"job#{name}"
            sk = "tags#" + "#".join(tags)

            data = {
                "pk": pk,
                "sk": sk,
                "type": type,
            }
            if type == "LAMBDA":
                data["arn"] = job['lambdaArn']

            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table(tablename)
            table.put_item(Item=data)
            print(f'Added Item: {data}')


def get_dynamodb_table(stackname: str) -> str:
    cloudformation_client = boto3.client('cloudformation')

    stack_resources = cloudformation_client.list_stack_resources(
        StackName=stackname
    )
    for resource in stack_resources['StackResourceSummaries']:
        if resource['ResourceType'] == 'AWS::DynamoDB::Table':
            if resource['LogicalResourceId'] == 'GitLabJobTagsMapping':
                return resource['PhysicalResourceId']

    return ''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stackname', required=False,
                        help='The name of the CloudFormation Stack with base infrastructure.')

    args = parser.parse_args()
    stackname = args.stackname

    dynamo_table = get_dynamodb_table(stackname)
    print('Adding Mapping....')
    update_dynamo_db(dynamo_table)
    print('Done!')


if __name__ == '__main__':
    main()
