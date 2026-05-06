import json


def lambda_handler(event, context):

    message = {
        "status": "success",
        "message": "AWS Cost Optimization System Lambda is working"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(message)
    }