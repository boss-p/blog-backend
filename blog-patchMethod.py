import boto3
import json
import logging
import random
from custom_encoder import CustomEncoder


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the name of the DynamoDB table and create a connection to the table using the boto3 library
dynamodbTableName = 'Blog'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

# Define the HTTP method and path that the Lambda function should respond to
blogPath = '/blog'
patchMethod = 'PATCH'

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == patchMethod and path == blogPath:
        requestBody = json.loads(event['body'])
        response = modifyblog(requestBody['id'], requestBody['updateKey'], requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == blogPath:
        requestBody = json.loads(event['body'])
        response = deleteblog(requestBody['id'])
    else:
        response = buildResponse(404, 'NotFound')
        
    return response
    
def modifyblog(id, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                'id': id
            },
            UpdateExpression='set %s = :value'  % updateKey,
            ExpressionAttributeValues={
                ':value': updateValue
            },
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttrebutes': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do custom error handlin here')
    
    # Define a function to build the response object with the appropriate status code, headers, and body
def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            }
        }
    if body is not None:
        # If a body is provided, encode it using a custom encoder and add it to the response object
        response['body'] = json.dumps(body, cls=CustomEncoder)
    # Return the response object
    return response