import logging
import json
import os
import boto3

logger = logging.getLogger("httpapi-auth")
logger.setLevel(logging.DEBUG)


def handler(event, context):
    debug_print(json.dumps(event, indent=2))

    gitlab_secret = event['identitySource'][0]
    is_authorized = False
    # Value should be fetched from Secrets Manager or Parameter Store to be highly secure.
    if gitlab_secret == os.environ['GITLAB_SECRET']:
        is_authorized = True

    state = {
        "isAuthorized": is_authorized,
        "context": {
        }
    }

    debug_print(state)

    return state


def debug_print(message):
    logger.debug(message)
